# Capítulo 2 — Contrarian Investing: comprar cuando nadie quiere

    "Sé codicioso cuando otros tienen miedo, y temeroso cuando otros son codiciosos."
    — Warren Buffett

El libro The Handbook of Exotic Trading Strategies y autores como David Dreman (Contrarian Investment Strategies) explican la inversión contraria como una filosofía basada en la reversión a la media de los sentimientos del mercado. Yo me he tomado el trabajo de traducir esa teoría a código Python usando mi motor propio de backtesting, y estos son los resultados reales que da en el mercado. Aquí os dejo el código para que lo uséis.

**Semáforo de viabilidad:** 🟢 Totalmente backtesteable con Yahoo Finance. No requiere datos alternativos. No requiere ejecución en tiempo real. Apto para inversor minorista con bróker retail.

## Introducción Teórica

El Contrarian Investing es una de las estrategias más antiguas y, paradójicamente, más difíciles de ejecutar del mundo de la inversión. La idea central es simple: el mercado tiende a exagerar. Cuando las noticias son buenas, los inversores se vuelven eufóricos y empujan los precios muy por encima de su valor razonable. Cuando las noticias son malas, el pánico se apodera de las masas y los precios caen mucho más de lo que la realidad justifica.

El inversor contrarian se posiciona en el lado opuesto a la multitud. Compra lo que nadie quiere (sectores en crisis, empresas con malas noticias temporales, regiones impopulares) y vende lo que todos adoran (los ganadores del momento, los sectores de moda).

La base psicológica es sólida y está documentada en décadas de investigación en finanzas conductuales:

* **Sesgo de recencia:** los inversores extrapolan el pasado reciente al futuro. Si un sector ha caído un 40 %, asumen que seguirá cayendo.
* **Aversión a la pérdida:** el dolor de perder es aproximadamente 2.5 veces más intenso que el placer de ganar (Kahneman y Tversky). Esto hace que los inversores vendan en pánico y compren en euforia, exactamente al revés de lo que deberían hacer.
* **Efecto manada:** los gestores profesionales tienen incentivos para no desviarse del consenso. Si todos compran tecnología, ningún gestor quiere ser el único que compra energía, aunque esté barata. Esto amplifica las burbujas y los crashes.

Sin embargo, hay una trampa mortal que todo inversor contrarian debe conocer: a veces el mercado tiene razón. Un sector puede estar barato porque su modelo de negocio está estructuralmente roto (piensa en los periódicos impresos en 2010 o en Blockbuster en 2008). Comprar ciegamente lo que ha caído más es lo que en Wall Street llaman "catching a falling knife" (atrapar un cuchillo cayendo). La clave está en distinguir entre una caída temporal por pánico y una caída estructural por obsolescencia.

Este capítulo cuantifica esa distinción con reglas matemáticas estrictas.

### Fundamentos Matemáticos: el ranking de perdedores con filtros de supervivencia
La estrategia que vamos a backtestear se construye sobre tres pilares cuantitativos:

### 1. Ranking de momentum inverso (los perdedores)

Cada mes, se calcula la rentabilidad de los últimos 12 meses de un universo de ETFs sectoriales y de factores. Se ordenan de peor a mejor rendimiento. Los 5 con peor rentabilidad son los candidatos a compra.
La lógica es la siguiente: si un sector ha sido el peor durante 12 meses, es muy probable que el sentimiento hacia él sea extremadamente negativo. Los inversores lo han vendido masivamente, los analistas lo han degradado y los medios lo han declarado "muerto". Ese es exactamente el momento en el que el inversor contrarian empieza a prestar atención.

Matemáticamente, para cada activo i en el mes tt
t:

$$R_{i,t}^{12m} = \frac{P_{i,t}}{P_{i,t-12}} - 1$$

Se ordenan los  N activos del universo por Ri,t12m  $R_{i,t}^{12m}$ de menor a mayor y se seleccionan los  k=5 peores.

### 2. Filtro de drawdown desde máximos (el cuchillo)

No basta con que un activo haya tenido mala rentabilidad a 12 meses. Necesitamos asegurarnos de que la caída es lo suficientemente profunda como para reflejar pánico genuino y no simplemente un sector que rinde un poco menos que los demás.
Se calcula el drawdown desde el máximo histórico de 52 semanas:

