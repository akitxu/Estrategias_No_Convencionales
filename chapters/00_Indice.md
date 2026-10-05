# Índice del Libro: Estrategias No Convencionales de Inversión Cuantitativa
## Prefacio — Cuando la ortodoxia no basta

Por qué este libro existe, para quién está escrito y cuándo tiene sentido salirse del guion. El inversor conservador no busca adrenalina, busca herramientas adicionales para blindar su patrimonio, capturar ineficiencias o cubrir riesgos que las estrategias clásicas (60/40, All Weather, Bogleheads) no pueden gestionar. Advertencia de honestidad intelectual: muchas de estas estrategias son de alto riesgo, requieren capital elevado o infraestructura profesional. Las marcaremos con un semáforo de viabilidad en el motor cuantitativo.

## Capítulo 1 — Arquitectura Común: el motor invisible (reutilizado) 
El mismo sistema de backtest, limpieza de datos y diagnóstico de riesgo del libro anterior, ahora extendido con nuevos módulos: gestor de señales binarias (miedo/codicia), calculador de cointegración, tracker de eventos y simulador de opciones. Todas las estrategias del libro se evalúan con las mismas reglas, aunque algunas requieran adaptaciones específicas que se documentan en cada capítulo.
Semáforo: 🟢 Totalmente backtesteable.

## BLOQUE I · Comportamiento y Psicología de Masas

El mercado no es racional: es humano. Aquí explotamos los sesgos cognitivos colectivos (pánico, euforia, anclaje) con reglas cuantitativas que sustituyen a la intuición.

### Capítulo 2 — Contrarian Investing: comprar cuando nadie quiere

En la práctica: se construye un ranking mensual de los 50 ETFs sectoriales y de factores (SPDRs, iShares) ordenados por rentabilidad a 12 meses. Se compran a partes iguales los 5 con peor rendimiento (los "perdedores") siempre que su precio esté al menos un 30% por debajo de su máximo histórico y su RSI(14) esté por debajo de 30. Se mantiene la posición 6 meses y se rota. El motor cuantitativo simula esta estrategia desde 2000 y compara su drawdown contra un simple Buy & Hold en SPY, demostrando empíricamente cuándo la reversión a la media premia al contrarian y cuándo solo atrapa "cuchillos cayendo".
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 3 — Momentum Crash: apostar contra la euforia

En la práctica: se monitoriza la rentabilidad a 3 meses del S&P 500 (SPY). Si supera el +20% sin una corrección intermedia del 5%, el sistema considera que el momentum está "sobrecalentado" y rota un 50% de la cartera a cash (SHV o BIL). Se vuelve a entrar solo cuando el precio vuelve a tocar la SMA de 50 sesiones. El motor cuantitativo calcula cuántas veces se activó la señal desde 1993 y qué rentabilidad habría generado evitar los crashes posteriores (Dotcom, 2008, 2020 marzo).
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 4 — Fear & Greed Index como temporizador táctico

En la práctica: se construye un índice propietario de sentimiento agregando 5 señales normalizadas: VIX (peso 25%), put/call ratio (20%), flujo de fondos monetarios (20%), dispersión de acciones sobre su SMA200 (20%) y bonos basura vs. Tesoro (15%). Cuando el índice cae por debajo de 20 (miedo extremo), se despliega un 20% adicional en RV global (VT). Cuando supera 80 (codicia extrema), se reduce la exposición a RV al mínimo histórico. El motor cuantitativo demuestra si este "termómetro" añade valor frente a un rebalanceo ciego.
Semáforo: 🟢 Totalmente backtesteable (con proxies de Yahoo Finance).

## BLOQUE II · Cuantitativas y Arbitraje Estadístico

Aquí dejamos de mirar al mercado como un todo y empezamos a mirar las relaciones matemáticas entre activos. El objetivo: rentabilidad descorrelada del mercado (alpha puro).

