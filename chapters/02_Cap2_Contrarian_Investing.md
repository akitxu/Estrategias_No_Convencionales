# Capítulo 2: Contrarian Investing — Comprar cuando nadie quiere
Versión: 2.1 | Motor: Modular Dinámico v1.0 | Última actualización: 2026-10-03

    "Sé codicioso cuando otros tienen miedo, y temeroso cuando otros son codiciosos."
    — Warren Buffett

Si la Cartera Permanente de Harry Browne nos enseñó a protegernos de las cuatro estaciones económicas, y el All Weather de Ray Dalio nos mostró cómo repartir el riesgo equitativamente, el Contrarian Investing representa un giro filosófico radical: **apostar contra la multitud en los momentos de máximo pánico.**

La premisa es contraintuitiva pero matemáticamente sólida: los mercados financieros están impulsados por la psicología humana (miedo y codicia), y esta psicología tiende a exagerar. Cuando las noticias son malas, los inversores venden en pánico empujando los precios muy por debajo de su valor razonable. Cuando las noticias son buenas, la euforia los empuja muy por encima. El inversor contrarian se posiciona sistemáticamente en el lado opuesto a la multitud.

Pero aquí viene la advertencia crítica que diferencia este capítulo de los manuales de autoayuda financiera: comprar ciegamente "lo que baja" es la forma más rápida de destruir capital. El mercado a veces tiene razón: un sector puede estar barato porque su modelo de negocio está estructuralmente roto (piensa en Blockbuster en 2008 o los periódicos impresos en 2010). La clave está en distinguir entre una caída temporal por pánico y una caída estructural por obsolescencia.

Este capítulo cuantifica esa distinción con reglas matemáticas estrictas.

## La Lógica del Contrarian Cuantitativo

A diferencia del contrarian "de intuición" (que compra porque "siente" que algo está barato), el contrarian cuantitativo exige que se cumplan tres condiciones simultáneamente antes de ejecutar una compra:

| Condición | Umbral | ¿Qué mide? |
|------------|---------|------------|
| **1. Ranking de perdedores** | Top 5 peores a 12 meses | Identifica los activos con peor comportamiento relativo y mayor nivel de impopularidad reciente. |
| **2. Drawdown desde máximos** | ≤ -15% desde el máximo de 52 semanas | Confirma que el pesimismo es significativo y no se trata de una simple corrección de mercado. |
| **3. RSI(14) técnico** | ≤ 45 | Verifica que la presión vendedora sigue siendo dominante y que el activo presenta debilidad técnica. |

Si un activo no cumple las tres condiciones, no se compra. El capital no asignado se aparca en letras del Tesoro a corto plazo (SHV), rindiendo el tipo libre de riesgo sin asumir riesgo de mercado.

## Reglas operativas completas

| Parámetro | Valor |
|-----------|--------|
| **Universo** | 16 ETFs sectoriales, factoriales, internacionales y alternativos. |
| **Frecuencia de revisión** | Mensual (último día hábil de cada mes). |
| **Ranking** | Selección de los 5 peores activos por rentabilidad a 12 meses. |
| **Filtro de drawdown** | Drawdown ≤ -15% respecto al máximo de 52 semanas. |
| **Filtro RSI** | RSI(14) ≤ 45. |
| **Asignación** | Reparto equiponderado entre los activos seleccionados (20% cada uno si hay 5 posiciones). |
| **Holding period** | 3 meses; posteriormente se vende y se reevalúa la cartera. |
| **Cash residual** | Si menos de 5 activos cumplen los filtros, el capital no asignado se destina a SHV. |
| **Benchmark** | SPY (S&P 500). |

**Observa la asimetría:** la estrategia pasa la mayor parte del tiempo en cash (a menudo 60-70% del patrimonio), esperando pacientemente a que el pánico colectivo cree oportunidades genuinas. Cuando actúa, lo hace con convicción matemática, no con intuición.

## Arquitectura Técnica (Motor Dinámico v1.0)**

El motor cuantitativo de este libro incorpora por primera vez un Motor de Backtest Dinámico (MotorBacktestDinamico), diseñado específicamente para estrategias que requieren asignaciones variables en el tiempo. A diferencia del MotorBacktest clásico (que recibe pesos fijos y rebalancea periódicamente), el motor dinámico acepta una función generadora de pesos que se ejecuta en cada fecha de decisión.  
Además, el sistema introduce cinco nuevos módulos especializados:

