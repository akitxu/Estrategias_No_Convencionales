"""
==========================================================================
MOTOR BACKTEST COMPLETO (DCA Simétrico + Benchmark + Buy&Hold + Métricas)
==========================================================================
"""
import pandas as pd
import numpy as np
import yfinance as yf

class OptimizadorCarteras:
    def __init__(self, rentabilidades_diarias):
        self.rentabilidades = rentabilidades_diarias
        self.matriz_covarianza = rentabilidades_diarias.cov() * 252

    def equal_weight(self):
        pesos = np.array([1/len(self.rentabilidades.columns)] * len(self.rentabilidades.columns))
        return dict(zip(self.rentabilidades.columns, pesos))


class MotorBacktest:
    def __init__(self, precios, rentabilidades, pesos, frecuencia_rebalanceo='Y', coste_transaccion=0.001, benchmark_ticker=None):
        self.precios = precios
        self.rentabilidades = rentabilidades
        self.nombres_activos = list(pesos.keys())
        self.pesos_objetivo = np.array(list(pesos.values()))
        self.frecuencia = frecuencia_rebalanceo
        self.coste_transaccion = coste_transaccion
        self.benchmark_ticker = benchmark_ticker
        self.serie_benchmark = None
        if benchmark_ticker:
            try:
                b = yf.download(benchmark_ticker, start=precios.index[0], end=precios.index[-1], progress=False, auto_adjust=True)
                if not b.empty:
                    if isinstance(b.columns, pd.MultiIndex): b.columns = b.columns.get_level_values(0)
                    self.serie_benchmark = b['Close'].squeeze().dropna()
            except: pass

    def ejecutar_backtest(self, capital_inicial=10000, aportacion_mensual=0):
        if len(self.rentabilidades) < 2:
            print("❌ Error: No hay suficientes datos históricos en el rango seleccionado para ejecutar el backtest.")
            self.serie_patrimonio = pd.Series(dtype=float)
            self.serie_buy_hold = pd.Series(dtype=float)
            self.log_transacciones = []
            self.pesos_actuales_finales = dict(zip(self.nombres_activos, self.pesos_objetivo))
            return self.serie_patrimonio
        
        valores_reb = self.pesos_objetivo * capital_inicial
        valores_bnh = self.pesos_objetivo * capital_inicial
        historial, historial_bnh, fechas = [np.sum(valores_reb)], [np.sum(valores_bnh)], [self.rentabilidades.index[0]]
        log, ult_mes, pesos_actuales = [], self.rentabilidades.index[0].replace(day=1), self.pesos_objetivo.copy()
        
        for i in range(1, len(self.rentabilidades)):
            fec, ret = self.rentabilidades.index[i], self.rentabilidades.iloc[i].values
            valores_reb = valores_reb * (1 + ret)
            valores_bnh = valores_bnh * (1 + ret)
            pri_dia = fec.replace(day=1)
            if aportacion_mensual > 0 and pri_dia > ult_mes:
                valores_reb += self.pesos_objetivo * aportacion_mensual
                valores_bnh += self.pesos_objetivo * aportacion_mensual
                ult_mes = pri_dia
            total_reb = np.sum(valores_reb)
            pesos_actuales = valores_reb / total_reb if total_reb > 0 else self.pesos_objetivo
            
            if (self.frecuencia=='Y' and fec.year != self.rentabilidades.index[i-1].year) or \
               (self.frecuencia=='Q' and fec.quarter != self.rentabilidades.index[i-1].quarter) or \
               (self.frecuencia=='M' and fec.month != self.rentabilidades.index[i-1].month):
                rotacion = np.sum(np.abs(self.pesos_objetivo - pesos_actuales)) / 2
                coste = rotacion * total_reb * self.coste_transaccion
                total_tras_coste = total_reb - coste
                valores_reb = self.pesos_objetivo * total_tras_coste
                pesos_actuales = self.pesos_objetivo.copy()
                log.append({'Fecha': fec.strftime('%Y-%m-%d'), 'Rotacion %': f"{rotacion:.2%}", 'Coste (€)': round(coste, 2), 'Patrimonio (€)': round(total_tras_coste, 2)})
            
            historial.append(np.sum(valores_reb))
            historial_bnh.append(np.sum(valores_bnh))
            fechas.append(fec)
            
        self.serie_patrimonio = pd.Series(historial, index=pd.to_datetime(fechas))
        self.serie_buy_hold = pd.Series(historial_bnh, index=pd.to_datetime(fechas))
        self.log_transacciones = log
        self.pesos_actuales_finales = dict(zip(self.nombres_activos, pesos_actuales))
        return self.serie_patrimonio


