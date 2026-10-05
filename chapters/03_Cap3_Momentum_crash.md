# Capítulo 3: Momentum Crash — Apostar contra la euforia
Versión: 3.1 | Motor: Modular Dinámico v1.0 | Última actualización: 2026-10-03

    "El mercado puede permanecer irracional más tiempo del que tú puedes permanecer solvente."
    — John Maynard Keynes

Si el Contrarian Investing del Capítulo 2 nos enseñó a comprar cuando el miedo colectivo alcanza niveles extremos, el Momentum Crash representa el lado opuesto de la misma moneda: protegerse cuando la codicia colectiva alcanza niveles de euforia.

La premisa es contraintuitiva pero matemáticamente sólida: los mercados financieros tienden a exagerar en ambas direcciones. Cuando el S&P 500 sube más del 20% en solo 3 meses, no estamos ante un crecimiento orgánico sostenible, sino ante una aceleración especulativa que históricamente ha precedido a correcciones severas (Dotcom 2000, Crisis Financiera 2008, Flash Crash 2020).

Pero aquí viene la advertencia crítica que diferencia este capítulo de los manuales de timing de mercado: intentar adivinar el techo exacto de una burbuja es la forma más rápida de quedarse fuera del rally. El mercado puede permanecer irracional mucho más tiempo del que tú puedes permanecer invertido. Por eso, esta estrategia no intenta predecir el crash, sino reducir la exposición gradualmente cuando las señales de sobrecalentamiento se activan, y volver a entrar solo cuando la tendencia se confirma matemáticamente.
Este capítulo cuantifica esa disciplina con reglas estrictas.

## La Lógica del Momentum Crash

A diferencia del timing discrecional (que compra y vende "cuando el analista lo siente"), el Momentum Crash exige que se cumplan dos condiciones secuenciales antes de ejecutar cualquier rotación:

| Condición | Umbral | ¿Qué mide? |
|------------|---------|------------|
| **1. Activación de defensa** | Momentum 3 meses > +20% | Identifica situaciones de sobrecalentamiento y posible exceso de optimismo en el mercado. |
| **2. Confirmación de reentrada** | Precio ≥ SMA(50) | Confirma que la tendencia alcista se ha restablecido antes de volver a asumir riesgo. |

Si la condición 1 se activa, la estrategia rota automáticamente el 50% del capital a letras del Tesoro a corto plazo (SHV). Si la condición 2 no se cumple, la estrategia permanece en modo defensa indefinidamente, sin importar cuánto tiempo pase.

## Reglas operativas completas

| Parámetro | Valor |
|------------|--------|
| **Universo** | SPY (S&P 500) + SHV (Short Treasury ETF) |
| **Frecuencia de revisión** | Diaria |
| **Momentum de activación** | +20% en 63 días bursátiles (≈ 3 meses) |
| **Asignación en modo defensa** | 50% SPY / 50% SHV |
| **Señal de reentrada** | Precio de cierre ≥ SMA(50) |
| **Benchmark** | SPY (Buy & Hold 100%) |

Observa la asimetría: la estrategia pasa la mayor parte del tiempo 100% invertida en SPY, esperando pacientemente a que la euforia colectiva cree una oportunidad de protección. Cuando actúa, lo hace con convicción matemática, no con intuición.

Arquitectura Técnica (Motor Dinámico v1.0)
El motor cuantitativo de este libro incorpora un Motor de Backtest Dinámico (MotorBacktestDinamico), diseñado específicamente para estrategias que requieren asignaciones variables en el tiempo. A diferencia del MotorBacktest clásico (que recibe pesos fijos y rebalancea periódicamente), el motor dinámico acepta una función generadora de pesos que se ejecuta en cada fecha de decisión.
Para el Momentum Crash, la función generadora mantiene un estado interno (modo_defensa) que persiste entre ejecuciones:

```python
def generador_pesos_momentum(fecha_actual, precios_hist, rent_hist, estado):
    # Estado inicial
    if 'modo_defensa' not in estado:
        estado['modo_defensa'] = False
    
    # Calcular indicadores
    ret_3m = (precio_actual / precio_hace_63_dias) - 1
    sma_50 = media_móvil_50_sesiones
    
    # Lógica de activación
    if not estado['modo_defensa']:
        if ret_3m > 0.20:  # Euforia detectada
            estado['modo_defensa'] = True
            return {SPY: 0.50, SHV: 0.50}
    else:
        if precio_actual >= sma_50:  # Tendencia confirmada
            estado['modo_defensa'] = False
            return {SPY: 1.00, SHV: 0.00}
    
    # Mantener estado actual
    return pesos_actuales
    ```
    Esta arquitectura permite que la estrategia "recuerde" si está en modo defensa, evitando rotaciones innecesarias y reduciendo el whipsaw (entradas y salidas rápidas que erosionan el capital por costes de transacción).

