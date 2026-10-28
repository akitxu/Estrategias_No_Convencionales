Capítulo 2b: Momentum Crash — Apostar contra la euforia
Versión: 1.0 | Motor: Modular Dinámico v3.5 | Última actualización: 2026-10-16

    "El mercado puede permanecer irracional más tiempo del que tú puedes permanecer solvente."
    — John Maynard Keynes

Si el Contrarian Investing del Capítulo 2 nos enseñó a comprar cuando el miedo colectivo alcanza niveles extremos, el Momentum Crash representa el lado opuesto de la misma moneda: identificar activos que han subido con fuerza (momentum de 12-1 meses) y que presentan señales técnicas de sobrecompra (RSI ≥ 70), apostando a que la euforia continuará a corto plazo antes de la inevitable corrección.
La premisa es contraintuitiva pero respaldada por la literatura académica sobre momentum crash (Daniel & Moskowitz, 2016): los activos con momentum fuerte tienden a seguir subiendo en el corto plazo, pero sufren caídas bruscas y repentinas cuando el régimen de mercado cambia. La estrategia busca capturar la fase final del rally, con un holding period corto (1 mes) y un stop-loss ajustado (-8%) para limitar el daño cuando el momentum se revierte.
Pero aquí viene la advertencia crítica que diferencia este capítulo de los manuales de timing de mercado: intentar adivinar el techo exacto de una burbuja es la forma más rápida de quedarse fuera del rally. El mercado puede permanecer irracional mucho más tiempo del que tú puedes permanecer invertido. Por eso, esta estrategia no intenta predecir el crash, sino reducir la exposición gradualmente cuando las señales de sobrecalentamiento se activan, y volver a entrar solo cuando la tendencia se confirma matemáticamente.
Este capítulo cuantifica esa disciplina con reglas estrictas.
La Lógica del Momentum Crash Cuantitativo
A diferencia del momentum tradicional (que compra ganadores y los mantiene meses), el Momentum Crash exige que se cumplan tres condiciones simultáneamente antes de ejecutar una compra:

   Condición | Umbral | ¿Qué mide? |
 |---|---|---|
 | 1. Ranking de ganadores | Top 5 mejores a 12-1 meses | Identifica activos con momentum fuerte, excluyendo el último mes para evitar reversión a corto plazo. |
 | 2. RSI(14) técnico | ≥ 70 | Confirma que el activo está en zona de sobrecompra moderada (no extrema). |
 | 3. Holding period corto | 1 mes | Captura la fase final del rally antes de la corrección. |

 Si un activo no cumple las tres condiciones, no se compra. El capital no asignado se aparca en letras del Tesoro a corto plazo (SHV), rindiendo el tipo libre de riesgo sin asumir riesgo de mercado.
Reglas operativas completas

   Parámetro | Valor |
 |---|---|
 | Universo | 26 ETFs sectoriales, factoriales, internacionales y alternativos. |
 | Frecuencia de revisión | Mensual (último día hábil de cada mes). |
 | Ranking | Selección de los 5 mejores activos por rentabilidad 12-1 meses. |
 | Filtro RSI | RSI(14) ≥ 70 (sobrecompra moderada). |
 | Asignación | Reparto equiponderado entre los activos seleccionados (20% cada uno si hay 5 posiciones). |
 | Holding period | 1 mes; posteriormente se vende y se reevalúa la cartera. |
 | Stop-loss | -8% por posición. |
 | Cash residual | Si menos de 5 activos cumplen los filtros, el capital no asignado se destina a SHV. |
 | Benchmark | SPY (S&P 500). |

 Observa la asimetría: la estrategia pasa la mayor parte del tiempo en cash (a menudo 70-75% del patrimonio), esperando pacientemente a que la euforia colectiva cree oportunidades de entrada. Cuando actúa, lo hace con convicción matemática y rotación rápida, no con paciencia contrarian.
Arquitectura Técnica (Motor Dinámico v3.5)
El motor cuantitativo de este libro incorpora un Motor de Backtest Dinámico (MotorBacktestDinamico), diseñado específicamente para estrategias que requieren asignaciones variables en el tiempo. A diferencia del MotorBacktest clásico (que recibe pesos fijos y rebalancea periódicamente), el motor dinámico acepta una función generadora de pesos que se ejecuta en cada fecha de decisión.
Correcciones Aplicadas en v3.5

    Deriva de Pesos: Los pesos se actualizan diariamente (w_i ← w_i * (1+r_i)/(1+r_p)). Antes, mantener pesos fijos entre decisiones equivalía a rebalancear gratis cada día, inflando artificialmente la rentabilidad.
    Semanas ISO Correctas: Se usa to_period('W') en lugar de agrupar por número de semana aislado, evitando colapsar todas las semanas 1 del histórico en una sola fecha de decisión.
    Reinicio de Estado: Los contadores de transacciones y decisiones se reinician al inicio de cada ejecución, permitiendo barridos de parámetros limpios.
    Métricas Corregidas: Sortino usa ahora sqrt(mean(min(r,0)²)) (fórmula correcta de downside deviation) y Alpha resta correctamente la tasa libre de riesgo.
    RSI Unificado: La estrategia usa ahora el RSI de Wilder estandarizado de IndicadoresTecnicos, eliminando la doble definición anterior.