| Módulo | Función |
|---------|----------|
| **🌡️ Termómetro** | Gestor de señales binarias de mercado orientadas a detectar estados de miedo y codicia. |
| **🔬 Gemelólogo** | Motor de análisis de cointegración y *pairs trading* mediante pruebas de Engle-Granger, z-scores y métricas estadísticas relacionadas. |
| **📅 Cronista** | Seguimiento y registro de eventos corporativos relevantes, como resultados empresariales, OPAs e informes Form 4. |
| **🎰 Actuario** | Simulador de estrategias con opciones financieras, incluyendo análisis de payoff, sensibilidades (griegas) y escenarios de riesgo. |
| **🔭 Observatorio** | Biblioteca de indicadores alternativos y métricas no convencionales para análisis cuantitativo. |

Para el Contrarian Investing, el módulo relevante es el Observatorio, que calcula el RSI(14), el drawdown desde máximos de 52 semanas y la rentabilidad a 12 meses en tiempo real.

## Validación inteligente con warm-up automático

El sistema introduce una capa de robustez inédita: validación automática de ventana mínima. Antes de ejecutar la estrategia, el motor verifica que haya suficientes datos históricos para calcular los indicadores (rentabilidad 12m = 252 días + drawdown 52s = 252 días + RSI(14) = 14 días ≈ 302 días mínimos). Si el período elegido por el usuario es más corto, el motor añade automáticamente un warm-up descargando datos históricos adicionales, sin que el usuario tenga que intervenir.

## Análisis de Resultados Reales (2007 - 2026)

Hemos sometido a backtest la estrategia Contrarian con los 16 ETFs más líquidos del mercado durante un período de 20 años que incluye las crisis más severas de las últimas dos décadas: la Crisis Financiera Mundial (2008), la Crisis de Deuda Soberana (2011), el Flash Crash (2015), la Pandemia COVID-19 (2020) y la crisis inflacionaria (2022).

### Informe de Limpieza de Datos

| Activo | Ticker | Filas | Desde | Hasta | Fuente |
|---------|:------:|------:|------------|------------|--------|
| SPDR S&P 500 | SPY | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Invesco QQQ | QQQ | 6.934 | 1999-03-10 | 2026-10-01 | CSV |
| Russell 2000 Small Cap | IWM | 6.626 | 2000-05-26 | 2026-10-01 | CSV |
| Technology Select Sector SPDR | XLK | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Financial Select Sector SPDR | XLF | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Energy Select Sector SPDR | XLE | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Health Care Select Sector SPDR | XLV | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Industrial Select Sector SPDR | XLI | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Consumer Staples Select Sector SPDR | XLP | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Utilities Select Sector SPDR | XLU | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Materials Select Sector SPDR | XLB | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| Consumer Discretionary Select Sector SPDR | XLY | 6.979 | 1999-01-04 | 2026-10-01 | CSV |
| MSCI EAFE Developed Markets | EFA | 6.311 | 2001-08-27 | 2026-10-01 | CSV |
| MSCI Emerging Markets | EEM | 5.905 | 2003-04-14 | 2026-10-01 | CSV |
| iShares 20+ Year Treasury Bond | TLT | 6.083 | 2002-07-30 | 2026-10-01 | CSV |
| SPDR Gold Shares | GLD | 5.501 | 2004-11-18 | 2026-10-01 | CSV |
| iShares Short Treasury Bond | SHV | 4.962 | 2007-01-11 | 2026-10-01 | CSV |

💡 Insight Clave: El backtest efectivo comienza en 2007-01-11 (cuando el último activo, SHV, tiene datos suficientes), aunque los datos de warm-up se descargan desde 1999 para permitir el cálculo de indicadores desde el primer día.

### Diagnóstico de Filtros en la Primera Fecha Válida

El motor ejecuta un diagnóstico inicial para verificar que los filtros no son tan estrictos que nunca se activen, ni tan laxos que se activen constantemente:

📅 Fecha de diagnóstico: 2008-01-11 (en plena Crisis Financiera Mundial)