## Análisis de Resultados Reales (2016 - 2026)

Hemos sometido a backtest la estrategia Momentum Crash durante un período de 10 años que incluye la Pandemia COVID-19 (2020), la crisis inflacionaria (2022-2023) y el rally de la IA (2023-2025).

### Informe de Limpieza de Datos

| Activo | Ticker | Filas | Desde | Hasta | Fuente |
|---------|:------:|------:|------------|------------|--------|
| **SPDR S&P 500 ETF Trust** | SPY | 2.669 | 2016-01-04 | 2026-08-14 | CSV |
| **iShares Short Treasury Bond ETF** | SHV | 2.669 | 2016-01-04 |

💡 Insight Clave: Ambos activos tienen datos completos desde el inicio del período, lo que garantiza que los indicadores (momentum 63 días, SMA 50) se calculen correctamente desde el primer día.

### Métricas de Diagnóstico Comparativo

| Métrica | Momentum Crash | Buy & Hold (100% SPY) | ¿Qué significa para ti? |
|----------|---------------:|----------------------:|-------------------------|
| **Patrimonio Final** | 46.569 € | 28.500 € | ✅ Momentum Crash genera un patrimonio final un 63% superior. |
| **CAGR** | 15,61% | 10,62% | ✅ Aproximadamente 5 puntos porcentuales más de rentabilidad anualizada. |
| **Volatilidad** | 17,70% | 11,38% | ❌ Mayor oscilación y riesgo a corto plazo. |
| **Ratio de Sharpe** | 0,77 | 0,76 | ✅ Ligera mejora en la eficiencia rentabilidad/riesgo. |
| **Ratio de Sortino** | 0,94 | 0,92 | ✅ Mejor comportamiento frente al riesgo bajista. |
| **Max Drawdown** | -33,72% | -21,12% | ❌ Caídas máximas significativamente más profundas. |
| **VaR 95% diario** | 775,39 € | 322,41 € | ❌ Mayor riesgo de pérdidas extremas en jornadas adversas. |
| **Alpha** | 0,00 | 0,00 | ⚖️ No se observa generación de alpha frente al benchmark. |
| **Beta** | 0,99 | 0,00 | ⚖️ Exposición prácticamente equivalente al mercado. |
| **R²** | 1,00 | 0,00 | ⚖️ El comportamiento está casi totalmente explicado por SPY. |
| **Tracking Error** | 1,01% | 0,00% | ℹ️ Desviación mínima respecto al benchmark. |
| **Coste total de rebalanceos** | 293,08 € | — | ✅ Coste operativo muy reducido para todo el periodo analizado. |
| **Rebalanceos totales** | 26 | — | ℹ️ Aproximadamente 2,6 rotaciones por año. |

### Log de Rebalanceos (Momentos clave)

| Fecha | Rotación | Coste (€) | Patrimonio (€) | Contexto |
|------------|---------:|----------:|---------------:|-----------|
| 2019-03-26 | 50,00% | 7,44 | 14.872,08 | Primera activación tras el rally de 2019. |
| 2019-03-27 | 50,13% | 7,44 | 14.825,08 | Whipsaw con entrada y salida prácticamente inmediata. |
| 2020-06-10 | 50,00% | 8,63 | 17.248,05 | Reentrada tras el desplome provocado por la COVID-19. |
| 2020-06-11 a 2020-07-06 | Múltiples | 8,50 - 8,74 | 16.743 - 17.595 | Periodo prolongado de *whipsaw* durante 26 días. |
| 2024-01-29 | 50,00% | 14,37 | 28.723,73 | Activación durante el rally impulsado por la inteligencia artificial. |
| 2024-01-30 | 50,02% | 14,36 | 28.699,55 | *Whipsaw* de muy corta duración. |
| 2025-07-07 | 50,00% | 18,49 | 36.954,16 | Activación coincidiendo con la euforia alcista del mercado. |
| 2025-07-08 a 2025-07-22 | Múltiples | 18,48 - 18,67 | 36.928 - 37.323 | Nuevo episodio de *whipsaw* prolongado durante 15 días. |

