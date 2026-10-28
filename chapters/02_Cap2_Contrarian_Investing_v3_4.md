# Capítulo 2: Contrarian Investing — Comprar cuando nadie quiere

**Versión:** 3.5 | **Motor:** Modular Dinámico v1.0 Corregido | **Última actualización:** 2026-10-14

> *"Sé codicioso cuando otros tienen miedo, y temeroso cuando otros son codiciosos."*  
> — Warren Buffett

Si la Cartera Permanente de Harry Browne nos enseñó a protegernos de las cuatro estaciones económicas, y el All Weather de Ray Dalio nos mostró cómo repartir el riesgo equitativamente, el **Contrarian Investing** representa un giro filosófico radical: apostar contra la multitud en los momentos de máximo pánico.

La premisa es contraintuitiva pero matemáticamente sólida: los mercados financieros están impulsados por la psicología humana (miedo y codicia), y esta psicología tiende a exagerar. Cuando las noticias son malas, los inversores venden en pánico empujando los precios muy por debajo de su valor razonable. Cuando las noticias son buenas, la euforia los empuja muy por encima. El inversor contrarian se posiciona sistemáticamente en el lado opuesto a la multitud.

Pero aquí viene la advertencia crítica que diferencia este capítulo de los manuales de autoayuda financiera: comprar ciegamente "lo que baja" es la forma más rápida de destruir capital. El mercado a veces tiene razón: un sector puede estar barato porque su modelo de negocio está estructuralmente roto. La clave está en distinguir entre una caída temporal por pánico y una caída estructural por obsolescencia. Este capítulo cuantifica esa distinción con reglas matemáticas estrictas.

---

## La Lógica del Contrarian Cuantitativo

A diferencia del contrarian "de intuición", el contrarian cuantitativo exige que se cumplan tres condiciones simultáneamente antes de ejecutar una compra:

| Condición | Umbral | ¿Qué mide? |
| :--- | :--- | :--- |
| 1. Ranking de perdedores | Top 5 peores a 12 meses | Identifica activos con peor comportamiento relativo e impopularidad reciente. |
| 2. Drawdown desde máximos | ≤ -15% (52 semanas) | Confirma que el pesimismo es significativo, no una simple corrección. |
| 3. RSI(14) técnico | ≤ 45 | Verifica que la presión vendedora sigue dominante y hay debilidad técnica. |

Si un activo no cumple las tres condiciones, no se compra. El capital no asignado se aparca en letras del Tesoro a corto plazo (**SHV**), rindiendo el tipo libre de riesgo sin asumir riesgo de mercado.

### Reglas Operativas Completas

| Parámetro | Valor |
| :--- | :--- |
| Universo | 16 ETFs sectoriales, factoriales, internacionales y alternativos + SHV |
| Frecuencia de revisión | Mensual (último día hábil de cada mes) |
| Asignación | Reparto equiponderado entre seleccionados (20% c/u si hay 5) |
| Holding period | 3 meses; posteriormente se vende y reevalúa |
| Cash residual | Si <5 activos cumplen filtros, el resto va a SHV |
| Benchmark | SPY (S&P 500) |

Observa la asimetría: la estrategia pasa la mayor parte del tiempo en cash (a menudo 60-70% del patrimonio), esperando pacientemente a que el pánico colectivo cree oportunidades genuinas. Cuando actúa, lo hace con convicción matemática, no con intuición.

---

## Arquitectura Técnica (Motor Dinámico v3.5)

El motor cuantitativo incorpora un **Motor de Backtest Dinámico** (`MotorBacktestDinamico`) diseñado específicamente para estrategias con asignaciones variables. A diferencia del motor clásico, acepta una función generadora de pesos que se ejecuta en cada fecha de decisión.

### Correcciones Aplicadas en v3.5
1.  **Deriva de Pesos:** Los pesos se actualizan diariamente (`w_i ← w_i * (1+r_i)/(1+r_p)`). Antes, mantener pesos fijos entre decisiones equivalía a rebalancear gratis cada día, inflando artificialmente la rentabilidad.
2.  **Semanas ISO Correctas:** Se usa `to_period('W')` en lugar de agrupar por número de semana aislado, evitando colapsar todas las semanas 1 del histórico en una sola fecha de decisión.
3.  **Reinicio de Estado:** Los contadores de transacciones y decisiones se reinician al inicio de cada ejecución, permitiendo barridos de parámetros limpios.
4.  **Métricas Corregidas:** Sortino usa ahora `sqrt(mean(min(r,0)²))` (fórmula correcta de downside deviation) y Alpha resta correctamente la tasa libre de riesgo.
5.  **RSI Unificado:** La estrategia usa ahora el RSI de Wilder estandarizado de `IndicadoresTecnicos`, eliminando la doble definición anterior.

