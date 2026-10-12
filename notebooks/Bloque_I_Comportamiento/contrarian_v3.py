import itertools
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
    rsi = rsi.where(~((al == 0.0) & ag.notna()), 100.0)   # sin pérdidas -> RSI 100
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
    retraso_senal_dias: int = 1,
    columna_spy=None,
    usar_regimen: bool = False,
    sma_regimen: int = 200,
    regimen_cierra_posiciones: bool = False,
    excluir_spy: bool = False,
    fecha_inicio_operativa=None,
    ventana: int = 252,
    periodo_rsi: int = 14,
    verbose: bool = True,
):
    """
    Contrarian v3 para MotorBacktestDinamico.

    Novedades respecto a v2:
      retraso_senal_dias (def. 1): la señal usa datos hasta t-L y se ejecuta al cierre de t. Con 0 se
          reproduce el supuesto optimista anterior (señal y ejecución en el mismo cierre). El stop-loss
          se evalúa con el precio de t-L; la rentabilidad registrada en el log usa el precio real de t.
      usar_regimen: solo se compra si SPY > SMA(sma_regimen) (evaluado en t-L). Con
          regimen_cierra_posiciones=True además se liquidan las posiciones abiertas al perder el régimen.
      excluir_spy: SPY deja de ser candidato (sigue disponible como referencia de régimen y benchmark).

    Resto de comportamiento (heredado de v2): slots de 1/top_n, capital sin asignar en cash (SHV),
    entradas escalonadas con holding por posición, pesos derivados (sin rotación espuria), no opera antes de
    fecha_inicio_operativa, registro de operaciones en estado['operaciones'].
    """
    precios = precios.copy()
    activos = list(precios.columns)
    if (usar_regimen or excluir_spy) and columna_spy is None:
        raise ValueError("usar_regimen / excluir_spy requieren columna_spy (columna de SPY en 'precios').")
    excluidos = {columna_spy} if (excluir_spy and columna_spy) else set()
    candidatos = [a for a in activos if a != cash_columna and a not in excluidos]
    px = precios[candidatos]
    L = max(0, int(retraso_senal_dias))

    ret12m = px.pct_change(ventana)
    dd = px / px.rolling(ventana, min_periods=ventana).max() - 1.0
    rsi = _rsi_wilder(px, periodo_rsi)
    rsi_ref = rsi.rolling(max(1, rsi_lookback_dias), min_periods=1).min()
    if estabilizacion_dias > 0:
        estable = px.pct_change(estabilizacion_dias) > 0.0
    else:
        estable = pd.DataFrame(True, index=px.index, columns=px.columns)
    valido = ret12m.notna() & dd.notna() & rsi.notna()
    senal_base = valido & (dd <= umbral_drawdown) & (rsi_ref <= umbral_rsi) & estable

    if usar_regimen:
        pr = precios[columna_spy]
        regimen_ok = pr > pr.rolling(sma_regimen, min_periods=sma_regimen).mean()
    else:
        regimen_ok = pd.Series(True, index=precios.index)

    # --- Retraso de señal: todo lo que decide t usa información hasta t-L ---
    def _lag(obj, fill):
        return obj.shift(L, fill_value=fill) if L > 0 else obj
    senal_L = _lag(senal_base, False)
    valido_L = _lag(valido, False)
    regimen_L = _lag(regimen_ok, False)
    ret12m_L = ret12m.shift(L) if L > 0 else ret12m
    px_L = precios.shift(L) if L > 0 else precios
    senal_ef = senal_L & regimen_L.values[:, None]

    f_ini = pd.Timestamp(fecha_inicio_operativa) if fecha_inicio_operativa is not None else None
    slot = 1.0 / top_n

    def _meses(a, b):
        return (b.year - a.year) * 12 + (b.month - a.month)

    def generador_pesos(fecha_actual, precios_hist, rent_hist, estado):
        pesos = {a: 0.0 for a in activos}
        estado.setdefault('posiciones', {})
        estado.setdefault('bloqueados', {})
        estado.setdefault('operaciones', [])
        estado.setdefault('pesos_ult', None)
        estado.setdefault('fecha_ult', None)

        if (f_ini is not None and fecha_actual < f_ini) or fecha_actual not in precios.index:
            return pesos, estado
        if 'fecha_primera_decision' not in estado:
            estado['fecha_primera_decision'] = fecha_actual

        pos = estado['posiciones']

        # 1) Pesos derivados (drift) desde la última decisión = lo que el motor tiene realmente
        if estado['pesos_ult'] is None:
            w = {a: 0.0 for a in activos}
            if cash_columna:
                w[cash_columna] = 1.0
        else:
            p0 = precios.loc[estado['fecha_ult']]
            p1 = precios.loc[fecha_actual]
            val = {a: estado['pesos_ult'][a] * (p1[a] / p0[a]) for a in activos}
            cash_idle = 1.0 - sum(estado['pesos_ult'].values())
            tot = sum(val.values()) + cash_idle
            w = {a: v / tot for a, v in val.items()}

        def _salir(a, motivo):
            info = pos[a]
            rend_real = precios.at[fecha_actual, a] / info['precio_entrada'] - 1.0   # precio de ejecución (t)
            estado['operaciones'].append({
                'activo': a, 'entrada': info['entrada'], 'salida': fecha_actual,
                'dias': (fecha_actual - info['entrada']).days,
                'motivo': motivo, 'beneficio': rend_real,
            })
            if cash_columna:
                w[cash_columna] += w[a]
            w[a] = 0.0
            del pos[a]

        regimen_malo = usar_regimen and not bool(regimen_L.at[fecha_actual])

        # 2) Salidas: régimen (opcional), stop-loss (evaluado con precio t-L) y holding
        for a in list(pos):
            info = pos[a]
            p_dec = px_L.at[fecha_actual, a]
            p_dec = precios.at[fecha_actual, a] if pd.isna(p_dec) else p_dec
            rend_dec = p_dec / info['precio_entrada'] - 1.0
            if regimen_cierra_posiciones and regimen_malo:
                _salir(a, 'regimen')
            elif stop_loss_pct is not None and rend_dec <= stop_loss_pct:
                estado['bloqueados'][a] = fecha_actual
                _salir(a, 'stop-loss')
            elif _meses(info['entrada'], fecha_actual) >= holding_meses:
                _salir(a, 'holding')

        # 3) Entradas: slots libres con los peores 12m (a t-L) que pasen filtros y régimen
        libres = top_n - len(pos)
        if libres > 0 and not regimen_malo:
            cand = []
            for a in candidatos:
                if a in pos or not senal_ef.at[fecha_actual, a]:
                    continue
                if a in estado['bloqueados'] and _meses(estado['bloqueados'][a], fecha_actual) < cooldown_stop_meses:
                    continue
                cand.append((ret12m_L.at[fecha_actual, a], a))
            cand.sort()
            for _, a in cand[:libres]:
                disponible = w[cash_columna] if cash_columna else 1.0 - sum(w.values())
                monto = min(slot, max(disponible, 0.0))
                if monto <= 1e-9:
                    break
                w[a] += monto
                if cash_columna:
                    w[cash_columna] -= monto
                pos[a] = {'entrada': fecha_actual, 'precio_entrada': float(precios.at[fecha_actual, a])}

        for a in activos:
            pesos[a] = max(w[a], 0.0)
        estado['pesos_ult'] = dict(pesos)
        estado['fecha_ult'] = fecha_actual
        return pesos, estado

    indicadores = {
        'ret12m': ret12m, 'drawdown': dd, 'rsi': rsi,
        'senal': senal_ef,                 # efectiva: retraso + régimen
        'senal_sin_regimen': senal_L,      # solo retraso
        'valido': valido_L, 'regimen_ok': regimen_L,
    }

    if verbose:
        print("🎯 Contrarian v3 configurado:")
        print(f"   • Slots: {top_n} (1/{top_n} cada uno) | Holding: {holding_meses} m | "
              f"Stop-loss: {f'{stop_loss_pct:.0%}' if stop_loss_pct is not None else 'no'}")
        print(f"   • Filtros: DD ≤ {umbral_drawdown:.0%}, RSI ≤ {umbral_rsi} (lookback {rsi_lookback_dias} d), "
              f"estabilización {estabilizacion_dias} d")
        print(f"   • Retraso de señal: {L} d | Régimen SPY>SMA{sma_regimen}: "
              f"{'ON' + (' (cierra posiciones)' if regimen_cierra_posiciones else ' (solo bloquea entradas)') if usar_regimen else 'OFF'}"
              f" | SPY como candidato: {'no' if excluidos else 'sí'}")
        print(f"   • Cash: {cash_columna or 'NINGUNO (capital ocioso al 0 %)'} | Candidatos: {len(candidatos)}")
    return generador_pesos, indicadores