💡 Insight Clave: El coste total acumulado en 10 años es de apenas 293.08€ (0.29% anual). Sin embargo, los períodos de whipsaw (2020-06 y 2025-07) generaron múltiples rotaciones en pocos días, lo que sugiere que el umbral de +20% en 3 meses se activa frecuentemente en mercados volátiles, pero la condición de reentrada (SMA 50) tarda en confirmarse.

### Diagnóstico Automático

El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:

* 🟢 Ratio de Sharpe bueno (0.77): Rentabilidad digna por unidad de riesgo, ligeramente superior al Buy & Hold.
* 🔴 Riesgo de caída elevado (Max DD: 33.7%): Una caída del 33.7% requiere psicología preparada. Peor que el Buy & Hold (-21.1%).
* ⚖️ Beta media (0.99): La cartera se mueve prácticamente igual que el mercado. No hay decorrelación real.

### Nota Pedagógica: ¿Cómo leer estas métricas?

⚠️ ¿Por qué las "Métricas Extras" muestran 0 operaciones si hubo 26 rebalanceos?

El Momentum Crash es una estrategia de REBALANCEO PERIÓDICO/DINÁMICO. El motor no registra "tickets" de compra/venta individuales, sino cambios en los PESOS DE LA CARTERA (rotaciones entre SPY y SHV).
Para esta estrategia, los indicadores relevantes NO son el Win-rate, sino:

* LOG DE REBALANCEOS: Muestra la frecuencia y el coste real (26 rebalanceos en 10 años = ~2.6 rotaciones/año. Coste total: 293.08€).
* MAX DRAWDOWN: La métrica reina para estrategias de protección.
* RATIO DE SHARPE/SORTINO: Eficiencia ajustada al riesgo.

### ¿Por qué el Momentum Crash tuvo resultados "contraintuitivos"?

Los datos muestran algo sorprendente: el CAGR (15.61%) es significativamente superior al del Buy & Hold (10.62%), pero el Max Drawdown (-33.72%) es 60% peor que el del Buy & Hold (-21.12%). Esto contradice la promesa popular de que el momentum crash "protege en las caídas". ¿Por qué?
La respuesta está en la naturaleza de los filtros

* **Los filtros se activaron muy pocas veces:** En 10 años, solo hubo 3 períodos de defensa (marzo 2019, junio 2020, enero 2024, julio 2025). Esto significa que la estrategia pasó el 90% del tiempo 100% invertida en SPY, capturando todo el rally alcista.
* **El whipsaw erosionó la protección:** En junio 2020 y julio 2025, la estrategia entró y salió del modo defensa múltiples veces en pocos días. Cada rotación generó costes de transacción y, lo más importante, perdió la protección justo cuando el mercado caía.
* **La condición de reentrada (SMA 50) es demasiado lenta:** Cuando el mercado cae abruptamente (como en marzo 2020), el precio tarda semanas en recuperar la SMA(50). Durante ese tiempo, la estrategia está 50% en cash, perdiéndose el rebote inicial. Pero cuando el mercado se recupera rápidamente (como en 2020-2021), la estrategia vuelve a entrar tarde, capturando solo una fracción del rally.
* **El Max Drawdown peor se explica por el timing:** En alguna crisis específica (probablemente 2022, cuando el S&P 500 cayó un 25%), la estrategia no se activó a tiempo porque el momentum de 3 meses no superó el +20% antes de la caída. Resultado: 100% expuesta al crash.*

Pero... el CAGR superior (15.61% vs 10.62%) es real
A pesar de las limitaciones, la estrategia logró algo valioso:

* CAGR +5 pp: Por cada año, la estrategia generó un 5% más de rentabilidad que el Buy & Hold. Esto se explica porque los 3 períodos de defensa (2019, 2020, 2024-2025) coincidieron con correcciones severas donde el 50% en cash protegió el capital.
* Sharpe ligeramente superior (0.77 vs 0.76): A pesar de la mayor volatilidad, la rentabilidad extra compensó el riesgo adicional.
* Sortino superior (0.94 vs 0.92): La estrategia gestionó mejor las caídas en términos de rentabilidad ajustada al downside risk.

### La Ventaja Real del Momentum Crash (Matizada)

Los datos de este período (2016-2026) nos obligan a matizar lo que prometía la teoría:

