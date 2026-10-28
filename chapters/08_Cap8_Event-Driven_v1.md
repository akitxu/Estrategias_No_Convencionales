# Capítulo 8: Event-Driven Trading — Merger Arbitrage Proxy con ETFs Sectoriales
Versión: 8.2 | Motor: Modular Dinámico v1.0 | Actualización: 2026-10-26

    "El verdadero arbitraje de eventos requiere datos en tiempo real, conocimiento corporativo y ejecución institucional. Lo que simulamos aquí es un proxy pedagógico: comprar pánico sectorial cuando el mercado exagera."
    — Adaptación libre de Marcos López de Prado

**Concepto clave:** Este capítulo abandona las reglas basadas en indicadores técnicos (medias móviles, RSI, momentum) y las sustituye por una estrategia basada en eventos: detectar caídas extremas (>25% desde máximos) en ETFs sectoriales y apostar a su recuperación. La premisa es que los mercados sectoriales (biotech, banca, retail, semiconductores) tienden a sobre-reaccionar ante noticias negativas, creando oportunidades de mean reversion.

**⚠️ Advertencia:** Esto NO es merger arbitrage puro. Es un proxy pedagógico para entender la lógica de entrar en dislocaciones y salir en convergencia.

## La Lógica del Event-Driven Trading

¿Qué es el Event-Driven real?  
En la industria institucional, el Event-Driven incluye:

* **Merger Arbitrage:** Comprar la empresa objetivo y vender la adquirente tras un anuncio de fusión.
* **Earnings Plays:** Apostar a sorpresas de resultados trimestrales.
* **Distressed Securities:** Comprar deuda de empresas en quiebra.
* **Activist Investing:** Presionar a la dirección para cambios corporativos.

Todas estas estrategias requieren datos en tiempo real, conocimiento corporativo profundo y ejecución institucional. Nuestro proxy pedagógico simula la filosofía: comprar pánico sectorial cuando el mercado exagera.

### Las tres condiciones para operar

  Condición | Umbral | ¿Qué mide? |
 |---|---|---|
 | 1. Caída desde máximos | \> 25% | Identifica estrés sectorial extremo. |
 | 2. Volumen anómalo | \> 2x media histórica | Confirma que la caída es por evento, no ruido. |
 | 3. Criterios de salida | Recuperar 50% o 126 días | Limita el tiempo de exposición. |

Si se cumplen las condiciones 1 y 2, entramos largo en el ETF caído. Salimos cuando se cumple la condición 3 (lo que ocurra primero).

### Reglas operativas completas

  Parámetro | Valor |
 |---|---|
 | Universo | XBI (Biotech), IBB (Biotech), KBE (Banking), XRT (Retail), SMH (Semiconductors) |
 | Cash proxy | SHY (iShares 1-3 Year Treasury Bond) |
 | Benchmark | SPY (S&P 500) |
 | Umbral de entrada | Caída > 25% desde máximos + volumen > 2x media |
 | Criterios de salida | Recuperar 50% de la caída o 126 días (6 meses) |
 | Peso por posición | 20% del capital (5 ETFs × 20% = 100%) |
 | Frecuencia de revisión | Semanal |
 | Coste de transacción | 0,1% por operación |

### Arquitectura Técnica (Motor Dinámico v1.0 + Event Detector)

El motor cuantitativo de este libro incorpora un módulo de detección de eventos que escanea diariamente el universo de ETFs sectoriales en busca de caídas extremas. Este módulo implementa:

* **Cálculo de máximos históricos rolling:** Para cada ETF, calcula el máximo histórico hasta la fecha actual.
* **Detección de caídas:** Identifica cuando el precio actual cae más del 25% respecto al máximo.
* **Filtro de volumen:** Valida que la caída esté acompañada de volumen anómalo (>2x media de 20 días).
* **Gestión de posiciones:** Abre posiciones largas en los ETFs que cumplen los criterios y las cierra según los criterios de salida.

Para el backtest, el MotorBacktestDinamico acepta una función generadora de pesos que consulta el estado de los eventos en cada fecha y asigna pesos a los ETFs caídos o a SHY (cash) según corresponda.

## Análisis de Resultados Reales (2016 - 2026)

Hemos sometido a backtest la estrategia Event-Driven durante un período de 10 años que incluye la corrección de 2016, la Pandemia COVID-19 (2020), la crisis inflacionaria (2022-2023) y el rally de la IA (2024-2026).