### Capítulo 5 — Pairs Trading: la danza de los correlacionados
En la práctica: se toma un universo de pares clásicos (KO/PEP, XOM/CVX, BAC/JPM, GOLD/NEM). Cada día se calcula el spread logarítmico entre ambos y su z-score sobre una ventana de 60 días. Cuando el z-score supera +2, se vende el caro y se compra el barato en proporción 1:1 en notional. Se cierra la posición cuando el z-score vuelve a 0 o cuando supera +3 (stop-loss por ruptura estructural). El motor cuantitativo ejecuta el test de Engle-Granger para validar la cointegración y muestra cuántas operaciones, win-rate y Sharpe genera cada par desde 2010.
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 6 — Statistical Arbitrage: ETFs vs. sus subyacentes

En la práctica: se monitoriza la divergencia entre un ETF (ej. GLD) y su subyacente (futuros de oro GC, o IAU como proxy). Cuando el descuento/premium supera 2 desviaciones estándar de su media de 30 días, se ejecuta la operación inversa esperando la convergencia. El motor cuantitativo simula esta estrategia midiendo el coste de transacción real y demostrando si el edge sobrevive después de comisiones y slippage.
Semáforo: 🟡 Parcialmente backtesteable (requiere datos de NAV intradía para precisión óptima).

### Capítulo 7 — Algorithmic Trading con IA/ML: el límite del motor

En la práctica: se entrena un modelo Random Forest con 30 features técnicos (RSI, MACD, volatilidad realizada, volumen relativo, etc.) para predecir la dirección del SPY a 5 días. Se usa walk-forward validation (entreno 5 años, test 1 año, rolling). El motor cuantitativo incluye un módulo experimental que genera la curva de equity del modelo versus SPY y calcula el Information Ratio. Advertencia de honestidad: este capítulo documenta por qué la mayoría de modelos de ML fallan fuera de muestra y qué overfitting traps evitar. No es una estrategia para ejecutar en real sin validación exhaustiva.
Semáforo:  Totalmente backtesteable (con validación walk-forward obligatoria).

## BLOQUE III · Estrategias Basadas en Eventos

Los eventos corporativos crean ineficiencias temporales medibles. Aquí cuantificamos lo que los analistas fundamentales hacen a mano.

### Capítulo 8 — Event-Driven: Merger Arbitrage con ETFs
En la práctica: dado que el motor no puede procesar OPAs en tiempo real, se construye un proxy: se monitorizan los ETFs de sectores que históricamente han sido objetivo de consolidación (biotech XBI, bancos regionales KBE). Cuando el sector cae más de un 25% desde máximos con volumen 2x la media, se interpreta como "descuento por miedo a M&A fallido" y se entra. Se sale a los 6 meses o al recuperar el 50% de la caída. El motor cuantitativo backtestea esta aproximación indirecta y compara contra Buy & Hold.
Semáforo: 🟡 Parcialmente backtesteable (proxy indirecto, no merger arbitrage puro).

### Capítulo 9 — Earnings Surprise: el efecto post-anuncio
En la práctica: se seleccionan 20 empresas del S&P 100 con historial de superar consenso en los últimos 8 trimestres (usando datos simulados o proxy de momentum fundamental). El sistema compra 10 días antes de la fecha de resultados estimada y mantiene 5 días después del anuncio. El motor cuantitativo mide el "earnings drift" histórico y calcula si la estrategia genera alpha real después de comisiones.
Semáforo: 🟡 Parcialmente backtesteable (requiere datos de earnings dates externos).

### Capítulo 10 — Insider Trading Legal: siguiendo al Form 4

En la práctica: se construye un proxy usando datos de compras agregadas de directivos (cuando están disponibles) o, en su defecto, se usa el ratio de recompras de acciones (buyback yield) como señal de confianza del management. Se compran a partes iguales las 20 empresas del S&P 500 con mayor buyback yield trimestral, siempre que su PER esté por debajo de la media del sector. Rebalanceo trimestral. El motor cuantitativo backtestea esta aproximación y compara contra un igual-weighted S&P 500.
Semáforo:  Parcialmente backtesteable (proxy con buyback yield, no Form 4 real).

## BLOQUE IV · Macro y Globales

Aquí el horizonte se amplía a divisas, tipos de interés y commodities. El inversor deja de mirar empresas y empieza a mirar países.

