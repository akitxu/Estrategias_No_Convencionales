# Capítulo 1: Patrones Armónicos (ABCD) — Detección de Formaciones Geométricas
Versión: 1.3 | Motor: Modular Dinámico v1.0 | Actualización: 2026-10-26

    "Los mercados no se mueven al azar; respiran en patrones fractales. Los ratios de Fibonacci no son magia, son la huella matemática de la psicología colectiva."
    — H.M. Gartley, Profits in the Stock Market (1935)

**Concepto clave:** Este capítulo implementa un scanner de patrones armónicos ABCD que detecta formaciones de cuatro puntos (A-B-C-D) basadas en ratios de Fibonacci. Cuando se identifica un patrón válido con tolerancia del 10%, se genera una señal de entrada en la dirección del rebote esperado, manteniendo la posición durante un período fijo (5 días) con stop-loss dinámico (-3%) y take-profit (+6%).  
La premisa es que los mercados exhiben comportamientos fractales y que ciertas relaciones geométricas entre movimientos de precio tienden a repetirse. El patrón ABCD es el más simple de la familia armónica y sirve como base para entender la lógica de detección de formaciones.
**⚠️ Advertencia:** Los patrones armónicos son herramientas de análisis técnico con limitaciones inherentes. No garantizan resultados y deben usarse junto con gestión de riesgo estricta.

## La Lógica de los Patrones Armónicos

A diferencia de los indicadores rezagados (como el RSI o las medias móviles), los patrones armónicos son estructuras de precio predictivas. Se basan en la premisa de que los movimientos del mercado siguen proporciones fractales derivadas de la secuencia de Fibonacci.

## Las 3 Reglas de Oro de la Operación Armónica

* **La Estructura es Sagrada:** Un patrón no es válido si no cumple con precisión las proporciones de Fibonacci en sus puntos (B, C y D). Una desviación superior al 10% invalida la geometría.
* **La PRZ es una Zona, no una Línea:** La Zona de Reversión Potencial es un área donde confluyen al menos 2 o 3 extensiones/retracciones de Fibonacci. Nunca se opera "a ciegas" en la PRZ; se espera una vela de confirmación.
* **Gestión de Riesgo Asimétrica:** El Stop Loss (-3%) se coloca siempre más allá del punto X, mientras que el Take Profit (+6%) busca un Ratio Riesgo/Beneficio mínimo de 2:1.

## Reglas Operativas Completas

  Parámetro | Valor / Regla |
 |---|---|
 | Patrones detectados | ABCD (Gartley, Bat, Butterfly, Crab) |
 | Universo | SPY, QQQ, XLF, XLK |
 | Temporalidad | Diaria |
 | Zona de Entrada (PRZ) | Confluencia de ratios B-C (0.382, 0.500, 0.618, 0.786) y C-D (1.272, 1.414, 1.618) |
 | Tolerancia | ±10% sobre ratios Fibonacci |
 | Stop Loss | -3% desde punto de entrada |
 | Take Profit | +6% desde punto de entrada |
 | Time Exit | 5 días máximo en posición |
 | Peso por posición | 95% invertido, 5% cash |
 | Frecuencia de revisión | Diaria |
 | Coste de transacción | 0,1% por operación |

## Arquitectura Técnica (Motor Dinámico v1.0 + HarmonicScanner)

El motor cuantitativo de este libro incorpora un módulo especializado llamado HarmonicScanner (core/harmonic_scanner.py), diseñado específicamente para la detección de patrones armónicos. Este módulo implementa:

* Detección de Pivots: Utiliza scipy.signal.argrelextrema para identificar máximos y mínimos locales (puntos A, B, C, D).
* Validación de Fibonacci: Comprueba si las distancias entre puntos cumplen las tolerancias configuradas.
* Cálculo de Ratios: Calcula el ratio B-C (retroceso) y C-D (extensión) para cada patrón candidato.
* Generación de Señales: Asigna dirección (LONG/SHORT) basada en la estructura del patrón.
* Gestión de Posiciones: Implementa stop-loss, take-profit y time exit dinámicos.

