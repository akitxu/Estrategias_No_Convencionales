"""
GEMELÓLOGO: Calculador de Cointegración para Pairs Trading
==========================================================
Implementa el test de Engle-Granger, cálculo de z-scores y
detección de ruptura estructural entre pares de activos.
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, coint
from typing import Tuple, Dict, Optional


class Gemelologo:
    """Analiza la cointegración entre pares de activos."""
    
    def __init__(self, precios: pd.DataFrame, ventana_rolling: int = 252):
        self.precios = precios
        self.ventana = ventana_rolling
        self.resultados = {}
    
    def test_cointegracion(self, activo_a: str, activo_b: str, 
                           p_valor_maximo: float = 0.05) -> Dict:
        """Ejecuta el test de Engle-Granger entre dos activos."""
        respuesta_fallback = {
            'cointegrado': False,
            'p_valor': 1.0,
            'stat': 0.0,
            'ratio_cointegracion': 1.0,
            'spread': pd.Series(dtype=float),
            'activo_a': activo_a,
            'activo_b': activo_b,
            'error': 'No iniciado'
        }
        
        if activo_a not in self.precios.columns or activo_b not in self.precios.columns:
            respuesta_fallback['error'] = f'Activo no encontrado. Columnas: {list(self.precios.columns)[:3]}...'
            return respuesta_fallback
        
        log_a = np.log(self.precios[activo_a].dropna())
        log_b = np.log(self.precios[activo_b].dropna())
        
        df = pd.DataFrame({'a': log_a, 'b': log_b}).dropna()
        if len(df) < 60:
            respuesta_fallback['error'] = 'Datos insuficientes (<60 días)'
            return respuesta_fallback
        
        try:
            stat, p_valor, _ = coint(df['a'], df['b'])
        except Exception as e:
            respuesta_fallback['error'] = f'Error en test coint: {e}'
            return respuesta_fallback
        
        beta = np.polyfit(df['b'].values, df['a'].values, 1)[0]
        spread = df['a'] - beta * df['b']
        
        return {
            'cointegrado': p_valor < p_valor_maximo,
            'p_valor': p_valor,
            'stat': stat,
            'ratio_cointegracion': beta,
            'spread': spread,
            'activo_a': activo_a,
            'activo_b': activo_b,
            'error': None
        }
    
    def calcular_zscore(self, spread: pd.Series, ventana: int = 60) -> pd.Series:
        media = spread.rolling(window=ventana).mean()
        std = spread.rolling(window=ventana).std()
        return (spread - media) / std
    
    def detectar_ruptura(self, spread: pd.Series, ventana: int = 60, umbral_adf: float = 0.05) -> bool:
        """
        Detecta si el spread ha perdido estacionariedad (ruptura estructural).
        Si el spread ya no es estacionario, el par ya NO está cointegrado.
        """
        spread_reciente = spread.tail(ventana).dropna()
        if len(spread_reciente) < 30:
            return True  # Datos insuficientes, asumir ruptura
        
        # Test ADF: H0 = no estacionario
        # adfuller retorna 5 valores: (stat, pvalue, usedlag, nobs, critical values)
        resultado_adf = adfuller(spread_reciente.values, maxlag=1)
        p_valor = resultado_adf[1]
        
        return p_valor > umbral_adf  # True si hay ruptura
    
    def analizar_par(self, activo_a: str, activo_b: str, 
                     p_valor_maximo: float = 0.05,
                     ventana_zscore: int = 60) -> Optional[Dict]:
        print(f"\n      [DEBUG] Analizando {activo_a} vs {activo_b}...")
        resultado = self.test_cointegracion(activo_a, activo_b, p_valor_maximo)
        
        print(f"      [DEBUG] Resultado: cointegrado={resultado.get('cointegrado')}, p_valor={resultado.get('p_valor'):.4f}, error={resultado.get('error')}")
        
        if 'error' in resultado and resultado['error'] is not None:
            print(f"      [DEBUG] ❌ Descartado por error: {resultado['error']}")
            return None
        
        if not resultado.get('cointegrado', False):
            print(f"      [DEBUG] ❌ Descartado por p_valor alto ({resultado.get('p_valor'):.4f} > {p_valor_maximo})")
            return None
        
        try:
            spread = resultado['spread']
            zscore = self.calcular_zscore(spread, ventana_zscore)
            print(f"      [DEBUG] ✅ ¡Éxito! Par cointegrado.")
            return {
                'activo_a': activo_a,
                'activo_b': activo_b,
                'ratio': resultado['ratio_cointegracion'],
                'p_valor': resultado['p_valor'],
                'spread': spread,
                'zscore': zscore,
                'cointegrado': True
            }
        except Exception as e:
            print(f"      [DEBUG] ❌ Excepción al calcular zscore: {e}")
            return None
    
    def escanear_pares(self, lista_pares: list, p_valor_maximo: float = 0.05,
                       ventana_zscore: int = 60) -> list:
        pares_validos = []
        print(f"\n🔬 Escaneando {len(lista_pares)} pares...")
        
        for a, b in lista_pares:
            print(f"   • {a} / {b}...", end=" ")
            resultado = self.analizar_par(a, b, p_valor_maximo, ventana_zscore)
            if resultado:
                print(f"✅ Cointegrado (p={resultado['p_valor']:.3f})")
                pares_validos.append(resultado)
            else:
                print("❌ Descartado") 
        
        print(f"\n📊 Resultado: {len(pares_validos)}/{len(lista_pares)} pares cointegrados")
        return pares_validos