### Capítulo 11 — Carry Trade: cobrar el diferencial de tipos
En la práctica: se construye una cartera larga en 3 divisas con tipos reales altos (MXN, BRL, INR) vía ETFs de mercado de divisas (UUP, EMB, INDA como proxy) y corta en divisas con tipos bajos (JPY, CHF) vía FXY. Se rebalancea mensualmente. Se aplica un filtro de salida: si el VIX supera 30, se cierra toda la posición y se aparca en USD (UUP). El motor cuantitativo simula la estrategia desde 2010 y mide los episodios de "carry unwind" (2015, 2020 marzo, 2024 agosto).
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 12 — Volatility Arbitrage: vender el miedo caro

En la práctica: se monitoriza la diferencia entre el VIX (volatilidad implícita) y la volatilidad realizada a 30 días del SPY. Cuando VIX supera en más de 5 puntos a la RV, se vende VXX (ETF de volatilidad) y se aparca en cash. Se vuelve a entrar cuando la diferencia se normaliza. Advertencia crítica: VXX tiene decaimiento estructural; el motor cuantitativo documenta este drag y calcula la rentabilidad real después de ajustar por roll cost.
Semáforo: 🟡 Parcialmente backtesteable (VXX tiene decay estructural complejo).

### Capítulo 13 — Global Macro: el estilo Soros
En la práctica: se construye un dashboard con 4 señales macro: (1) curva de tipos US (10Y-2Y), (2) PMI manufacturero global, (3) índice dólar (DXY), (4) precio del petróleo (USO). Según el régimen (expansión/recesión), se asigna dinámicamente entre 4 ETFs: RV global (VT), bonos largos (TLT), oro (GLD) y cash (SHY). Rebalanceo trimestral. El motor cuantitativo backtestea los 4 regímenes desde 2000 y muestra qué asignación habría ganado en cada ciclo.
Semáforo:  Totalmente backtesteable (con proxies de Yahoo Finance).

## BLOQUE V · Alternativas y Exóticas

Estrategias que no encajan en los buckets tradicionales. Algunas son defensivas (tail hedging), otras temáticas, otras de provisión de liquidez.

### Capítulo 14 — Tail Risk Hedging: el seguro de Nassim Taleb
En la práctica: se asigna un 3% anual del capital a comprar opciones put OTM (-5% delta) a 3 meses sobre SPY (proxy: comprar VIX calls o usar el ETF SVOL como aproximación liquidable). El 97% restante va a una cartera All Weather. El motor cuantitativo simula el coste anual del "seguro" y muestra en qué crisis (2008, 2020, 2022) el hedge generó rentabilidad positiva suficiente para compensar los años de primas perdidas.
Semáforo: 🟡 Parcialmente backtesteable (proxy con SVOL, no opciones reales).

### Capítulo 15 — Liquidity Provision: ser el mercado
En la práctica: dado que el market making tradicional requiere infraestructura HFT, se construye un proxy usando ETFs de baja volatilidad (SPLV) y se simula una estrategia de "mean reversion intramensual": comprar cuando el precio toca la banda inferior de Bollinger (20, 2) y vender en la media. El motor cuantitativo mide el Sharpe de esta aproximación versus Buy & Hold y documenta por qué la provisión de liquidez real requiere spreads y latencia que este motor no puede simular.
Semáforo: 🟡 Parcialmente backtesteable (proxy simplificado).

### Capítulo 16 — Thematic Investing: apostar a megatendencias

En la práctica: se construye una cartera con 5 ETFs temáticos (ARKK innovación, LIT litio, ICLN renovables, CIBR ciberseguridad, BOTZ robótica). Se asigna 20% a cada uno. Se rebalancea semestralmente. Se aplica un filtro de tendencia: si un ETF cotiza por debajo de su SMA200, se reduce su peso al 10% y el excedente va a cash. El motor cuantitativo backtestea la cartera temática versus SPY desde 2015 y documenta la volatilidad extrema de estas apuestas.
Semáforo: 🟢 Totalmente backtesteable.

### BLOQUE VI · Nicho y Tácticas Específicas