Markdown
| Activo | Ret_12m | Drawdown | RSI | ✓DD | ✓RSI | ✓AMBOS |
|---------|---------:|---------:|----:|:---:|:----:|:------:|
| SPDR S&P 500 | -0,4% | -10,0% | 33 | ❌ | ✅ | — |
| Invesco QQQ | 4,1% | -14,4% | 30 | ❌ | ✅ | — |
| **Russell 2000 Small Cap** | **-10,2%** | **-16,8%** | **29** | ✅ | ✅ | 🎯 |
| Technology SPDR | 1,8% | -14,1% | 24 | ❌ | ✅ | — |
| **Financials SPDR** | **-23,7%** | **-26,1%** | **39** | ✅ | ✅ | 🎯 |
| Energy SPDR | 37,9% | -6,1% | 44 | ❌ | ✅ | — |
| Healthcare SPDR | 8,1% | -0,6% | 61 | ❌ | ❌ | — |
| Industrial SPDR | 3,9% | -12,6% | 30 | ❌ | ✅ | — |
| Consumer Staples SPDR | 9,0% | -3,6% | 45 | ❌ | ✅ | — |
| Utilities SPDR | 24,4% | -1,4% | 56 | ❌ | ❌ | — |
| Materials SPDR | 15,8% | -8,0% | 42 | ❌ | ✅ | — |
| **Consumer Discretionary SPDR** | **-21,9%** | **-24,3%** | **26** | ✅ | ✅ | 🎯 |
| MSCI EAFE Developed | 5,4% | -10,5% | 38 | ❌ | ✅ | — |
| MSCI Emerging Markets | 32,9% | -11,0% | 49 | ❌ | ❌ | — |
| iShares 20+ Year Treasury | 12,2% | -0,7% | 58 | ❌ | ❌ | — |
| Gold ETF | 42,5% | 0,0% | 88 | ❌ | ❌ | — |

🎯 3 activos cumplieron ambos filtros: Russell 2000 Small Cap, Financials SPDR y Consumer Disc SPDR. Exactamente los sectores que más sufrirían en los meses siguientes, pero que también ofrecerían los mayores rebotes.

### Métricas de Diagnóstico Comparativo

Log de Rebalanceos (Extracto de momentos clave)

| Fecha | Rotación | Coste (€) | Patrimonio (€) | Contexto |
|------------|---------:|----------:|---------------:|-----------|
| 2008-07-01 | 50,00% | 5,00 | 9.995,00 | Primera entrada contrarian |
| 2008-10-01 | 60,81% | 5,74 | 9.439,52 | Lehman Brothers |
| 2008-12-01 | 0,72% | 0,05 | 6.571,47 | Fondo de la crisis financiera |
| 2009-01-02 | 50,00% | 3,86 | 7.707,36 | Rotación tras la crisis |
| 2012-01-03 | 100,00% | 12,10 | 12.089,78 | Rotación completa de cartera |
| 2016-04-01 | 100,00% | 13,80 | 13.787,65 | Rotación completa de cartera |
| 2020-10-01 | 50,00% | 7,45 | 14.892,97 | Crisis COVID-19 |
| 2021-04-01 | 50,00% | 12,64 | 25.274,61 | Recuperación post-COVID |
| 2022-10-03 | 40,37% | 9,65 | 23.904,06 | Crisis inflacionaria |
| 2023-01-03 | 41,48% | 10,40 | 25.052,78 | Rotación tras la crisis inflacionaria |
| 2024-01-02 | 50,00% | 16,36 | 32.707,69 | Última rotación completa registrada |
| 2026-10-01 | 50,00% | 16,35 | 32.691,34 | Cierre del backtest |

💡 Insight Clave: El coste total acumulado en 20 años es de apenas 305.66€ (0.17% anual). La estrategia es extremadamente eficiente en términos de fricción: solo rota cuando los filtros se activan, no por calendario.

## Diagnóstico Automático

El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:

    **🟡 Ratio de Sharpe aceptable (0.28):** Rentabilidad digna por unidad de riesgo, aunque inferior al Buy & Hold en este período concreto.
    **🔴 Riesgo de caída elevado (Max DD: 42.3%):** Una caída del 42% requiere psicología preparada. No es una cartera "tranquila" en términos absolutos.
    **🛡️ Beta baja (0.37):** Cartera altamente defensiva. Si el S&P 500 cae un 10%, tu cartera probablemente caerá solo un 3.7%.
    **🌟 Alpha positivo (+2.16%):** Ajustado al riesgo asumido, el rebalanceo generó valor añadido frente a no hacer nada.