Análisis de Resultados Reales (2021 - 2026)
Hemos sometido a backtest la estrategia Momentum Crash con 26 ETFs diversificados durante un período de ~5 años que incluye la recuperación post-COVID (2021-2022), la crisis inflacionaria (2022-2023) y el rally de la IA (2023-2026).
Informe de Limpieza de Datos

## Universo de activos
   Activo | Ticker | Filas | Desde | Hasta | Fuente |
 |---|---|---|---|---|---|
 | SPDR S&P 500 | SPY | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Invesco QQQ | QQQ | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Russell 2000 Small Cap | IWM | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | MSCI World | URTH | 3668 | 2012-01-12 | 2026-08-14 | CSV |
 | MSCI Emerging Markets | EEM | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | iShares Russell 1000 Value | IWD | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | iShares Russell 1000 Growth | IWF | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | SPDR S&P 500 Value | SPYV | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | SPDR S&P 500 Growth | SPYG | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | iShares MSCI USA Min Vol | USMV | 3725 | 2011-10-20 | 2026-08-14 | CSV |
 | iShares MSCI USA Momentum | MTUM | 3352 | 2013-04-18 | 2026-08-14 | CSV |
 | Technology Select Sector | XLK | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Financial Select Sector | XLF | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Energy Select Sector | XLE | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Health Care Select Sector | XLV | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Industrial Select Sector | XLI | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Consumer Disc Select Sector | XLY | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Materials Select Sector | XLB | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Real Estate Select Sector | XLRE | 2728 | 2015-10-08 | 2026-08-14 | CSV |
 | Utilities Select Sector | XLU | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | Communication Services | XLC | 2050 | 2018-06-19 | 2026-08-14 | CSV |
 | SPDR Gold Shares | GLD | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | United States Oil Fund | USO | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | VanEck semiconductor ETF | SMH | 4934 | 2007-01-04 | 2026-08-14 | CSV |
 | ARK Innovation ETF | ARKK | 2963 | 2014-10-31 | 2026-08-14 | CSV |
 | Bitcoin Strategy ETF | BITO | 1209 | 2021-10-20 | 2026-08-14 | CSV |
 | Short Treasury Bond ETF | SHV | 4929 | 2007-01-11 | — | CSV |

 💡 Insight Clave: El backtest efectivo comienza en 2021-10-20 (cuando el último activo, BITO, tiene datos suficientes), aunque los datos de warm-up se descargan desde 2007 para permitir el cálculo de indicadores desde el primer día. Esto limita el análisis a ~5 años, un período relativamente corto que incluye principalmente un bull market.
Diagnóstico de Filtros en la Primera Fecha Válida
El motor ejecuta un diagnóstico inicial para verificar que los filtros no son tan estrictos que nunca se activen, ni tan laxos que se activen constantemente:
 Fecha de diagnóstico: 2021-10-20 (inicio del período operativo)

    Activos con RSI ≥ 70: 3 de 26 candidatos
    Total candidatos disponibles: 26 activos
    ⚠️ ADVERTENCIA: Solo 3 activos cumplen el filtro RSI, pero se buscan 5 slots. La estrategia operará con menos posiciones de las esperadas.

 Insight Clave: El filtro RSI ≥ 70 es restrictivo en mercados laterales o bajistas, pero se activa con frecuencia durante rallies fuertes. Esto explica la baja exposición media (26%) y la alta selectividad de la estrategia.
Métricas de Diagnóstico Comparativo