Estrategias de libro, tácticas fiscales, patrones estacionales. Pequeños edges que suman.
Capítulo 17 — Dividend Capture: cobrar y salir
En la práctica: se seleccionan 10 acciones del Dividend Aristocrats con ex-dividend date en los próximos 5 días. Se compran 2 días antes del ex-date y se venden 3 días después. El motor cuantitativo simula esta rotación durante 5 años y calcula si el dividendo cobrado compensa el dividend drop y las comisiones. Resultado típico: la estrategia apenas genera alpha después de fricciones.
Semáforo: 🟡 Parcialmente backtesteable (requiere datos de ex-dividend dates).

### Capítulo 18 — Short Selling con ETFs Inversos: apostar a la caída

En la práctica: se usa SQQQ (Nasdaq -3x) como cobertura táctica. Cuando el sistema de momentum del Capítulo 3 detecta sobrecalentamiento, se asigna un 15% a SQQQ durante un máximo de 20 días. El motor cuantitativo documenta el volatility drag del ETF apalancado y demuestra por qué esta táctica solo funciona en ventanas muy cortas.
Semáforo:  Totalmente backtesteable.

### Capítulo 19 — Tax-Loss Harvesting: la deducción silenciosa
En la práctica: cada trimestre, el motor identifica posiciones con pérdidas no realizadas superiores al 10%. Propone venderlas y reemplazarlas por un ETF correlacionado pero no idéntico (ej. SPY → VOO, o VT → ACWI) para evitar la wash sale rule. El motor cuantitativo calcula el beneficio fiscal estimado (según tramo del inversor) y el coste de tracking error del reemplazo.
Semáforo: 🟡 Parcialmente backtesteable (requiere datos fiscales personalizados).

### Capítulo 20 — Seasonal Strategies: el calendario como edge

En la práctica: se implementa "Sell in May and Go Away": el 1 de mayo se rota un 50% de la cartera de RV a bonos cortos (SHV). Se vuelve a entrar el 1 de noviembre. El motor cuantitativo backtestea esta regla desde 1990 y compara contra Buy & Hold, documentando si el edge estacional persiste en las últimas dos décadas.
Semáforo: 🟢 Totalmente backtesteable.

## BLOQUE VII · Alto Riesgo (Solo para Expertos)

⚠️ Estrategias que requieren conocimientos avanzados, capital elevado o infraestructura profesional. El motor cuantitativo las documenta pero no las backtestea automáticamente: el usuario debe validarlas manualmente.

### Capítulo 21 — Options Butterfly Spread: apostar al rango
En la práctica: se documenta la construcción de un butterfly con opciones del SPY: comprar 1 call ITM, vender 2 calls ATM, comprar 1 call OTM. Se calcula el punto muerto, el máximo beneficio y la probabilidad teórica de éxito usando la distribución log-normal. El motor cuantitativo incluye un módulo educativo que grafica el payoff al vencimiento, pero no simula P&L histórico (requeriría datos de opciones completos, fuera del scope de Yahoo Finance).
Semáforo: 🔴 Solo documentable (requiere datos de opciones).

### Capítulo 22 — Credit Default Swaps: asegurar deuda
En la práctica: se explica la mecánica de los CDS usando como proxy los ETFs de bonos high-yield (HYG, JNK). Cuando el spread de HYG sobre Tesoro supera 600 pb, se interpreta como "seguro caro" y se vende protección (proxy: vender HYG). El motor cuantitativo backtestea esta aproximación indirecta y documenta por qué un CDS real requiere contrapartida OTC y no es replicable con ETFs.
Semáforo: 🟡 Parcialmente backtesteable (proxy con HYG, no CDS real).

### Capítulo 23 — Crypto Yield Farming: el nuevo carry trade

En la práctica: se documenta la mecánica de depositar criptomonedas en protocolos DeFi (Aave, Compound) para ganar yield. Se construye un proxy usando BTC-USD y ETH-USD de Yahoo Finance y se simula una estrategia de "hold + rebalanceo trimestral" versus stablecoins. El motor cuantitativo no puede simular yield farming real (requiere datos on-chain), pero documenta el impermanent loss, el smart contract risk y el histórico de rug pulls.
Semáforo: 🔴 Solo documentable (requiere datos on-chain).

## BLOQUE VIII · Indicadores Técnicos No Convencionales y Patrones Cuantitativos

