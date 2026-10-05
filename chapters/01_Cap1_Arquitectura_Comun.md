# Capítulo 1 — Arquitectura Común: el motor invisible (ampliado)

    "Las estrategias cambian, pero el motor que las evalúa debe seguir siendo el mismo. Solo así podemos comparar manzanas con manzanas."

Antes de entrar a analizar las estrategias no convencionales de este libro (contrarian investing, pairs trading, Fibonacci moving averages, tail risk hedging, etc.), es fundamental entender cómo vamos a evaluarlas. En el primer libro construimos un "motor común" para las estrategias ortodoxas. En este segundo libro, ese motor se amplía con cinco nuevos departamentos especializados para abordar la complejidad de las estrategias no convencionales, sin perder la coherencia del sistema original.

Para entenderlo sin necesidad de saber programar, retomemos la metáfora del primer libro: imagina una fábrica moderna. Tú (el inversor) eres el director de la fábrica. Tú decides qué producto se va a fabricar (la estrategia de inversión). Sin embargo, no tienes que ir a la máquina de tornillos, ni a la de pintura, ni a la de empaquetado; simplemente le das a un botón y la cadena de montaje hace el resto.

En el primer libro, la cadena de montaje tenía cinco departamentos. En este segundo libro, la fábrica crece: añadimos cinco nuevos departamentos especializados que trabajan en equipo con los originales. Este es el organigrama completo.

## Los 5 departamentos originales (reutilizados)

Estos son los mismos que ya conoces del primer libro. Los mencionamos brevemente para que el lector nuevo entienda el contexto, y para que el lector veterano recuerde la base sobre la que se construye todo lo demás.

### 1. El Archivista: Gestor de Datos
Todo análisis comienza con datos fiables. Este departamento se encarga de conectarse a las fuentes financieras (Yahoo Finance, FRED, CBOE), descargar el historial de precios de los activos, limpiarlos de errores y guardarlos de forma ordenada. Es el cimiento sobre el que se construye todo lo demás.

## 2. El Estratega: Optimizador de Carteras

El cerebro matemático. Una vez que sabemos qué activos queremos en nuestra cartera, este departamento calcula cómo repartir el dinero. En el primer libro hacía asignaciones estáticas, paridad de riesgo o mínima varianza. En este segundo libro, además, es capaz de ejecutar asignaciones dinámicas basadas en señales (miedo/codicia, cointegración, fractales, regímenes de volatilidad).

## 3. La Máquina del Tiempo: Motor de Backtest

Aquí ocurre la verdadera magia. Un backtest es una simulación histórica: este motor toma las decisiones del Estratega y las aplica sobre los precios reales del pasado. Simula día a día, mes a mes, cómo habría evolucionado tu cartera, calcula comisiones, reinvierte dividendos y aplica los rebalanceos. Al final, devuelve una línea temporal mostrando cómo habría crecido tu dinero.

## 4. El Auditor: Calculador de Métricas

Tener una línea temporal no es suficiente. El Auditor calcula indicadores estandarizados de riesgo y rentabilidad: Rentabilidad Anualizada (CAGR), Volatilidad, Máximo Drawdown, Ratio Sharpe, Sortino, Calmar, VaR y CVaR. En este segundo libro, el Auditor se amplía con métricas específicas para estrategias no convencionales: win-rate, profit factor, Information Ratio, ratio de cobertura del hedge, coste anual del seguro de cola.

## 5. El Editor: Generador de Informes

Toma los números del Auditor y los traduce a un lenguaje visual y comprensible. Genera gráficos de evolución, tablas de comparación y el diagnóstico final. En este segundo libro, el Editor añade dashboards específicos: semáforos de viabilidad, rankings de activos contrarian, mapas de calor de cointegración y reportes de señales de indicadores no convencionales.

## Los 5 nuevos departamentos (exclusivos de este libro)

Las estrategias no convencionales requieren herramientas que el motor original no tenía. Estos cinco nuevos departamentos se añaden a la fábrica para abordar la nueva complejidad.