def diagnostico_filtros(indicadores: dict, fecha_inicio=None, con_regimen: bool = True) -> pd.Series:
    """Nº de ETFs que pasan los filtros a fin de cada mes."""
    s = indicadores['senal' if con_regimen else 'senal_sin_regimen']
    if fecha_inicio is not None:
        s = s.loc[pd.Timestamp(fecha_inicio):]
    s = s[indicadores['valido'].reindex(s.index).any(axis=1)]
    return s.sum(axis=1).groupby([s.index.year, s.index.month]).last().rename('n_candidatos')


# ==============================================================================
# Utilidades de comparación (escenarios y barrido de parámetros)
# ==============================================================================
def metricas_serie(s: pd.Series, rf: float = 0.02) -> dict:
    s = s.dropna()
    if len(s) < 30:
        return {'CAGR': np.nan, 'Vol': np.nan, 'Sharpe': np.nan, 'MaxDD': np.nan}
    r = s.pct_change().dropna()
    cagr = (s.iloc[-1] / s.iloc[0]) ** (252 / (len(s) - 1)) - 1
    vol = r.std() * np.sqrt(252)
    return {'CAGR': cagr, 'Vol': vol, 'Sharpe': (cagr - rf) / vol if vol > 0 else np.nan,
            'MaxDD': float((s / s.cummax() - 1).min())}


