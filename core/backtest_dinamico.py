"""
MOTOR BACKTEST DINÁMICO
=======================
Motor de backtest para estrategias que requieren asignaciones variables en el tiempo:
- Pesos que dependen de señales (momentum, RSI, drawdown, sentimiento)
- Holding periods fijos (ej. 6 meses en Contrarian)
- Posiciones cortas (short selling)
- Cash como posición activa (SHV, BIL)

Compatible con CalculadorMetricas y GeneradorInformes del motor original.
"""
import pandas as pd
import numpy as np
from typing import Callable, Dict, List, Optional


class MotorBacktestDinamico:
    """
    Motor de backtest que acepta una función generadora de pesos.
    
    La función generadora recibe:
        - fecha_actual: pd.Timestamp
        - precios_historicos: pd.DataFrame (precios hasta la fecha)
        - rentabilidades_historicas: pd.DataFrame (retornos hasta la fecha)
        - estado_estrategia: dict (estado interno que la estrategia puede modificar)
    
    Y debe devolver:
        - pesos_objetivo: dict {ticker: peso} (pueden ser negativos para short)
        - estado_estrategia: dict (actualizado)
    """
    
    def __init__(
        self,
        precios: pd.DataFrame,
        rentabilidades: pd.DataFrame,
        generador_pesos: Callable,
        frecuencia_decision: str = 'M',  # 'D', 'W', 'M', 'Q'
        coste_transaccion: float = 0.001,
        benchmark_ticker: Optional[str] = None,
        permitir_short: bool = False,
        max_short_porcentaje: float = 0.30
    ):
        self.precios = precios
        self.rentabilidades = rentabilidades
        self.generador_pesos = generador_pesos
        self.frecuencia = frecuencia_decision
        self.coste_transaccion = coste_transaccion
        self.permitir_short = permitir_short
        self.max_short = max_short_porcentaje
        self.nombres_activos = list(precios.columns)
        
        # Benchmark (SPY por defecto)
        self.serie_benchmark = None
        if benchmark_ticker:
            try:
                import yfinance as yf
                b = yf.download(
                    benchmark_ticker,
                    start=precios.index[0],
                    end=precios.index[-1],
                    progress=False,
                    auto_adjust=True
                )
                if not b.empty:
                    if isinstance(b.columns, pd.MultiIndex):
                        b.columns = b.columns.get_level_values(0)
                    self.serie_benchmark = b['Close'].squeeze().dropna()
            except Exception as e:
                print(f"⚠️ No se pudo descargar benchmark {benchmark_ticker}: {e}")
    
    def _es_fecha_decision(self, fecha_actual, fecha_anterior) -> bool:
        """Determina si hoy toca tomar una decisión según la frecuencia."""
        if self.frecuencia == 'D':
            return True
        elif self.frecuencia == 'W':
            return fecha_actual.isocalendar()[1] != fecha_anterior.isocalendar()[1]
        elif self.frecuencia == 'M':
            return fecha_actual.month != fecha_anterior.month
        elif self.frecuencia == 'Q':
            return fecha_actual.quarter != fecha_anterior.quarter
        return False
    
    def _validar_pesos(self, pesos: Dict[str, float]) -> Dict[str, float]:
        """Valida y normaliza los pesos según las reglas del motor."""
        # Filtrar activos que no existen en el universo
        pesos = {k: v for k, v in pesos.items() if k in self.nombres_activos}
        
        # Si no hay pesos, todo a cash (peso 0 en todos los activos)
        if not pesos:
            return {a: 0.0 for a in self.nombres_activos}
        
        # Control de short selling
        if not self.permitir_short:
            pesos = {k: max(0.0, v) for k, v in pesos.items()}
        else:
            # Limitar exposición corta
            total_short = sum(abs(v) for v in pesos.values() if v < 0)
            if total_short > self.max_short:
                factor = self.max_short / total_short
                pesos = {k: v * factor if v < 0 else v for k, v in pesos.items()}
        
        # Normalizar: la suma de valores absolutos debe ser <= 1.0
        suma_abs = sum(abs(v) for v in pesos.values())
        if suma_abs > 1.0:
            factor = 1.0 / suma_abs
            pesos = {k: v * factor for k, v in pesos.items()}
        
        # Rellenar activos faltantes con 0
        for activo in self.nombres_activos:
            if activo not in pesos:
                pesos[activo] = 0.0
        
        return pesos
    
    def ejecutar_backtest(
        self,
        capital_inicial: float = 10000,
        estado_inicial: Optional[Dict] = None
    ) -> pd.Series:
        """
        Ejecuta el backtest día a día, llamando al generador de pesos en las fechas de decisión.
        El capital no asignado a activos se mantiene como CASH (preserva valor, no genera rentabilidad).
        """
        if len(self.rentabilidades) < 2:
            print("❌ Error: No hay suficientes datos históricos.")
            self.serie_patrimonio = pd.Series(dtype=float)
            self.serie_buy_hold = pd.Series(dtype=float)
            self.log_transacciones = []
            self.log_operaciones = []
            return self.serie_patrimonio
        
        # Inicialización
        pesos_actuales = {a: 0.0 for a in self.nombres_activos}
        valores = {a: 0.0 for a in self.nombres_activos}
        cash_disponible = capital_inicial  # ← NUEVO: cash como variable independiente
        estado = estado_inicial or {}
        
        historial_patrimonio = [capital_inicial]
        historial_buy_hold = [capital_inicial]
        fechas = [self.rentabilidades.index[0]]
        
        log_transacciones = []
        log_operaciones = []
        
        valores_bh = {a: capital_inicial / len(self.nombres_activos) for a in self.nombres_activos}
        
        # Primera decisión en la primera fecha
        fecha_anterior = self.rentabilidades.index[0]
        try:
            pesos_objetivo, estado = self.generador_pesos(
                fecha_anterior,
                self.precios.loc[:fecha_anterior],
                self.rentabilidades.loc[:fecha_anterior],
                estado
            )
            pesos_objetivo = self._validar_pesos(pesos_objetivo)
        except Exception as e:
            print(f"⚠️ Error en primera decisión: {e}. Todo a cash.")
            pesos_objetivo = {a: 0.0 for a in self.nombres_activos}
        
        # Asignar capital inicial según pesos
        suma_pesos = sum(pesos_objetivo.values())
        for activo in self.nombres_activos:
            valores[activo] = capital_inicial * pesos_objetivo[activo]
        cash_disponible = capital_inicial * (1.0 - suma_pesos)  # ← NUEVO: lo que sobra va a cash
        pesos_actuales = pesos_objetivo.copy()
        
        # Bucle día a día
        for i in range(1, len(self.rentabilidades)):
            fecha = self.rentabilidades.index[i]
            ret = self.rentabilidades.iloc[i]
            
            # Actualizar valores por rentabilidad del día
            for activo in self.nombres_activos:
                valores[activo] = valores[activo] * (1 + ret[activo])
            # El cash NO genera rentabilidad (se mantiene constante)
            
            total_patrimonio = sum(valores.values()) + cash_disponible
            
            # Calcular pesos actuales reales
            if total_patrimonio > 0:
                pesos_actuales = {a: v / total_patrimonio for a, v in valores.items()}
            else:
                pesos_actuales = {a: 0.0 for a in self.nombres_activos}
            
            # Buy & Hold (pesos iniciales fijos)
            for activo in self.nombres_activos:
                valores_bh[activo] = valores_bh[activo] * (1 + ret[activo])
            
            # ¿Toca tomar decisión?
            if self._es_fecha_decision(fecha, fecha_anterior):
                try:
                    nuevos_pesos, estado = self.generador_pesos(
                        fecha,
                        self.precios.loc[:fecha],
                        self.rentabilidades.loc[:fecha],
                        estado
                    )
                    nuevos_pesos = self._validar_pesos(nuevos_pesos)
                except Exception as e:
                    print(f"⚠️ Error en decisión {fecha.strftime('%Y-%m-%d')}: {e}")
                    nuevos_pesos = pesos_actuales.copy()
                
                # Calcular rotación y costes
                rotacion = sum(
                    abs(nuevos_pesos[a] - pesos_actuales[a])
                    for a in self.nombres_activos
                ) / 2
                coste = rotacion * total_patrimonio * self.coste_transaccion
                total_tras_coste = total_patrimonio - coste
                
                # Reasignar: nuevo capital invertido + nuevo cash
                suma_nuevos_pesos = sum(nuevos_pesos.values())
                for activo in self.nombres_activos:
                    valores[activo] = total_tras_coste * nuevos_pesos[activo]
                cash_disponible = total_tras_coste * (1.0 - suma_nuevos_pesos)  # ← NUEVO
                
                # Log
                if rotacion > 0.001:
                    log_transacciones.append({
                        'Fecha': fecha.strftime('%Y-%m-%d'),
                        'Rotacion %': f"{rotacion:.2%}",
                        'Coste (€)': round(coste, 2),
                        'Patrimonio (€)': round(total_tras_coste, 2),
                        '% Cash': f"{(1.0 - suma_nuevos_pesos):.1%}"
                    })
                
                pesos_actuales = nuevos_pesos.copy()
                fecha_anterior = fecha
            
            historial_patrimonio.append(sum(valores.values()) + cash_disponible)
            historial_buy_hold.append(sum(valores_bh.values()))
            fechas.append(fecha)
        
        # Resultados
        self.serie_patrimonio = pd.Series(historial_patrimonio, index=pd.to_datetime(fechas))
        self.serie_buy_hold = pd.Series(historial_buy_hold, index=pd.to_datetime(fechas))
        self.log_transacciones = log_transacciones
        self.log_operaciones = log_operaciones
        self.pesos_actuales_finales = pesos_actuales
        self.estado_final = estado
        
        return self.serie_patrimonio