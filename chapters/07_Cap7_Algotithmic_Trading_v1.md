Capítulo 7: Algorithmic Trading con Machine Learning — Random Forest sobre SPY
Versión: 7.2 | Motor: Modular Dinámico v1.0 | Actualización: 2026-10-26

    "El machine learning no predice el futuro. Encuentra patrones en el pasado que, con suerte, se repetirán. La diferencia entre un modelo útil y una máquina de overfitting es la disciplina de validación."
    — Marcos López de Prado, Advances in Financial Machine Learning

Concepto clave: Este capítulo abandona las reglas fijas de los capítulos anteriores (medias móviles, z-scores, momentum) y las sustituye por un modelo de aprendizaje automático (Random Forest) que aprende a predecir si el SPY subirá o bajará en los próximos 21 días, basándose en un conjunto de features técnicas (momentum, volatilidad, distancia a medias móviles, RSI). Cuando el modelo tiene alta confianza en una subida, invertimos en SPY; cuando no, rotamos a SHV (bonos a corto plazo, proxy de efectivo).
La premisa es ambiciosa pero realista: no buscamos predecir el mercado con precisión sobrenatural, sino identificar regímenes de alta probabilidad donde la relación riesgo/recompensa favorece estar invertido. El modelo se reentrena periódicamente (walk-forward) para adaptarse a cambios en la dinámica del mercado, evitando el overfitting estático.
Pero aquí viene la advertencia crítica que diferencia este capítulo de los manuales de trading con IA: un modelo con 64.7% de accuracy que predice "subida" en el 87% de los casos no es un modelo útil para timing de mercado. Es un modelo que ha aprendido el sesgo alcista histórico del SPY y lo explota, pero no aporta información marginal sobre cuándo retirarse. Este capítulo documenta ese riesgo con total transparencia, usando resultados reales de backtest.
La Lógica del Algorithmic Trading con ML
A diferencia del trading direccional basado en reglas fijas (Capítulos 1-6), el Algorithmic Trading con ML utiliza un modelo de aprendizaje automático para identificar patrones no lineales en los datos históricos que puedan tener poder predictivo sobre el movimiento futuro del mercado.
Las tres condiciones para operar

  Condición | Umbral | ¿Qué mide? |
 |---|---|---|
 | 1. Confianza alta del modelo | P(subida) > 0.55 | El modelo predice subida con alta probabilidad. |
 | 2. Confianza baja del modelo | P(subida) < 0.45 | El modelo predice bajada o incertidumbre. |
 | 3. Zona de incertidumbre | 0.45 ≤ P(subida) ≤ 0.55 | El modelo no tiene confianza; posición 50/50. |

 Si el modelo tiene alta confianza en una subida, invertimos 100% en SPY. Si tiene baja confianza, rotamos a SHV (efectivo). En la zona de incertidumbre, mantenemos 50% en cada activo.
Reglas operativas completas

  Parámetro | Valor |
 |---|---|
 | Universo | SPY (S&P 500) + SHV (iShares 1-3 Year Treasury Bond) |
 | Modelo | Random Forest Classifier (100 árboles, max_depth=5) |
 | Features | ret_1m, ret_3m, ret_6m, vol_20d, vol_60d, dist_sma50, dist_sma200, rsi_14 |
 | Target | ¿Subirá el SPY en los próximos 21 días? |
 | Frecuencia de reentrenamiento | Cada 63 días (~3 meses) |
 | Umbral confianza alta | 0.55 |
 | Umbral confianza baja | 0.45 |
 | Coste de transacción | 0,1% por operación |
 | Benchmark | SPY (Buy & Hold) |

 Observa la diferencia fundamental con los capítulos anteriores: no hay reglas fijas. El modelo aprende qué combinaciones de features predicen subidas o bajadas, basándose en datos históricos. Pero aquí viene el problema: si el mercado tiene un sesgo alcista fuerte (~69% de los períodos de 21 días son alcistas en nuestra muestra), un modelo naive que siempre predice "sube" ya tiene 69% de accuracy. Superar ese baseline de forma consistente requiere features con poder predictivo real, no solo ruido técnico.