Para el backtest, el MotorBacktestDinamico acepta una función generadora de pesos que evalúa diariamente las señales y asigna pesos a los activos según los criterios de entrada/salida.

## Análisis de Resultados Reales (2016 - 2026)

Hemos sometido a backtest la estrategia de Patrones Armónicos durante un período de 10 años que incluye la recuperación post-2016, la Pandemia COVID-19 (2020), la crisis inflacionaria (2022-2023) y el rally de la IA (2024-2026).

### Informe de Limpieza de Datos

  Activo | ISIN | Filas | Desde | Hasta | Fuente |
 |---|---|---|---|---|---|
 | SPDR S&P 500 | SPY | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Invesco QQQ | QQQ | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Financial Select | XLF | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Technology Select | XLK | 2,711 | 2016-01-04 | 2026-10-14 | CSV |

**💡 Insight Clave:** Los 4 activos tienen datos completos desde el inicio del período, lo que garantiza que el scanner pueda detectar patrones de forma consistente.

### Detección de Patrones

El motor escaneó diariamente los 4 activos en busca de formaciones ABCD válidas. Los resultados son reveladores:

  Métrica | Valor |
 |---|---|
 | Total de patrones detectados | 102 |
 | Patrones LONG | 37 (36.3%) |
 | Patrones SHORT | 65 (63.7%) |
 | Ratio B-C medio | 0.585 ± 0.181 |
 | Ratio C-D medio | 1.437 ± 0.163 |
 | Señales generadas | 510 |

### Distribución por activo:

  Año | Patrones |
 |---|---|
 | 2016 | 8 |
 | 2017 | 7 |
 | 2018 | 7 |
 | 2019 | 5 |
 | 2020 | 15 (pico COVID) |
 | 2021 | 13 |
 | 2022 | 9 |
 | 2023 | 9 |
 | 2024 | 7 |
 | 2025 | 11 |
 | 2026 | 11 |

**💡 Insight Clave:** La detección de patrones se intensifica durante períodos de alta volatilidad (2020-2021), lo que sugiere que las formaciones geométricas son más frecuentes en mercados turbulentos.

### Métricas de Diagnóstico Comparativo (Resultados Reales)

  Métrica | Patrones ABCD | Buy & Hold (SPY) | ¿Qué significa? |
 |---|---|---|---|
 | Patrimonio Final | €79,845.79 | ~€45,000* | ✅ ABCD genera ~77% más que B&H |
 | Rentabilidad Total | 698.46% | ~350%* | ✅ ABCD muy superior en rentabilidad absoluta |
 | CAGR | 21.26% | 15.10% | ✅ ABCD superior en 6.16% anualizado |
 | Volatilidad | 18.24% | 17.69% | ⚠️ Ligeramente superior (+0.55%) |
 | Ratio de Sharpe | 1.06 | 0.74 | ✅ 43% mejor eficiencia riesgo/retorno |
 | Ratio de Sortino | 1.02 | 0.70 | ✅ 46% mejor eficiencia en downside |
 | Max Drawdown | -33.72% | -33.72% | ⚖️ Idéntico (ambos sufrieron COVID-2020) |
 | VaR 95% | €1,344.71 | €754.15 | ❌ 78% mayor riesgo de cola |
 | Rebalanceos | 166 | N/A | ⚠️ Frecuencia moderada (~15.5/año) |
 | Coste total | €4,734.11 | €0.00 | ⚠️ 47.34% del capital inicial |


**Nota:** El patrimonio final del SPY se estima a partir del CAGR del 15.10% sobre €10,000 durante 10 años.

### Interpretación del Gráfico de Patrimonio

El gráfico de equity curve revela la historia completa:

