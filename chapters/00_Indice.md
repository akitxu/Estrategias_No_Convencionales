# Índice del Blog: Estrategias No Convencionales de Inversión Cuantitativa

## Prefacio — Cuando la ortodoxia no basta
Por qué este Blog existe, para quién está escrito y cuándo tiene sentido salirse del guion. El inversor conservador no busca adrenalina, busca herramientas adicionales para blindar su patrimonio, capturar ineficiencias o cubrir riesgos que las estrategias clásicas (60/40, All Weather, Bogleheads) no pueden gestionar. Advertencia de honestidad intelectual: muchas de estas estrategias son de alto riesgo, requieren capital elevado o infraestructura profesional. Las marcaremos con un semáforo de viabilidad en el motor cuantitativo.

## Capítulo 1 — Arquitectura Común: el motor invisible (reutilizado)
Sistema de backtest, limpieza de datos y diagnóstico de riesgo extendido con nuevos módulos: gestor de señales binarias, calculador de cointegración, tracker de eventos y simulador de opciones.

Objetivos:
  1. Presentar la arquitectura común que se reutilizará en todos los capítulos.
  2. Documentar los nuevos módulos añadidos al motor cuantitativo.
  3. Establecer las reglas de evaluación uniformes para todas las estrategias.

Semáforo: 🟢 Totalmente backtesteable.

## BLOQUE I · Comportamiento y Psicología de Masas
El mercado no es racional: es humano. Aquí explotamos los sesgos cognitivos colectivos (pánico, euforia, anclaje) con reglas cuantitativas que sustituyen a la intuición.

### Capítulo 2 — Contrarian Investing: comprar cuando nadie quiere
Estrategia de reversión a la media aplicada a los 5 ETFs con peor rendimiento a 12 meses, filtrados por distancia al máximo histórico y RSI.

Objetivos:
  1. Construir un ranking mensual de 50 ETFs sectoriales ordenados por rentabilidad a 12 meses.
  2. Identificar los 5 "perdedores" que cumplan: precio >30% bajo máximo histórico Y RSI(14) < 30.
  3. Simular rotación semestral y comparar drawdown contra Buy & Hold en SPY desde 2000.
  4. Demostrar empíricamente cuándo la reversión a la media premia al contrarian y cuándo atrapa "cuchillos cayendo".

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 2b — Contrarian Investing: comprar cuando nadie quiere
Estrategia de reversión a la media aplicada a los 5 ETFs con peor rendimiento a 12 meses, filtrados por distancia al máximo histórico y RSI.

Objetivos:
  1. Construir un ranking mensual de 50 ETFs sectoriales ordenados por rentabilidad a 12 meses.
  2. Identificar los 5 "perdedores" que cumplan: precio >30% bajo máximo histórico Y RSI(14) < 30.
  3. Simular rotación semestral y comparar drawdown contra Buy & Hold en SPY desde 2000.
  4. Demostrar empíricamente cuándo la reversión a la media premia al contrarian y cuándo atrapa "cuchillos cayendo".

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 3 — Momentum Crash: apostar contra la euforia
Sistema de rotación a cash cuando el momentum a 3 meses del SPY supera +20% sin corrección intermedia del 5%.

Objetivos:
  1. Monitorizar la rentabilidad a 3 meses del S&P 500 (SPY).
  2. Detectar condiciones de "sobrecalentamiento" (>+20% sin corrección del 5%).
  3. Rotar 50% de la cartera a cash (SHV/BIL) y volver al tocar la SMA-50.
  4. Calcular cuántas veces se activó la señal desde 1993 y qué rentabilidad habría generado evitar crashes posteriores (Dotcom, 2008, 2020 marzo).

Semáforo:  Totalmente backtesteable.

### Capítulo 4 — Fear & Greed Index como temporizador táctico
Índice propietario de sentimiento que agrega 5 señales normalizadas para desplegar o reducir exposición a RV global.

Objetivos:
  1. Construir un índice de sentimiento con 5 señales: VIX (25%), put/call ratio (20%), flujo de fondos monetarios (20%), dispersión sobre SMA200 (20%) y bonos basura vs. Tesoro (15%).
  2. Definir umbrales de miedo extremo (<20) y codicia extrema (>80).
  3. Desplegar 20% adicional en VT en miedo extremo; reducir RV al mínimo en codicia extrema.
  4. Demostrar si este "termómetro" añade valor frente a un rebalanceo ciego.

