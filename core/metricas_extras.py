"""
MÉTRICAS EXTRAS PARA ESTRATEGIAS NO CONVENCIONALES
===================================================
Métricas específicas para estrategias de trading activo:
- Win-rate (% de operaciones rentables)
- Profit factor (ganancias brutas / pérdidas brutas)
- Information Ratio vs benchmark
- Frecuencia de señales
- Ratio beneficio medio / pérdida media
- Coste anual del hedge (para estrategias de cobertura)
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional


class CalculadorMetricasExtras:
    """Calcula métricas específicas para estrategias de trading activo."""
    
    def __init__(
        self,
        serie_patrimonio: pd.Series,
        log_operaciones: Optional[List[Dict]] = None,
        serie_benchmark: Optional[pd.Series] = None
    ):
        self.patrimonio = serie_patrimonio
        self.operaciones = log_operaciones or []
        self.serie_benchmark = serie_benchmark
    
    def win_rate(self) -> float:
        """Porcentaje de operaciones rentables."""
        if not self.operaciones:
            return 0.0
        rentables = sum(1 for op in self.operaciones if op.get('beneficio', 0) > 0)
        return rentables / len(self.operaciones)
    
    def profit_factor(self) -> float:
        """Ratio entre ganancias brutas y pérdidas brutas."""
        if not self.operaciones:
            return 0.0
        ganancias = sum(op.get('beneficio', 0) for op in self.operaciones if op.get('beneficio', 0) > 0)
        perdidas = abs(sum(op.get('beneficio', 0) for op in self.operaciones if op.get('beneficio', 0) < 0))
        if perdidas == 0:
            return float('inf') if ganancias > 0 else 0.0
        return ganancias / perdidas
    
    def ratio_beneficio_perdida(self) -> Dict[str, float]:
        """Beneficio medio y pérdida media por operación."""
        if not self.operaciones:
            return {'beneficio_medio': 0.0, 'perdida_media': 0.0, 'ratio': 0.0}
        
        beneficios = [op.get('beneficio', 0) for op in self.operaciones if op.get('beneficio', 0) > 0]
        perdidas = [abs(op.get('beneficio', 0)) for op in self.operaciones if op.get('beneficio', 0) < 0]
        
        ben_medio = np.mean(beneficios) if beneficios else 0.0
        per_medio = np.mean(perdidas) if perdidas else 0.0
        ratio = ben_medio / per_medio if per_medio > 0 else 0.0
        
        return {
            'beneficio_medio': ben_medio,
            'perdida_media': per_medio,
            'ratio': ratio
        }
    
    def information_ratio(self) -> float:
        """
        Information Ratio = (Rp - Rb) / tracking_error
        Mide el alpha por unidad de riesgo de seguimiento.
        """
        if self.serie_benchmark is None or self.serie_benchmark.empty:
            return 0.0
        
        ret_p = self.patrimonio.pct_change().dropna()
        b = self.serie_benchmark.reindex(ret_p.index, method='ffill').dropna()
        ret_b = b.pct_change().dropna()
        
        # Alinear
        df = pd.DataFrame({'p': ret_p, 'b': ret_b}).dropna()
        if len(df) < 20:
            return 0.0
        
        diff = df['p'] - df['b']
        tracking_error = diff.std() * np.sqrt(252)
        
        if tracking_error == 0:
            return 0.0
        
        rp_anual = (1 + df['p']).prod() ** (252 / len(df)) - 1
        rb_anual = (1 + df['b']).prod() ** (252 / len(df)) - 1
        
        return (rp_anual - rb_anual) / tracking_error
    
    def frecuencia_senales(self) -> Dict[str, float]:
        """Frecuencia anual de señales/operaciones."""
        if not self.operaciones or len(self.patrimonio) < 2:
            return {'operaciones_totales': 0, 'operaciones_anuales': 0.0}
        
        años = (self.patrimonio.index[-1] - self.patrimonio.index[0]).days / 365.25
        if años == 0:
            return {'operaciones_totales': len(self.operaciones), 'operaciones_anuales': 0.0}
        
        return {
            'operaciones_totales': len(self.operaciones),
            'operaciones_anuales': len(self.operaciones) / años
        }
    
    def coste_anual_hedge(self, prima_anual_pct: float = 0.03) -> float:
        """
        Coste anual estimado del hedge (para estrategias de tail risk).
        prima_anual_pct: porcentaje del patrimonio que se paga anualmente como prima.
        """
        return prima_anual_pct
    
    def calcular_todas_las_metricas(self) -> Dict[str, float]:
        """Devuelve todas las métricas extras en un diccionario."""
        bp = self.ratio_beneficio_perdida()
        freq = self.frecuencia_senales()
        
        return {
            'Win-rate': self.win_rate(),
            'Profit Factor': self.profit_factor(),
            'Beneficio Medio': bp['beneficio_medio'],
            'Pérdida Media': bp['perdida_media'],
            'Ratio B/P': bp['ratio'],
            'Information Ratio': self.information_ratio(),
            'Operaciones Totales': freq['operaciones_totales'],
            'Operaciones Anuales': freq['operaciones_anuales']
        }
    
    def diagnosticar(self) -> str:
        """Diagnóstico cualitativo de las métricas extras."""
        m = self.calcular_todas_las_metricas()
        d = []
        
        wr = m['Win-rate']
        if wr > 0.60:
            d.append(f"✅ Win-rate alto ({wr:.1%}).")
        elif wr > 0.45:
            d.append(f"🟢 Win-rate aceptable ({wr:.1%}).")
        elif wr > 0:
            d.append(f"🟡 Win-rate bajo ({wr:.1%}).")
        else:
            d.append("⚪ Sin operaciones registradas.")
        
        pf = m['Profit Factor']
        if pf > 2.0:
            d.append(f"✅ Profit factor excelente ({pf:.2f}).")
        elif pf > 1.5:
            d.append(f"🟢 Profit factor bueno ({pf:.2f}).")
        elif pf > 1.0:
            d.append(f"🟡 Profit factor ajustado ({pf:.2f}).")
        elif pf > 0:
            d.append(f"🔴 Profit factor negativo ({pf:.2f}).")
        
        ir = m['Information Ratio']
        if ir > 0.5:
            d.append(f"✅ Information Ratio excelente ({ir:.2f}).")
        elif ir > 0.2:
            d.append(f"🟢 Information Ratio bueno ({ir:.2f}).")
        elif ir > 0:
            d.append(f"🟡 Information Ratio bajo ({ir:.2f}).")
        else:
            d.append(f"🔴 Information Ratio negativo ({ir:.2f}).")
        
        return "\n  ".join(d)