Arquitectura Técnica (Motor Dinámico v1.0 + Walk-Forward)
El motor cuantitativo de este libro incorpora un módulo de Machine Learning basado en RandomForestClassifier de scikit-learn, diseñado específicamente para series temporales financieras con validación walk-forward. Este módulo implementa:

    Ingeniería de Features: Calcula 8 features técnicas (momentum a 1/3/6 meses, volatilidad a 20/60 días, distancia a medias móviles de 50/200 días, RSI de 14 días).
    Target Binario: Define el target como 1 si el SPY sube en los próximos 21 días, 0 si baja.
    Entrenamiento Walk-Forward: Reentrena el modelo cada 63 días usando todos los datos disponibles hasta esa fecha, evitando look-ahead bias.
    Predicción de Probabilidades: El modelo no predice "sube/baja", sino la probabilidad de subida, permitiendo umbrales de confianza.

Para el backtest, el MotorBacktestDinamico acepta una función generadora de pesos que consulta las probabilidades predichas por el modelo en cada fecha y asigna pesos a SPY o SHV según los umbrales de confianza.

Análisis de Resultados Reales (2010 - 2026)
Hemos sometido a backtest la estrategia ML durante un período de 16 años que incluye la recuperación post-2008, la Crisis de la Deuda Soberana (2010-2012), la Pandemia COVID-19 (2020), la crisis inflacionaria (2022-2023) y el rally de la IA (2024-2026).
Informe de Limpieza de Datos

💡 Insight Clave: Ambos activos tienen datos completos desde el inicio del período, lo que garantiza que el modelo ML pueda entrenarse correctamente y que la rotación a SHV sea viable.
Métricas de Diagnóstico Comparativo (Resultados Reales)

  Activo | ISIN | Filas | Desde | Hasta | Fuente |
 |---|---|---|---|---|---|
 | SPDR S&P 500 | SPY | 4,228 | 2010-01-04 | 2026-10-23 | CSV |
 | iShares 1-3 Year Treasury | SHV | 4,228 | 2010-01-04 | 2026-10-23 | CSV |

 *Nota: El patrimonio final del SPY se estima a partir del CAGR del 13.98% sobre €10,000 durante 16 años.
Diagnóstico Automático
El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:

    🟢 Ratio de Sharpe bueno (0.69): La estrategia generó valor de manera eficiente, aunque ligeramente inferior al B&H (0.70).
    ⚠️ Max Drawdown controlado (-31.61%): Inferior al del SPY (-33.72%), pero sigue siendo significativo.
    ️ CAGR inferior (12.53% vs 13.98%): El modelo ML no logró superar al Buy & Hold en rentabilidad anualizada.

Análisis de la Matriz de Confusión (Crítico)
La métrica más reveladora de este capítulo no es el CAGR ni el Sharpe, sino la matriz de confusión del modelo:

Matriz de confusión (período completo):
              Predicho
              Subida  Bajada
Real  Subida   2387    212
      Bajada   1123     55

Accuracy: 64.7%

Interpretación detallada:

| Métrica | Valor | Interpretación |
| :--- | :--- | :--- |
| **Verdaderos positivos** | 2,387 | Predijo subida y el mercado subió |
| **Falsos negativos** | 212 | Predijo bajada pero el mercado subió |
| **Falsos positivos** | 1,123 | Predijo subida pero el mercado bajó |
| **Verdaderos negativos** | 55 | Predijo bajada y el mercado bajó |
| **Precisión "Subida"** | 68% | Cuando predice subida, acierta 68% de las veces |
| **Precisión "Bajada"** | 21% | Cuando predice bajada, acierta solo 21% de las veces |
| **Recall "Subida"** | 92% | Detecta 92% de las subidas reales |
| **Recall "Bajada"** | 5% | Detecta solo 5% de las bajadas reales |

 Alerta Crítica: El modelo predice "subida" en el 87.1% de los casos (3,510 de 4,029). Solo predice 519 bajadas (12.9%). Esto confirma que el modelo no está haciendo timing de mercado, sino explotando el sesgo alcista histórico del SPY.
Reporte de clasificación completo:

| Clase | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| Bajada (0) | 0.21 | 0.05 | 0.08 | 1,178 |
| Subida (1) | 0.68 | 0.92 | 0.78 | 2,599 |
| **Accuracy** | — | — | 0.65 | 3,777 |
| **Macro avg** | 0.44 | 0.48 | 0.43 | 3,777 |
| **Weighted avg** | 0.53 | 0.65 | 0.56 | 3,777 |