## 📌 Nota Pedagógica: ¿Cómo leer estas métricas?

⚠️ ¿Por qué las "Métricas Extras" muestran 0 operaciones si hubo 63 rebalanceos?
Las métricas de "Trading Activo" (Win-rate, Profit Factor, Ratio B/P) están diseñadas para estrategias con OPERACIONES DISCRETAS (ej. Patrones Armónicos, Tortuga Coja), donde cada entrada y salida es una operación independiente con un precio de compra y venta definido.  
El Contrarian Investing es una estrategia de REBALANCEO PERIÓDICO. El motor dinámico no registra "tickets" de compra/venta individuales, sino cambios en los PESOS DE LA CARTERA (rotaciones).  
Para esta estrategia, los indicadores relevantes NO son el Win-rate, sino:

* LOG DE REBALANCEOS: Muestra la frecuencia y el coste real (63 rebalanceos en 20 años = ~3 rotaciones/año. Coste total: 305.66€).
* INFORMATION RATIO: Mide si el Alpha generado justifica el riesgo de seguimiento (Tracking Error) frente al benchmark.
* ALPHA (+2.16%) y BETA (0.37): Miden la decorrelación y el valor añadido real de la estrategia defensiva.

### ¿Por qué el Contrarian tuvo resultados "matizados"?

Los datos muestran algo contraintuitivo: el Max Drawdown (-42.31%) es prácticamente igual al del Buy & Hold (-42.09%), y el CAGR (6.19%) es significativamente inferior al del Buy & Hold (9.84%). Esto contradice la promesa popular de que el contrarian "siempre gana en crisis". ¿Por qué?
La respuesta está en la naturaleza de los filtros

* Los filtros se activan DESPUÉS de que la crisis haya empezado: Cuando el drawdown alcanza -15% y el RSI cae a 45, la crisis ya está en marcha. La estrategia compra en el pánico, pero no en el fondo exacto. En 2008, por ejemplo, los filtros se activaron en julio-octubre, pero el fondo real llegó en marzo de 2009.
* El holding period de 3 meses es demasiado corto para capturar rebotes completos: Cuando la estrategia compra en pánico y mantiene solo 3 meses, a menudo vende antes de que el rebote se complete. En 2009, por ejemplo, el mercado subió un 80% entre marzo de 2009 y marzo de 2010, pero la estrategia rotó posiciones cada 3 meses, capturando solo fracciones de ese movimiento.
* El cash es un lastre en bull markets prolongados: Entre 2012 y 2019, el mercado subió de forma sostenida. La estrategia pasó la mayor parte de ese tiempo en cash (SHV), perdiéndose el rally completo. Esto explica por qué el CAGR es 3.65 pp inferior al Buy & Hold.*

Pero... el Alpha positivo (+2.16%) y la Beta baja (0.37) son reales

A pesar de las limitaciones, la estrategia logra algo valioso:

* Alpha +2.16%: Por cada unidad de riesgo de mercado asumida, la estrategia genera un 2.16% extra. Esto es lo que buscan los gestores profesionales.
* Beta 0.37: La cartera es 63% menos sensible al mercado que un Buy & Hold. En una crisis del -50% del mercado, esta estrategia caería teóricamente solo un -18.5% (0.37 × 50%).
* VaR 95% diario 60% menor: El peor día esperado es 380€ vs 965€ del mercado.

### La Ventaja Real del Contrarian (Matizada)

Los datos de este período (2007-2026) nos obligan a matizar lo que prometía la teoría:

| Ventaja real | Evidencia |
|-------------|-----------|
| ✅ **Alpha positivo** | +2,16% de rentabilidad ajustada al riesgo respecto al benchmark. |
| ✅ **Beta ultra baja** | 0,37, lo que implica una sensibilidad al mercado un 63% inferior. |
| ✅ **VaR diario controlado** | Riesgo extremo diario aproximadamente un 60% menor que el del mercado. |
| ✅ **Coste de fricción mínimo** | Coste anual estimado de tan solo el 0,17%. |
| ❌ **CAGR inferior** | 6,19% frente al 9,84% obtenido por la estrategia Buy & Hold. |
| ❌ **Max Drawdown similar** | -42,31% frente al -42,09% del benchmark, sin mejora relevante. |
| ❌ **Sharpe inferior** | 0,28 frente a 0,50, indicando una menor eficiencia riesgo-retorno. |