Semáforo: 🟢 Totalmente backtesteable (con proxies de Yahoo Finance).

## BLOQUE II · Cuantitativas y Arbitraje Estadístico
Aquí dejamos de mirar al mercado como un todo y empezamos a mirar las relaciones matemáticas entre activos. El objetivo: rentabilidad descorrelada del mercado (alpha puro).

### Capítulo 5 — Pairs Trading: la danza de los correlacionados
Estrategia de mean reversion sobre spreads logarítmicos entre pares clásicos, validada con test de Engle-Granger.

Objetivos:
  1. Seleccionar pares clásicos (KO/PEP, XOM/CVX, BAC/JPM, GOLD/NEM).
  2. Calcular spread logarítmico y z-score sobre ventana de 60 días.
  3. Ejecutar operaciones cuando z-score supera +2 (vender caro, comprar barato 1:1).
  4. Validar cointegración con test de Engle-Granger y medir operaciones, win-rate y Sharpe desde 2010.

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 6 — Statistical Arbitrage: ETFs vs. sus subyacentes
Estrategia de convergencia entre ETF y su subyacente cuando el descuento/premium supera 2 desviaciones estándar.

Objetivos:
  1. Monitorizar divergencia entre ETF (ej. GLD) y subyacente (futuros GC o IAU como proxy).
  2. Detectar cuando el descuento/premium supera 2 desviaciones estándar de la media de 30 días.
  3. Ejecutar operación inversa esperando convergencia.
  4. Simular coste de transacción real y demostrar si el edge sobrevive después de comisiones y slippage.

Semáforo: 🟡 Parcialmente backtesteable (requiere datos de NAV intradía para precisión óptima).

### Capítulo 7 — Algorithmic Trading con IA/ML: el límite del motor
Modelo Random Forest con 30 features técnicos para predecir dirección del SPY a 5 días, con validación walk-forward.

Objetivos:
  1. Entrenar modelo Random Forest con 30 features técnicos (RSI, MACD, volatilidad realizada, volumen relativo, etc.).
  2. Implementar walk-forward validation (entreno 5 años, test 1 año, rolling).
  3. Generar curva de equity del modelo versus SPY y calcular Information Ratio.
  4. Documentar por qué la mayoría de modelos de ML fallan fuera de muestra y qué overfitting traps evitar.

Semáforo: 🟢 Totalmente backtesteable (con validación walk-forward obligatoria).

## BLOQUE III · Estrategias Basadas en Eventos
Los eventos corporativos crean ineficiencias temporales medibles. Aquí cuantificamos lo que los analistas fundamentales hacen a mano.

Capítulo 8 — Event-Driven: Merger Arbitrage con ETFs
Proxy de merger arbitrage usando ETFs de sectores históricamente objetivo de consolidación.

Objetivos:
  1. Monitorizar ETFs de sectores objetivo de consolidación (biotech XBI, bancos regionales KBE).
  2. Detectar caídas >25% desde máximos con volumen 2x la media.
  3. Interpretar como "descuento por miedo a M&A fallido" y entrar.
  4. Salir a los 6 meses o al recuperar el 50% de la caída; comparar contra Buy & Hold.

Semáforo:  Parcialmente backtesteable (proxy indirecto, no merger arbitrage puro).

Capítulo 9 — Earnings Surprise: el efecto post-anuncio
Estrategia de compra previa a anuncios de resultados de empresas con historial de superar consenso.

Objetivos:
  1. Seleccionar 20 empresas del S&P 100 con historial de superar consenso en los últimos 8 trimestres.
  2. Comprar 10 días antes de la fecha de resultados estimada y mantener 5 días después.
  3. Medir el "earnings drift" histórico.
  4. Calcular si la estrategia genera alpha real después de comisiones.

Semáforo: 🟡 Parcialmente backtesteable (requiere datos de earnings dates externos).

### Capítulo 10 — Insider Trading Legal: siguiendo al Form 4
Proxy de confianza del management usando buyback yield como señal de compra.