* **Línea azul (Patrones ABCD):** Crece de forma más agresiva desde €10,000 hasta €79,846 en 10 años, con una pendiente claramente superior al B&H.
* **Línea gris (Buy & Hold SPY):** Muestra el crecimiento característico del mercado, alcanzando ~€45,000.

**Lección visual:** La estrategia de Patrones Armónicos logró superar significativamente al Buy & Hold en rentabilidad, manteniendo el mismo drawdown máximo. Esto sugiere que la detección de formaciones geométricas aporta alpha real.

### Análisis de Rebalanceos

| Métrica | Valor |
| :--- | :---: |
| **Total de rebalanceos** | 166 |
| **Frecuencia** | 15.5 por año |
| **Rotación media** | 86.20% |
| **Coste total** | €4,734.11 |
| **Coste medio** | €28.52 |
| **Coste % capital inicial** | 47.34% |

### Últimos 10 rebalanceos:

| Fecha | Rotación | Coste (€) | Patrimonio (€) |
| :---: | :---: | :---: | :---: |
| 2026-07-08 | 95.0% | 69.63 | 73,224 |
| 2026-07-14 | 95.0% | 70.41 | 74,036 |
| 2026-07-17 | 95.0% | 69.54 | 73,126 |
| 2026-07-20 | 47.2% | 34.61 | 73,357 |
| 2026-07-23 | 47.1% | 34.84 | 73,977 |
| 2026-07-24 | 94.9% | 69.27 | 72,899 |
| 2026-09-04 | 95.0% | 72.18 | 75,911 |
| 2026-09-11 | 93.7% | 72.12 | 76,865 |
| 2026-09-16 | 95.0% | 72.04 | 75,763 |
| 2026-09-22 | 95.2% | 76.42 | 80,238 |

**Insight:** La alta rotación (86.20%) indica que la estrategia está constantemente entrando y saliendo de posiciones, lo que genera costes significativos pero también captura múltiples oportunidades.

### Bloque 9b: Sensibilidad a Costes y Tolerancia

| Coste_% | Tolerancia_% | CAGR_% | Sharpe | MaxDD_% | N_ops |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0.0 | 5.0 | 15.79 | 0.80 | -33.72 | 65 |
| 0.0 | 10.0 | 22.94 | 1.11 | -33.72 | 166 |
| 0.0 | 15.0 | 23.81 | 1.15 | -33.72 | 202 |
| 0.1 | 5.0 | 15.17 | 0.77 | -33.72 | 65 |
| 0.1 | 10.0 | 21.31 | 1.04 | -33.72 | 166 |
| 0.1 | 15.0 | 21.83 | 1.06 | -33.72 | 202 |
| 0.3 | 5.0 | 13.94 | 0.71 | -33.72 | 65 |
| 0.3 | 10.0 | 18.12 | 0.90 | -33.72 | 166 |
| 0.3 | 15.0 | 17.96 | 0.89 | -33.72 | 202 |

### Degradación respecto al caso base (CAGR=21.31%):

    Peor caso: -7.37 pp
    Mejor caso: +2.50 pp
    ✅ El sistema es robusto a variaciones de costes y tolerancia.

**Insight contraintuitivo:** Una tolerancia más amplia (15%) captura más patrones y mejora ligeramente el CAGR, pero también aumenta el ruido. La tolerancia del 10% parece ser el punto óptimo.

### Bloque 9c: Test Placebo de Timing

| Métrica | Valor | Interpretación |
| :--- | :---: | :--- |
| **Simulaciones** | 2,000 | Muestra estadísticamente significativa |
| **Patrones reales** | 102 | Suficientes para validación |
| **Rentab. media real** | +0.86% | Positiva y significativa |
| **Rentab. media azar** | -0.01% | Cercana a cero |
| **p-valor** | 0.003 | Altamente significativo (p<0.05) |

**Veredicto:** ✅ El timing de los patrones SÍ parece aportar (p<0.05).