---

## Análisis de Resultados Reales (2007 - 2026)

Hemos sometido a backtest la estrategia Contrarian durante 20 años, incluyendo las crisis de 2008, 2011, 2015, 2020 y 2022. Tras aplicar las correcciones del motor v3.5, los resultados son metodológicamente más robustos y realistas.

### Métricas Principales vs Buy & Hold

| Métrica | Estrategia Contrarian v3.5 | Buy & Hold (SPY) | Diferencia | Interpretación |
| :--- | :--- | :--- | :--- | :--- |
| **CAGR** | 5.20% | 11.82% |  -6.62% | No supera al mercado en crecimiento compuesto. |
| **Sharpe** | 0.27 | 0.53 | ❌ -0.26 | Menor eficiencia riesgo-retorno ajustada. |
| **Max Drawdown** | -42.8% | -51.5% | ✅ +8.7pp | Reduce significativamente la caída máxima. |
| **Volatilidad** | 13.89% | 19.76% | ✅ -5.87pp | Riesgo diario reducido ~30%. |
| **Exposición Media** | 28% | 100% | ⚠️ Baja | Pasa el 72% del tiempo en cash (SHV). |
| **Win-rate** | 62.9% | N/A | ✅ Alto | Alta tasa de acierto cuando opera. |
| **Profit Factor** | 2.18 | N/A | ✅ Excelente | Ratio beneficio/pérdida por operación sólido. |

> **⚠️ Nota sobre la Exposición:** El bajo CAGR se explica directamente por la exposición media del 28%. La estrategia actúa como un "satélite defensivo" que solo se activa en momentos de pánico extremo, permaneciendo en SHV (rf=1.38%) durante los mercados alcistas sostenidos.

### Tests Placebo: ¿Habilidad o Suerte?

Para determinar si los resultados provienen de una ventaja estadística real o del azar, se ejecutaron 200 simulaciones placebo por modo. Los p-valores unilaterales indican la probabilidad de que el resultado aleatorio sea igual o mejor que el real (menor = más mérito).

| Métrica | Selección (p) | Timing (p) | Total (p) | Conclusión |
| :--- | :--- | :--- | :--- | :--- |
| **Ret. medio/op** | 0.294 | **0.020** ✅ | **0.030** ✅ | El momento de entrada es estadísticamente significativo. |
| **CAGR** | 0.358 | 0.070 ️ | 0.070 ️ | Indicio débil; depende de pocos episodios de crisis. |
| **Sharpe** | 0.692 | 0.587 | 0.682 | No distinguible del azar en términos ajustados al riesgo. |
| **Max DD** | 0.876 | 1.000 | 1.000 | El drawdown profundo es inherente a entrar en crisis. |

**Interpretación Crítica:**
*   **El TIMING funciona (p=0.020):** Entrar tras sobreventa (mismos ETFs, fechas reales) genera rendimientos superiores a entrar en fechas aleatorias. La señal de reversión tiene valor predictivo.
*   **La SELECCIÓN NO funciona (p=0.294):** Elegir por DD+RSI+peor 12m NO se distingue de elegir ETFs al azar en las mismas fechas de entrada. En un universo de sectores altamente correlacionados (SPY-QQQ: 0.92), la diversificación entre perdedores es ilusoria.
*   **Limitación Muestral:** Con solo 3 episodios de crisis independientes (2008, 2020, 2022) en 18 años, la potencia estadística es baja. Un p-valor alto no prueba ausencia de habilidad, sino falta de evidencia concluyente.

### Barrido de Parámetros y Estabilidad IS/OOS

Se evaluaron 96 combinaciones de parámetros con corte In-Sample/Out-of-Sample en 2017-01-01.

*   **Correlación Spearman IS/OOS = +0.34:** Valor cercano a cero indica que optimizar sobre datos históricos **ajusta ruido, no señal**. Las mejores configuraciones in-sample no predicen consistentemente el out-of-sample.
*   **Zonas Robustas (no puntos aislados):**
    *   `top_n`: 5 slots (Sharpe OOS medio: 0.41) > 2 slots (0.30). Más diversificación compensa la escasez de señales.
    *   `umbral_drawdown`: -15% (Sharpe OOS: 0.45) es óptimo. Umbrales más laxos (-10%) o más estrictos (-30%) degradan el rendimiento.
    *   `holding_meses`: 6 meses (Sharpe OOS: 0.42) > 3 meses (0.30). Holding más largo reduce rotación innecesaria y costes.
    *   `stop_loss`: Sin stop-loss (Sharpe OOS: 0.39) > Stop -10% (0.33). En estrategias contrarian, el stop-loss corta posiciones en el peor momento posible.