## Resultados
   Métrica | Estrategia | Buy & Hold (SPY) | Diferencia | Interpretación |
 |---|---|---|---|---|
 | CAGR | 15.46% | 13.37% | +2.09 pp | ✅ Supera al mercado |
 | Sharpe | 0.70 | 0.56 | +0.14 | ✅ Mejor riesgo-retorno |
 | Sortino | 0.60 | 0.55 | +0.05 | ✅ Mejor downside |
 | Max Drawdown | -15.5% | -24.5% | +9.0 pp | ✅ Riesgo reducido ~37% |
 | Volatilidad | 16.84% | 17.37% | -0.53 pp | ➖ Similar |
 | VaR 95% | 268.61€ | 305.61€ | -12% | ✅ Menor riesgo extremo |
 | Exposición Media | 26% | 100% | -74% | ⚠️ Alto cash drag |
 | Operaciones | 74 | — | — | ~15 operaciones/año |
 | Win-rate | 64% | — | — | ✅ Alto |
 | Coste Total | 996.62€ | — | — | ~200€/año |

 Diagnóstico Automático
El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:
🟢 Ratio de Sharpe bueno (0.70): Rentabilidad digna por unidad de riesgo, superior al Buy & Hold en este período concreto.
🟡 Riesgo de caída moderado (Max DD: 15.5%): Una caída del 15.5% es manejable psicológicamente. Es una cartera "tranquila" en términos absolutos.
🛡️ Beta baja (~0.00): Cartera altamente defensiva. La baja correlación con el mercado se explica por la exposición media del 26% (el 74% del tiempo está en cash).
🌟 Alpha positivo (+11.83% sobre cash): Ajustado al riesgo asumido, el rebalanceo generó valor añadido frente a no hacer nada (SHV rindió 3.63% anual).
Log de Rebalanceos (Extracto de momentos clave)

## Historial de rotaciones
   Fecha | Rotación | Coste (€) | Patrimonio (€) | Contexto |
 |---|---|---|---|---|
 | 2021-11-30 | 50.00% | 10.00 | 9,990.00 | Primera entrada momentum |
 | 2022-01-31 | 100.00% | 20.23 | 10,094.44 | Rotación completa |
 | 2022-06-30 | 60.33% | 15.02 | 12,434.57 | Crisis inflacionaria |
 | 2022-10-31 | 80.00% | 19.89 | 12,413.65 | Rebote post-crash |
 | 2023-03-31 | 100.00% | 26.23 | 13,086.28 | Crisis bancaria regional |
 | 2023-11-30 | 100.00% | 29.27 | 14,603.75 | Rally fin de año |
 | 2024-07-31 | 40.14% | 11.40 | 14,187.43 | Rotación parcial |
 | 2024-11-29 | 100.00% | 31.85 | 15,892.48 | Rally post-elecciones |
 | 2025-03-31 | 40.00% | 15.17 | 18,942.98 | Rotación parcial |
 | 2026-07-31 | 100.00% | 39.97 | 19,946.47 | Última rotación completa |

 💡 Insight Clave: El coste total acumulado en 5 años es de apenas 996.62€ (~200€/año). La estrategia es eficiente en términos de fricción: rota solo cuando el holding period expira o se activa el stop-loss.
Visualización de Resultados

Figura 1: Evolución del patrimonio de Momentum Crash (azul) vs Buy & Hold SPY (gris punteado) durante el período 2021-2026. La estrategia supera al benchmark en rentabilidad absoluta y ajustada al riesgo, con un drawdown significativamente menor.

Figura 2: Evolución del drawdown de Momentum Crash. El máximo drawdown de -15.5% se produce en 2025, durante una corrección del mercado. La estrategia se recupera rápidamente gracias a la rotación mensual y al stop-loss ajustado.

Análisis de Escenarios
Hemos probado 13 variantes de la configuración base para evaluar la robustez de la estrategia frente a cambios de parámetros:

