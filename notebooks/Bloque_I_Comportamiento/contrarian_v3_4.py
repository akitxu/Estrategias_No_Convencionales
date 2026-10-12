import itertools
from collections import Counter
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
    placebo=None,
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

      placebo: dict con 'rng' (np.random.Generator) y UNO de:
          'calendario' {fecha: n_entradas}  -> placebo de SELECCIÓN: fechas reales, activo al azar entre los
              válidos (las entradas que no caben se pierden).
          'programa' {fecha: [activo | None]} -> placebo de TIMING/TOTAL: entradas programadas en fechas dadas;
              un activo concreto, o None = activo al azar. Lo que no cabe (slot ocupado, activo ya en cartera,
              cooldown) se aplaza a la siguiente decisión.
          Todo lo demás (slots, holding, stop, régimen, costes) es idéntico a la estrategia real.

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
            # El periodo evaluado empieza cuando los indicadores ya son válidos (no antes): el primer año
            # de calentamiento no se cuenta como 'rendimiento' de la estrategia.
            if not bool(valido_L.loc[fecha_actual].any()):
                return pesos, estado
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

        def _bloqueado(a):
            return a in estado['bloqueados'] and _meses(estado['bloqueados'][a], fecha_actual) < cooldown_stop_meses

        modo_prog = placebo is not None and 'programa' in placebo
        if modo_prog:   # las entradas programadas para hoy pasan a la cola de pendientes
            estado.setdefault('pend_placebo', []).extend(placebo['programa'].get(fecha_actual, []))

        if libres > 0 and not regimen_malo:
            if modo_prog:
                elegidos, pendientes, ocupados, libres_loc = [], [], set(pos), libres
                for item in estado['pend_placebo']:
                    if libres_loc <= 0:
                        pendientes.append(item)
                        continue
                    if item is None:
                        pool = [x for x in candidatos
                                if x not in ocupados and bool(valido_L.at[fecha_actual, x]) and not _bloqueado(x)]
                        if not pool:
                            pendientes.append(item)
                            continue
                        x = str(placebo['rng'].choice(pool))
                    else:
                        x = item
                        if x in ocupados or not bool(valido_L.at[fecha_actual, x]) or _bloqueado(x):
                            pendientes.append(item)
                            continue
                    elegidos.append(x)
                    ocupados.add(x)
                    libres_loc -= 1
                estado['pend_placebo'] = pendientes
            elif placebo is not None:
                n_obj = min(libres, placebo['calendario'].get(fecha_actual, 0))
                pool = [x for x in candidatos
                        if x not in pos and bool(valido_L.at[fecha_actual, x]) and not _bloqueado(x)]
                elegidos = ([str(x) for x in placebo['rng'].choice(pool, size=min(n_obj, len(pool)), replace=False)]
                            if n_obj > 0 and pool else [])
            else:
                cand = []
                for x in candidatos:
                    if x in pos or not senal_ef.at[fecha_actual, x] or _bloqueado(x):
                        continue
                    cand.append((ret12m_L.at[fecha_actual, x], x))
                cand.sort()
                elegidos = [x for _, x in cand[:libres]]
            for x in elegidos:
                disponible = w[cash_columna] if cash_columna else 1.0 - sum(w.values())
                monto = min(slot, max(disponible, 0.0))
                if monto <= 1e-9:
                    break
                w[x] += monto
                if cash_columna:
                    w[cash_columna] -= monto
                pos[x] = {'entrada': fecha_actual, 'precio_entrada': float(precios.at[fecha_actual, x])}

        for a in activos:
            pesos[a] = max(w[a], 0.0)
        estado['pesos_ult'] = dict(pesos)
        estado['fecha_ult'] = fecha_actual
        estado.setdefault('fechas_decision', []).append(fecha_actual)
        estado.setdefault('exposicion', []).append(
            1.0 - pesos[cash_columna] if cash_columna else sum(pesos[a] for a in candidatos))
        return pesos, estado

    indicadores = {
        'ret12m': ret12m, 'drawdown': dd, 'rsi': rsi,
        'senal': senal_ef,                 # efectiva: retraso + régimen
        'senal_sin_regimen': senal_L,      # solo retraso
        'valido': valido_L, 'regimen_ok': regimen_L,
    }

    if verbose:
        print("🎯 Contrarian v3.4 configurado:")
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
                      coste, fecha_inicio_operativa=None, capital=10000, placebo=None):
    """Un backtest completo. 'coste' es el que recibe el motor (pasa COSTE*2 para cobrar ambos lados)."""
    gen, _ = crear_generador_contrarian(
        precios, cash_columna=cash_columna, columna_spy=columna_spy,
        fecha_inicio_operativa=fecha_inicio_operativa, placebo=placebo, verbose=False, **cfg)
    m = MotorCls(precios=precios, rentabilidades=rentabilidades, generador_pesos=gen,
                 frecuencia_decision='M', coste_transaccion=coste, benchmark_ticker=None,
                 permitir_short=False, max_short_porcentaje=0.0)
    s = m.ejecutar_backtest(capital_inicial=capital, estado_inicial={})
    est = m.estado_final
    ini = pd.Timestamp(est.get('fecha_primera_decision', s.index[0]))
    s = s.loc[ini:]
    return s / s.iloc[0] * capital, est.get('operaciones', []), m