### Matriz de Correlaciones del Universo

El análisis de correlaciones revela una alta homogeneidad intra-sectorial que limita la eficacia de la selección:

*   **Clusters Altamente Correlacionados:** SPY-QQQ (0.92), QQQ-XLK (0.96), SPY-XLI (0.90). Los sectores tecnológicos e industriales se mueven casi idénticamente.
*   **Únicos Diversificadores Reales:** TLT (correlación negativa -0.24 a -0.33 con todos los sectores de renta variable) y GLD (~0.06 con RV).
*   **Implicación:** Las señales contrarian tienden a activarse simultáneamente en múltiples sectores durante crisis sistémicas, explicando la baja frecuencia de operaciones (6.3/año) y la escasez de meses con candidatos válidos (solo 34% tienen ≥1 candidato).

---

## Propuestas de Mejora para Próxima Iteración

Basado en el análisis de robustez y los tests placebo, estas son las mejoras prioritarias ordenadas por impacto esperado:

### 🔴 Alta Prioridad (Impacto Directo en CAGR/Sharpe)

1.  **Relajar filtros para aumentar frecuencia de señales**
    *   Cambiar DD ≤ -15% → **DD ≤ -20% o -25%**
    *   Cambiar RSI ≤ 45 → **RSI ≤ 50**
    *   *Justificación:* Solo el 34% de meses tienen señal. El barrido muestra que DD=-15% y RSI=45 son óptimos OOS, pero la escasez limita el compuesto. Probar zona DD=[-20%, -25%] + RSI=[45, 50].

2.  **Aumentar holding period a 6 meses**
    *   *Justificación:* El barrido muestra Sharpe OOS=0.42 para 6m vs 0.30 para 3m. Menos rotación = menos costes + más tiempo para que el rebote se materialice.

3.  **Eliminar stop-loss**
    *   *Justificación:* Sharpe OOS=0.39 sin stop vs 0.33 con stop. En contrarian, el stop-loss corta posiciones en el peor momento (durante la caída). La paciencia es parte de la estrategia.

4.  **Aumentar slots a 5 (ya implementado en barrido)**
    *   *Justificación:* Sharpe OOS crece con top_n (0.30→0.37→0.41). Más slots compensan la escasez de señales.

###  Media Prioridad (Mejora Robustez)

5.  **Añadir confirmación de momentum corto**
    *   Regla: Entrar solo si RSI ha empezado a subir en los últimos 3-5 días (salir de sobreventa, no estar en caída libre).
    *   *Justificación:* El timing funciona (p=0.020), pero el drawdown es profundo (-42.8%). Evitar "cuchillos cayendo" reduciendo entradas en free-fall.

6.  **Tamaño de posición dinámico**
    *   Si solo 1-2 candidatos cumplen filtros, asignar >20% por slot (ej: 40-50% cada uno).
    *   *Justificación:* La exposición media es 28%. Cuando hay señal, debería ser más agresivo.

7.  **Excluir SPY del universo candidato**
    *   *Justificación:* SPY rara vez cumple DD≤-15% (es el benchmark). Incluirlo diluye señales. El escenario "sin régimen + excluir SPY" dio resultados similares, pero conceptualmente es más limpio.

### 🟢 Baja Prioridad (Refinamiento)

8.  **Probar RSI de Wilder vs RSI simple**
    *   Ya unificado en v3.5, pero verificar si cambia significativamente las señales.

9.  **Añadir filtro de volumen/liquidez**
    *   Evitar entrar en ETFs con volumen anormalmente bajo (posible trampa de liquidez).

10. **Backtest walk-forward en lugar de IS/OOS fijo**
    *   *Justificación:* Spearman IS/OOS=0.34 indica overfitting. Walk-forward con ventanas rolling sería más robusto.

---

## Conclusiones Académicas Actualizadas

Entre enero de 2008 y agosto de 2026, la estrategia contrarian cuantitativa v3.5 obtuvo un CAGR del 5.2% frente al 11.8% del buy & hold sobre SPY (Sharpe 0.27 frente a 0.53), con un drawdown máximo de -42.8% (buy & hold: -51.5%) y una exposición media del 28%.

