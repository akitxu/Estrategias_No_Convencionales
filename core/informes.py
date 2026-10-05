"""
==========================================================================
GENERADOR INFORMES (Consola, Logs y Gráficos)
==========================================================================
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class GeneradorInformes:
    def __init__(self, serie_patrimonio, metricas, nombre_estrategia="Estrategia", 
                 serie_buy_hold=None, log_transacciones=None, 
                 pesos_actuales=None, pesos_ideales=None):
        self.patrimonio = serie_patrimonio
        self.metricas_reb, self.metricas_bh = metricas
        self.nombre = nombre_estrategia
        self.serie_buy_hold = serie_buy_hold
        self.log_transacciones = log_transacciones if log_transacciones else []
        self.pesos_actuales = pesos_actuales
        self.pesos_ideales = pesos_ideales

    def imprimir_metricas(self):
        print(f"\n{'='*75}\nINFORME DE DIAGNÓSTICO: {self.nombre}\n{'='*75}")
        try:
            from IPython.display import display
            datos_tabla = []
            for k, v_reb in self.metricas_reb.items():
                v_bh = self.metricas_bh.get(k, 0) if self.metricas_bh else 0
                if k in ['CAGR', 'Volatilidad', 'Max Drawdown', 'Tracking Error']:
                    fmt_reb, fmt_bh = f"{v_reb:.2%}", f"{v_bh:.2%}"
                elif k in ['Sharpe', 'Sortino', 'Alpha', 'Beta', 'R2']:
                    fmt_reb, fmt_bh = f"{v_reb:.2f}", f"{v_bh:.2f}"
                else:
                    fmt_reb, fmt_bh = f"{v_reb:.2f}€", f"{v_bh:.2f}€"
                datos_tabla.append({'Métrica': k, 'Estrategia': fmt_reb, 'Buy & Hold': fmt_bh})
            display(pd.DataFrame(datos_tabla))
        except ImportError:
            print(f"{'Métrica':<25} | {'Con Rebalanceo':<18} | {'Buy & Hold':<18}\n" + "-" * 75)
            for key in self.metricas_reb.keys():
                val_reb = self.metricas_reb[key]
                val_bh = self.metricas_bh.get(key, 0) if self.metricas_bh else 0
                if key in ['CAGR', 'Volatilidad', 'Max Drawdown', 'Tracking Error']:
                    print(f"{key:<25} | {val_reb:>18.2%} | {val_bh:>18.2%}")
                elif key in ['Sharpe', 'Sortino', 'Alpha', 'Beta', 'R2']:
                    print(f"{key:<25} | {val_reb:>18.2f} | {val_bh:>18.2f}")
                else:
                    print(f"{key:<25} | {val_reb:>18.2f}€ | {val_bh:>18.2f}€")
        print(f"{'='*75}\n")

    def imprimir_log(self):
        if not self.log_transacciones: return
        print(f"--- LOG DE REBALANCEOS ---\n{'Fecha':<12} | {'Rotación':<10} | {'Coste (€)':<10} | {'Patrimonio (€)':<15}\n" + "-" * 55)
        for t in self.log_transacciones:
            print(f"{t['Fecha']:<12} | {t['Rotacion %']:<10} | {t['Coste (€)']:<10.2f} | {t['Patrimonio (€)']:<15.2f}")
        print(f"Coste total: {sum(t['Coste (€)'] for t in self.log_transacciones):.2f}€\n")

    def imprimir_seguimiento(self):
        if not self.pesos_actuales or not self.pesos_ideales: return
        print(f"\n--- SEGUIMIENTO ACTUAL ({datetime.now().strftime('%Y-%m-%d')}) ---")
        print(f"{'Activo':<30} | {'Peso Ideal':>10} | {'Peso Actual':>11} | {'Desviación':>11} | {'Acción':<8}")
        print("-" * 85)
        for ticker in self.pesos_ideales.keys():
            nombre_corto = (ticker[:27] + '...') if len(ticker) > 30 else ticker
            p_ideal, p_actual = self.pesos_ideales[ticker], self.pesos_actuales[ticker]
            desv = p_actual - p_ideal
            accion = "Vender" if desv > 0.005 else ("Comprar" if desv < -0.005 else "Mantener")
            print(f"{nombre_corto:<30} | {p_ideal:>10.2%} | {p_actual:>11.2%} | {desv:>+11.2%} | {accion:<8}")
        print("-" * 85 + "\n")

    def graficar(self, guardar_como=None):
        """Genera gráfico de evolución del patrimonio, lo muestra y lo guarda si se indica."""
        plt.figure(figsize=(10, 5))
        plt.plot(self.patrimonio.index, self.patrimonio, label='Rebalanceo (DCA)', color='blue', lw=2)
        
        if self.serie_buy_hold is not None:
            plt.plot(self.serie_buy_hold.index, self.serie_buy_hold, label='Buy & Hold', color='gray', ls='--', lw=2)
        
        plt.title(f'Evolución del Patrimonio - {self.nombre}')
        plt.grid(linestyle='--', alpha=0.5)
        plt.xlabel('Fecha')
        plt.ylabel('Patrimonio (€)')
        plt.legend()
        
        # 1. Mostrar SIEMPRE en el entorno Jupyter/Colab
        plt.show()
        
        # 2. Guardar en disco si se proporciona una ruta
        if guardar_como: 
            plt.savefig(guardar_como, dpi=150, bbox_inches='tight')
            print(f"✅ Gráfico guardado en: {guardar_como}")
        
        plt.close()