Objetivos:
  1. Construir proxy usando ratio de recompras de acciones (buyback yield) como señal de confianza.
  2. Comprar a partes iguales las 20 empresas del S&P 500 con mayor buyback yield trimestral.
  3. Filtrar por PER por debajo de la media del sector.
  4. Rebalanceo trimestral; comparar contra igual-weighted S&P 500.

Semáforo: 🟡 Parcialmente backtesteable (proxy con buyback yield, no Form 4 real).

## BLOQUE IV · Macro y Globales
Aquí el horizonte se amplía a divisas, tipos de interés y commodities. El inversor deja de mirar empresas y empieza a mirar países.

### Capítulo 11 — Carry Trade: cobrar el diferencial de tipos
Cartera larga en divisas con tipos reales altos y corta en divisas con tipos bajos, con filtro de salida por VIX.

Objetivos:
  1. Construir cartera larga en 3 divisas con tipos reales altos (MXN, BRL, INR) vía ETFs proxy.
  2. Cortar divisas con tipos bajos (JPY, CHF) vía FXY.
  3. Rebalanceo mensual con filtro de salida: si VIX > 30, cerrar toda posición.
  4. Simular desde 2010 y medir episodios de "carry unwind" (2015, 2020 marzo, 2024 agosto).

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 12 — Volatility Arbitrage: vender el miedo caro
Estrategia de venta de VXX cuando VIX supera en más de 5 puntos a la volatilidad realizada.

Objetivos:
  1. Monitorizar diferencia entre VIX (volatilidad implícita) y volatilidad realizada a 30 días del SPY.
  2. Vender VXX cuando VIX supera en más de 5 puntos a la RV.
  3. Volver a entrar cuando la diferencia se normaliza.
  4. Documentar el decaimiento estructural de VXX y calcular rentabilidad real después de ajustar por roll cost.

Semáforo: 🟡 Parcialmente backtesteable (VXX tiene decay estructural complejo).

### Capítulo 13 — Global Macro: el estilo Soros
Dashboard con 4 señales macro para asignación dinámica entre RV global, bonos largos, oro y cash.

Objetivos:
  1. Construir dashboard con 4 señales: curva de tipos US (10Y-2Y), PMI manufacturero global, índice dólar (DXY), precio del petróleo (USO).
  2. Clasificar régimen (expansión/recesión).
  3. Asignar dinámicamente entre 4 ETFs: VT, TLT, GLD y SHY.
  4. Backtestear los 4 regímenes desde 2000 y mostrar qué asignación habría ganado en cada ciclo.

Semáforo:  Totalmente backtesteable (con proxies de Yahoo Finance).

## BLOQUE V · Alternativas y Exóticas
Estrategias que no encajan en los buckets tradicionales. Algunas son defensivas (tail hedging), otras temáticas, otras de provisión de liquidez.

Capítulo 14 — Tail Risk Hedging: el seguro de Nassim Taleb
Asignación del 3% anual a opciones put OTM sobre SPY como seguro de cartera All Weather.

Objetivos:
  1. Asignar 3% anual del capital a comprar opciones put OTM (-5% delta) a 3 meses sobre SPY.
  2. Usar proxy (VIX calls o ETF SVOL) como aproximación liquidable.
  3. Destinar 97% restante a cartera All Weather.
  4. Simular coste anual del "seguro" y mostrar en qué crisis (2008, 2020, 2022) el hedge compensó los años de primas perdidas.

Semáforo: 🟡 Parcialmente backtesteable (proxy con SVOL, no opciones reales).

### Capítulo 15 — Liquidity Provision: ser el mercado
Proxy de market making usando ETFs de baja volatilidad y estrategia de mean reversion intramensual.

Objetivos:
  1. Construir proxy usando ETFs de baja volatilidad (SPLV).
  2. Simular estrategia de "mean reversion intramensual": comprar en banda inferior de Bollinger (20, 2) y vender en la media.
  3. Medir Sharpe de esta aproximación versus Buy & Hold.
  4. Documentar por qué la provisión de liquidez real requiere spreads y latencia que este motor no puede simular.

Semáforo: 🟡 Parcialmente backtesteable (proxy simplificado).

### Capítulo 16 — Thematic Investing: apostar a megatendencias
Cartera de 5 ETFs temáticos con filtro de tendencia y rebalanceo semestral.