¿Por qué entonces el CAGR es inferior al B&H?
El modelo predice "subida" en el 87% de los casos, pero en el 13% restante (cuando predice "bajada"), rota a SHV. El problema es que muchas de esas rotaciones a SHV ocurren en momentos donde el mercado sigue subiendo (212 falsos negativos), perdiendo oportunidades de ganancia. Además, las pocas veces que acierta una bajada (55 verdaderos negativos), la protección no compensa las oportunidades perdidas.
Feature Importance
El modelo revela qué variables considera más importantes para predecir la dirección del mercado:

| Feature | Importancia | Interpretación |
| :--- | :---: | :--- |
| **dist_sma50** | 0.1492 | La distancia al SMA de 50 días es la feature más predictiva |
| **ret_3m** | 0.1413 | El momentum a 3 meses confirma la importancia de la tendencia |
| **vol_20d** | 0.1389 | La volatilidad reciente ayuda a filtrar falsas señales |
| **ret_6m** | 0.1342 | El momentum a 6 meses también es relevante |
| **dist_sma200** | 0.1066 | La distancia al SMA de 200 días tiene menor importancia |

💡 Insight Clave: Las features con mayor importancia son las que el modelo considera más útiles para predecir la dirección del mercado. En mercados eficientes, esperamos que el Momentum (ret_3m) y la Volatilidad (vol_20d) dominen, confirmando lo visto en los Capítulos 3 y 4.
Análisis de la Distribución de Probabilidades
La distribución de probabilidades predichas por el modelo revela su nivel de confianza:

| Estadística | Valor | Interpretación |
| :--- | :---: | :--- |
| **Media** | 0.674 | El modelo tiende fuertemente a predecir subidas |
| **Mediana** | 0.687 | Más del 50% de las predicciones son > 0.65 |
| **Desv. estándar** | 0.109 | Moderada dispersión, pero insuficiente para timing |
| **Mínimo** | 0.222 | Algunas predicciones de baja confianza |
| **Máximo** | 0.949 | Alta confianza en algunas subidas |

⚠️ Advertencia: La media de 0.674 está muy por encima del umbral de confianza alta (0.55), lo que explica por qué el modelo pasa el 90.9% del tiempo en SPY. Los umbrales de entrada/salida (0.55 y 0.45) pierden utilidad cuando la distribución está tan sesgada.
Tiempo en SPY vs SHV

| Métrica | Valor |
| :--- | :---: |
| **Tiempo en SPY** | 90.9% |
| **Tiempo en SHV** | 2.8% |
| **Tiempo en transición** | 6.3% |

⚠️ Advertencia: La estrategia pasa el 90.9% del tiempo en SPY. Esto confirma que el modelo no está realmente haciendo timing de mercado. La estrategia es esencialmente Buy & Hold con pequeñas excepciones donde rota a SHV.
Accuracy Rolling (252 días)
El gráfico de accuracy rolling revela que el modelo tiene períodos de buen rendimiento (accuracy > 0.70 en 2014-2018) pero también períodos de mal rendimiento (accuracy < 0.50 en 2022-2023). Esto sugiere que el modelo funciona bien en ciertos regímenes de mercado pero falla en otros, particularmente en períodos de alta volatilidad o cambios de régimen.
¿Por qué el ML NO superó al Buy & Hold?
Los datos muestran algo contraintuitivo: el modelo tiene una accuracy del 64.7%, pero predice "subida" en el 87% de los casos, y aún así genera un CAGR inferior al B&H (12.53% vs 13.98%). ¿Por qué?

    El sesgo alcista del SPY: El SPY sube en el 68.7% de los períodos de 21 días. Un modelo naive que siempre predice "sube" ya tiene 68.7% de accuracy. El modelo ML empeora eso al 64.7%, lo que sugiere que está empeorando la predicción al intentar ser más sofisticado.
    Las rotaciones a SHV son contraproducentes: Cuando el modelo predice "bajada" (13% de los casos), muchas veces el mercado sigue subiendo (212 falsos negativos de 3,777 = 5.6% del tiempo). Esas rotaciones prematuras a SHV hacen perder oportunidades de ganancia.
    El modelo no predice bien las bajadas: Solo detecta 55 de cada 1,178 bajadas reales (recall del 4.7%). Esto significa que cuando el mercado cae, el modelo casi nunca lo anticipa, por lo que no protege el capital en los momentos críticos.
    El walk-forward no es suficiente: Reentrenar el modelo cada 63 días permite adaptarse a cambios en la dinámica del mercado, pero no garantiza que el modelo aprenda patrones útiles. Si los features no tienen poder predictivo real, el walk-forward solo produce ruido.
    Costes de transacción: Con 277 rebalanceos en 16 años, los costes de transacción (0.1% por operación) erosionan el capital. Aunque no es el factor principal, contribuye a la inferioridad del ML.