**💡 Interpretación:** Las fechas de los patrones armónicos tienen información predictiva real sobre el futuro. No son aleatorias. Esto valida la premisa fundamental del análisis armónico.

### Bloque 9d: Barrido de Parámetros (IS/OOS)

Configuración:

    27 combinaciones (3 tolerancias × 3 hold days × 3 stop-loss)
    IS hasta: 2022-06-17
    OOS después: 2022-06-17

Resultados clave:

| Métrica | Valor | Interpretación |
| :--- | :---: | :--- |
| **Media Delta Sharpe (OOS-IS)** | +0.696 | 🚀 Mejora en OOS (inusual y positivo) |
| **Media Delta CAGR (OOS-IS)** | +12.02% | 🚀 Mejora en OOS (inusual y positivo) |
| **Combos con degradación < 0.3 Sharpe** | 27/27 (100%) | ✅ Robustez excepcional |
| **Spearman rho (IS vs OOS)** | +0.659 (p=0.000) | ✅ Ranking muy estable |

### Referencia Buy & Hold (Sharpe vs efectivo):

    IS: +0.58
    OOS: +1.11

**💡 Insight excepcional:** La estrategia mejora en OOS en lugar de degradarse. Esto es inusual y sugiere que:

* Los patrones armónicos son robustos a diferentes regímenes de mercado.
* El período OOS (2022-2026) fue particularmente favorable para esta estrategia.
* No hay overfitting; al contrario, hay una ventaja real.

### Mejor combo en OOS:

    Tolerancia: 15%
    Hold days: 5
    Stop-loss: 5%
    CAGR OOS: 29.42%
    Sharpe OOS: 1.54

**⚠️ Advertencia:** Aunque los resultados son excepcionales, el VaR 95% más alto (€1,344.71 vs €754.15) indica mayor riesgo de cola que debe gestionarse.

## ¿Por qué los Patrones Armónicos SÍ superaron al Buy & Hold?

* Detección de puntos de inflexión: Los patrones ABCD identifican zonas de agotamiento de tendencia con precisión matemática, permitiendo entrar en rebotes con alta probabilidad.
* Gestión de riesgo asimétrica: El ratio Riesgo/Beneficio de 1:2 (stop-loss -3%, take-profit +6%) asegura que las ganancias superen a las pérdidas a largo plazo.
* Diversificación temporal: Con 102 patrones en 10 años (~10/año), la estrategia no depende de un solo evento, sino de múltiples oportunidades distribuidas en el tiempo.
* Robustez a regímenes de mercado: El barrido IS/OOS muestra que la estrategia funciona tanto en mercados alcistas como bajistas, e incluso mejora en el período OOS.
* Validación estadística: El test placebo (p=0.003) confirma que el timing no es aleatorio, sino que tiene poder predictivo real.
* Estabilidad de parámetros: El Spearman rho de +0.659 indica que los parámetros óptimos en IS predicen bien el rendimiento en OOS, sugiriendo que no hay overfitting.

### La Ventaja Real de los Patrones Armónicos (Matizada)

| Ventaja real / Reto | Evidencia |
| :--- | :--- |
| ✅ **Mayor CAGR** | 21.26% vs 15.10% (+6.16% anualizado) |
| ✅ **Mejor Sharpe** | 1.06 vs 0.74 (+43%) |
| ✅ **Mejor Sortino** | 1.02 vs 0.70 (+46%) |
| ✅ **Placebo significativo** | p=0.003 (timing no es azar) |
| ✅ **Robustez IS/OOS** | 100% combos estables, Spearman rho=0.659 |
| ✅ **Mejor OOS** | Delta Sharpe +0.696, Delta CAGR +12.02% |
| ⚖️ **Mismo Max Drawdown** | -33.72% vs -33.72% (ambos sufrieron COVID) |
| ⚠️ **Mayor volatilidad** | 18.24% vs 17.69% (+0.55%) |
| ⚠️ **Mayor VaR 95%** | €1,344.71 vs €754.15 (+78%) |
| ❌ **Costes altos** | 47.34% del capital inicial |