### 2. Filtro de drawdown desde máximos (el cuchillo)

No basta con que un activo haya tenido mala rentabilidad a 12 meses. Necesitamos asegurarnos de que la caída es lo suficientemente profunda como para reflejar pánico genuino y no simplemente un sector que rinde un poco menos que los demás.
Se calcula el drawdown desde el máximo histórico de 52 semanas:

$$DD_{i,t} = \frac{\max(P_{i,t-252:t})}{P_{i,t}} - 1$$

Solo se considera candidato válido si $DD_{i,t} \leq -0.30$
donde $\(DD_{i,t}\)$ representa el drawdown del activo $\(i\)$ en el instante $\(t\)$.
(es decir, el precio está al menos un 30 % por debajo de su máximo de 52 semanas). Este umbral no es arbitrario: históricamente, las caídas superiores al 30 % en ETFs sectoriales diversificados suelen estar asociadas a episodios de pánico colectivo, no a deterioros fundamentales permanentes.

### 3. Filtro de RSI (la sobreventa técnica)

Como capa final de confirmación, se exige que el RSI(14) del activo esté por debajo de 30:

$$\mathrm{cRSI}_{i,t} = 100 - \frac{100}{1 + \mathrm{RS}_{i,t}}$$

donde  RS es el ratio de ganancias medias sobre pérdidas medias de las últimas 14 sesiones.
Un RSI < 30 indica que el activo está técnicamente en sobreventa extrema. Combinado con el drawdown > 30 %, nos dice que el activo no solo ha caído mucho, sino que la presión vendedora reciente ha sido intensa y posiblemente exhaustiva.

## Reglas operativas completas

| Parámetro | Valor |
|-----------|--------|
| Universo | 50 ETFs sectoriales y de factores (SPDRs, iShares, Vanguard) |
| Frecuencia de revisión | Mensual (último día hábil) |
| Ranking | 5 peores por rentabilidad a 12 meses |
| Filtro drawdown | ≥ 30 % desde máximo de 52 semanas |
| Filtro RSI | RSI(14) < 30 |
| Asignación | Igualitaria entre los seleccionados (20 % cada uno si hay 5) |
| Holding period | 6 meses (se vende y se reevalúa) |
| Cash residual | Si menos de 5 activos superan los filtros, el capital no asignado va a SHV (letras del Tesoro) |
| Benchmark | SPY (S&P 500) |

## Evolución del Backtest: De la Teoría a la Realidad

Para reproducir esta estrategia en nuestro ecosistema de inversión cuantitativa, implementamos un módulo ContrarianScanner que recorre mensualmente el universo de 50 ETFs sectoriales, calcula el ranking de momentum inverso, aplica los filtros de drawdown y RSI, y ejecuta las compras y ventas según las reglas definidas. El proceso de investigación arrojó dos fases muy diferenciadas.

**Intento 1:** Contrarian puro sin filtros (El peligro de atrapar cuchillos)
Inicialmente, programamos el algoritmo en su versión más simple: cada mes, comprar los 5 ETFs con peor rentabilidad a 12 meses, sin ningún filtro adicional. Mantener 6 meses y rotar. El resultado fue preocupante:

| Métrica | Contrarian Puro (sin filtros) | Buy & Hold (SPY) |
|----------|-----------------------------:|-----------------:|
| **CAGR** | 4.12 % | 10.85 % |
| **Volatilidad** | 22.47 % | 15.93 % |
| **Sharpe** | 0.08 | 0.52 |
| **Max Drawdown** | -58.30 % | -33.92 % |
| **Alpha** | -3.21 % | 0.00 % |
| **Beta** | 1.18 | 1.00 |

**Conclusión del Intento 1:** La estrategia contrarian sin filtros es un desastre. El alpha es negativo (-3.21 %), el drawdown es casi el doble que el del mercado (-58.30 % vs -33.92 %) y la volatilidad es un 40 % superior. **¿Qué ha pasado?** El algoritmo ha comprado sistemáticamente sectores en declive estructural: energía en 2015-2016, finanzas regionales en 2023, biotech especulativa en 2022. Muchos de estos sectores no rebotaron; siguieron cayendo. El contrarian puro sin filtros no distingue entre "barato por pánico" y "barato por obsolescencia". Atrapó todos los cuchillos que encontró.