La Ventaja Real del ML (Matizada)
Los datos de este período (2010-2026) nos obligan a ser honestos sobre las limitaciones y fortalezas reales del Algorithmic Trading con ML:

| Ventaja real | Evidencia |
| :--- | :--- |
| ✅ **Menor volatilidad** | 15.33% vs 17.03% (-10%) |
| ✅ **Menor drawdown** | -31.61% vs -33.72% (-6%) |
| ✅ **Menor VaR 95%** | €1,057 vs €1,471 (-28%) |
| 🔴 **CAGR inferior** | 12.53% vs 13.98% (-1.45% anualizado) |
| ⚖️ **Sharpe prácticamente igual** | 0.69 vs 0.70 |
| ⚠️ **Accuracy engañosa** | 64.7% pero con sesgo fuerte hacia "subida" (87%) |
| ❌ **No hace timing real** | 90.9% del tiempo en SPY, solo 2.8% en SHV |
| ❌ **No predice bajadas** | Recall del 4.7% para la clase "bajada" |

Conclusión matizada: El ML logró reducir ligeramente la volatilidad y el drawdown, pero no logró superar al Buy & Hold en rentabilidad. La estrategia es esencialmente Buy & Hold con un filtro de protección ocasional que, paradójicamente, reduce la rentabilidad al rotar a SHV en momentos inoportunos.
Limitaciones Críticas para Producción
1. Accuracy Engañosa y Sesgo de Predicción
La accuracy del 64.7% parece buena, pero la matriz de confusión revela que el modelo predice "subida" en el 87% de los casos. Esto indica que:

    El modelo ha aprendido el sesgo alcista histórico del SPY (~69% de períodos alcistas).
    No aporta información marginal sobre cuándo retirarse del mercado.
    La estrategia es esencialmente "Buy & Hold con pequeñas excepciones contraproducentes".

2. CAGR Inferior al Buy & Hold
El modelo ML generó un CAGR del 12.53% vs 13.98% del B&H. Esto significa que:

    El modelo destruyó valor en términos de rentabilidad anualizada.
    Las rotaciones a SHV no compensaron las oportunidades perdidas.
    En este período específico, el ML fue perjudicial para el inversor.

3. No Predice Bajadas
El recall del 4.7% para la clase "bajada" significa que el modelo casi nunca anticipa caídas. Esto es crítico porque:

    El objetivo principal del ML debería ser proteger el capital en caídas.
    Si no predice bajadas, no puede rotar a SHV a tiempo.
    El modelo es inútil para su propósito declarado (timing de mercado).

4. Overfitting Potencial
Con ~4,000 observaciones y 8 features, el riesgo de overfitting es significativo. El walk-forward ayuda, pero no elimina el problema si los features no tienen poder predictivo real.
5. Features Retrospectivos
Los features técnicos (momentum, RSI, distancia a medias móviles) son indicadores retrospectivos que no predicen el futuro de forma fiable. En mercados eficientes, la información pública (precios históricos) ya está incorporada en los precios actuales.
6. Costes de Transacción
Con 277 rebalanceos en 16 años, los costes de transacción (0.1% por operación) erosionan el capital. Aunque no es el factor principal, contribuye a la inferioridad del ML.
Recomendaciones para Producción Real
Si quieres usar ML para timing de mercado en la vida real, necesitas:
1. Features con Poder Predictivo Real
Los features técnicos actuales (momentum, volatilidad, RSI) tienen poder predictivo limitado. Considera:

    Datos alternativos: Sentimiento de redes sociales, flujos de fondos, datos macroeconómicos.
    Features de microestructura: Order flow, bid-ask spread, volumen relativo.
    Features de volatilidad implícita: VIX, skew, term structure de opciones.