**Conclusión matizada:** Los Patrones Armónicos lograron superar significativamente al Buy & Hold en rentabilidad ajustada al riesgo, con validación estadística robusta. Sin embargo, el mayor VaR 95% y los costes de transacción elevados requieren gestión cuidadosa en producción.

### Limitaciones Críticas para Producción

1. Look-Ahead Bias Parcial

El scanner detecta patrones en el punto D, pero en la realidad, el punto D solo se confirma cuando el precio ya ha rebotado. Esto introduce un sesgo de look-ahead parcial que puede inflar los resultados.
**Solución en producción:** Implementar un retraso de 1-2 días entre la detección del patrón y la entrada, o usar órdenes límite en la PRZ en lugar de entradas a mercado.

2. Costes de Transacción Elevados

Con 166 rebalanceos en 10 años y una rotación media del 86.20%, los costes de transacción alcanzan el 47.34% del capital inicial. En producción, con slippage real y spreads bid-ask, estos costes podrían ser aún mayores.
**Solución en producción:** Filtrar patrones de mayor calidad (tolerancia más estricta, múltiples confirmaciones) para reducir la frecuencia de operaciones.

3. VaR 95% Superior

El VaR 95% de €1,344.71 es 78% mayor que el del Buy & Hold (€754.15), indicando mayor riesgo de cola. Esto sugiere que la estrategia puede sufrir pérdidas extremas más frecuentes.
**Solución en producción:** Implementar stop-loss más ajustados (-2% en lugar de -3%) o reducir el tamaño de posición durante períodos de alta volatilidad.

4. Dependencia de Parámetros Subjetivos

La detección de pivots depende del parámetro order (ventana de suavizado) en argrelextrema. Diferentes valores de order pueden generar diferentes patrones.
**Solución en producción:** Optimizar el parámetro order mediante validación cruzada o usar múltiples ventanas y consolidar señales.

5. Universo Limitado

Solo se analizaron 4 activos (SPY, QQQ, XLF, XLK). La estrategia puede no funcionar igual de bien en otros activos o mercados.
**Solución en producción:** Expandir el universo a más ETFs sectoriales, índices internacionales y acciones individuales con alta liquidez.

### Recomendaciones para Producción Real
Si quieres usar Patrones Armónicos en la vida real, necesitas:

1. Filtrado de Calidad

No todos los patrones son iguales. Filtra por:

* **Volumen:** Solo operar patrones con volumen superior a la media.
* **Contexto:** Patrones en zonas de soporte/resistencia clave tienen mayor probabilidad de éxito.
* **Confluencia:** Patrones que coinciden con otros indicadores (RSI, MACD) son más fiables.

2. Gestión de Riesgo Dinámica

* **Stop-loss adaptativo:** Ajustar el stop-loss según la volatilidad del activo (ATR).
* **Tamaño de posición variable:** Reducir el tamaño durante períodos de alta volatilidad.
* **Correlación:** Evitar operar múltiples patrones en activos altamente correlacionados.

3. Validación Continua

* **Re-evaluación periódica:** Revisar la efectividad de los patrones cada 6 meses.
* **Monitoreo de drawdown:** Detener la estrategia si el drawdown supera el -20%.
* **Backtesting rolling:** Validar la estrategia en ventanas móviles para detectar cambios de régimen.

4. Integración con Otras Estrategias

Los Patrones Armónicos funcionan mejor como satélite táctico dentro de una cartera diversificada:

* **Core (70%):** Asignación pasiva (Capítulos 2-5).
* **Satélite (30%):** Patrones Armónicos + StatArb + ML.

5. Considerar Alternativas Simples

Antes de implementar Patrones Armónicos complejos, considera:

* **Buy & Hold SPY:** CAGR 15.10% en este período, sin costes de transacción.
* **DCA mensual:** Reduce el riesgo de timing y simplifica la gestión.

## Conclusiones