### 6. El Termómetro: Gestor de Señales Binarias (Miedo/Codicia)

Muchas estrategias de este libro (Fear & Greed Index, Contrarian Investing, Tail Risk Hedging) necesitan saber en qué estado emocional está el mercado. Este departamento construye índices propietarios de sentimiento agregando múltiples señales normalizadas:

* VIX (volatilidad implícita)
* Put/Call ratio de CBOE
* % de miembros del SPY por debajo de su SMA-200
* Spread de bonos high-yield sobre Tesoro
* Flujo neto de fondos monetarios*

El Termómetro devuelve un valor entre 0 y 100 que clasifica el mercado en cinco regímenes: miedo extremo (0-20), miedo (20-40), neutral (40-60), codicia (60-80), codicia extrema (80-100). Las estrategias tácticas usan este termómetro como disparador de entradas y salidas.

### 7. El Gemelólogo: Calculador de Cointegración

Estrategias como Pairs Trading o Statistical Arbitrage necesitan saber si dos activos están matemáticamente unidos (cointegrados) o si su correlación es casual. Este departamento ejecuta el test de Engle-Granger, calcula el spread logarítmico entre pares y genera z-scores sobre ventanas móviles de 60 días.

**Regla de oro del Gemelólogo:** si dos activos no superan el test de cointegración con un p-valor < 0.05, el motor aborta la simulación y muestra una advertencia. No se hace pairs trading con activos que no están cointegrados, aunque hayan estado correlacionados en el pasado. Esta es una de las protecciones más importantes del motor frente a estrategias que parecen funcionar en el backtest pero fracasan en la realidad.

## 8. El Cronista: Tracker de Eventos

Estrategias basadas en eventos (Merger Arbitrage, Earnings Surprise, Insider Trading legal) necesitan saber cuándo ocurren cosas en las empresas. Este departamento mantiene un calendario de:

* Fechas de resultados trimestrales (earnings)
* Anuncios de OPAs y M&A
* Compras de directivos (Form 4 de la SEC)
* Ex-dividend dates
* Halvings de Bitcoin

El Cronista no puede predecir eventos, pero sí alertar cuando se acercan y permitir que el motor simule cómo se habría comportado la cartera en ventanas pre/post evento. Para los eventos no cotizados directamente (Form 4, OPAs), el motor usa proxies ETF (ej. XBI para biotech, KBE para bancos regionales) y documenta honestamente la limitación.

### 9. El Actuario: Simulador de Opciones

Estrategias como Tail Risk Hedging, Volatility Arbitrage o Butterfly Spreads requieren entender derivados. Este departamento calcula:

* Payoff diagrams al vencimiento (gráficos de beneficio/pérdida)
* Griegas (Delta, Gamma, Theta, Vega)
* Probabilidades teóricas usando la distribución log-normal
* Coste anual del "seguro" de cola (puts OTM -5% delta)*

**Limitación honesta:** el Actuario no puede simular P&L histórico completo de opciones porque Yahoo Finance no provee histórico de cadenas de opciones. Lo que sí hace es documentar la mecánica, calcular el coste teórico del hedge y mostrar en qué crisis históricas el hedge habría compensado las primas perdidas.

### 10. El Observatorio: Biblioteca de Indicadores No Convencionales

El Bloque VIII del libro introduce diez indicadores técnicos no convencionales que no aparecen en el primer libro. El Observatorio los implementa todos como funciones modulares reutilizables:

Markdown
| Indicador | Función en el motor |
|------------|---------------------|
| Fibonacci Moving Averages | EMAs en niveles 21, 34, 55, 89, 144 y 233 |
| Bollinger Bands Alternativas | Media triangular de Wilder, 2.5σ |
| Augmented Bollinger Bands | Ajustadas por volatilidad condicional GARCH(1,1) |
| Stochastic RSI | RSI aplicado dos veces (KDJ-like) |
| Dynamic RSI | Ventana adaptativa vía transformada de Hilbert |
| Stochastic Oscillators | %K/%L clásicos de Wilder (14,3,3) |
| Fractal Indicator | Fractales de Williams de 5 barras |
| Volatility Range Indicators | Choppiness Index, Keltner Squeeze y Pure Range Volatility |
| Contrarian Indicators Agregados | Índice Contrarian Compuesto (CCI) de 5 señales |
| Moving Average Contrarian | Cruce inverso EMA-50/EMA-200 con filtro de drawdown |