def ejecutar_variante(MotorCls, precios, rentabilidades, cfg, cash_columna, columna_spy,
                      coste, fecha_inicio_operativa=None, capital=10000):
    """Un backtest completo. 'coste' es el que recibe el motor (pasa COSTE*2 para cobrar ambos lados)."""
    gen, _ = crear_generador_contrarian(
        precios, cash_columna=cash_columna, columna_spy=columna_spy,
        fecha_inicio_operativa=fecha_inicio_operativa, verbose=False, **cfg)
    m = MotorCls(precios=precios, rentabilidades=rentabilidades, generador_pesos=gen,
                 frecuencia_decision='M', coste_transaccion=coste, benchmark_ticker=None,
                 permitir_short=False, max_short_porcentaje=0.0)
    s = m.ejecutar_backtest(capital_inicial=capital, estado_inicial={})
    est = m.estado_final
    ini = pd.Timestamp(est.get('fecha_primera_decision', s.index[0]))
    s = s.loc[ini:]
    return s / s.iloc[0] * capital, est.get('operaciones', []), m


def _fila(s, ops, rf):
    d = metricas_serie(s, rf)
    d['Final €'] = s.iloc[-1]
    d['Ops'] = len(ops)
    d['Win-rate'] = float(np.mean([o['beneficio'] > 0 for o in ops])) if ops else np.nan
    return d


def comparar_escenarios(MotorCls, precios, rentabilidades, cfg_base, escenarios, cash_columna, columna_spy,
                        coste, fecha_inicio_operativa=None, capital=10000, rf=0.02):
    """Ejecuta cada escenario (override sobre cfg_base). Devuelve (tabla, dict de series)."""
    filas, series = {}, {}
    for nombre, override in escenarios.items():
        cfg = {**cfg_base, **override}
        try:
            s, ops, _ = ejecutar_variante(MotorCls, precios, rentabilidades, cfg, cash_columna, columna_spy,
                                          coste, fecha_inicio_operativa, capital)
            filas[nombre] = _fila(s, ops, rf)
            series[nombre] = s
        except Exception as e:
            print(f"⚠️ Escenario '{nombre}' falló: {e}")
    if columna_spy is not None and series:
        ini = next(iter(series.values())).index[0]
        spy = precios[columna_spy].loc[ini:]
        spy = spy / spy.iloc[0] * capital
        filas['(ref) SPY buy & hold'] = {**metricas_serie(spy, rf), 'Final €': spy.iloc[-1], 'Ops': 0, 'Win-rate': np.nan}
        series['(ref) SPY buy & hold'] = spy
    return pd.DataFrame(filas).T, series


def barrido_parametros(MotorCls, precios, rentabilidades, cfg_base, grid, cash_columna, columna_spy,
                       coste, fecha_inicio_operativa=None, fecha_corte='2017-01-01', capital=10000, rf=0.02):
    """
    Producto cartesiano de 'grid' (dict nombre -> lista de valores). Para cada combinación calcula las métricas
    en muestra (antes de fecha_corte) y fuera de muestra (desde fecha_corte) a partir de UNA sola ejecución.
    """
    nombres = list(grid)
    combos = list(itertools.product(*[grid[k] for k in nombres]))
    corte = pd.Timestamp(fecha_corte)
    filas = []
    for vals in combos:
        cfg = {**cfg_base, **dict(zip(nombres, vals))}
        try:
            s, ops, _ = ejecutar_variante(MotorCls, precios, rentabilidades, cfg, cash_columna, columna_spy,
                                          coste, fecha_inicio_operativa, capital)
        except Exception as e:
            print(f"⚠️ {dict(zip(nombres, vals))} falló: {e}")
            continue
        mi, mo = metricas_serie(s.loc[:corte], rf), metricas_serie(s.loc[corte:], rf)
        filas.append({**dict(zip(nombres, vals)),
                      'CAGR_IS': mi['CAGR'], 'Sharpe_IS': mi['Sharpe'], 'MaxDD_IS': mi['MaxDD'],
                      'CAGR_OOS': mo['CAGR'], 'Sharpe_OOS': mo['Sharpe'], 'MaxDD_OOS': mo['MaxDD'],
                      'Ops': len(ops)})
    return pd.DataFrame(filas)