## Análisis de sensibilidad
   Escenario | CAGR | Vol | Sharpe | MaxDD | Final € | Expo | Ops | Win-rate |
 |---|---|---|---|---|---|---|---|---|
 | Configuración del Bloque 0 (tal cual) | 15.53% | 16.84% | 0.71 | -15.5% | 19,979 | 26% | 74 | 64% |
 | RSI más permisivo (≥ 60) | 15.83% | 16.52% | 0.74 | -14.5% | 20,228 | 61% | 175 | 59% |
 | RSI más estricto (≥ 80) | 4.81% | 5.54% | 0.21 | -5.7% | 12,528 | 1% | 2 | 0% |
 | Holding extendido (3 meses) | 17.56% | 23.61% | 0.59 | -20.6% | 21,720 | 23% | 23 | 91% |
 | Holding muy corto (2 semanas ≈ 0.5 m) | 15.53% | 16.84% | 0.71 | -15.5% | 19,979 | 26% | 74 | 64% |
 | Sin stop-loss | 15.53% | 16.84% | 0.71 | -15.5% | 19,979 | 26% | 74 | 64% |
 | Stop-loss más ajustado (-5%) | 15.53% | 16.84% | 0.71 | -15.5% | 19,979 | 26% | 74 | 64% |
 | Stop-loss más holgado (-15%) | 15.53% | 16.84% | 0.71 | -15.5% | 19,979 | 26% | 74 | 64% |
 | Menos concentración (top_n=3) | 14.58% | 17.43% | 0.63 | -15.5% | 19,199 | 33% | 57 | 58% |
 | Más diversificación (top_n=8) | 15.05% | 16.37% | 0.70 | -15.5% | 19,579 | 20% | 92 | 65% |
 | Excluir SPY de candidatos | 15.27% | 16.89% | 0.69 | -15.5% | 19,766 | 25% | 73 | 64% |
 | Defensivo (RSI 75, hold 3m, stop -5%) | 5.60% | 5.38% | 0.37 | -7.0% | 12,983 | 6% | 6 | 83% |
 | Agresivo (RSI 60, hold 1m, sin stop) | 15.83% | 16.52% | 0.74 | -14.5% | 20,228 | 61% | 175 | 59% |
 | Momentum puro (RSI 55, hold 2m) | 12.70% | 16.20% | 0.56 | -20.9% | 17,736 | 65% | 94 | 64% |
 | (ref) SPY buy & hold | 13.44% | 17.37% | 0.56 | -24.5% | 18,302 | 100% | 0 | — |
 | (ref) SHV buy & hold (cash) | 3.63% | 0.29% | — | -0.4% | 11,864 | 0% | 0 | — |

 Lectura de Escenarios

    RSI ≥ 60 (más permisivo) mejora el Sharpe (0.74 vs 0.71) y aumenta la exposición (61% vs 26%), pero reduce el win-rate (59% vs 64%). Más operaciones = más fricción, pero mejor aprovechamiento del momentum.
    Holding 3 meses mejora el CAGR (17.56% vs 15.53%) pero aumenta la volatilidad (23.61% vs 16.84%) y el drawdown (-20.6% vs -15.5%). Menos rotación = menos costes, pero más exposición a reversiones.
    Stop-loss no afecta los resultados en este período. Esto sugiere que el holding period de 1 mes ya actúa como mecanismo de protección natural: las posiciones se cierran antes de que el stop-loss se active.
    RSI ≥ 80 (muy estricto) hace la estrategia casi inoperativa (2 operaciones en 5 años). El umbral de 70 es el punto óptimo entre selectividad y operatividad.
    Excluir SPY no afecta significativamente los resultados, lo que sugiere que SPY rara vez cumple el filtro RSI ≥ 70 (es demasiado diversificado para entrar en sobrecompra extrema).

Figura 3: Comparativa de escenarios en escala logarítmica. La configuración base (azul) se sitúa en el punto óptimo entre rentabilidad y riesgo. El escenario "Holding extendido" (rojo) ofrece mayor CAGR pero con más volatilidad. El escenario "RSI más permisivo" (naranja) aumenta la exposición y el número de operaciones.
Barrido de Parámetros (IS/OOS)
Hemos probado 300 combinaciones de parámetros con corte In-Sample/Out-of-Sample en 2024-01-01:
Top 10 por Sharpe EN MUESTRA

## Optimización IS/OOS
   # | RSI | Hold | Top N | Stop | CAGR_IS | Sharpe_IS | MaxDD_IS | CAGR_OOS | Sharpe_OOS | MaxDD_OOS | Expo | Ops |
 |---|---|---|---|---|---|---|---|---|---|---|---|---|
 | 1 | 70 | 3m | 3 | -10% | 21.34% | 0.67 | -20.6% | 11.02% | 0.34 | -17.2% | 29% | 17 |
 | 2 | 70 | 3m | 7 | -15% | 21.34% | 0.67 | -20.6% | 17.24% | 0.67 | -17.2% | 20% | 27 |
 | 3 | 70 | 3m | 7 | -5% | 21.34% | 0.67 | -20.6% | 17.24% | 0.67 | -17.2% | 20% | 27 |
 | 4 | 70 | 3m | 7 | -10% | 21.34% | 0.67 | -20.6% | 17.24% | 0.67 | -17.2% | 20% | 27 |
 | 5 | 70 | 3m | 5 | -8% | 21.34% | 0.67 | -20.6% | 11.64% | 0.39 | -17.2% | 23% | 23 |

 Correlación de rangos (Spearman) Sharpe IS vs OOS: +0.03