Objetivos:
  1. Construir cartera con 5 ETFs temáticos (ARKK, LIT, ICLN, CIBR, BOTZ).
  2. Asignar 20% a cada uno con rebalanceo semestral.
  3. Aplicar filtro de tendencia: si ETF cotiza bajo SMA200, reducir peso al 10% y excedente a cash.
  4. Backtestear cartera temática versus SPY desde 2015 y documentar volatilidad extrema.

Semáforo:  Totalmente backtesteable.

## BLOQUE VI · Nicho y Tácticas Específicas
Estrategias de libro, tácticas fiscales, patrones estacionales. Pequeños edges que suman.

### Capítulo 17 — Dividend Capture: cobrar y salir
Rotación de 10 acciones del Dividend Aristocrats alrededor del ex-dividend date.

Objetivos:
  1. Seleccionar 10 acciones del Dividend Aristocrats con ex-dividend date en los próximos 5 días.
  2. Comprar 2 días antes del ex-date y vender 3 días después.
  3. Simular rotación durante 5 años.
  4. Calcular si el dividendo cobrado compensa el dividend drop y las comisiones.

Semáforo: 🟡 Parcialmente backtesteable (requiere datos de ex-dividend dates).

### Capítulo 18 — Short Selling con ETFs Inversos: apostar a la caída
Uso de SQQQ (Nasdaq -3x) como cobertura táctica de corta duración.

Objetivos:
  1. Usar SQQQ (Nasdaq -3x) como cobertura táctica.
  2. Asignar 15% a SQQQ cuando el sistema de momentum (Cap. 3) detecta sobrecalentamiento.
  3. Mantener posición máximo 20 días.
  4. Documentar volatility drag del ETF apalancado y demostrar por qué solo funciona en ventanas muy cortas.

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 19 — Tax-Loss Harvesting: la deducción silenciosa
Identificación trimestral de posiciones con pérdidas para vender y reemplazar por ETF correlacionado.

Objetivos:
  1. Identificar cada trimestre posiciones con pérdidas no realizadas >10%.
  2. Proponer venta y reemplazo por ETF correlacionado pero no idéntico (SPY → VOO, VT → ACWI).
  3. Evitar la wash sale rule.
  4. Calcular beneficio fiscal estimado y coste de tracking error del reemplazo.

Semáforo: 🟡 Parcialmente backtesteable (requiere datos fiscales personalizados).

### Capítulo 20 — Seasonal Strategies: el calendario como edge
Implementación de "Sell in May and Go Away" con rotación semestral a bonos cortos.

Objetivos:
  1. Implementar regla "Sell in May and Go Away": rotar 50% de RV a bonos cortos (SHV) el 1 de mayo.
  2. Volver a entrar el 1 de noviembre.
  3. Backtestear regla desde 1990.
  4. Comparar contra Buy & Hold y documentar si el edge estacional persiste en las últimas dos décadas.

Semáforo:  Totalmente backtesteable.

## BLOQUE VII · Alto Riesgo (Solo para Expertos)
️ Estrategias que requieren conocimientos avanzados, capital elevado o infraestructura profesional. El motor cuantitativo las documenta pero no las backtestea automáticamente: el usuario debe validarlas manualmente.

### Capítulo 21 — Options Butterfly Spread: apostar al rango
Construcción educativa de un butterfly con opciones del SPY y análisis de payoff al vencimiento.

Objetivos:
  1. Documentar construcción de butterfly: comprar 1 call ITM, vender 2 calls ATM, comprar 1 call OTM.
  2. Calcular punto muerto, máximo beneficio y probabilidad teórica de éxito usando distribución log-normal.
  3. Incluir módulo educativo que grafica payoff al vencimiento.
  4. Explicar por qué no se simula P&L histórico (requiere datos de opciones completos, fuera del scope de Yahoo Finance).

Semáforo: 🔴 Solo documentable (requiere datos de opciones).

### Capítulo 22 — Credit Default Swaps: asegurar deuda
Explicación de la mecánica de los CDS usando como proxy los ETFs de bonos high-yield.

Objetivos:
  1. Explicar mecánica de los CDS usando como proxy ETFs de bonos high-yield (HYG, JNK).
  2. Detectar cuando spread de HYG sobre Tesoro supera 600 pb.
  3. Interpretar como "seguro caro" y vender protección (proxy: vender HYG).
  4. Documentar por qué un CDS real requiere contrapartida OTC y no es replicable con ETFs.