El Observatorio no usa estos indicadores como señales únicas de entrada (eso sería irresponsable). Los ofrece como capas de confirmación que las estrategias de los bloques anteriores pueden activar opcionalmente. El motor permite combinarlas en un dashboard unificado (Capítulo 33) que genera un semáforo final contrarian por activo.

## La gran novedad: el semáforo de viabilidad

El primer libro evaluaba todas las estrategias con las mismas reglas. El segundo libro introduce una capa adicional de honestidad: el semáforo de viabilidad. Antes de ejecutar cualquier estrategia, el motor te dice qué puede y qué no puede hacer con ella.

### ¿Qué evalúa el semáforo?

Cuatro preguntas clave para cada capítulo:

| Pregunta | Significado |
|-----------|-------------|
| ¿Es backtesteable con Yahoo Finance? | ¿Puedo simularlo con datos gratuitos? |
| ¿Requiere datos alternativos? | ¿Necesito CBOE, SEC EDGAR, FRED, datos on-chain u otras fuentes especializadas? |
| ¿Requiere ejecución en tiempo real? | ¿Es solo para HFT o también para swing trading? |
| ¿Es apto para inversor minorista? | ¿Puedo ejecutarlo con un bróker retail? |

Los tres colores

    🟢 Verde: totalmente backtesteable y ejecutable por un inversor minorista con datos gratuitos.
    🟡 Ámbar: backtesteable parcialmente, o requiere datos/infraestructura adicional que el motor provee mediante proxies.
    🔴 Rojo: solo documentable; el motor explica la mecánica pero no simula P&L histórico completo.

Ejemplos de semáforo en este libro

| Capítulo | Estrategia | Semáforo | Motivo |
|-----------|------------|:---------:|---------|
| Cap. 2 | Contrarian Investing | 🟢 | ETFs sectoriales en Yahoo Finance |
| Cap. 5 | Pairs Trading | 🟢 | Pares clásicos cotizados |
| Cap. 7 | Algorithmic Trading con IA/ML | 🟡 | Requiere walk-forward validation exhaustiva |
| Cap. 14 | Tail Risk Hedging | 🟡 | Proxy con SVOL/VIX calls, no opciones reales |
| Cap. 22 | Credit Default Swaps | 🔴 | Requiere contrapartida OTC, no replicable |
| Cap. 23 | Crypto Yield Farming | 🔴 | Requiere datos on-chain, fuera del scope |

El semáforo aparece al inicio de cada capítulo y en la cabecera de cada notebook. Evita frustraciones: el lector sabe antes de abrir el Notebook qué puede esperar.

### El flujo de trabajo ampliado

Cada vez que leamos una estrategia en los siguientes capítulos, detrás de ella estará ocurriendo esto:

GestorDatos → Limpia el escenario
     ↓
OptimizadorCarteras → Decide los pesos (estáticos o dinámicos según señales)
     ↓
[Termómetro] → Mide miedo/codicia (si la estrategia lo requiere)
     ↓
[Gemelólogo] → Valida cointegración (si es pairs trading)
     ↓
[Cronista] → Alinea con calendario de eventos (si es event-driven)
     ↓
[Observatorio] → Aplica indicadores no convencionales (si es Bloque VIII)
     ↓
MotorBacktest → Simula el pasado
     ↓
[Actuario] → Calcula payoff de opciones (si es estrategia de derivados)
     ↓
CalculadorMetricas → Evalúa el riesgo (métricas estándar + específicas)
     ↓
GeneradorInformes → Te entrega el diagnóstico + semáforo de viabilidad

Los departamentos entre corchetes [...] son los nuevos módulos que solo se activan cuando la estrategia los necesita. El motor es modular: no carga peso innecesario en estrategias simples, pero despliega toda la artillería cuando la estrategia lo requiere.