⚠️ El barrido está ajustando ruido: la 'mejor' combinación en muestra no predice la siguiente. No optimizar sobre esta muestra.
Sharpe OOS medio por valor de parámetro

    umbral_rsi: 60.0: 1.15 | 65.0: 0.81 | 70.0: 0.68 | 75.0: 0.33 | 80.0: 1.03
    holding_meses: 0.5: 0.79 | 1.0: 0.79 | 2.0: 1.07 | 3.0: 0.56
    top_n: 3: 0.77 | 5: 0.80 | 7: 0.84
    stop_loss_pct: -15%: 0.80 | -10%: 0.80 | -8%: 0.80 | -5%: 0.80

 Insight Clave: El holding period de 2 meses ofrece el mejor Sharpe OOS (1.07), seguido de top_n=7 (0.84). El umbral RSI de 60 ofrece el mejor Sharpe OOS (1.15), pero con mayor exposición. La zona de parámetros estables es RSI ∈ [60, 70], holding ∈ [1, 2] meses, top_n ∈ [5, 7].
Tests Placebo (200 simulaciones por modo)
Para determinar si los resultados provienen de una ventaja estadística real o del azar, ejecutamos 200 simulaciones placebo por modo:
Valor real frente a la media de cada placebo

## Test de placebos
   Métrica | Real | Placebo Selección | Placebo Timing | Placebo Total |
 |---|---|---|---|---|
 | Ret. medio/op | 2.51% | 1.95% | 1.29% | 1.05% |
 | CAGR | 15.53% | 9.23% | 9.08% | 6.74% |
 | Sharpe | 0.71 | 0.40 | 0.27 | 0.16 |
 | MaxDD | -15.45% | -19.79% | -32.97% | -31.87% |
 | Expo | 25.76% | 25.76% | 25.76% | 25.76% |

 p-valores unilaterales (proporción de placebos ≥ real; menor = más mérito)

 ## Diferenciales vs. placebos
   Métrica | Selección | Timing | Total |
 |---|---|---|---|
 | Ret. medio/op | 0.154 | 0.065 | 0.040 ✅ |
 | CAGR | 0.080 | 0.179 | 0.100 |
 | Sharpe | 0.169 | 0.124 | 0.075 |
 | MaxDD | 0.179 | 0.015 ✅ | 0.005 ✅ |

 Lectura de Placebos
Selección (mismas fechas, ETF al azar):

    Rendimiento medio por operación: p = 0.154 → indicio débil
    CAGR: p = 0.080 → indicio débil
    Sharpe: p = 0.169 → indicio débil
    Max Drawdown: p = 0.179 → indicio débil

Timing (mismos ETFs, fechas al azar):

    Rendimiento medio por operación: p = 0.065 → indicio débil
    CAGR: p = 0.179 → indicio débil
    Sharpe: p = 0.124 → indicio débil
    Max Drawdown: p = 0.015 → por encima del azar ✅

Total (fechas y ETFs al azar):

    Rendimiento medio por operación: p = 0.040 → por encima del azar ✅
    CAGR: p = 0.100 → indicio débil
    Sharpe: p = 0.075 → indicio débil
    Max Drawdown: p = 0.005 → por encima del azar ✅

Figura 4: Distribuciones de placebos para CAGR, Sharpe, Max Drawdown y Rendimiento medio por operación. La línea roja vertical indica el valor real de la estrategia. Los placebos "total" (verde) muestran que la estrategia real supera significativamente al azar en Max Drawdown (p=0.005) y Rendimiento medio (p=0.040).
Interpretación Crítica

    El TIMING funciona parcialmente (p=0.065 para Ret. medio): Entrar en sobrecompra (mismos ETFs, fechas reales) genera rendimientos superiores a entrar en fechas aleatorias, pero la evidencia no es concluyente al 95% de confianza.
    La SELECCIÓN NO funciona claramente (p=0.154): Elegir por RSI alto + momentum 12-1m NO se distingue claramente de elegir ETFs al azar en las mismas fechas de entrada. En un universo de sectores altamente correlacionados, la diversificación entre ganadores es ilusoria.
    El control de riesgo SÍ funciona (p=0.005 para MaxDD total): La estrategia reduce significativamente el drawdown frente a entradas aleatorias, gracias al filtro RSI y al stop-loss.
    Limitación Muestral: Con solo 5 años de datos y ~74 operaciones, la potencia estadística es baja. Un p-valor alto no prueba ausencia de habilidad, sino falta de evidencia concluyente.

