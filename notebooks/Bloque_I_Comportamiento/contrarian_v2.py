import numpy as np
import pandas as pd


def _rsi_wilder(px: pd.DataFrame, periodo: int = 14) -> pd.DataFrame:
    """RSI de Wilder (suavizado exponencial alpha=1/periodo), vectorizado y causal."""
    delta = px.diff()
    ganancia = delta.clip(lower=0.0)
    perdida = (-delta).clip(lower=0.0)
    ag = ganancia.ewm(alpha=1.0 / periodo, adjust=False, min_periods=periodo).mean()
    al = perdida.ewm(alpha=1.0 / periodo, adjust=False, min_periods=periodo).mean()
    rs = ag / al.replace(0.0, np.nan)
    rsi = 100.0 - 100.0 / (1.0 + rs)
    # Sin pérdidas en la ventana -> RSI = 100 (si hay ganancias)
    rsi = rsi.where(~((al == 0.0) & ag.notna()), 100.0)
    return rsi


def crear_generador_contrarian(
    precios: pd.DataFrame,
    cash_columna=None,
    top_n: int = 5,
    umbral_drawdown: float = -0.30,
    umbral_rsi: float = 30.0,
    holding_meses: int = 6,
    stop_loss_pct=None,
    cooldown_stop_meses: int = 3,
    rsi_lookback_dias: int = 1,
    estabilizacion_dias: int = 0,
    fecha_inicio_operativa=None,
    ventana: int = 252,
    periodo_rsi: int = 14,
    verbose: bool = True,
):
    """
    Contrarian v2 para MotorBacktestDinamico.

    Diferencias frente a GestorDatos.contrarian_ranking (v1):
      * Slots fijos de 1/top_n: si solo 1 ETF pasa los filtros NO se concentra el 100% en él.
      * El capital sin asignar va al activo cash (SHV) en lugar de quedar a 0 % de rentabilidad.
      * Entradas escalonadas: cada mes se rellenan los slots libres (v1 esperaba holding_meses
        completos tras una rotación vacía) y cada posición tiene su propio holding.
      * stop_loss_pct realmente conectado (comprobación en cada fecha de decisión, es decir mensual).
      * Los pesos de las posiciones que continúan se devuelven ya 'derivados' (drift), de modo que el
        motor no genera rotación/costes espurios cada mes.
      * Indicadores vectorizados y causales (RSI de Wilder); sin recalcular series en cada fecha.
      * No opera antes de fecha_inicio_operativa (el warm-up solo sirve para calentar indicadores).
      * Registra operaciones discretas (entrada/salida/motivo/rendimiento) en estado['operaciones'].

    Parámetros opcionales de mejora (por defecto desactivados / equivalentes a v1):
      rsi_lookback_dias   : usa el RSI mínimo de los últimos N días (1 = solo el día de decisión).
      estabilizacion_dias : exige rentabilidad > 0 en los últimos N días (evita comprar mientras cae).
    """
    precios = precios.copy()
    activos = list(precios.columns)
    candidatos = [a for a in activos if a != cash_columna]
    px = precios[candidatos]

    ret12m = px.pct_change(ventana)
    dd = px / px.rolling(ventana, min_periods=ventana).max() - 1.0
    rsi = _rsi_wilder(px, periodo_rsi)
    rsi_ref = rsi.rolling(max(1, rsi_lookback_dias), min_periods=1).min()
    if estabilizacion_dias > 0:
        estable = px.pct_change(estabilizacion_dias) > 0.0
    else:
        estable = pd.DataFrame(True, index=px.index, columns=px.columns)
    valido = ret12m.notna() & dd.notna() & rsi.notna()
    senal = valido & (dd <= umbral_drawdown) & (rsi_ref <= umbral_rsi) & estable

    f_ini = pd.Timestamp(fecha_inicio_operativa) if fecha_inicio_operativa is not None else None
    slot = 1.0 / top_n
    precios_arr = precios

    def _meses(a: pd.Timestamp, b: pd.Timestamp) -> int:
        return (b.year - a.year) * 12 + (b.month - a.month)

    def generador_pesos(fecha_actual, precios_hist, rent_hist, estado):
        pesos = {a: 0.0 for a in activos}
        estado.setdefault('posiciones', {})
        estado.setdefault('bloqueados', {})
        estado.setdefault('operaciones', [])
        estado.setdefault('pesos_ult', None)
        estado.setdefault('fecha_ult', None)

        if (f_ini is not None and fecha_actual < f_ini) or fecha_actual not in precios_arr.index:
            return pesos, estado
        if 'fecha_primera_decision' not in estado:
            estado['fecha_primera_decision'] = fecha_actual

        pos = estado['posiciones']

        # 1) Pesos derivados (drift) desde la última decisión: lo que el motor tiene realmente
        if estado['pesos_ult'] is None:
            w = {a: 0.0 for a in activos}
            if cash_columna:
                w[cash_columna] = 1.0
        else:
            p0 = precios_arr.loc[estado['fecha_ult']]
            p1 = precios_arr.loc[fecha_actual]
            val = {a: estado['pesos_ult'][a] * (p1[a] / p0[a]) for a in activos}
            cash_idle = 1.0 - sum(estado['pesos_ult'].values())   # cash fuera de columnas: 0 % rent.
            tot = sum(val.values()) + cash_idle
            w = {a: v / tot for a, v in val.items()}

        def _mover_a_cash(a):
            if cash_columna:
                w[cash_columna] += w[a]
            w[a] = 0.0

        # 2) Salidas: holding cumplido o stop-loss
        for a in list(pos):
            info = pos[a]
            rend = precios_arr.at[fecha_actual, a] / info['precio_entrada'] - 1.0
            motivo = None
            if stop_loss_pct is not None and rend <= stop_loss_pct:
                motivo = 'stop-loss'
                estado['bloqueados'][a] = fecha_actual
            elif _meses(info['entrada'], fecha_actual) >= holding_meses:
                motivo = 'holding'
            if motivo:
                estado['operaciones'].append({
                    'activo': a, 'entrada': info['entrada'], 'salida': fecha_actual,
                    'dias': (fecha_actual - info['entrada']).days,
                    'motivo': motivo, 'beneficio': rend,   # rendimiento por slot (tamaño fijo)
                })
                _mover_a_cash(a)
                del pos[a]

        # 3) Entradas: rellenar slots libres con los peores 12m que pasen los filtros
        libres = top_n - len(pos)
        if libres > 0:
            cand = []
            for a in candidatos:
                if a in pos or not senal.at[fecha_actual, a]:
                    continue
                if a in estado['bloqueados'] and _meses(estado['bloqueados'][a], fecha_actual) < cooldown_stop_meses:
                    continue
                cand.append((ret12m.at[fecha_actual, a], a))
            cand.sort()
            for _, a in cand[:libres]:
                disponible = w[cash_columna] if cash_columna else 1.0 - sum(w.values())
                monto = min(slot, max(disponible, 0.0))
                if monto <= 1e-9:
                    break
                w[a] += monto
                if cash_columna:
                    w[cash_columna] -= monto
                pos[a] = {'entrada': fecha_actual, 'precio_entrada': float(precios_arr.at[fecha_actual, a])}

        for a in activos:
            pesos[a] = max(w[a], 0.0)
        estado['pesos_ult'] = dict(pesos)
        estado['fecha_ult'] = fecha_actual
        return pesos, estado

    indicadores = {'ret12m': ret12m, 'drawdown': dd, 'rsi': rsi, 'senal': senal, 'valido': valido}

    if verbose:
        print("🎯 Contrarian v2 configurado:")
        print(f"   • Slots: {top_n} (1/{top_n} cada uno) | Holding: {holding_meses} m | Stop-loss: {stop_loss_pct}")
        print(f"   • Filtros: DD ≤ {umbral_drawdown:.0%}, RSI ≤ {umbral_rsi} (lookback {rsi_lookback_dias} d), "
              f"estabilización {estabilizacion_dias} d")
        print(f"   • Cash: {cash_columna or 'NINGUNO (capital ocioso al 0 %)'} | Candidatos: {len(candidatos)}")
    return generador_pesos, indicadores


def diagnostico_filtros(indicadores: dict, fecha_inicio=None) -> pd.DataFrame:
    """Nº de ETFs que pasan los filtros cada mes (fin de mes) -> cuánto tiempo hay señal."""
    s = indicadores['senal']
    if fecha_inicio is not None:
        s = s.loc[pd.Timestamp(fecha_inicio):]
    s = s[indicadores['valido'].reindex(s.index).any(axis=1)]
    n = s.sum(axis=1).groupby([s.index.year, s.index.month]).last()
    return n.rename('n_candidatos')