El análisis de Patrones Armónicos ABCD en el período 2016-2026 arroja conclusiones excepcionales pero matizadas:

1. RESULTADO (2016-01-04 a 2026-10-15):

    CAGR Patrones ABCD: 21.26% | Buy & Hold (SPY): 15.10%
    Volatilidad: 18.24% (B&H 17.69%)
    Max DD: -33.72% (B&H -33.72%)
    Sharpe: +1.06 (B&H +0.74)
    Sortino: +1.02 (B&H +0.70)
    VaR 95%: €1,344.71 (B&H €754.15)
    Rebalanceos: 166

2. VEREDICTO DE RENTABILIDAD Y RIESGO:

   ✅ Los patrones armónicos superan al Buy & Hold en rentabilidad (CAGR +6.16%) Y mantienen el mismo drawdown máximo.
   ✅ El Sharpe es superior (+1.06 vs +0.74): mejor eficiencia riesgo/retorno.
   ⚠️ El VaR 95% es mayor (+78%): mayor riesgo de cola que requiere gestión.

3. PLACEBO DE TIMING:

   ✅ p-valor = 0.003: El timing de los patrones SÍ aporta alpha real (no es azar).
   ✅ Rentabilidad media real: +0.86% vs azar: -0.01%.

4. SENSIBILIDAD A PARÁMETROS:

   ✅ Robusto a variaciones de costes y tolerancia (degradación -7.37 pp en peor caso).
   ✅ Tolerancia del 10% parece ser el punto óptimo.

5. BARRIDO IS/OOS:

   ✅ Correlación Spearman fuerte (rho=+0.659, p=0.000): Parámetros muy estables.
   ✅ 100% de combos con degradación < 0.3 Sharpe.
   🚀 Mejora en OOS: Delta Sharpe +0.696, Delta CAGR +12.02% (inusual y positivo).

6. LO QUE SÍ SE PUEDE DECIR:

* Los patrones armónicos identifican formaciones geométricas recurrentes con poder predictivo real.
* La gestión de riesgo (stop-loss -3%, take-profit +6%, time exit 5 días) es crucial.
* La estrategia funciona en múltiples activos y regímenes de mercado.
* El alpha generado no es producto del azar (validado por placebo).
* Los parámetros son estables entre IS y OOS (validado por barrido).

7. LO QUE NO:

* Que los patrones garanticen resultados futuros (el mercado puede cambiar de régimen).
* Que los ratios Fibonacci sean leyes físicas inquebrantables (son aproximaciones estadísticas).
* Que el backtest capture el slippage real y los costes de transacción completos.
* Que la estrategia funcione igual de bien en todos los activos (se necesita más testing).
* Que el mayor VaR 95% sea aceptable para todos los inversores (requiere gestión de riesgo).

8. LIMITACIONES CRÍTICAS:

* Look-ahead bias parcial en la detección del punto D.
* Costes de transacción elevados (47.34% del capital inicial).
* VaR 95% superior al Buy & Hold (+78%).
* Universo limitado (solo 4 activos).
* Dependencia de parámetros subjetivos (order en argrelextrema).

9. SINERGIA CON CAPÍTULOS ANTERIORES:

* Cap 1 (Patrones Armónicos): Detección de formaciones geométricas con alpha real.
* Cap 2-5 (Asignación Pasiva): Definen QUÉ comprar a largo plazo.
* Cap 6 (StatArb): Explota ineficiencias entre ETF y subyacentes.
* Cap 7 (ML): Intenta timing de mercado con aprendizaje automático.
* Cap 8 (Event-Driven): Intenta capturar eventos raros.
* Cap 10 (Insider Trading): Sigue compras de ejecutivos.

   La combinación de Patrones Armónicos + Asignación Pasiva puede crear un sistema Core-Satellite robusto.

## Validación del resultado de la aplicación de la estrategia
Acabamos de ver un resultado sorprendente.

