"""
STATARB: Motor de Arbitraje Estadístico (ETF vs. Cesta de Subyacentes)
======================================================================
Construye un NAV sintético, calcula el spread logarítmico y genera 
señales de trading market-neutral basadas en z-scores.
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from typing import Dict, Optional, List

class StatArbEngine:
    """Construye NAV sintético y detecta dislocaciones ETF vs. cesta."""
    
    def __init__(self, etf_col: str, cesta_cols: List[str], pesos_cesta: Optional[List[float]] = None):
        """
        Args:
            etf_col: Nombre de la columna del ETF en precios_ajustados
            cesta_cols: Lista de nombres de columna de los subyacentes
            pesos_cesta: Pesos de cada subyacente (None = igualitarios)
        """
        self.etf = etf_col
        self.cesta = cesta_cols
        self.pesos = pesos_cesta or [1.0 / len(cesta_cols)] * len(cesta_cols)
    
    def construir_nav_sintetico(self, precios_df: pd.DataFrame):
        """
        Construye el NAV normalizado (base 1.0 en el día 1) 
        como la suma ponderada de los subyacentes normalizados.
        """
        nav = pd.Series(0.0, index=precios_df.index)
        for col, peso in zip(self.cesta, self.pesos):
            if col in precios_df.columns:
                precio_norm = precios_df[col] / precios_df[col].iloc[0]
                nav += peso * precio_norm
        
        if self.etf not in precios_df.columns:
            raise KeyError(f"Columna ETF '{self.etf}' no encontrada. Columnas disponibles: {list(precios_df.columns)[:5]}...")
        
        etf_norm = precios_df[self.etf] / precios_df[self.etf].iloc[0]
        return nav, etf_norm

    def calcular_spread(self, precios_df: pd.DataFrame) -> pd.Series:
        """Spread logarítmico: log(ETF_norm) - log(NAV_norm)."""
        nav, etf_norm = self.construir_nav_sintetico(precios_df)
        spread = np.log(etf_norm) - np.log(nav)
        return spread
    
    def test_estacionariedad(self, spread: pd.Series, p_valor_max: float = 0.10) -> Dict:
        """Test ADF sobre el spread para validar la oportunidad de arbitraje."""
        spread_clean = spread.dropna()
        if len(spread_clean) < 60:
            return {'estacionario': False, 'p_valor': 1.0, 'stat': 0.0, 'error': 'Datos insuficientes'}
        try:
            stat, p_valor, _, _, _, _ = adfuller(spread_clean.values, maxlag=1)
            return {
                'estacionario': p_valor < p_valor_max,
                'p_valor': p_valor,
                'stat': stat,
                'error': None
            }
        except Exception as e:
            return {'estacionario': False, 'p_valor': 1.0, 'stat': 0.0, 'error': str(e)}
    
    def calcular_zscore(self, spread: pd.Series, ventana: int = 60) -> pd.Series:
        """Calcula el z-score del spread sobre una ventana móvil."""
        media = spread.rolling(window=ventana).mean()
        std = spread.rolling(window=ventana).std()
        return (spread - media) / std