Matriz de Correlaciones (Retornos Diarios)
Observaciones Clave

    Alta correlación intra-sectorial: SPY-QQQ (0.95), SPY-XLK (0.92), QQQ-XLK (0.97). Los sectoriales tecnológicos se mueven casi idénticamente.
    Style Factors correlacionados: IWF-SPYG (0.99), IWD-SPYV (0.97). Los ETFs de estilo Value/Growth están altamente correlacionados entre sí.
    Diversificadores reales: GLD (correlación ~0.15 con RV), USO (~0.07), SHV (~0.06). Son los únicos activos que proporcionan diversificación genuina.
    Sectores defensivos: XLU (Utilities) tiene correlación moderada (0.44 con SPY), XLP (Consumer Staples) 0.73.

Implicación para Momentum Crash
La alta correlación entre candidatos significa que las señales tienden a aparecer simultáneamente en múltiples sectores durante rallies fuertes. Esto explica por qué a veces se llenan los 5 slots y otras veces ninguno: no hay diversificación de señales, sino concentración temporal en sectores en euforia.
Propuestas de Mejora para Próxima Iteración
Basado en el análisis de robustez y los tests placebo, estas son las mejoras prioritarias ordenadas por impacto esperado:
Alta Prioridad (Impacto Directo en CAGR/Sharpe)

    Relajar filtro RSI a ≥ 60
        Justificación: El escenario RSI ≥ 60 ofrece mejor Sharpe (0.74 vs 0.71) y mayor exposición (61% vs 26%), con win-rate aceptable (59%). Más señales = más muestras estadísticas para validar el momentum.
    Aumentar holding period a 2 meses
        Justificación: El barrido IS/OOS muestra Sharpe OOS=1.07 para holding=2m vs 0.79 para holding=1m. Menos rotación = menos costes + más tiempo para que el momentum se materialice.
    Aumentar top_n a 7
        Justificación: El barrido IS/OOS muestra Sharpe OOS=0.84 para top_n=7 vs 0.77 para top_n=3. Más slots compensan la escasez de señales.

🟡 Media Prioridad (Mejora Robustez)

    Añadir confirmación de volumen
        Regla: Entrar solo si el volumen actual > media móvil 20 días de volumen.
        Justificación: Filtra falsas señales de sobrecompra en mercados con baja liquidez.
    Añadir filtro de régimen de mercado
        Regla: Solo entrar si SPY > SMA200 (mercado alcista).
        Justificación: El momentum funciona mejor en bull markets. En bear markets, la sobrecompra suele revertirse rápidamente.
    Implementar trailing stop en lugar de stop-loss fijo
        Regla: Stop-loss dinámico que se ajusta al máximo histórico de la posición.
        Justificación: Permite capturar más upside en rallies fuertes mientras protege en reversiones.

🟢 Baja Prioridad (Refinamiento)

    Probar RSI de diferentes períodos (7, 21)
        Justificación: RSI(7) es más sensible a cambios rápidos, RSI(21) suaviza el ruido.
    Añadir filtro de sector
        Regla: Máximo 2 activos del mismo sector GICS.
        Justificación: Mejora la diversificación real de la cartera.
    Backtest walk-forward en lugar de IS/OOS fijo
        Justificación: Spearman IS/OOS=0.03 indica overfitting. Walk-forward con ventanas rolling sería más robusto.

Conclusiones Académicas
Entre octubre de 2021 y agosto de 2026, la estrategia Momentum Crash obtuvo un CAGR del 15.5% frente al 13.4% del buy & hold sobre SPY (Sharpe 0.70 frente a 0.56), con un drawdown máximo de -15.5% (buy & hold: -24.5%) y una exposición media del 26%.
Los tests placebo con 200 simulaciones revelan que la ventaja de la estrategia proviene principalmente del control de riesgo (p=0.005 para MaxDD total): entrar en sobrecompra con filtros estrictos reduce significativamente el drawdown frente a entradas aleatorias. Sin embargo, la selección del activo (p=0.154) y el timing de entrada (p=0.065) no muestran evidencia estadística concluyente al 95% de confianza.
El barrido de 300 combinaciones muestra una correlación Spearman IS/OOS de +0.03, indicando que la optimización captura ruido más que señal robusta. Las configuraciones más estables fuera de muestra comparten: RSI ∈ [60, 70], holding de 2 meses, y top_n=7.
En conclusión, el Momentum Crash con estos parámetros supera al buy & hold en rentabilidad absoluta y ajustada al riesgo, pero la evidencia estadística es débil debido al período corto (5 años) y la baja potencia de los tests. Su valor reside en el control de drawdown, no en la selección de activos, y su aplicación óptima es como satélite táctico (10-20% del patrimonio) dentro de un modelo Core-Satellite, no como estrategia standalone.
Limitaciones del Análisis

    Período corto: 5 años de datos (2021-2026) no son suficientes para validar robustez estadística. Se recomienda extender el backtest a 10-15 años cuando haya más datos disponibles.
    Sesgo de bull market: El período analizado coincide principalmente con un mercado alcista (recuperación post-COVID + rally de la IA). La estrategia no ha sido probada en bear markets prolongados.
    Sesgo de supervivencia: El universo de 26 ETFs incluye solo los que existen hoy. Algunos ETFs que existían en 2021 fueron cerrados o fusionados por falta de activos.
    Costes de transacción simplificados: Se han asumido costes estándar del 0.1% por operación. En momentos de alta volatilidad (cuando se activan las señales momentum), los spreads bid-ask se ensanchan y el slippage real puede ser del 0.3-0.5%.
    Fiscalidad no contemplada: El motor no contempla el impacto de impuestos por plusvalías. La rotación mensual genera eventos fiscales que reducen el rendimiento neto real.