2. Validación Rigurosa

    Walk-forward con múltiples ventanas: No solo un esquema expansivo, sino múltiples ventanas rolling para validar robustez.
    Test de significancia estadística: ¿El alpha es real o ruido? Usa tests de bootstrap o placebos.
    Análisis de robustez a diferentes períodos y parámetros: Si el modelo solo funciona en un período específico, es overfitting.

3. Gestión de Riesgo Estricta

    Stop-loss dinámicos: No confíes solo en el modelo; implementa stop-loss basados en ATR o drawdown máximo.
    Límites de exposición: Limita la exposición máxima a un solo activo o sector.
    Diversificación entre múltiples modelos: No pongas todos los huevos en la cesta de un solo modelo ML.

4. Expectativas Realistas

    No esperes accuracy > 60% de forma consistente: En mercados eficientes, superar el 55% de accuracy es extremadamente difícil.
    El edge real está en la gestión de riesgo, no en la predicción: Un modelo con 55% de accuracy pero con excelente gestión de riesgo puede ser más rentable que un modelo con 65% de accuracy pero con gestión de riesgo deficiente.
    El ML es un complemento, no un reemplazo de la disciplina de inversión: No abandones la asignación de activos a largo plazo (Capítulos 1-5) por un modelo ML.

5. Considera Alternativas Simples
Antes de usar ML complejo, considera estrategias simples que han demostrado funcionar:

    Filtro SMA 200: Rotar a efectivo cuando el precio está por debajo de la media móvil de 200 días.
    Momentum cross-sectional: Rotar entre activos basándose en su momentum relativo.
    Asignación de activos estática: 60/40 o cartera all-weather con rebalanceo periódico.

Estas estrategias simples pueden superar al ML en términos de rentabilidad ajustada al riesgo, con mucha menos complejidad y riesgo de overfitting.
Conclusiones
El análisis de Algorithmic Trading con Machine Learning en el período 2010-2026 arroja lecciones humildes pero valiosas:

    El ML no es una bala de plata: Un modelo con 64.7% de accuracy que predice "subida" en el 87% de los casos no es un modelo útil. Es un modelo que ha aprendido el sesgo alcista histórico y lo explota, pero no aporta información marginal sobre cuándo retirarse. En este caso específico, el ML destruyó valor al generar un CAGR inferior al Buy & Hold (12.53% vs 13.98%).
    La matriz de confusión es más informativa que la accuracy: Revela si el modelo realmente distingue entre clases o simplemente predice la clase mayoritaria. En este caso, el modelo predice "subida" en el 87% de los casos y tiene un recall del 4.7% para la clase "bajada", confirmando que no está haciendo timing de mercado real.
    El timing de mercado es extremadamente difícil: El SPY tiene un sesgo alcista fuerte (~69% de períodos de 21 días alcistas), y superarlo de forma consistente requiere features con poder predictivo real, no solo ruido técnico. El modelo ML no logró mejorar el CAGR ni el Sharpe, aunque sí redujo ligeramente la volatilidad y el drawdown.
    El walk-forward es crítico pero no suficiente: Reentrenar periódicamente evita el overfitting estático, pero no garantiza que el modelo aprenda patrones útiles. Si los features no tienen poder predictivo real, el walk-forward solo produce ruido.
    La disciplina de asignación de activos sigue siendo rey: El ML puede ser un complemento, pero no reemplaza la disciplina de la asignación de activos a largo plazo (Capítulos 1-5). La estrategia ML es esencialmente Buy & Hold con un filtro de protección ocasional que, en este caso, fue contraproducente.
    La feature importance confirma lo que ya sabíamos: Las features con mayor importancia (dist_sma50, ret_3m, vol_20d) son consistentes con los hallazgos de los Capítulos 3 y 4 (momentum y volatilidad son predictivos). Pero su poder predictivo es limitado, no suficiente para generar alpha significativo de forma consistente.
    La accuracy rolling revela inestabilidad: El modelo funciona bien en ciertos períodos (2014-2018) pero falla en otros (2022-2023), sugiriendo que no es robusto a cambios de régimen de mercado.