class CalculadorMetricas:
    def __init__(self, serie_patrimonio, serie_buy_hold=None, serie_benchmark=None):
        self.patrimonio = serie_patrimonio
        self.rentabilidades = serie_patrimonio.pct_change().dropna()
        self.serie_buy_hold = serie_buy_hold
        self.serie_benchmark = serie_benchmark

    def _calc(self, s, rf):
        s = s.dropna()
        if len(s) < 2: return {k:0 for k in ['CAGR','Volatilidad','Sharpe','Sortino','Max Drawdown','VaR 95%','Alpha','Beta','R2','Tracking Error']}
        años_totales = (s.index[-1] - s.index[0]).days / 365.25
        r = s.pct_change().dropna()
        cagr = (s.iloc[-1]/s.iloc[0]) ** (1 / años_totales) - 1 if años_totales > 0 else 0
        vol = r.std() * np.sqrt(252.0 if len(s) > 200 else 12.0)
        vol_baja = r[r < 0].std() * np.sqrt(252.0 if len(s) > 200 else 12.0) if not r[r < 0].empty else 0
        return {'CAGR': cagr, 'Volatilidad': vol, 'Sharpe': (cagr-rf)/vol if vol>0 else 0, 'Sortino': (cagr-rf)/vol_baja if vol_baja>0 else 0, 'Max Drawdown': ((s-s.cummax())/s.cummax()).min(), 'VaR 95%': -np.percentile(r,5)*s.iloc[-1]}

    def calcular_todas_las_metricas(self, rf=0.02):
        reb, bh = self._calc(self.patrimonio, rf), self._calc(self.serie_buy_hold, rf) if self.serie_buy_hold is not None else None
        if self.serie_benchmark is not None and not self.serie_benchmark.empty:
            b = self.serie_benchmark.reindex(self.patrimonio.index, method='ffill').dropna()
            if len(b) > 1:
                d = pd.DataFrame({'c':self.patrimonio.pct_change().dropna(), 'b':b.pct_change().dropna()}).dropna()
                beta = d['c'].cov(d['b'])/d['b'].var() if d['b'].var()!=0 else 0
                alpha = reb['CAGR'] - (((1+d['b']).prod()**(252/len(d['b']))-1)*beta)
                reb.update({'Alpha': alpha, 'Beta': beta, 'R2': d['c'].corr(d['b'])**2, 'Tracking Error': (d['c']-d['b']).std()*np.sqrt(252)})
            else: reb.update({'Alpha': 0, 'Beta': 0, 'R2': 0, 'Tracking Error': 0})
        else: reb.update({'Alpha': 0, 'Beta': 0, 'R2': 0, 'Tracking Error': 0})
        return reb, bh

    def diagnosticar(self):
        m, _ = self.calcular_todas_las_metricas()
        d = []
        s = m.get('Sharpe', 0)
        if s > 1: d.append(f"✅ Ratio de Sharpe excelente ({s:.2f}).")
        elif s > 0.5: d.append(f"🟢 Ratio de Sharpe bueno ({s:.2f}).")
        elif s > 0: d.append(f"🟡 Ratio de Sharpe aceptable ({s:.2f}).")
        else: d.append(f"🔴 Ratio de Sharpe negativo ({s:.2f}).")
        dd = abs(m.get('Max Drawdown', 0))
        if dd < 0.10: d.append(f"✅ Riesgo de caída muy controlado (Max DD: {dd:.1%}).")
        elif dd < 0.20: d.append(f"🟡 Riesgo de caída moderado (Max DD: {dd:.1%}).")
        else: d.append(f"🔴 Riesgo de caída elevado (Max DD: {dd:.1%}).")
        b = m.get('Beta', 0)
        if b > 0:
            if b < 0.8: d.append(f"🛡️ Beta baja ({b:.2f}).")
            elif b > 1.2: d.append(f"📈 Beta alta ({b:.2f}).")
            else: d.append(f"⚖️ Beta media ({b:.2f}).")
        a = m.get('Alpha', 0)
        if a > 0.005: d.append(f"🌟 Alpha positivo ({a:.2%}).")
        elif a < -0.005: d.append(f"📉 Alpha negativo ({a:.2%}).")
        return "\n  ".join(d)