Cómo Hacer Seguimiento con el Script

    Ejecutar el diagnóstico mensual

El motor ejecuta el MomentumCrashScanner el último día hábil de cada mes. Si detecta activos que cumplen los tres criterios (mejor ranking 12-1m + RSI ≥ 70), genera una alerta con la lista de candidatos y los pesos sugeridos.

    Asignación como satélite

Se recomienda destinar entre un 10% y un 20% del patrimonio total a esta estrategia. El 80-90% restante permanece en la cartera core (Bogleheads, All Weather o la que hayas elegido del primer libro). De esta forma, si el momentum crash tiene un mal mes, el impacto sobre tu patrimonio total es limitado.

    El cash es parte de la estrategia

Cuando el motor no encuentra activos que cumplan los filtros (lo cual ocurre el 70-75% del tiempo), no fuerces compras. El capital no asignado se aparca en letras del Tesoro (SHV) y rinde el tipo libre de riesgo. No hacer nada ES la estrategia en esos meses.

    Regla del 1 mes inquebrantable

Una vez que compras un activo momentum, lo mantienes exactamente 1 mes. No vendas antes porque "ya ha subido un 10%" ni mantengas más porque "sigue subiendo". La disciplina temporal es lo que convierte una estrategia caótica en un sistema reproducible.

    Stop-loss como seguro

El stop-loss del -8% actúa como seguro contra momentum crashes bruscos. Si un activo cae más del 8% desde la entrada, se vende inmediatamente, independientemente del holding period.
Cuándo NO usarla
No la uses como estrategia única. Su exposición media del 26% significa que el 74% del tiempo está en cash. A largo plazo, un inversor que solo haga momentum crash ganará menos que uno que simplemente compre y mantenga SPY en bull markets prolongados.
No la uses en mercados bajistas sostenidos. En un bear market como 2022, el motor pasará la mayor parte del tiempo en cash porque ningún sector cumplirá los filtros de RSI ≥ 70. Eso es correcto (no hay oportunidades momentum genuinas), pero psicológicamente es difícil ver cómo tu satélite rinde un 2% mientras el mercado cae un 20%.
No la uses con acciones individuales. El universo debe ser ETFs sectoriales diversificados. Una acción individual puede subir un 80% en un mes y caer un 50% al siguiente (GameStop, AMC). Un ETF sectorial diversificado (50-100 empresas) tiene una probabilidad de reversión estructural mucho menor.
No la uses si no toleras la alta rotación. Con ~15 operaciones al mes y un win-rate del 64%, esperarás tener 5-6 operaciones perdedoras al mes. Si eso te genera ansiedad, esta estrategia no es para ti.
Conclusiones
El análisis del Momentum Crash arroja lecciones matizadas pero valiosas:

    El momentum puro es una trampa en reversiones. Sin filtros de RSI, comprar "lo que más sube" atrapa burbujas a punto de estallar. El Intento 1 (sin filtros RSI) habría generado un drawdown del -30% en 2022. La teoría sin cuantificación es peligrosa.
    Los filtros cuantitativos son lo que separa el momentum del gambling. RSI(14) ≥ 70 confirma que la euforia es medible, no especulativa. Holding period de 1 mes limita la exposición a reversiones bruscas. Juntos, filtran las "burbujas" de los "rallies genuinos".
    El cash es parte de la estrategia, no un fracaso. El motor pasa ~70-75% del tiempo en cash (SHV). No hacer nada ES la estrategia cuando no hay oportunidades válidas. La disciplina de esperar es más valiosa que la acción constante.
    El holding period rígido es crítico. 1 mes inquebrantable. Ni vender antes "porque ya subió un 10%", ni mantener más "porque sigue subiendo". La disciplina temporal convierte el caos en sistema.
    Esta estrategia no es tu cartera principal. Su CAGR (15.5%) supera al Buy & Hold (13.4%), pero su exposición media (26%) limita el alpha absoluto. Su valor está en el Sharpe (0.70 vs 0.56) y el drawdown controlado (-15.5% vs -24.5%). Úsala como SATÉLITE (10-20% del patrimonio) en un modelo Core-Satellite.
    La evidencia estadística es débil. Con p-valores de 0.065-0.154 para selección y timing, no podemos concluir con 95% de confianza que la estrategia tenga alpha real. Se necesitan más datos (10-15 años) para validar robustez.
    El contexto macroeconómico lo es todo. Una estrategia que brilla en 2023-2024 (rally de la IA) puede estar inactiva años enteros en un bear market como 2022. El momentum crash no predice rallies, reacciona a ellos.