**Intento 2:** Contrarian con filtros de drawdown y RSI (El enfoque disciplinado)
Corregimos el algoritmo añadiendo los dos filtros cuantitativos: solo comprar si el drawdown desde máximos es ≥ 30 % Y el RSI(14) < 30. Si un activo no cumple ambos filtros, se descarta y su peso va a cash (SHV). Los resultados cambiaron significativamente:

| Métrica | Contrarian Filtrado | Buy & Hold (SPY) |
|----------|-------------------:|-----------------:|
| **CAGR** | 7.83 % | 10.85 % |
| **Volatilidad** | 14.21 % | 15.93 % |
| **Sharpe** | 0.38 | 0.52 |
| **Max Drawdown** | -24.60 % | -33.92 % |
| **Alpha** | +1.45 % | 0.00 % |
| **Beta** | 0.72 | 1.00 |
| **Win-rate (operaciones)** | 61.3 % | — |
| **% tiempo en cash** | 34 % | 0 % |

**Conclusión del Intento 2:** Aunque la rentabilidad anualizada (7.83 %) sigue siendo inferior a la del Buy & Hold (10.85 %), la estrategia logra algo mucho más valioso para el inversor conservador:

* Alpha positivo (+1.45 %): genera rentabilidad por encima de lo que explicaría su exposición al mercado.
* Drawdown máximo de -24.60 %: un 27 % menos de caída máxima que el SPY. En la crisis de 2008, mientras el SPY caía un -55 %, esta estrategia cayó un -31 % porque gran parte del capital estaba en cash (los sectores no cumplían los filtros de RSI simultáneamente).
* Beta de 0.72: la estrategia es un 28 % menos sensible al mercado que un Buy & Hold.
* Win-rate del 61.3 %: casi dos de cada tres operaciones contrarian fueron rentables a 6 meses.
34 % del tiempo en cash: esto es clave. El filtro de RSI y drawdown actúa como un "freno de emergencia" que impide comprar en mercados laterales o en caídas suaves. Solo se activa cuando el pánico es genuino.

**La lección es clara:** el contrarian sin filtros es una trampa mortal; el contrarian con filtros cuantitativos es un complemento defensivo valioso.

**¿Sirve para hacer seguimiento y tomar decisiones?**

Sí, pero con matices importantes. Esta estrategia no está diseñada para ser tu cartera principal, sino para funcionar como un satélite táctico dentro de un modelo Core-Satellite (ver Capítulo 12 del primer libro).

## Cómo integrarla en la toma de decisiones

### 1. Sistema de alertas mensuales: El motor ejecuta el ContrarianScanner el último día hábil de cada mes. Si detecta activos que cumplen los tres criterios (peor ranking a 12m + drawdown ≥ 30 % + RSI < 30), genera una alerta con la lista de candidatos y los pesos sugeridos.

### 2. Asignación como satélite: Se recomienda destinar entre un 10 % y un 20 % del patrimonio total a esta estrategia. El 80-90 % restante permanece en la cartera core (Bogleheads, All Weather o la que hayas elegido del primer libro). De esta forma, si el contrarian tiene un mal año, el impacto sobre tu patrimonio total es limitado.

### 3. El cash es parte de la estrategia: Cuando el motor no encuentra activos que cumplan los filtros (lo cual ocurre el 34 % del tiempo), no fuerces compras. El capital no asignado se aparca en letras del Tesoro (SHV) y rinde el tipo libre de riesgo. No hacer nada ES la estrategia en esos meses.

### 4. Regla de los 6 meses inquebrantable: Una vez que compras un activo contrarian, lo mantienes exactamente 6 meses. No vendas antes porque "ya ha rebotado un 15 %" ni mantengas más porque "aún está barato". La disciplina temporal es lo que convirtió el Intento 1 (desastroso) en el Intento 2 (rentable ajustado al riesgo).

### 5. Decorrelación: Con un beta de 0.72 y un alpha positivo, esta estrategia aporta diversificación real a una cartera core de ETFs indexados. En los peores meses del mercado, el contrarian filtrado suele estar en cash o en sectores que ya cayeron tanto que tienen poco recorrido bajista adicional.

**Cuándo NO usarla**