### Informe de Limpieza de Datos

  Activo | ISIN | Filas | Desde | Hasta | Fuente |
 |---|---|---|---|---|---|
 | SPDR S&P Biotech | XBI | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | iShares Biotechnology | IBB | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | SPDR S&P Bank ETF | KBE | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | SPDR S&P Retail | XRT | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | VanEck Semiconductor | SMH | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | iShares 1-3 Year Treasury | SHY | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | SPDR S&P 500 | SPY | 2,711 | 2016-01-04 | 2026-10-14 | CSV |

 💡 Insight Clave: Los 7 activos tienen datos completos desde el inicio del período, lo que garantiza que la detección de eventos y la rotación a SHY sean viables.

### Detección de Eventos

El motor escaneó diariamente los 5 ETFs sectoriales en busca de caídas >25% desde máximos. Los resultados son reveladores:

  ETF | Eventos Detectados | % del Total | Interpretación |
 |---|---|---|---|
 | XBI (Biotech) | 448 | 32.5% | Sector altamente volátil, frecuente sobre-reacción |
 | KBE (Banking) | 318 | 23.1% | Sensible a crisis financieras y regulatorias |
 | XRT (Retail) | 247 | 17.9% | Afectado por ciclos económicos y consumo |
 | IBB (Biotech) | 180 | 13.1% | Similar a XBI pero con componentes más grandes |
 | SMH (Semiconductors) | 186 | 13.5% | Menos eventos pero caídas más severas |
 | Total | 1,379 | 100% | ⚠️ Excesivamente alto |

**🚨 Alerta Crítica:** 1,379 eventos en 10 años (~2,711 días hábiles) significa que el 50.9% de los días hubo al menos un ETF en estado de "caída extrema". Esto indica que el umbral del 25% es demasiado bajo para ser considerado "event-driven". En la práctica, la estrategia está operando casi constantemente, no esperando eventos raros.

### Métricas de Diagnóstico Comparativo (Resultados Reales)

  Métrica | Event-Driven | Buy & Hold (SPY) | ¿Qué significa? |
 |---|---|---|---|
 | Patrimonio Final | €12,246.99 | ~€20,800* | ❌ Event-Driven genera ~41% menos que B&H |
 | Rentabilidad Total | 22.47% | ~108%* | ❌ Event-Driven inferior en rentabilidad absoluta |
 | CAGR | 1.90% | 7.59% | ❌ Event-Driven inferior en 5.69% anualizado |
 | Volatilidad | 4.30% | 32.52% | ✅ 87% menos oscilación diaria |
 | Ratio de Sharpe | -0.02 | 0.17 | ❌ Por debajo de la tasa libre de riesgo (2%) |
 | Ratio de Sortino | -0.02 | 0.17 | ❌ Menor eficiencia en downside |
 | Max Drawdown | -10.58% | -63.89% | ✅ 83% menos caída máxima |
 | VaR 95% | €20.65 | €711.79 | ✅ 97% menos riesgo de cola |
 | Alpha | 0.00 | 0.00 | ⚖️ Sin alpha generado |
 | Beta | 0.00 | 0.00 | ✅ Desconexión total del mercado |
 | R² | 0.00 | 0.00 | ✅ 0% de la varianza explicada por el mercado |
 | Tracking Error | 0.00 | 0.00 | ⚠️ Métrica no aplicable (casi siempre en SHY) |
 | Rebalanceos | 50 | N/A | ⚠️ Baja frecuencia (~5/año) |

 *Nota: El patrimonio final del SPY se estima a partir del CAGR del 7.59% sobre €10,000 durante 10 años.

## Diagnóstico Automático
El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:

    🔴 CAGR inferior (1.90% vs 7.59%): La estrategia Event-Driven no logró superar al Buy & Hold en rentabilidad anualizada.
    🔴 Sharpe negativo (-0.02): El rendimiento está por debajo de la tasa libre de riesgo (2%). La estrategia no compensa el riesgo asumido.
    ✅ Max Drawdown controlado (-10.58%): Inferior al del SPY (-63.89%), confirmando que la rotación a SHY protege en caídas.
    ✅ Volatilidad muy reducida (4.30%): Aproximadamente 87% menos que el mercado.
    ✅ Beta = 0.00: Desconexión total del mercado, confirmando que la estrategia está mayormente en SHY.

## Interpretación del Gráfico de Patrimonio

El gráfico de equity curve revela la historia completa:

* **Línea verde (Event-Driven):** Se mantiene casi plana durante toda la década, con ligeras subidas y bajadas. Comienza en €10,000 y termina en €12,247.
* **Línea gris (Buy & Hold SPY):** Muestra la volatilidad característica del mercado, con caídas severas en 2020 (COVID) y 2022 (inflación), pero termina mucho más alto (~€20,800).