**Conclusión matizada:** El Contrarian Investing no es una estrategia para batir al mercado en rentabilidad absoluta. Es un satélite defensivo que aporta alpha positivo y decorrelación, diseñado para integrarse en un modelo Core-Satellite (80% Bogleheads + 20% Contrarian), no para reemplazar la cartera principal.

## Cómo Hacer Seguimiento con el Script

### 1. Ejecutar el diagnóstico mensual

El motor ejecuta el ContrarianScanner el último día hábil de cada mes. Si detecta activos que cumplen los tres criterios (peor ranking a 12m + drawdown ≤ -15% + RSI ≤ 45), genera una alerta con la lista de candidatos y los pesos sugeridos.

### 2. Asignación como satélite

Se recomienda destinar entre un 10% y un 20% del patrimonio total a esta estrategia. El 80-90% restante permanece en la cartera core (Bogleheads, All Weather o la que hayas elegido del primer libro). De esta forma, si el contrarian tiene un mal año, el impacto sobre tu patrimonio total es limitado.

### 3. El cash es parte de la estrategia

Cuando el motor no encuentra activos que cumplan los filtros (lo cual ocurre el 60-70% del tiempo), no fuerces compras. El capital no asignado se aparca en letras del Tesoro (SHV) y rinde el tipo libre de riesgo. No hacer nada ES la estrategia en esos meses.

### 4. Regla de los 3 meses inquebrantable

Una vez que compras un activo contrarian, lo mantienes exactamente 3 meses. No vendas antes porque "ya ha rebotado un 15%" ni mantengas más porque "aún está barato". La disciplina temporal es lo que convierte una estrategia caótica en un sistema reproducible.

### 5. Decorrelación real

Con un beta de 0.37 y un alpha positivo, esta estrategia aporta diversificación real a una cartera core de ETFs indexados. En los peores meses del mercado, el contrarian filtrado suele estar en cash o en sectores que ya cayeron tanto que tienen poco recorrido bajista adicional.

### Cuándo NO usarla

* No la uses como estrategia única. Su CAGR (6.19%) es inferior al Buy & Hold (9.84%). A largo plazo, un inversor que solo haga contrarian filtrado ganará menos que uno que simplemente compre y mantenga SPY.
* No la uses en mercados alcistas sostenidos. En un bull market como 2012-2019, el motor pasará la mayor parte del tiempo en cash porque ningún sector cumplirá los filtros de drawdown y RSI. Eso es correcto (no hay oportunidades contrarian genuinas), pero psicológicamente es difícil ver cómo tu satélite rinde un 2% mientras el mercado sube un 25%.
* No la uses con acciones individuales. El universo debe ser ETFs sectoriales diversificados. Una acción individual puede caer un 80% y nunca recuperarse (Enron, Lehman, Wirecard). Un ETF sectorial diversificado (50-100 empresas) tiene una probabilidad de recuperación estructural mucho mayor.

## Conclusiones

El análisis del Contrarian Investing arroja lecciones matizadas pero valiosas:

* El contrarian puro es una trampa mortal. Sin filtros, comprar "lo que más baja" atrapa cuchillos cayendo. El Intento 1 (sin filtros) habría generado un drawdown del -58% y un alpha negativo. La teoría sin cuantificación es peligrosa.
* Los filtros cuantitativos son lo que separa el contrarian del suicidio. Drawdown ≤ -15% desde máximos garantiza que el pánico es genuino. RSI(14) ≤ 45 confirma que la presión vendedora está exhaustiva. Juntos, filtran los "cuchillos" de los "suelos de pánico".
* El cash es parte de la estrategia, no un fracaso. El motor pasa ~60-70% del tiempo en cash (SHV). No hacer nada ES la estrategia cuando no hay oportunidades válidas. La disciplina de esperar es más valiosa que la acción constante.
* El holding period rígido es crítico. 3 meses inquebrantables. Ni vender antes "porque ya rebotó", ni mantener más "porque sigue barato". La disciplina temporal convierte el caos en sistema.
* Esta estrategia no es tu cartera principal. Su CAGR (6.19%) es inferior al Buy & Hold (9.84%). Su valor está en el alpha positivo (+2.16%) y la beta baja (0.37). Úsala como SATÉLITE (10-20% del patrimonio) en un modelo Core-Satellite.
* Beta baja = decorrelación real. Beta de 0.37: la estrategia es 63% menos sensible al mercado. Aporta diversificación genuina a una cartera Bogleheads o All Weather.
* El contexto macroeconómico lo es todo. Una estrategia que brilla en 2008-2009 puede estar inactiva años enteros en un bull market como 2012-2019. El contrarian no predice crisis, reacciona a ellas.