Aquí se amplía el motor con indicadores técnicos avanzados que no aparecen en el libro original. Todos son codificables con datos OHLCV de Yahoo Finance y backtesteables en el motor. Se presentan como capas de confirmación sobre las estrategias de los bloques anteriores, nunca como señales únicas de entrada.

### Capítulo 24 — Fibonacci Moving Averages: la sucesión como soporte dinámico
En la práctica: se construyen medias móviles exponenciales en los niveles de la sucesión de Fibonacci (21, 34, 55, 89, 144 y 233 sesiones) sobre el activo objetivo. El sistema considera "zona de acumulación contrarian" cuando el precio toca la EMA-144 con RSI(14) < 30 simultáneamente. Se backtestea desde 2000 comparando contra la SMA-200 clásica en términos de drawdown máximo, Sharpe ratio y número de señales falsas.
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 25 — Bollinger Bands Alternativas y Aumentadas
En la práctica: se comparan tres variantes sobre el mismo activo: (1) Bollinger clásicas (SMA-20, 2σ), (2) Alternative BB con media triangular de Wilder y 2.5σ, (3) Augmented BB ajustadas por volatilidad condicional GARCH(1,1). El motor genera un ranking empírico de cuál variante captura mejor las reversiones a la media en cada régimen de mercado (tendencia alcista, lateral, bajista). Se mide el porcentaje de veces que el precio toca la banda externa y revierte dentro de 5 sesiones.
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 26 — Stochastic RSI: el oscilador del oscilador

En la práctica: se calcula el RSI(14) y luego se aplica el estocástico sobre el propio RSI con ventana de 14 sesiones. Se considera sobreventa extrema cuando Stoch-RSI < 10 y sobrecompra extrema cuando > 90. Se usa como filtro de confirmación para las estrategias contrarian de los Capítulos 2 y 4: solo se ejecuta la compra contrarian si Stoch-RSI está en sobreventa extrema Y el precio toca la banda inferior de Bollinger. El motor mide el win-rate de la confluencia frente a señales individuales.
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 27 — Dynamic RSI: el oscilador adaptativo

En la práctica: se implementa el RSI dinámico de John Ehlers con ventana adaptativa basada en el ciclo dominante del mercado (calculado mediante transformada de Hilbert). En mercados tendenciales la ventana se alarga (evita señales falsas); en mercados laterales se acorta (captura reversiones rápidas). Se backtestea comparando contra el RSI(14) fijo en términos de ratio señal/ruido y Sharpe ajustado por comisiones.
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 28 — Estocásticos Clásicos y Osciladores Combinados
En la práctica: se construye un "panel de sobrecompra/sobreventa" que agrega tres osciladores: (1) Stoch-RSI < 10, (2) RSI dinámico < 25, (3) %K estocástico clásico (14,3,3) < 20. Solo se considera señal contrarian válida cuando los tres coinciden simultáneamente. El motor cuantitativo mide el win-rate de esta confluencia triple frente a señales individuales y documenta la frecuencia de aparición (típicamente 3-5 veces al año por activo).
Semáforo:  Totalmente backtesteable.

### Capítulo 29 — Fractal Indicator de Williams: soportes y resistencias dinámicos

En la práctica: se detectan fractales de 5 barras (máximo local con 2 barras a cada lado más bajas, o mínimo local con 2 barras a cada lado más altas) según la definición original de Bill Williams. Los fractales alcistas se usan como niveles de stop-loss dinámico; los fractales bajistas como objetivos de toma de beneficios. Se integra como capa de confirmación en la estrategia de "Tortuga Coja" del Capítulo 8.5 del libro original.
Semáforo:  Totalmente backtesteable.

### Capítulo 30 — Indicadores de Rango de Volatilidad No Estándar
En la práctica: se construyen tres indicadores propietarios: (1) Choppiness Index (CHOP) de Dreiss normalizado a 0-100, (2) detector de Bollinger-Keltner squeeze (cuando las BB quedan dentro de los canales de Keltner), (3) Pure Range Volatility (ATR de 20 días dividido por el precio, expresado en %). El sistema los usa como filtro de régimen: solo opera estrategias contrarian cuando el mercado está en "rango comprimido" (CHOP > 61.8) y evita operar cuando está en "tendencia explosiva" (CHOP < 38.2). El motor backtestea el valor añadido del filtro sobre la estrategia base.
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 31 — Contrarian Indicators Agregados: el miedo cuantificado