## Detrás del telón: la robustez de los datos (ampliada)

En el mundo cuantitativo, "basura entra, basura sale". El pipeline de depuración automática del primer libro se mantiene y se amplía con nuevas validaciones:

Detección de huecos temporales en series de Yahoo Finance.
Normalización de formatos al importar extractos bancarios o datos de FRED.
Validación de cointegración antes de ejecutar pairs trading (si dos activos no están cointegrados, el motor aborta).
Validación de estacionariedad en series de spreads para arbitraje estadístico.
Control de supervivencia (survivorship bias): el motor documenta cuándo un universo de activos sufre este sesgo.
Control de look-ahead bias en estrategias con señales técnicas (los indicadores se calculan solo con datos disponibles en el momento de la decisión).
Ajuste por dividends y splits en todas las series de precios.

Al final de cada ejecución, el sistema muestra un "Informe de Limpieza" que garantiza la calidad de los datos. No hay simulaciones sobre datos sucios.
Cómo usar este motor ampliado
El flujo de trabajo recomendado para cada capítulo es:

    Lee la teoría y el semáforo: comprende la filosofía de la estrategia y verifica si el motor puede simularla completamente (🟢), parcialmente (🟡) o solo documentarla (🔴).
    Ejecuta el motor: abre el Notebook del capítulo y pulsa "Play". El motor activará los departamentos necesarios (Termómetro, Gemelólogo, Cronista, Observatorio, Actuario) según la estrategia.
    Analiza el diagnóstico: el sistema entrega métricas estándar (CAGR, Sharpe, Drawdown) acompañadas de métricas específicas (win-rate, Information Ratio, coste del hedge) y un diagnóstico cualitativo automático.
    Revisa el seguimiento actual: el sistema lee tu cartera y te indica si ha derivado de su objetivo, sugiriendo ajustes respetando costes de transacción y fiscalidad.
    Consulta el dashboard de indicadores (Bloque VIII): para estrategias basadas en indicadores no convencionales, el motor genera un ranking semanal de los activos más "contrarian" del momento.

En resumen
Este segundo libro no reemplaza al primero: lo amplía. El motor común se convierte en un ecosistema modular capaz de evaluar desde la clásica 60/40 hasta el tail risk hedging con opciones de cola, pasando por pairs trading cointegrado y estrategias contrarian basadas en Fibonacci moving averages.
La filosofía sigue siendo la misma: no predecir el futuro, sino prepararse matemáticamente para él. Pero ahora, con herramientas que reconocen que el mercado no siempre es racional, que las correlaciones no siempre son estables, y que a veces la mejor defensa es salirse del guion ortodoxo con reglas frías y cuantitativas.
Con esta arquitectura común funcionando de fondo —ampliada con los cinco nuevos departamentos y el semáforo de viabilidad—, podemos dedicar el resto del libro a lo que realmente importa: entender la lógica de cada estrategia no convencional y decidir cuál se adapta mejor a nuestros objetivos, siempre con los ojos abiertos sobre lo que el motor puede y no puede simular.
Aviso legal
Las herramientas, códigos y simulaciones presentadas en este capítulo y en todo el libro tienen fines exclusivamente educativos y de investigación cuantitativa. No constituyen asesoramiento financiero ni recomendación de inversión. El rendimiento pasado no garantiza resultados futuros.
Advertencia específica para este segundo libro: muchas de las estrategias aquí presentadas son de alto riesgo, requieren capital elevado, conocimientos avanzados o infraestructura profesional. Algunas operan con apalancamiento, derivados o activos ilíquidos. El lector debe entender que las pérdidas pueden superar el capital invertido en ciertos escenarios. Consulta siempre con un asesor financiero cualificado antes de ejecutar cualquier estrategia real, y nunca inviertas dinero que no puedas permitirte perder.
El semáforo de viabilidad es una guía, no una garantía. Que el motor pueda simular una estrategia no significa que sea adecuada para tu perfil de riesgo, tu horizonte temporal o tu situación fiscal.