Semáforo: 🟡 Parcialmente backtesteable (proxy con HYG, no CDS real).

### Capítulo 23 — Crypto Yield Farming: el nuevo carry trade
Documentación de la mecánica DeFi con proxy de hold + rebalanceo trimestral versus stablecoins.

Objetivos:
  1. Documentar mecánica de depositar criptomonedas en protocolos DeFi (Aave, Compound) para ganar yield.
  2. Construir proxy usando BTC-USD y ETH-USD de Yahoo Finance.
  3. Simular estrategia de "hold + rebalanceo trimestral" versus stablecoins.
  4. Documentar impermanent loss, smart contract risk y histórico de rug pulls.

Semáforo: 🔴 Solo documentable (requiere datos on-chain).

## BLOQUE VIII · Indicadores Técnicos No Convencionales y Patrones Cuantitativos
Aquí se amplía el motor con indicadores técnicos avanzados. Todos son codificables con datos OHLCV de Yahoo Finance y backtesteables en el motor. Se presentan como capas de confirmación sobre las estrategias de los bloques anteriores, nunca como señales únicas de entrada.

### Capítulo 24 — Fibonacci Moving Averages: la sucesión como soporte dinámico
Medias móviles exponenciales en niveles de la sucesión de Fibonacci (21, 34, 55, 89, 144, 233) como zonas de acumulación contrarian.

Objetivos:
  1. Construir EMAs en niveles de la sucesión de Fibonacci (21, 34, 55, 89, 144, 233 sesiones).
  2. Identificar "zona de acumulación contrarian" cuando precio toca EMA-144 con RSI(14) < 30.
  3. Backtestear desde 2000 comparando contra SMA-200 clásica.
  4. Medir drawdown máximo, Sharpe ratio y número de señales falsas.

Hallazgo clave: 🔴 No viable (falló estrepitosamente en backtest). Los niveles de Fibonacci no ofrecen edge estadístico significativo sobre medias móviles convencionales.

Semáforo:  Totalmente backtesteable.

### Capítulo 25 — Bollinger Bands Alternativas y Aumentadas
Comparación empírica de tres variantes de Bollinger Bands: clásicas, con media triangular de Wilder, y ajustadas por GARCH(1,1).

Objetivos:
  1. Comparar tres variantes: (1) Bollinger clásicas (SMA-20, 2σ), (2) Alternative BB con media triangular de Wilder y 2.5σ, (3) Augmented BB ajustadas por GARCH(1,1).
  2. Generar ranking empírico de cuál variante captura mejor las reversiones a la media en cada régimen.
  3. Medir porcentaje de veces que el precio toca la banda externa y revierte dentro de 5 sesiones.
  4. Validar en tendencias alcistas, laterales y bajistas.

Hallazgo clave: 🟢 Viable como táctica defensiva. Las Bollinger aumentadas con GARCH capturan mejor las reversiones en mercados laterales, pero no superan al Buy & Hold en tendencias fuertes.

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 26 — Stochastic RSI: el oscilador del oscilador
Aplicación del estocástico sobre el propio RSI como filtro de confirmación para estrategias contrarian.

Objetivos:
  1. Calcular RSI(14) y aplicar estocástico sobre el propio RSI con ventana de 14 sesiones.
  2. Definir sobreventa extrema (Stoch-RSI < 10) y sobrecompra extrema (>90).
  3. Usar como filtro de confirmación para estrategias contrarian de los Capítulos 2 y 4.
  4. Medir win-rate de la confluencia frente a señales individuales.

Hallazgo clave: 🟡 No viable como estrategia standalone. Con filtros estrictos, solo 18 transacciones en 19 años, CAGR 1.90% (inferior a tasa libre de riesgo), Max DD -4.65%. Viable solo como filtro de confirmación.

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 27 — Dynamic RSI: el oscilador adaptativo
RSI dinámico de John Ehlers con ventana adaptativa basada en el ciclo dominante del mercado (transformada de Hilbert).