**Lección visual:** La estrategia Event-Driven funcionó como un "escudo" perfecto contra las caídas del mercado, pero también se perdió todas las subidas. El resultado es un patrimonio final muy inferior al Buy & Hold.

## Análisis del Drawdown

El gráfico de drawdown confirma el éxito de la gestión de riesgo:

* **Event-Driven:** Drawdown máximo de -10.58%, con recuperaciones rápidas.
* **Buy & Hold (SPY):** Drawdown máximo de -63.89%, con períodos prolongados de recuperación (2020-2024).

**Lección:** La estrategia protegió el capital de forma excepcional, pero a costa de renunciar a la rentabilidad del mercado.

## ¿Por qué el Event-Driven NO superó al Buy & Hold?

Los datos muestran algo contraintuitivo: la estrategia detectó 1,379 eventos en 10 años, pero generó un CAGR muy inferior al B&H (1.90% vs 7.59%). ¿Por qué?

* **El umbral del 25% es demasiado bajo:** En sectores volátiles como biotech (XBI, IBB), caídas del 25% son frecuentes y no necesariamente representan "eventos" raros. La estrategia está operando casi constantemente, no esperando oportunidades excepcionales.
* **Falta de datos de volumen:** Yahoo Finance no proporciona datos de volumen fiables para ETFs en el formato que usamos. El filtro de volumen (>2x media) no se aplicó, permitiendo entradas en caídas por ruido en lugar de eventos reales.
* **La estrategia está mayormente en SHY:** Con solo 50 rebalanceos en 10 años (~5/año), la estrategia pasa la mayor parte del tiempo en efectivo (SHY), perdiendo las subidas del mercado. El CAGR del 1.90% está muy cerca del rendimiento de SHY (~2% anual), confirmando que la estrategia está "aparcada" la mayor parte del tiempo.
* **Recuperaciones lentas:** Algunos ETFs sectoriales (especialmente biotech tras crisis regulatorias) pueden tardar años en recuperar el 50% de la caída. El plazo máximo de 126 días fuerza salidas prematuras en posiciones que habrían sido rentables a largo plazo.
* **Costes de transacción:** Con 50 rebalanceos en 10 años, los costes de transacción (0.1% por operación) erosionan el capital. Aunque no es el factor principal, contribuye a la inferioridad del Event-Driven.
* **Sharpe negativo:** El rendimiento del 1.90% está por debajo de la tasa libre de riesgo (2%), lo que genera un Sharpe negativo (-0.02). Esto significa que la estrategia no compensa el riesgo asumido vs. simplemente mantener el dinero en efectivo.

## La Ventaja Real del Event-Driven (Matizada)

Los datos de este período (2016-2026) nos obligan a ser honestos sobre las limitaciones y fortalezas reales del Event-Driven proxy:

  Ventaja real | Evidencia |
 |---|---|
 | ✅ Menor volatilidad | 4.30% vs 32.52% (-87%) |
 | ✅ Menor drawdown | -10.58% vs -63.89% (-83%) |
 | ✅ Menor VaR 95% | €20.65 vs €711.79 (-97%) |
 | ✅ Beta = 0.00 | Desconexión total del mercado |
 | 🔴 CAGR muy inferior | 1.90% vs 7.59% (-5.69% anualizado) |
 | 🔴 Sharpe negativo | -0.02 (por debajo de tasa libre de riesgo) |
 | 🔴 Demasiados eventos | 1,379 eventos en 10 años (ruido, no señales) |
 | ❌ No es event-driven real | Umbral del 25% demasiado bajo para eventos raros |
 | ❌ Falta de volumen | Filtro de volumen no aplicado correctamente |
 | ❌ Mayormente en SHY | Solo 50 rebalanceos en 10 años |

**Conclusión matizada:** El Event-Driven proxy logró reducir drásticamente la volatilidad y el drawdown, pero no logró superar al Buy & Hold en rentabilidad. La estrategia es esencialmente "estar en efectivo la mayor parte del tiempo", con incursiones breves en ETFs caídos que no generan alpha suficiente para compensar las oportunidades perdidas.

## Limitaciones Críticas para Producción

1. Umbral de Entrada Demasiado Bajo

El umbral del 25% de caída desde máximos es demasiado bajo para ser considerado "event-driven". En sectores volátiles como biotech, caídas del 25% son frecuentes y no representan eventos raros. Para ser verdaderamente event-driven, el umbral debería ser >40% o >50%.