def _expo(m):
    e = m.estado_final.get('exposicion', [])
    return float(np.mean(e)) if len(e) else np.nan


def _fila(s, ops, rf, m=None):
    d = metricas_serie(s, rf)
    d['Final €'] = s.iloc[-1]
    d['Expo'] = _expo(m) if m is not None else np.nan      # % medio del capital fuera de cash (en cada decisión)
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
            s, ops, m = ejecutar_variante(MotorCls, precios, rentabilidades, cfg, cash_columna, columna_spy,
                                          coste, fecha_inicio_operativa, capital)
            filas[nombre] = _fila(s, ops, rf, m)
            series[nombre] = s
        except Exception as e:
            print(f"⚠️ Escenario '{nombre}' falló: {e}")
    if series:
        ini = next(iter(series.values())).index[0]
        if columna_spy is not None:
            spy = precios[columna_spy].loc[ini:]
            spy = spy / spy.iloc[0] * capital
            filas['(ref) SPY buy & hold'] = {**metricas_serie(spy, rf), 'Final €': spy.iloc[-1], 'Expo': 1.0,
                                             'Ops': 0, 'Win-rate': np.nan}
            series['(ref) SPY buy & hold'] = spy
        if cash_columna is not None:
            shv = precios[cash_columna].loc[ini:]
            shv = shv / shv.iloc[0] * capital
            filas['(ref) SHV buy & hold (cash)'] = {**metricas_serie(shv, rf), 'Final €': shv.iloc[-1], 'Expo': 0.0,
                                                    'Ops': 0, 'Win-rate': np.nan}
            filas['(ref) SHV buy & hold (cash)']['Sharpe'] = np.nan   # sin sentido con volatilidad ~0
            series['(ref) SHV buy & hold (cash)'] = shv
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
            s, ops, m = ejecutar_variante(MotorCls, precios, rentabilidades, cfg, cash_columna, columna_spy,
                                          coste, fecha_inicio_operativa, capital)
        except Exception as e:
            print(f"⚠️ {dict(zip(nombres, vals))} falló: {e}")
            continue
        mi, mo = metricas_serie(s.loc[:corte], rf), metricas_serie(s.loc[corte:], rf)
        filas.append({**dict(zip(nombres, vals)),
                      'CAGR_IS': mi['CAGR'], 'Sharpe_IS': mi['Sharpe'], 'MaxDD_IS': mi['MaxDD'],
                      'CAGR_OOS': mo['CAGR'], 'Sharpe_OOS': mo['Sharpe'], 'MaxDD_OOS': mo['MaxDD'],
                      'Expo': _expo(m), 'Ops': len(ops)})
    return pd.DataFrame(filas)