Objetivos:
  1. Implementar RSI dinámico de John Ehlers con ventana adaptativa basada en ciclo dominante.
  2. Alargar ventana en mercados tendenciales (evita señales falsas); acortar en laterales (captura reversiones rápidas).
  3. Backtestear comparando contra RSI(14) fijo en términos de ratio señal/ruido y Sharpe ajustado.
  4. Validar si la adaptabilidad mejora el rendimiento respecto al RSI estático.

Hallazgo clave: 🔴 No viable. Peor que el Stochastic RSI: solo 4 transacciones en 19 años, CAGR 1.21%, Sharpe -0.55. Los umbrales dinámicos (20/80 en tendencia) son demasiado estrictos.

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 28 — Estocásticos Clásicos y Osciladores Combinados
Panel de sobrecompra/sobreventa que agrega tres osciladores para generar señales contrarian con triple confirmación.

Objetivos:
  1. Construir panel que agrega: (1) Stoch-RSI < 10, (2) RSI dinámico < 25, (3) %K estocástico clásico (14,3,3) < 20.
  2. Considerar señal contrarian válida solo cuando los tres coinciden simultáneamente.
  3. Medir win-rate de la confluencia triple frente a señales individuales.
  4. Documentar frecuencia de aparición (típicamente 3-5 veces al año por activo).

Hallazgo clave: 🔴 No viable. Peor Sharpe (-0.77) de todas las estrategias de osciladores. Solo 6 transacciones en 19 años, CAGR 1.35%. La confluencia extrema paraliza la estrategia.

Semáforo:  Totalmente backtesteable.

### Capítulo 29 — Fractal Indicator de Williams: soportes y resistencias dinámicos
Detección de fractales de 5 barras según Bill Williams, integrados como capa de confirmación con filtro de tendencia.

Objetivos:
  1. Detectar fractales de 5 barras (máximo/mínimo local con 2 barras a cada lado más extremas).
  2. Usar fractales alcistas como stop-loss dinámico y bajistas como objetivos de toma de beneficios.
  3. Integrar como capa de confirmación con filtro EMA-50.
  4. Backtestear rupturas de fractales versus estrategias de osciladores de los capítulos anteriores.

Hallazgo clave:  Viable, mejor Sharpe que el SPY. CAGR 6.91%, Sharpe 0.70, Max DD -11.89%. Primera estrategia del Bloque VII con edge real. La estructura geométrica del precio supera a los osciladores de momentum.

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 30 — Indicadores de Rango de Volatilidad: la estrategia Turtle Traders
Estrategia de trend following basada en Donchian Channels + ATR Trailing Stop (Chandelier Exit), inspirada en los Turtle Traders de Richard Dennis.

Objetivos:
  1. Implementar Donchian Channels (entrada 20 días, salida 10 días).
  2. Añadir ATR Trailing Stop (Chandelier Exit: máximo - 3×ATR).
  3. Filtrar con EMA-50 para operar solo en dirección de la tendencia.
  4. Validar si las rupturas de rango de volatilidad ofrecen ventajas sobre fractales y osciladores.

Hallazgo clave: 🔴 No viable. Whipsaws constantes: 315 transacciones en 19 años, CAGR 1.59%, Sharpe -1.16 (el peor del Bloque VII). Los períodos de Donchian (20/10 días) son demasiado cortos para mercados modernos.

Semáforo: 🟢 Totalmente backtesteable.

Capítulo 31 — Contrarian Indicators Agregados: el miedo cuantificado
Índice Contrarian Compuesto (CCI) que agrega 5 señales de sentimiento para identificar extremos de miedo/codicia.

Objetivos:
  1. Construir CCI que agrega 5 señales normalizadas: (1) Put/Call ratio, (2) flujo de fondos monetarios, (3) % de miembros del SPY bajo SMA-200, (4) spread HY sobre Tesoro, (5) VIX.
  2. Ponderar por inversa de volatilidad histórica.
  3. Backtestear regla: comprar VT cuando CCI > 85, reducir al 50% cuando CCI < 15.
  4. Comparar contra Fear & Greed Index de CNN (Cap. 4) y Buy & Hold ciego.

Hallazgo clave: 🔴 No viable. Parálisis por sobre-filtrado: solo 6 transacciones en 19 años, CAGR 1.21%, Sharpe -0.80. Exigir 2 de 3 condiciones extremas simultáneas elimina todas las oportunidades.