En la práctica: se construye un "Índice Contrarian Compuesto" (CCI) que agrega 5 señales normalizadas a escala 0-100: (1) Put/Call ratio de CBOE, (2) flujo neto de fondos monetarios, (3) % de miembros del SPY por debajo de su SMA-200, (4) spread de bonos high-yield sobre Tesoro, (5) VIX. Se ponderan por inversa de su volatilidad histórica. El motor backtestea la regla: comprar RV global (VT) cuando CCI > 85, reducir exposición al 50% cuando CCI < 15. Se compara contra el Fear & Greed Index de CNN (Capítulo 4) y contra un Buy & Hold ciego.
Semáforo: 🟢 Totalmente backtesteable (con proxies de Yahoo Finance para las señales no directamente cotizadas).

### Capítulo 32 — Moving Average Contrarian: el cruce inverso

En la práctica: en lugar del clásico "cruce dorado" (EMA-50 cruza al alza EMA-200), se opera el inverso: se compra RV global cuando la EMA-50 cruza a la BAJA la EMA-200 (señal de pánico colectivo), siempre que el precio esté al menos un 20% por debajo de su máximo de 52 semanas. Se backtestea desde 1993 sobre SPY y se compara contra el cruce dorado tradicional, el filtro de SMA-200 del Capítulo 8 del libro original, y un Buy & Hold. Se documenta cuántas veces se activó la señal en cada crisis histórica (Dotcom, Subprime, Covid, 2022).
Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 33 — Integración Maestra: el Dashboard de Indicadores No Convencionales
En la práctica: se construye un dashboard unificado que agrega los 10 indicadores de este bloque en una sola vista. Para cada activo del universo, el sistema muestra: (1) posición respecto a Fibonacci MAs, (2) estado en Bollinger alternativas, (3) lectura de Stoch-RSI, (4) lectura de RSI dinámico, (5) estado estocástico, (6) fractales activos, (7) régimen de volatilidad (CHOP), (8) lectura del CCI agregado, (9) estado del cruce inverso de MAs, (10) semáforo final contrarian (verde/ámbar/rojo). El motor genera un informe PDF semanal con el ranking de los 10 activos más "contrarian" del momento.
Semáforo: 🟢 Totalmente backtesteable.

## Apéndice A — Glosario de Términos
Definición, fórmula y umbral de referencia para cada término técnico utilizado en el libro: cointegración, z-score, test de Engle-Granger, Information Ratio, volatility drag, wash sale rule, impermanent loss, smart contract risk, put/call ratio, VIX term structure, sucesión de Fibonacci aplicada a series temporales, media triangular de Wilder, volatilidad condicional GARCH(1,1), transformada de Hilbert para ciclo dominante, fractales de Williams, Choppiness Index de Dreiss, Bollinger-Keltner squeeze, y todos los términos financieros y estadísticos clave.

## Apéndice B — Semáforo de viabilidad del motor
Tabla resumen de cada capítulo indicando: (1) ¿Es backtesteable con Yahoo Finance? (2) ¿Requiere datos alternativos? (3) ¿Requiere ejecución en tiempo real? (4) ¿Es apto para inversor minorista? Esta tabla evita frustraciones: el lector sabe antes de empezar qué puede simular y qué solo puede leer.

## Apéndice C — Fuentes de datos alternativas

Dónde obtener datos de opciones (CBOE DataShop), Form 4 (SEC EDGAR), sentimiento (AAII, CNN Fear & Greed API), on-chain crypto (Glassnode, Dune Analytics) y macro (FRED). Cómo integrarlos en el motor mediante módulos personalizados.

## Apéndice D — Ética y regulación
Qué estrategias son legales, cuáles están en zona gris y cuáles son directamente ilegales (front-running con información privilegiada, insider trading clásico, manipulación de mercado). El inversor cuantitativo debe conocer los límites antes de ejecutar.