La filosofía del Contrarian Investing, democratizada a través de este motor cuantitativo, demuestra que no necesitas predecir el futuro. Solo necesitas reglas frías y matemáticas para comprar cuando el miedo colectivo alcanza niveles extremos... siempre que entiendas sus limitaciones y la integres correctamente en una cartera más amplia.

## ⚠️ Descargo de Responsabilidad y Advertencia de Riesgos

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa. Antes de finalizar, es imperativo que el lector comprenda las siguientes limitaciones:

* Los Resultados Pasados No Garantizan Resultados Futuros
* El backtest presentado es una simulación histórica basada en datos pasados (2007-2026). Que la estrategia Contrarian haya generado un alpha positivo del +2.16% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los umbrales de los filtros (-15% de drawdown, RSI 45) fueron elegidos antes de ver los resultados, pero cualquier umbral fijo puede dejar de funcionar si cambia la microestructura del mercado o la composición de los ETFs sectoriales.

### Limitaciones del Backtest

* **Sesgo de supervivencia (Survivorship Bias):** El universo de 16 ETFs incluye solo los que existen hoy. Algunos ETFs que existían en 2007 fueron cerrados o fusionados por falta de activos. Si esos ETFs cerraron porque su sector era estructuralmente inviable, nuestro backtest los excluye y sobreestima la rentabilidad de la estrategia.
* **Costes de transacción y deslizamiento (Slippage):** Se han asumido costes estándar del 0.1% por operación. En momentos de pánico extremo (cuando se activan las señales contrarian), los spreads bid-ask se ensanchan y el slippage real puede ser del 0.3-0.5%, reduciendo el alpha.
* **Look-ahead bias controlado:** El RSI y el drawdown se calculan con datos disponibles el último día del mes, antes de ejecutar la orden. No hay filtración de información futura.
* **Fiscalidad:** El motor no contempla el impacto de impuestos por plusvalías. La rotación trimestral genera eventos fiscales que reducen el rendimiento neto real.
* **Datos parciales:** Algunos ETFs (EFA, EEM, TLT, GLD, SHV) no tienen datos desde 1999 porque no existían entonces. El backtest efectivo comienza en 2007-01-11, cuando el último activo (SHV) tiene datos suficientes.

### No es Asesoramiento Financiero

Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe evaluar su tolerancia al riesgo, considerar su horizonte temporal y consultar con un asesor financiero independiente.

### Riesgo de Pérdida de Capital

Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. La estrategia contrarian, incluso con filtros, tiene un drawdown histórico del -42.31%. En un escenario futuro más adverso (crisis sistémica prolongada, depresión económica), las caídas podrían ser significativamente mayores. Un inversor que no pueda tolerar ver su satélite contrarian caer un 40-50% no debería usar esta estrategia.

### Uso del Código

El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de fallos en la detección automática de señales debido a ruido en los datos de cotización.

**Recuerda**
El Contrarian Investing cuantitativo no es "comprar lo que baja". Eso es atrapar cuchillos cayendo y es la forma más rápida de destruir capital. El Contrarian Investing cuantitativo es comprar lo que ha caído mucho, cuando el pánico es medible (drawdown ≤ -15%), cuando la presión vendedora está técnicamente exhausta (RSI ≤ 45), y solo durante un tiempo limitado (3 meses).
Es una estrategia de paciencia y disciplina, no de intuición. Su verdadero valor no está en batir al mercado en rentabilidad absoluta, sino en generar alpha positivo (+2.16%) con una beta ultra baja (0.37), actuando como un seguro táctico que se activa exactamente cuando el miedo colectivo alcanza niveles extremos.
La capacidad de quedarse en cash el 60-70% del tiempo, sin hacer nada, sin sentir la ansiedad de "perderse algo", es quizás la habilidad más valiosa que esta estrategia enseña al inversor conservador. La paciencia, la disciplina y la validación rigurosa de los datos son tus mayores aliados.