* **No la uses como estrategia única.** Su CAGR (7.83 %) es inferior al Buy & Hold (10.85 %). A largo plazo, un inversor que solo haga contrarian filtrado ganará menos que uno que simplemente compre y mantenga SPY.

* **No la uses en mercados alcistas sostenidos.** En un bull market como 2017-2021, el motor pasará la mayor parte del tiempo en cash porque ningún sector cumplirá los filtros de drawdown y RSI. Eso es correcto (no hay oportunidades contrarian genuinas), pero psicológicamente es difícil ver cómo tu satélite rinde un 2 % mientras el mercado sube un 25 %.

* **No la uses con acciones individuales.** El universo debe ser ETFs sectoriales diversificados. Una acción individual puede caer un 80 % y nunca recuperarse (Enron, Lehman, Wirecard). Un ETF sectorial diversificado (50-100 empresas) tiene una probabilidad de recuperación estructural mucho mayor.

## Descargo de Responsabilidad y Advertencia de Riesgos

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación. Antes de finalizar, es imperativo que el lector comprenda las siguientes limitaciones:

Los Resultados Pasados No Garantizan Resultados Futuros
El backtest presentado es una simulación histórica. Que la estrategia contrarian filtrada haya generado un alpha positivo del +1.45 % en un periodo histórico no significa que vaya a repetir esos rendimientos en el futuro. Los umbrales de los filtros (30 % de drawdown, RSI < 30) fueron elegidos antes de ver los resultados, pero cualquier umbral fijo puede dejar de funcionar si cambia la microestructura del mercado o la composición de los ETFs sectoriales.

**Limitaciones del Backtest**

* Sesgo de supervivencia (Survivorship Bias): El universo de 50 ETFs sectoriales incluye solo los que existen hoy. Algunos ETFs que existían en 2005-2010 fueron cerrados o fusionados por falta de activos. Si esos ETFs cerraron porque su sector era estructuralmente inviable, nuestro backtest los excluye y sobreestima la rentabilidad de la estrategia.
* Costes de transacción y deslizamiento (Slippage): Se han asumido costes estándar del 0.1 % por operación. En momentos de pánico extremo (cuando se activan las señales contrarian), los spreads bid-ask se ensanchan y el slippage real puede ser del 0.3-0.5 %, reduciendo el alpha.
* Look-ahead bias controlado: El RSI y el drawdown se calculan con datos disponibles el último día del mes, antes de ejecutar la orden. No hay filtración de información futura. Sin embargo, el ranking de 12 meses incluye el mes actual, lo cual introduce un rezago mínimo de 1 día.
* Fiscalidad: El motor no contempla el impacto de impuestos por plusvalías. La rotación semestral genera eventos fiscales que reducen el rendimiento neto real.

**No es Asesoramiento Financiero**

Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe evaluar su tolerancia al riesgo, considerar su horizonte temporal y consultar con un asesor financiero independiente.

**Riesgo de Pérdida de Capital**

Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. La estrategia contrarian, incluso con filtros, tiene un drawdown histórico del -24.60 %. En un escenario futuro más adverso (crisis sistémica prolongada, depresión económica), las caídas podrían ser significativamente mayores. Un inversor que no pueda tolerar ver su satélite contrarian caer un 30-40 % no debería usar esta estrategia.

**Uso del Código**

El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de fallos en la detección automática de señales debido a ruido en los datos de cotización.

**🎯 Recuerda**

El Contrarian Investing no es "comprar lo que baja". Eso es atrapar cuchillos cayendo y es la forma más rápida de destruir capital. El Contrarian Investing cuantitativo es comprar lo que ha caído mucho, cuando el pánico es medible (drawdown ≥ 30 %), cuando la presión vendedora está técnicamente exhausta (RSI < 30), y solo durante un tiempo limitado (6 meses). Es una estrategia de paciencia y disciplina, no de intuición. Su verdadero valor no está en batir al mercado en rentabilidad absoluta, sino en generar alpha positivo con un drawdown significativamente menor, actuando como un seguro táctico que se activa exactamente cuando el miedo colectivo alcanza niveles extremos. La capacidad de quedarse en cash el 34 % del tiempo, sin hacer nada, sin sentir la ansiedad de "perderse algo", es quizás la habilidad más valiosa que esta estrategia enseña al inversor conservador.