Semáforo: 🟢 Totalmente backtesteable (con proxies de Yahoo Finance).

### Capítulo 32 — Moving Average Contrarian: el cruce inverso
Entrada escalonada contrarian basada en distancia del precio a la EMA-200, medida en unidades de ATR.

Objetivos:
  1. Calcular distancia del precio a EMA-200 en unidades de ATR.
  2. Implementar entrada escalonada: -1 ATR (25%), -2 ATR (50%), -3 ATR (75%), -4 ATR (100%).
  3. Venta escalonada simétrica: +1 ATR (75%), +2 ATR (50%), +3 ATR (25%), +4 ATR (0%).
  4. Validar si la entrada escalonada captura correcciones profundas mejor que la confluencia extrema del Cap. 31.

Hallazgo clave: 🔴 No viable. Umbrales mal calibrados: 487 transacciones con CAGR 0.89% y Sharpe -0.32. Los umbrales de -1 a -4 ATR son apropiados para EMA-20, no para EMA-200.

Semáforo: 🟢 Totalmente backtesteable.

### Capítulo 33 — Integración Maestra: la síntesis del Bloque VII
Análisis comparativo de las 8 estrategias técnicas avanzadas (Capítulos 24-32) y propuesta de estrategia ensamble.

Objetivos:
  1. Comparar objetivamente las estrategias de los Capítulos 24-32 mediante métricas normalizadas (Sharpe, CAGR, Max Drawdown, frecuencia operativa).
  2. Identificar patrones de éxito y fracaso: ¿qué tienen en común las estrategias que funcionaron? ¿Qué comparten las que fallaron?
  3. Proponer una estrategia ensamble basada en evidencias: Fractal Williams (motor) + ADX (filtro de régimen) + RSI contrarian moderado (entrada en crisis).
  4. Cerrar el Bloque VII con conclusiones pedagógicas sólidas sobre la relación entre complejidad y rendimiento.

Hallazgo clave: La simplicidad supera a la complejidad. El Fractal Williams puro (Sharpe 0.70) superó a la estrategia ensamble más compleja (Sharpe 0.61). Añadir filtros no siempre mejora la eficiencia. El principio de Saint-Exupéry se cumplió: "La perfección no se alcanza cuando no hay nada más que añadir, sino cuando no hay nada más que quitar."

Semáforo: 🟢 Totalmente backtesteable.

## Apéndice A — Glosario de Términos
Definición, fórmula y umbral de referencia para cada término técnico utilizado en el Blog.

Contenido:
  • Cointegración, z-score, test de Engle-Granger, Information Ratio.
  • Volatility drag, wash sale rule, impermanent loss, smart contract risk.
  • Put/call ratio, VIX term structure.
  • Sucesión de Fibonacci aplicada a series temporales, media triangular de Wilder.
  • Volatilidad condicional GARCH(1,1), transformada de Hilbert para ciclo dominante.
  • Fractales de Williams, Choppiness Index de Dreiss, Bollinger-Keltner squeeze.
  • Todos los términos financieros y estadísticos clave del Blog.

## Apéndice B — Semáforo de viabilidad del motor
Tabla resumen de cada capítulo indicando viabilidad técnica y requisitos.

Contenido:
  1. ¿Es backtesteable con Yahoo Finance?
  2. ¿Requiere datos alternativos?
  3. ¿Requiere ejecución en tiempo real?
  4. ¿Es apto para inversor minorista?

Esta tabla evita frustraciones: el lector sabe antes de empezar qué puede simular y qué solo puede leer.

## Apéndice C — Fuentes de datos alternativas
Guía de fuentes de datos especializados y cómo integrarlas en el motor.

Contenido:
  • Datos de opciones: CBOE DataShop.
  • Form 4 (insider trading): SEC EDGAR.
  • Sentimiento: AAII, CNN Fear & Greed API.
  • On-chain crypto: Glassnode, Dune Analytics.
  • Macro: FRED.
  • Integración en el motor mediante módulos personalizados.

## Apéndice D — Ética y regulación
Marco legal de las estrategias presentadas en el Blog.

Contenido:
  • Estrategias legales, en zona gris y directamente ilegales.
  • Front-running con información privilegiada, insider trading clásico, manipulación de mercado.
  • El inversor cuantitativo debe conocer los límites antes de ejecutar.