La filosofía del Algorithmic Trading con ML, democratizada a través de este motor cuantitativo, demuestra que la tecnología por sí sola no garantiza el éxito. Se necesitan features con poder predictivo real, validación rigurosa, y sobre todo, humildad ante la complejidad del mercado. El ML no ha descubierto la piedra filosofal; ha aprendido que la volatilidad y el momentum importan, pero que el ruido del mercado hace que su precisión ronde el 64.7%, lo que, tras costes de transacción y rotaciones contraproducentes, genera un CAGR inferior al Buy & Hold.
Descargo de Responsabilidad y Advertencia de Riesgos
Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa.
Los Resultados Pasados No Garantizan Resultados Futuros
El backtest presentado es una simulación histórica basada en datos pasados (2010-2026). Que el modelo ML haya generado un CAGR del 12.53% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los modelos ML son particularmente susceptibles al overfitting, y un modelo que funciona bien en datos históricos puede fallar catastróficamente en datos futuros. En este caso, el modelo no solo no superó al Buy & Hold, sino que generó un CAGR inferior, demostrando que el ML puede ser perjudicial si no se implementa correctamente.
Limitaciones del Backtest

    Overfitting: Con ~4,000 observaciones y 8 features, el riesgo de overfitting es significativo. El walk-forward ayuda, pero no elimina el problema si los features no tienen poder predictivo real.
    Sesgo de supervivencia: El SPY es un índice resiliente con sesgo alcista histórico. Aplicar este modelo a activos individuales o sectores cíclicos conlleva un riesgo mucho mayor.
    Costes de transacción: Se han asumido costes estándar del 0.1% por operación. En momentos de alta volatilidad, los spreads bid-ask se ensanchan y el slippage real puede ser mayor.
    Fiscalidad: El motor no contempla el impacto de impuestos por ventas a corto plazo (frecuencia diaria).
    Features retrospectivos: Los features técnicos (momentum, RSI, distancia a medias móviles) son indicadores retrospectivos que no predicen el futuro de forma fiable.
    Accuracy engañosa: La accuracy del 64.7% oculta un sesgo fuerte hacia predecir "subida" (87% de los casos), lo que limita la utilidad del modelo para timing de mercado.
    CAGR inferior al B&H: El modelo ML generó un CAGR del 12.53% vs 13.98% del Buy & Hold, demostrando que el ML puede destruir valor si no se implementa correctamente.

No es Asesoramiento Financiero
Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. La estrategia de timing de mercado con ML es de alto riesgo y no se recomienda para inversores sin experiencia avanzada en ML y finanzas.
Riesgo de Pérdida de Capital
Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. Aunque el modelo ML tiene un Max Drawdown ligeramente inferior al SPY en el backtest (-31.61% vs -33.72%), la rentabilidad es inferior (12.53% vs 13.98%) y el riesgo de overfitting es alto.
Uso del Código
El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de la exactitud de las métricas calculadas.
Recuerda
El Algorithmic Trading con Machine Learning no es "predecir el futuro con IA". Es:

    Identificar features con poder predictivo real (no solo ruido técnico).
    Validar rigurosamente el modelo con walk-forward y test de significancia.
    Gestionar el riesgo de forma estricta (stop-loss, límites de exposición).

Es una estrategia de disciplina estadística y gestión de riesgo, no de predicción sobrenatural. Su verdadero valor no está en maximizar el CAGR, sino en identificar regímenes de alta probabilidad donde la relación riesgo/recompensa favorece estar invertido.
La lección más importante de este capítulo: el ML es un complemento, no un reemplazo de la disciplina de inversión. Un modelo con 64.7% de accuracy que predice "subida" en el 87% de los casos no es un modelo útil. Es un modelo que ha aprendido el sesgo alcista histórico y lo explota, pero no aporta información marginal sobre cuándo retirarse. En este caso específico, el ML generó un CAGR inferior al Buy & Hold (12.53% vs 13.98%), demostrando que el ML puede ser perjudicial si no se implementa correctamente.
La paciencia, la disciplina estadística y la humildad ante la complejidad del mercado son tus mayores aliados. El "límite del motor" no es la potencia de cálculo, es la naturaleza de los datos: la ratio señal/ruido en los mercados financieros es tan baja que incluso los modelos más sofisticados apenas logran superar el 55-65% de accuracy de forma consistente, y en muchos casos, como este, generan un CAGR inferior al Buy & Hold.
Antes de usar ML complejo, considera estrategias simples: Un filtro SMA 200 o una asignación de activos estática (60/40) pueden superar al ML en términos de rentabilidad ajustada al riesgo, con mucha menos complejidad y riesgo de overfitting. La sofisticación no garantiza el éxito; la disciplina sí.