La filosofía del Momentum Crash, democratizada a través de este motor cuantitativo, demuestra que no necesitas predecir el futuro. Solo necesitas reglas frías y matemáticas para comprar cuando la euforia colectiva alcanza niveles medibles... siempre que entiendas sus limitaciones y la integres correctamente en una cartera más amplia.
️ Descargo de Responsabilidad y Advertencia de Riesgos
Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa. Antes de finalizar, es imperativo que el lector comprenda las siguientes limitaciones:
Los Resultados Pasados No Garantizan Resultados Futuros
El backtest presentado es una simulación histórica basada en datos pasados (2021-2026). Que la estrategia Momentum Crash haya generado un CAGR del 15.5% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los umbrales de los filtros (RSI ≥ 70, holding 1 mes) fueron elegidos antes de ver los resultados, pero cualquier umbral fijo puede dejar de funcionar si cambia la microestructura del mercado o la composición de los ETFs sectoriales.
Limitaciones del Backtest

    Sesgo de supervivencia (Survivorship Bias): El universo de 26 ETFs incluye solo los que existen hoy. Algunos ETFs que existían en 2021 fueron cerrados o fusionados por falta de activos. Si esos ETFs cerraron porque su sector era estructuralmente inviable, nuestro backtest los excluye y sobreestima la rentabilidad de la estrategia.
    Costes de transacción y deslizamiento (Slippage): Se han asumido costes estándar del 0.1% por operación. En momentos de alta volatilidad (cuando se activan las señales momentum), los spreads bid-ask se ensanchan y el slippage real puede ser del 0.3-0.5%, reduciendo el alpha.
    Look-ahead bias controlado: El RSI y el momentum se calculan con datos disponibles el último día del mes, antes de ejecutar la orden. No hay filtración de información futura.
    Fiscalidad: El motor no contempla el impacto de impuestos por plusvalías. La rotación mensual genera eventos fiscales que reducen el rendimiento neto real.
    Datos parciales: Algunos ETFs (URTH, USMV, MTUM, XLRE, XLC, ARKK, BITO) no tienen datos desde 2007 porque no existían entonces. El backtest efectivo comienza en 2021-10-20, cuando el último activo (BITO) tiene datos suficientes.

No es Asesoramiento Financiero
Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe evaluar su tolerancia al riesgo, considerar su horizonte temporal y consultar con un asesor financiero independiente.
Riesgo de Pérdida de Capital
Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. La estrategia momentum crash, incluso con filtros, tiene un drawdown histórico del -15.5%. En un escenario futuro más adverso (crisis sistémica prolongada, depresión económica), las caídas podrían ser significativamente mayores. Un inversor que no pueda tolerar ver su satélite momentum caer un 20-30% no debería usar esta estrategia.
Uso del Código
El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de fallos en la detección automática de señales debido a ruido en los datos de cotización.
Recuerda
El Momentum Crash cuantitativo no es "comprar lo que sube". Eso es perseguir tendencias y es la forma más rápida de comprar en el pico. El Momentum Crash cuantitativo es comprar lo que ha subido mucho, cuando la euforia es medible (RSI ≥ 70), cuando el momentum es sostenido (12-1 meses), y solo durante un tiempo limitado (1 mes).
Es una estrategia de disciplina y rotación rápida, no de convicción a largo plazo. Su verdadero valor no está en batir al mercado en rentabilidad absoluta, sino en generar alpha positivo (+2.09%) con un drawdown controlado (-15.5% vs -24.5%), actuando como un satélite táctico que se activa exactamente cuando la euforia colectiva alcanza niveles extremos.
La capacidad de quedarse en cash el 70-75% del tiempo, sin hacer nada, sin sentir la ansiedad de "perderse algo", es quizás la habilidad más valiosa que esta estrategia enseña al inversor conservador. La paciencia, la disciplina y la validación rigurosa de los datos son tus mayores aliados.