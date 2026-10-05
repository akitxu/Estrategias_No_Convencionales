# Prefacio: Cuando la ortodoxia no basta — Filosofía del proyecto y objetivos

El inversor conservador que llegó al primer libro de esta serie buscaba algo claro: proteger su patrimonio, hacerlo crecer de forma estable y dormir tranquilo por la noche. Las estrategias convencionales —la 60/40, la Cartera Permanente, el All Weather de Dalio, los Bogleheads— cumplieron esa promesa durante décadas. Pero el mundo ha cambiado, y con él, los límites de lo que esas recetas pueden ofrecer.
Este segundo libro nace de una pregunta incómoda: ¿qué hacemos cuando la ortodoxia deja de funcionar? Cuando las acciones y los bonos caen a la vez (como en 2022), cuando la inflación vuelve tras cuarenta años de letargo, cuando los ciclos se aceleran y las crisis ya no se parecen a las anteriores. El inversor conservador no busca adrenalina ni batir al mercado, pero sí necesita herramientas adicionales para blindar su patrimonio, capturar ineficiencias o cubrir riesgos que las estrategias clásicas no pueden gestionar.
Este libro es esa caja de herramientas complementaria. No sustituye a la primera parte: la construye sobre ella.

## ¿Por qué existe este libro?
Las estrategias del primer libro eran robustas, simples y probadas. Funcionaban porque no intentaban predecir nada: se limitaban a diversificar, rebalancear y mantener la disciplina. Pero esa misma fortaleza es también su límite. Una cartera All Weather no sabe distinguir entre una recesión cíclica y una crisis sistémica. Un Boglehead no puede aprovechar el pánico colectivo para comprar barato. Un 60/40 no tiene defensa contra la correlación positiva entre acciones y bonos en entornos de tipos altos.
Este segundo libro aborda esas limitaciones con estrategias no convencionales, organizadas en ocho bloques temáticos:

* **Comportamiento y psicología de masas:** explotar el pánico y la euforia con reglas frías (contrarian, momentum crash, fear & greed).
* **Cuantitativas y arbitraje estadístico:** pares trading, arbitraje ETF-subyacente, machine learning.
* **Basadas en eventos:** merger arbitrage, earnings surprise, insider trading legal.
* **Macro y globales:** carry trade, arbitraje de volatilidad, global macro.
* **Alternativas y exóticas:** tail risk hedging, provisión de liquidez, inversión temática.
* **Nicho y tácticas específicas:** dividend capture, ETFs inversos, tax-loss harvesting, estacionalidad.
* **Alto riesgo (solo expertos):** butterfly spreads, CDS, crypto yield farming.
* **Indicadores técnicos no convencionales:** Fibonacci MAs, Bollinger alternativas, Stoch-RSI, fractales de Williams, Choppiness Index.

Pero aquí viene la advertencia de honestidad intelectual que diferencia este libro de otros del género: no todas estas estrategias son iguales. Algunas están sólidamente documentadas en la literatura académica; otras son tácticas de libro con edge estadístico débil; otras requieren infraestructura profesional que un inversor minorista no tiene; y unas pocas son directamente especulativas. Este libro no las disfraza: las etiqueta con un semáforo de viabilidad para que el lector sepa antes de empezar qué puede simular, qué puede ejecutar y qué solo debe leer con espíritu crítico.

* **Honestidad intelectual:** lo que el motor puede y no puede hacer

En el primer libro, el motor cuantitativo era un backtester puro: descargaba datos, simulaba estrategias y devolvía métricas. En este segundo libro, el motor se amplía con módulos especializados para abordar la nueva complejidad:

* Gestor de señales binarias (miedo/codicia) para las estrategias de sentimiento.
* Calculador de cointegración (test de Engle-Granger, z-scores) para pairs trading.
* Tracker de eventos (earnings, OPAs, Form 4) como proxy de estrategias event-driven.
* Simulador de opciones (payoff diagrams, griegas) para tail hedging y spreads.
* Biblioteca de indicadores técnicos no convencionales (Fibonacci MAs, Bollinger aumentadas, RSI dinámico de * Ehlers, fractales de Williams, Choppiness Index).

Pero hay límites que debemos nombrar con claridad:

* No podemos backtestear yield farming real (requiere datos on-chain de Glassnode o Dune).
* No podemos simular CDS reales (requieren contrapartida OTC, no replicable con ETFs).
* No podemos backtestear opciones históricas completas (Yahoo Finance no provee ese histórico).
* Los modelos de ML/IA requieren validación walk-forward exhaustiva antes de considerarlos ejecutables.

Cuando el motor no pueda simular algo, lo documentará. Cuando pueda hacerlo solo parcialmente, usará proxies y lo declarará. No hay cajas negras, pero tampoco hay milagros.

## Cómo usar el motor cuantitativo