def test_placebo(MotorCls, precios, rentabilidades, cfg, cash_columna, columna_spy, coste,
                 fecha_inicio_operativa=None, n_sim=200, semilla=42, capital=10000, rf=0.02,
                 modo='seleccion', progreso=True):
    """
    Tests placebo. Se ejecuta la estrategia real y se extraen sus entradas (fecha, activo). Después se repite el
    backtest n_sim veces con el mismo holding/stop/régimen/costes y el mismo nº de entradas, cambiando:

      modo='seleccion': MISMAS FECHAS, activo al azar entre los válidos.
                        Pregunta: dadas las fechas de entrada, ¿elegir con drawdown+RSI+peor 12 m bate al azar?
      modo='timing'   : MISMOS ACTIVOS (el conjunto de activos de las operaciones reales), fechas al azar
                        entre las fechas de decisión mensuales.
                        Pregunta: con esos activos, ¿entrar tras sobreventa bate a entrar en fechas aleatorias?
      modo='total'    : fechas Y activos al azar. Línea base sin ninguna habilidad: misma exposición y holding.

    En 'timing' y 'total' las entradas que no caben (slots llenos, activo ya en cartera) se aplazan al mes
    siguiente para conservar la exposición. En 'seleccion' se pierden (el calendario real ya es factible).
    Devuelve (resumen, simulaciones, real). p_valor = (1 + nº placebos >= real) / (n + 1), unilateral.
    """
    if modo not in ('seleccion', 'timing', 'total'):
        raise ValueError("modo debe ser 'seleccion', 'timing' o 'total'")
    s_real, ops_real, m_real = ejecutar_variante(MotorCls, precios, rentabilidades, cfg, cash_columna, columna_spy,
                                                 coste, fecha_inicio_operativa, capital)
    est = m_real.estado_final
    entradas = [(o['entrada'], o['activo']) for o in ops_real]
    entradas += [(info['entrada'], a) for a, info in est.get('posiciones', {}).items()]
    calendario = Counter(f for f, _ in entradas)
    activos_reales = [a for _, a in entradas]
    fechas_dec = list(est.get('fechas_decision', []))

    def _stats(s, ops, m):
        d = metricas_serie(s, rf)
        d['Ret_medio_op'] = float(np.mean([o['beneficio'] for o in ops])) if ops else np.nan
        d['Win-rate'] = float(np.mean([o['beneficio'] > 0 for o in ops])) if ops else np.nan
        d['Expo'] = _expo(m)
        d['Ops'] = len(ops)
        return d

    real = _stats(s_real, ops_real, m_real)
    rng = np.random.default_rng(semilla)
    filas = []
    for i in range(n_sim):
        if modo == 'seleccion':
            placebo = dict(calendario=calendario, rng=rng)
        else:
            idx = rng.integers(0, len(fechas_dec), size=len(entradas))
            if modo == 'timing':
                items = list(activos_reales)
                rng.shuffle(items)
            else:
                items = [None] * len(entradas)
            programa = {}
            for j, it in zip(idx, items):
                programa.setdefault(fechas_dec[j], []).append(it)
            placebo = dict(programa=programa, rng=rng)
        s, ops, m = ejecutar_variante(MotorCls, precios, rentabilidades, cfg, cash_columna, columna_spy, coste,
                                      fecha_inicio_operativa, capital, placebo=placebo)
        filas.append(_stats(s, ops, m))
        if progreso and (i + 1) % 25 == 0:
            print(f"   ... {i + 1}/{n_sim} simulaciones ({modo})")
    sims = pd.DataFrame(filas)

    resumen = {}
    for k in ['CAGR', 'Sharpe', 'MaxDD', 'Ret_medio_op', 'Win-rate', 'Expo', 'Ops']:
        x = sims[k].dropna()
        resumen[k] = {
            'real': real[k], 'placebo_media': x.mean(), 'placebo_p5': x.quantile(0.05),
            'placebo_p50': x.median(), 'placebo_p95': x.quantile(0.95),
            'p_valor': (1 + (x >= real[k]).sum()) / (len(x) + 1) if len(x) else np.nan,
        }
    return pd.DataFrame(resumen).T, sims, real