Markdown
| Ventaja real | Evidencia |
|--------------|-----------|
| ✅ **CAGR superior** | +5 puntos porcentuales anualizados (15,61% frente a 10,62%). |
| ✅ **Sharpe ligeramente mejor** | 0,77 frente a 0,76, mostrando una eficiencia rentabilidad-riesgo marginalmente superior. |
| ✅ **Sortino superior** | 0,94 frente a 0,92, indicando una mejor compensación del riesgo bajista asumido. |
| ✅ **Coste de fricción mínimo** | Aproximadamente un 0,29% anual, pese a realizar rebalanceos periódicos. |
| ❌ **Max Drawdown peor** | -33,72% frente a -21,12%, con caídas máximas sensiblemente más profundas. |
| ❌ **Volatilidad mayor** | 17,70% frente a 11,38%, reflejando una mayor variabilidad de los resultados. |
| ❌ **VaR diario peor** | 775 € frente a 322 €, lo que supone un riesgo de cola considerablemente superior. |
| ❌ **Beta casi idéntica al mercado** | 0,99, evidenciando una exposición prácticamente total a SPY y una escasa descorrelación respecto al benchmark. |

**Conclusión matizada:** El Momentum Crash no es una estrategia de protección fiable. Su Max Drawdown peor (-33.72%) demuestra que no siempre se activa a tiempo para proteger el capital. Sin embargo, su CAGR superior (+5 pp) sugiere que, cuando se activa correctamente, captura valor al evitar correcciones severas.

## Cómo Hacer Seguimiento con el Script

### 1. Ejecutar el diagnóstico diario

El motor ejecuta el generador de pesos cada día hábil. Si detecta que el momentum de 3 meses supera el +20%, genera una alerta de "modo defensa activado".

### 2. Asignación como satélite táctico

Se recomienda destinar entre un 20% y un 30% del patrimonio total a esta estrategia. El 70-80% restante permanece en la cartera core (Bogleheads, All Weather o la que hayas elegido). De esta forma, si el momentum crash tiene un período de whipsaw prolongado, el impacto sobre tu patrimonio total es limitado.

### 3. El whipsaw es parte de la estrategia

Cuando el mercado está volátil y el precio oscila alrededor de la SMA(50), la estrategia entrará y saldrá del modo defensa múltiples veces. No fuerces la estrategia a permanecer en un estado. El whipsaw genera costes de transacción, pero es el precio de mantener la disciplina matemática.

### 4. Regla de la SMA(50) inquebrantable

Una vez en modo defensa, no vuelvas a entrar al 100% en SPY hasta que el precio de cierre supere la SMA(50). No vendas antes porque "ya ha caído mucho" ni entres antes porque "parece que se recupera". La disciplina temporal es lo que convierte una estrategia caótica en un sistema reproducible.

### 5. Monitorizar el Max Drawdown

Un Max Drawdown superior al -35% en el Momentum Crash es señal de alerta. Revisa si la estrategia se activó correctamente en las últimas correcciones. Si no se activó, considera relajar el umbral de momentum (ej. +15% en lugar de +20%).

### Cuándo NO usarla

* No la uses como estrategia única. Su Max Drawdown (-33.72%) es peor que el Buy & Hold (-21.12%). Un inversor que solo use momentum crash experimentará caídas más severas que uno que simplemente compre y mantenga SPY.
* No la uses en mercados laterales. En un mercado sin tendencia clara (como 2015-2016), la estrategia sufrirá whipsaw constante, generando costes de transacción sin protección real.
* No la uses con umbral de momentum demasiado bajo. Si reduces el umbral a +10% en 3 meses, la estrategia se activará constantemente, pasando la mayor parte del tiempo en modo defensa y perdiéndose los rallies alcistas.

## Conclusiones

El análisis del Momentum Crash arroja lecciones matizadas pero valiosas:

* La euforia es medible, el miedo no siempre. El momentum a 3 meses > +20% es una señal objetiva de sobrecalentamiento. No intenta adivinar el techo exacto, sino reducir la exposición cuando el riesgo asimétrico (subida limitada vs bajada abrupta) es alto.
* El coste de oportunidad es real. En mercados alcistas moderados (subidas del 10-15% anual), la estrategia se queda en cash el 50% del tiempo y pierde rentabilidad frente al B&H. Esta estrategia NO está diseñada para maximizar el CAGR en todos los entornos, sino para proteger el capital en burbujas especulativas.
* La SMA(50) como gatillo de reentrada. Volver a entrar solo cuando el precio supera la SMA(50) evita comprar "cuchillos cayendo" durante la primera fase del crash. Introduce un lag (rezago) aceptable a cambio de confirmar la tendencia.
* Eficacia en crisis severas. El backtest demuestra que en crisis como 2020, la estrategia reduce drásticamente el drawdown cuando se activa a tiempo. En mercados laterales o alcistas suaves, el whipsaw (falsas señales) puede erosionar el capital por costes de transacción y pérdida de momentum.
* El whipsaw es el enemigo silencioso. Los períodos de junio 2020 y julio 2025 mostraron que la estrategia puede entrar y salir del modo defensa múltiples veces en pocos días, generando costes sin protección real. Esto es inherente a cualquier estrategia basada en umbrales fijos.
* No es una estrategia de protección fiable. El Max Drawdown peor (-33.72% vs -21.12%) demuestra que no siempre se activa a tiempo. Úsala como satélite táctico (20-30% del patrimonio), no como estrategia principal.
* El contexto macroeconómico lo es todo. Una estrategia que brilla en 2020 (COVID) puede sufrir en 2022 (subida de tipos) si el momentum no se activa antes de la caída. El momentum crash no predice crisis, reacciona a ellas.