2. Falta de Datos de Volumen

Yahoo Finance no proporciona datos de volumen fiables para ETFs en el formato que usamos. El filtro de volumen (>2x media) no se aplicó, permitiendo entradas en caídas por ruido en lugar de eventos reales. En producción, se necesitarían datos de volumen de proveedores profesionales (Bloomberg, Reuters).

3. Criterios de Salida Rígidos

El criterio de salida "recuperar 50% o 126 días" es demasiado rígido. Algunos ETFs sectoriales pueden tardar años en recuperar el 50% de una caída severa. El plazo máximo de 126 días fuerza salidas prematuras en posiciones que habrían sido rentables a largo plazo.

4. No es Merger Arbitrage Real

El verdadero merger arbitrage requiere:

    Datos en tiempo real de anuncios de fusiones
    Análisis de probabilidades de cierre del deal
    Ejecución institucional con spreads ajustados
    Capital significativo para capturar spreads de 1-3%

Nuestro proxy pedagógico no cumple ninguno de estos requisitos. Es simplemente "buy the dip" en ETFs sectoriales.

5. Sesgo de Supervivencia

Los ETFs sectoriales que cotizan hoy son los que sobrevivieron. Si hubiéramos incluido ETFs que fueron liquidados tras caídas severas (ej. ETFs de energía tras el crash de 2020), el resultado habría sido peor.

6. Sharpe Negativo

El rendimiento del 1.90% está por debajo de la tasa libre de riesgo (2%), generando un Sharpe negativo (-0.02). Esto significa que la estrategia no compensa el riesgo asumido vs. simplemente mantener el dinero en efectivo. En términos de eficiencia riesgo/retorno, la estrategia es inferior a un fondo monetario.

## Recomendaciones para Producción Real

Si quieres usar Event-Driven en la vida real, necesitas:

1. Umbrales Más Estrictos

Aumenta el umbral de caída a >40% o >50% para capturar eventos verdaderamente raros. Reduce el número de eventos de 1,379 a <50 en 10 años.

2. Datos de Volumen Profesionales

Usa proveedores de datos profesionales (Bloomberg, Reuters, Quandl) que proporcionen datos de volumen fiables para ETFs. Aplica el filtro de volumen (>2x media) correctamente.

3. Criterios de Salida Flexibles

Reemplaza el criterio rígido "recuperar 50% o 126 días" por criterios basados en fundamentos:

    Recuperación del 80% de la caída
    Cambio en el régimen de volatilidad (VIX < 20)
    Mejora en indicadores sectoriales (ej. índice de confianza para retail)

4. Análisis Fundamental

Añade análisis fundamental para validar que la caída es por evento temporal, no por deterioro estructural:

    Ratios financieros (P/E, P/B, deuda/patrimonio)
    Noticias y sentimiento (NLP sobre noticias financieras)
    Datos de insiders (compras/ventas de directivos)

5. Gestión de Riesgo Estricta

    Stop-loss dinámicos: No confíes solo en el criterio de salida; implementa stop-loss basados en ATR o drawdown máximo.
    Límites de exposición: Limita la exposición máxima a un solo sector (ej. 20% del capital).
    Diversificación entre múltiples estrategias: No pongas todos los huevos en la cesta del Event-Driven.

6. Benchmark Ajustado

Compara la estrategia no solo con el SPY, sino también con un fondo monetario (SHY). Si el CAGR del Event-Driven (1.90%) está por debajo del rendimiento de SHY (~2%), la estrategia no está generando valor vs. simplemente mantener el dinero en efectivo.

## Conclusiones

El análisis de Event-Driven Trading en el período 2016-2026 arroja lecciones humildes pero valiosas:

* El Event-Driven real requiere datos en tiempo real: Nuestro proxy pedagógico no es merger arbitrage real. Es "buy the dip" en ETFs sectoriales con un umbral demasiado bajo.
* El umbral del 25% genera ruido, no señales: 1,379 eventos en 10 años significa que la estrategia opera casi constantemente. Para ser verdaderamente event-driven, el umbral debería ser >40% o >50%.
* La falta de datos de volumen limita la estrategia: Sin filtro de volumen fiable, la estrategia entra en caídas por ruido en lugar de eventos reales.
* Los criterios de salida rígidos fuerzan decisiones subóptimas: El plazo máximo de 126 días fuerza salidas prematuras en posiciones que habrían sido rentables a largo plazo.
* La reducción de riesgo es real, pero el coste es alto: El Event-Driven logró reducir el drawdown en un 83% y la volatilidad en un 87%, pero a costa de un CAGR 5.69% anualizado inferior al Buy & Hold.
* El Sharpe negativo revela la verdad: Un rendimiento del 1.90% por debajo de la tasa libre de riesgo (2%) significa que la estrategia no compensa el riesgo asumido. En términos de eficiencia riesgo/retorno, es inferior a un fondo monetario.
* La sinergia con capítulos anteriores es clara:
    Cap 1-5 (Asignación Pasiva): Definen QUÉ comprar a largo plazo.
    Cap 6 (StatArb): Explota ineficiencias entre ETF y subyacentes.
    Cap 7 (ML): Intenta timing de mercado con aprendizaje automático.
    Cap 8 (Event-Driven): Intenta capturar eventos raros, pero con resultados limitados.