El núcleo del libro sigue siendo la práctica. El mismo "motor común" del primer libro —la arquitectura modular en Python— actúa ahora como tu analista personal ampliado. El flujo de trabajo recomendado es:

* **Le la teoría y el semáforo:** comprende la filosofía de la estrategia y, sobre todo, verifica si el motor puede simularla completamente (🟢), parcialmente (🟡) o solo documentarla (🔴).
* **Ejecuta el motor:** abre el Notebook del capítulo y pulsa "Play". El motor descargará datos, aplicará los módulos específicos de la estrategia (cointegración, señales binarias, indicadores no convencionales) y simulará el backtest.
* **Analiza el diagnóstico:** el sistema entrega métricas de riesgo (Rentabilidad, Volatilidad, Máximo Drawdown, Ratio Sharpe, Sortino, Calmar) acompañadas de un diagnóstico cualitativo automático. En estrategias no convencionales, se añaden métricas específicas: win-rate, profit factor, Information Ratio, o coste del hedge según el caso.
* **Revisa el seguimiento actual:** el sistema lee tu cartera y te indica si ha derivado de su objetivo, sugiriendo ajustes respetando costes de transacción y fiscalidad.
* **Consulta el dashboard de indicadores (Bloque VIII):** para las estrategias basadas en indicadores técnicos no convencionales, el motor genera un ranking semanal de los activos más "contrarian" del momento, agregando las 10 capas de confirmación.

## El semáforo de viabilidad: tu brújula de honestidad
Cada capítulo del libro lleva adjunta una etiqueta de viabilidad que responde a cuatro preguntas:

| Aspecto | Local | Google Colab |
|----------|----------|-------------|
| **Velocidad** | ⚡ Rápida | 🐢 Media |
| **Almacenamiento** | 💾 Ilimitado (según tu equipo) | 15 GB (Google Drive) |
| **Sesión** | ♾️ Permanente | 12 h máximo |
| **Privacidad** | 🔒 Total control de los datos | ☁️ Dependencia de Google |
| **API Yahoo Finance** | ✅ Sin limitaciones prácticas de uso | ⚠️ Posibles rate limits y desconexiones |

    🟢 Verde: totalmente backtesteable y ejecutable por un inversor minorista.
    🟡 Ámbar: backtesteable parcialmente o requiere datos/infraestructura adicional.
    🔴 Rojo: solo documentable; el motor explica la mecánica pero no simula P&L histórico.

Este semáforo evita frustraciones: el lector sabe antes de abrir el Notebook qué puede esperar.

## Detrás del telón: la robustez de los datos

En el mundo cuantitativo, "basura entra, basura sale". El pipeline de depuración automática del primer libro se mantiene y se amplía:

* Detección de huecos temporales en series de Yahoo Finance.
* Normalización de formatos al importar extractos bancarios o datos de FRED.
* Validación de cointegración antes de ejecutar pairs trading (si dos activos no están cointegrados, el motor lo advierte y aborta la simulación).
* Control de supervivencia (survivorship bias): el motor documenta cuándo un universo de activos sufre este sesgo y cómo afecta a las conclusiones.

Al final de cada ejecución, el sistema muestra un "Informe de Limpieza" que garantiza la calidad de los datos. No hay simulaciones sobre datos sucios.

En resumen, este libro no trata de predecir el futuro, sino de prepararse matemáticamente para escenarios que las recetas clásicas no cubren. Al finalizar, sabrás:

* Qué estrategias no convencionales tienen edge estadístico real y cuáles son solo ruido.
* Cómo integrarlas como satélites de una cartera central ortodoxa (Core-Satellite).
* Cuándo activarlas (regímenes de mercado) y cuándo apagarlas.
* Qué riesgos específicos conlleva cada una y cómo monitorizarlos.*

Tendrás a tu disposición un sistema de seguimiento ampliado que te permitirá gestionar inversiones no convencionales con la misma rigurosidad que un gestor profesional, pero con la transparencia que ofrece la tecnología.

## Aviso legal
Las herramientas, códigos y simulaciones presentadas en este libro tienen fines exclusivamente educativos y de investigación cuantitativa. No constituyen asesoramiento financiero ni recomendación de inversión. El rendimiento pasado no garantiza resultados futuros.
Advertencia específica para este segundo libro: muchas de las estrategias aquí presentadas son de alto riesgo, requieren capital elevado, conocimientos avanzados o infraestructura profesional. Algunas operan con apalancamiento, derivados o activos ilíquidos. El lector debe entender que las pérdidas pueden superar el capital invertido en ciertos escenarios. Consulta siempre con un asesor financiero cualificado antes de ejecutar cualquier estrategia real, y nunca inviertas dinero que no puedas permitirte perder.
El semáforo de viabilidad es una guía, no una garantía. Que el motor pueda simular una estrategia no significa que sea adecuada para tu perfil de riesgo, tu horizonte temporal o tu situación fiscal.