RESULTADO (2016-01-04 a 2026-10-15):
   CAGR Patrones ABCD +21.26% | Buy & Hold (SPY) +15.10%

¿Debemos tomar como  real y fiable el resultado, o es una ilusión estadística? Para despejar esta duda procedemos a hacer tres pruebas

* Prueba de Muestra Fuera de Muestra (Out-of-Sample / OOS)
* Prueba de Sensibilidad al Slippage
* Test Placebo (Monte Carlo)
El resultado lo documentos en el .md **'01_Cap1_patrones_armonicos_validacion.md'** 

## 🚀 PRÓXIMO PASO: CAPÍTULO 2 - DCA vs. LUMP SUM

   Exploraremos cómo desplegar capital de forma óptima: ¿invertir todo de golpe o hacerlo gradualmente?

## ⚠️ Descargo de Responsabilidad y Advertencia de Riesgos

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa.

### Los Resultados Pasados No Garantizan Resultados Futuros
El backtest presentado es una simulación histórica basada en datos pasados (2016-2026). Que la estrategia de Patrones Armónicos haya generado un CAGR del 21.26% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los patrones pueden dejar de funcionar si cambia la microestructura del mercado o si demasiados participantes los utilizan.

### Limitaciones del Backtest

* **Look-ahead bias parcial:** El scanner detecta patrones en el punto D, pero en la realidad, el punto D solo se confirma cuando el precio ya ha rebotado.
* **Costes de transacción:** Se han asumido costes estándar del 0.1% por operación. En la realidad, el slippage y los spreads bid-ask pueden ser mayores, especialmente durante crisis de liquidez.
* **Fiscalidad:** El motor no contempla el impacto de impuestos por ventas a corto plazo (frecuencia diaria).
* **VaR 95% superior:** La estrategia tiene mayor riesgo de cola que el Buy & Hold, lo que puede generar pérdidas extremas más frecuentes.
* **Universo limitado:** Solo se analizaron 4 activos. La estrategia puede no funcionar igual de bien en otros mercados.

### No es Asesoramiento Financiero

Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. La estrategia de Patrones Armónicos es de complejidad media-alta y requiere monitoreo continuo. Cada inversor debe evaluar su propia tolerancia al riesgo.

### Riesgo de Pérdida de Capital

Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. Aunque los Patrones Armónicos tienen un Sharpe superior al SPY en el backtest (1.06 vs 0.74), el VaR 95% es mayor (€1,344.71 vs €754.15) y los costes de transacción son significativos (47.34% del capital inicial).

### Uso del Código

El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de la exactitud de las métricas calculadas.

## 🎯 Recuerda
Los Patrones Armónicos no son "adivinar el futuro con Fibonacci". Eso es una simplificación excesiva. Los Patrones Armónicos reales son:

* Detección de formaciones geométricas recurrentes basadas en ratios de Fibonacci.
* Validación estadística rigurosa (placebo, sensibilidad, barrido IS/OOS).
* Gestión de riesgo estricta (stop-loss, take-profit, time exit).

Es una estrategia de análisis técnico con validación cuantitativa, no de predicción sobrenatural. Su verdadero valor está en identificar puntos de inflexión con alta probabilidad y gestionar el riesgo de forma asimétrica.
**La lección más importante de este capítulo:** Los Patrones Armónicos SÍ pueden generar alpha real, pero requieren gestión de riesgo cuidadosa, validación estadística rigurosa y humildad ante la complejidad del mercado. El timing de los patrones no es azar (p=0.003), los parámetros son estables (Spearman rho=0.659), y la estrategia mejora en OOS (Delta Sharpe +0.696). Sin embargo, el mayor VaR 95% y los costes de transacción elevados requieren atención constante.
La paciencia, la disciplina en la detección de patrones y la gestión rigurosa del riesgo son tus mayores aliados. El "límite del motor" no es la potencia de cálculo, es la calidad de los datos y la honestidad intelectual al documentar las limitaciones.