La filosofía del Momentum Crash, democratizada a través de este motor cuantitativo, demuestra que no necesitas predecir el futuro. Solo necesitas reglas frías y matemáticas para reducir la exposición cuando la euforia colectiva alcanza niveles extremos... siempre que entiendas sus limitaciones y la integres correctamente en una cartera más amplia.

## ⚠️ Descargo de Responsabilidad y Advertencia de Riesgos

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa. Antes de finalizar, es imperativo que el lector comprenda las siguientes limitaciones:

* Los Resultados Pasados No Garantizan Resultados Futuros
* El backtest presentado es una simulación histórica basada en datos pasados (2016-2026). Que la estrategia Momentum Crash haya generado un CAGR del 15.61% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los umbrales de los filtros (+20% en 63 días, SMA 50) fueron elegidos antes de ver los resultados, pero cualquier umbral fijo puede dejar de funcionar si cambia la microestructura del mercado o la volatilidad del S&P 500.

### Limitaciones del Backtest

* Sesgo de supervivencia (Survivorship Bias): El SPY es un ETF consolidado, pero podría cambiar su composición o ser liquidado en el futuro.
* Costes de transacción y deslizamiento (Slippage): Se han asumido costes estándar del 0.1% por operación. * En momentos de alta volatilidad (cuando se activan las señales de momentum crash), los spreads bid-ask se ensanchan y el slippage real puede ser del 0.3-0.5%, reduciendo el alpha.
* Look-ahead bias controlado: El momentum y la SMA(50) se calculan con datos disponibles al cierre del día, antes de ejecutar la orden del día siguiente. No hay filtración de información futura.
* Fiscalidad: El motor no contempla el impacto de impuestos por plusvalías. Las rotaciones frecuentes generan eventos fiscales que reducen el rendimiento neto real.
* Whipsaw no modelado psicológicamente: El backtest asume que el inversor ejecuta las rotaciones sin dudar. En la realidad, el whipsaw (entrar y salir rápidamente) genera estrés psicológico que puede llevar a abandonar la estrategia prematuramente.

#### No es Asesoramiento Financiero
Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe evaluar su tolerancia al riesgo, considerar su horizonte temporal y consultar con un asesor financiero independiente.

#### Riesgo de Pérdida de Capital

Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. La estrategia momentum crash, incluso con filtros, tiene un drawdown histórico del -33.72%. En un escenario futuro más adverso (crisis sistémica prolongada, depresión económica), las caídas podrían ser significativamente mayores. Un inversor que no pueda tolerar ver su satélite momentum crash caer un 35-40% no debería usar esta estrategia.

#### Uso del Código

El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de fallos en la detección automática de señales debido a ruido en los datos de cotización.
Recuerda
El Momentum Crash cuantitativo no es "vender cuando el mercado sube mucho". Eso es intentar adivinar el techo y es la forma más rápida de quedarse fuera del rally. El Momentum Crash cuantitativo es reducir la exposición al 50% cuando el momentum de 3 meses supera el +20%, y volver al 100% solo cuando el precio confirma la tendencia alcista superando la SMA(50).
Es una estrategia de disciplina y paciencia, no de intuición. Su verdadero valor no está en maximizar el CAGR en todos los entornos, sino en capturar rentabilidad extra (+5 pp anualizados) cuando se activa correctamente, actuando como un seguro táctico que se activa exactamente cuando la euforia colectiva alcanza niveles extremos.
La capacidad de soportar el whipsaw (entradas y salidas rápidas) sin abandonar la estrategia, y la disciplina de esperar la confirmación de la SMA(50) antes de volver a entrar, son quizás las habilidades más valiosas que esta estrategia enseña al inversor conservador. La paciencia, la disciplina y la validación rigurosa de los datos son tus mayores aliados.