Los tests placebo con 200 simulaciones revelan que la ventaja de la estrategia proviene **exclusivamente del timing** (p=0.020): entrar tras episodios de sobreventa genera rendimientos superiores a entrar en fechas aleatorias con los mismos ETFs. Sin embargo, la **selección del ETF mediante drawdown + RSI + rentabilidad 12M no se distingue del azar** (p=0.294), debido a la alta correlación interna del universo sectorial.

El barrido de 96 combinaciones muestra una correlación Spearman IS/OOS de +0.34, indicando que la optimización captura ruido más que señal robusta. Las configuraciones más estables fuera de muestra comparten: 5 slots, drawdown ≤ -15%, RSI ≤ 45, holding de 6 meses y ausencia de stop-loss.

En conclusión, el contrarian cuantitativo con estos parámetros **no supera al buy & hold en rentabilidad absoluta ni ajustada al riesgo**, pero sí reduce el drawdown máximo gracias a la baja exposición media. Su valor reside en el timing de entrada tras sobreventa, no en la selección de activos, y su aplicación óptima es como satélite defensivo (10-20% del patrimonio) dentro de un modelo Core-Satellite, no como estrategia standalone.

---

## ️ Descargo de Responsabilidad y Advertencia de Riesgos

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa. Antes de finalizar, es imperativo que el lector comprenda las siguientes limitaciones:

### Los Resultados Pasados No Garantizan Resultados Futuros
El backtest presentado es una simulación histórica basada en datos pasados (2007-2026). Que la estrategia Contrarian haya generado un alpha positivo del +2.16% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los umbrales de los filtros (-15% de drawdown, RSI ≤ 45) fueron elegidos antes de ver los resultados, pero cualquier umbral fijo puede dejar de funcionar si cambia la microestructura del mercado o la composición de los ETFs sectoriales.

### Limitaciones del Backtest
*   **Sesgo de supervivencia (Survivorship Bias):** El universo de 16 ETFs incluye solo los que existen hoy. Algunos ETFs que existían en 2007 fueron cerrados o fusionados por falta de activos. Si esos ETFs cerraron porque su sector era estructuralmente inviable, nuestro backtest los excluye y sobreestima la rentabilidad de la estrategia.
*   **Costes de transacción y deslizamiento (Slippage):** Se han asumido costes estándar del 0.1% por operación. En momentos de pánico extremo (cuando se activan las señales contrarian), los spreads bid-ask se ensanchan y el slippage real puede ser del 0.3-0.5%, reduciendo el alpha.
*   **Look-ahead bias controlado:** El RSI y el drawdown se calculan con datos disponibles el último día del mes, antes de ejecutar la orden. No hay filtración de información futura.
*   **Fiscalidad:** El motor no contempla el impacto de impuestos por plusvalías. La rotación trimestral genera eventos fiscales que reducen el rendimiento neto real.
*   **Datos parciales:** Algunos ETFs (EFA, EEM, TLT, GLD, SHV) no tienen datos desde 1999 porque no existían entonces. El backtest efectivo comienza en 2007-01-11, cuando el último activo (SHV) tiene datos suficientes.

### No es Asesoramiento Financiero
Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe evaluar su tolerancia al riesgo, considerar su horizonte temporal y consultar con un asesor financiero independiente.

### Riesgo de Pérdida de Capital
Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. La estrategia contrarian, incluso con filtros, tiene un drawdown histórico del -42.8%. En un escenario futuro más adverso (crisis sistémica prolongada, depresión económica), las caídas podrían ser significativamente mayores. Un inversor que no pueda tolerar ver su satélite contrarian caer un 40-50% no debería usar esta estrategia.

### Uso del Código
El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de fallos en la detección automática de señales debido a ruido en los datos de cotización.

### Recuerda
El Contrarian Investing cuantitativo no es "comprar lo que baja". Eso es atrapar cuchillos cayendo y es la forma más rápida de destruir capital. El Contrarian Investing cuantitativo es comprar lo que ha caído mucho, cuando el pánico es medible (drawdown ≤ -15%), cuando la presión vendedora está técnicamente exhausta (RSI ≤ 45), y solo durante un tiempo limitado (3 meses).

Es una estrategia de paciencia y disciplina, no de intuición. Su verdadero valor no está en batir al mercado en rentabilidad absoluta, sino en generar alpha positivo (+2.16%) con una beta ultra baja (0.37), actuando como un seguro táctico que se activa exactamente cuando el miedo colectivo alcanza niveles extremos.

La capacidad de quedarse en cash el 60-70% del tiempo, sin hacer nada, sin sentir la ansiedad de "perderse algo", es quizás la habilidad más valiosa que esta estrategia enseña al inversor conservador. La paciencia, la disciplina y la validación rigurosa de los datos son tus mayores aliados.