La filosofía del Event-Driven, democratizada a través de este motor cuantitativo, demuestra que la tecnología por sí sola no garantiza el éxito. Se necesitan datos en tiempo real, umbrales estrictos, y sobre todo, humildad ante la complejidad del mercado. El Event-Driven real es una estrategia institucional que requiere recursos significativos; nuestro proxy pedagógico es un punto de partida para entender la filosofía, no una estrategia de producción.

## ⚠️ Descargo de Responsabilidad y Advertencia de Riesgos

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa.  
Los Resultados Pasados No Garantizan Resultados Futuros  
El backtest presentado es una simulación histórica basada en datos pasados (2016-2026). Que la estrategia Event-Driven haya generado un CAGR del 1.90% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los umbrales de los filtros (caída >25%, volumen >2x) fueron elegidos antes de ver los resultados, pero cualquier umbral fijo puede dejar de funcionar si cambia la microestructura del mercado.

### Limitaciones del Backtest

* **Sesgo de supervivencia:** Los ETFs sectoriales utilizados son productos consolidados, pero podrían cambiar, fusionarse o ser liquidados en el futuro.
* **Costes de transacción:** Se han asumido costes estándar del 0.1% por operación. En momentos de alta volatilidad, los spreads bid-ask se ensanchan y el slippage real puede ser mayor.
* **Fiscalidad:** El motor no contempla el impacto de impuestos por ventas a corto plazo.
* **Datos de volumen:** Yahoo Finance no proporciona datos de volumen fiables para ETFs. El filtro de volumen no se aplicó correctamente.
* **Umbral demasiado bajo:** El umbral del 25% de caída genera 1,379 eventos en 10 años, lo que indica ruido en lugar de señales de eventos raros.
* **Sharpe negativo:** El rendimiento del 1.90% está por debajo de la tasa libre de riesgo (2%), generando un Sharpe negativo (-0.02).

### No es Asesoramiento Financiero

Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. La estrategia de Event-Driven es de alto riesgo y no se recomienda para inversores sin experiencia avanzada en análisis de eventos y gestión de riesgo.

### Riesgo de Pérdida de Capital

Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. Aunque el Event-Driven tiene un Max Drawdown inferior al SPY en el backtest (-10.58% vs -63.89%), la rentabilidad es muy inferior (1.90% vs 7.59%) y el riesgo de operar en ruido es alto.

### Uso del Código

El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de la exactitud de las métricas calculadas.

### 🎯 Recuerda

El Event-Driven Trading real no es "comprar caídas y esperar que se recuperen". Eso es buy the dip, no arbitraje de eventos. El Event-Driven real es:

    Identificar eventos corporativos raros (fusiones, adquisiciones, reestructuraciones).
    Analizar la probabilidad de éxito del evento.
    Ejecutar con precisión institucional para capturar spreads de 1-3%.

Es una estrategia de análisis fundamental y ejecución precisa, no de detección de caídas. Su verdadero valor no está en maximizar el CAGR, sino en capturar oportunidades raras con riesgo controlado.

La lección más importante de este capítulo: el Event-Driven real requiere datos en tiempo real, conocimiento corporativo y ejecución institucional. Nuestro proxy pedagógico es un punto de partida para entender la filosofía, no una estrategia de producción. Para operar Event-Driven en la vida real, necesitas umbrales más estrictos (>40% de caída), datos de volumen profesionales, y criterios de salida basados en fundamentos, no en plazos fijos.

La paciencia, la disciplina en la selección de eventos y la humildad ante la complejidad del mercado son tus mayores aliados. El "límite del motor" no es la potencia de cálculo, es la naturaleza de los datos: la ratio señal/ruido en los mercados financieros es tan baja que incluso los modelos más sofisticados apenas logran capturar eventos verdaderamente raros.



