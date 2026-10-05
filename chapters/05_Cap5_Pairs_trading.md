# Capítulo 5: Pairs Trading — La danza de los correlacionados
Versión: 5.1 | Motor: Modular Dinámico v1.0 | Última actualización: 2026-10-04

    "En el arbitraje estadístico, no apostamos a la dirección del mercado, sino a que la relación histórica entre dos activos se mantendrá. Es una apuesta sobre la estabilidad, no sobre el futuro."
    — Ernie Chan, Quantitative Trading

Si los capítulos anteriores nos enseñaron a navegar el mercado como un todo (All Weather, Contrarian, Momentum), el Pairs Trading representa un cambio de paradigma radical: dejamos de mirar el mercado y empezamos a mirar las relaciones matemáticas entre activos individuales. El objetivo: generar rentabilidad descorrelada del mercado (alpha puro) mediante el arbitraje estadístico.
La premisa es contraintuitiva pero matemáticamente sólida: cuando dos activos están cointegrados (mantienen una relación estable a largo plazo), cualquier desviación temporal de esa relación es una oportunidad de arbitraje. Si el spread se abre demasiado, apostamos a que volverá a cerrarse. No nos importa si el mercado sube o baja; solo nos importa que la relación entre los dos activos se mantenga.
Pero aquí viene la advertencia crítica que diferencia este capítulo de los manuales de trading ingenuos: la cointegración no es una propiedad mágica ni permanente. Dos activos pueden estar cointegrados durante una década y romper su relación al año siguiente. Por eso, el Pairs Trading profesional no se basa en la intuición ("estas dos empresas son similares"), sino en el test estadístico de Engle-Granger, que valida matemáticamente si la relación es estacionaria.
Este capítulo cuantifica esa disciplina con reglas estrictas.

## La Lógica del Pairs Trading

A diferencia del trading direccional (que apuesta a que un activo subirá o bajará), el Pairs Trading es market-neutral: simultáneamente compramos un activo y vendemos otro, de modo que la exposición neta al mercado sea cero.

## Las tres condiciones para operar

| Condición | Umbral | ¿Qué mide? |
|------------|---------|------------|
| **1. Cointegración estadística** | p-valor < 0,15 (Test de Engle-Granger) | Verifica que existe una relación de equilibrio de largo plazo entre ambos activos y que el spread es estacionario. |
| **2. Z-score del spread** | \(|z| > 2,0\) | Detecta desviaciones extremas del spread respecto a su media histórica, generando señales de entrada. |
| **3. Mean Reversion** | \(|z| < 0,5\) | Confirma que el spread ha convergido nuevamente hacia su valor de equilibrio, generando la señal de salida. |

Si un par no cumple la condición 1, no se opera, independientemente de lo "similar" que parezcan las dos empresas. La condición 2 activa la posición (largo en el barato, corto en el caro). La condición 3 cierra la posición cuando el spread ha revertido.

## Reglas operativas completas


| Parámetro | Valor |
|------------|--------|
| **Universo** | 3 pares candidatos: KO/PEP, EWA/EWC y GLD/GDX |
| **Frecuencia de revisión** | Diaria |
| **Umbral de entrada** | \(|z\text{-score}| > 2.0\) |
| **Umbral de salida** | \(|z\text{-score}| < 0.5\) |
| **Umbral de stop-loss** | \(|z\text{-score}| > 3.5\) (ruptura estructural) |
| **Máximo de pares simultáneos** | 3 |
| **Tamaño por posición** | 20% del capital |
| **Coste de transacción** | 0,1% por operación |
| **Benchmark** | SPY (S&P 500) |

**Observa la asimetría:** la estrategia no predice la dirección del mercado. Solo predice que el spread entre dos activos cointegrados volverá a su media histórica. Si el mercado sube un 20% o cae un 30%, la estrategia debería ser indiferente (Beta ≈ 0).

## Arquitectura Técnica (Motor Dinámico v1.0 + Gemelólogo)## 

El motor cuantitativo de este libro incorpora un módulo especializado llamado Gemelólogo (core/gemelologo.py), diseñado específicamente para el análisis de cointegración. Este módulo implementa:

* **Test de Engle-Granger:** Valida estadísticamente si dos series temporales están cointegradas (p-valor < umbral).
* **Cálculo de Z-score:** Normaliza el spread sobre una ventana móvil de 60 días para identificar desviaciones extremas.
* **Detección de ruptura estructural:** Usa el test ADF (Augmented Dickey-Fuller) rolling para detectar si el spread ha perdido estacionariedad.

Para el Pairs Trading, el MotorBacktestDinamico acepta una función generadora de pesos que evalúa diariamente el z-score de cada par válido. Cuando |z| > 2.0, la función asigna pesos positivos al activo barato y negativos al caro (posición market-neutral). Cuando |z| < 0.5, cierra la posición.

## El problema del whipsaw en Pairs Trading

Durante el desarrollo de este capítulo, detectamos que el generador de pesos estaba reasignando posiciones todos los días (687 rebalanceos en 10 años), generando costes de transacción acumulados de 1,371 € (13.7% del capital inicial). Este exceso de rotación se debía a que los umbrales de entrada/salida (2.0/0.5) eran demasiado estrechos para la volatilidad residual de los spreads.
**La lección:** En Pairs Trading, los costes de transacción son el enemigo silencioso. Un par puede estar cointegrado y generar señales válidas, pero si el spread no tiene suficiente amplitud para compensar el 0.2% de coste por operación (ida y vuelta), la estrategia erosionará el capital.

## Análisis de Resultados Reales (2010 - 2020)

Hemos sometido a backtest la estrategia Pairs Trading durante un período de 10 años que incluye la recuperación post-crisis financiera (2010-2014), el período de tipos bajos (2015-2019) y la Pandemia COVID-19 (2020).

### Informe de Limpieza de Datos

| Activo | Ticker | Filas | Desde | Hasta | Fuente |
|---------|:------:|------:|------------|------------|--------|
| Coca-Cola | KO | 2.595 | 2010-09-09 | 2020-12-29 | CSV |
| PepsiCo | PEP | 2.595 | 2010-09-09 | 2020-12-29 | CSV |
| iShares MSCI Australia ETF | EWA | 2.595 | 2010-09-09 | 2020-12-29 | CSV |
| iShares MSCI Canada ETF | EWC | 2.595 | 2010-09-09 | 2020-12-29 | CSV |
| SPDR Gold Trust | GLD | 2.595 | 2010-09-09 | 2020-12-29 | CSV |
| VanEck Gold Miners ETF | GDX | 2.595 | 2010-09-09 | 2020-12-29 | CSV |

**Insight Clave:** Los 6 activos tienen datos completos desde el inicio del período, lo que garantiza que los tests de cointegración se calculen correctamente.

**Escaneo de Cointegración:** El Filtro Matemático

Antes de ejecutar el backtest, el Gemelólogo escaneó los 3 pares candidatos con un umbral de p-valor < 0.15:

| Par | p-valor | ¿Cointegrado? | Decisión |
|------|:------:|:-------------:|-----------|
| **Coca-Cola / PepsiCo (KO / PEP)** | **0,002** | ✅ Sí | **Operar** |
| **iShares MSCI Australia / iShares MSCI Canada (EWA / EWC)** | **0,072** | ✅ Sí | **Operar** |
| SPDR Gold Trust / Gold Miners (GLD / GDX) | 0,319 | ❌ No | **Descartado** |

**💡 Lección pedagógica:** El par GLD/GDX fue rechazado correctamente por el sistema. Un p-valor de 0.319 indica que el spread entre el oro físico y las mineras no fue estacionario en esta década. Operar este par habría sido una apuesta especulativa, no arbitraje estadístico. El filtro matemático protegió al inversor de una operación perdedora.

## Métricas de Diagnóstico Comparativo

| Métrica | Pairs Trading | Buy & Hold (SPY) | ¿Qué significa para ti? |
|----------|-------------:|-----------------:|-------------------------|
| **Patrimonio Final** | 9.552 € | 25.900 € | ❌ Pairs Trading pierde un 4,47%, mientras SPY gana aproximadamente un 159%. |
| **CAGR** | -0,44% | 9,63% | ❌ Rentabilidad anualizada negativa frente a una rentabilidad claramente positiva del benchmark. |
| **Volatilidad** | 1,55% | 14,96% | ✅ Aproximadamente un 90% menos de oscilación diaria. |
| **Ratio de Sharpe** | -1,57 | 0,51 | ❌ Relación riesgo-retorno negativa. |
| **Ratio de Sortino** | -1,18 | 0,61 | ❌ Peor comportamiento frente al riesgo bajista. |
| **Max Drawdown** | -7,72% | -32,70% | ✅ Un 76% menos de caída máxima que el mercado. |
| **VaR 95% diario** | 5,86 € | 358,40 € | ✅ Aproximadamente un 98% menos de riesgo extremo diario. |
| **Alpha** | -0,00 | 0,00 | ⚖️ No se observa generación de valor añadido ajustado al riesgo. |
| **Beta** | -0,01 | 0,00 | ✅ Estrategia prácticamente market-neutral (Beta ≈ 0). |
| **R²** | 0,01 | 0,00 | ✅ El 99% del comportamiento es independiente del mercado. |
| **Tracking Error** | 17,31% | 0,00% | ⚠️ Elevada desviación respecto al benchmark. |
| **Coste total de rebalanceos** | 1.371,49 € | 0,00 € | ❌ Costes acumulados equivalentes a aproximadamente el 13,7% del capital inicial. |
| **Rebalanceos totales** | 687 | 0 | ❌ Cerca de 69 rotaciones por año, un nivel muy elevado de operativa. |

### Log de Rebalanceos (Extracto)

| Fecha | Rotación | Coste (€) | Patrimonio (€) | Contexto |
|------------|---------:|----------:|---------------:|-----------|
| 2010-12-02 | 20,00% | 2,00 | 9.998,00 | Primera apertura de posición. |
| 2010-12-03 | 20,10% | 2,01 | 10.017,10 | Ajuste menor de la cartera. |
| 2010-12-06 | 20,00% | 2,00 | 10.015,10 | Rotación diaria asociada a la estrategia. |
| ... | ... | ... | ... | ... |
| 2020-11-04 | 20,04% | 1,91 | 9.552,96 | Últimos días del backtest. |
| 2020-11-05 | 20,00% | 1,91 | 9.551,05 | Rotación diaria. |
| 2020-11-16 | 20,32% | 1,94 | 9.552,66 | Cierre del período analizado. |

**💡 Insight Clave:** El log muestra rotaciones del ~20% todos los días hábiles durante 10 años (687 rebalanceos). Esto indica que el generador de pesos estaba cambiando las posiciones constantemente, generando costes de transacción acumulados de 1,371 € que erosionaron completamente cualquier ganancia potencial del arbitraje.

## Diagnóstico Automático

El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:

* 🔴 Ratio de Sharpe negativo (-1.57): La estrategia destruyó valor en términos de eficiencia riesgo/retorno.
* ✅ Riesgo de caída muy controlado (Max DD: 7.7%): Una caída máxima del 7.7% es excepcionalmente baja, confirmando la naturaleza market-neutral.
* ✅ Beta prácticamente cero (-0.01): La cartera es completamente indiferente a los movimientos del mercado.
*✅ R² cercano a cero (0.01): El 99% del movimiento de la cartera NO se explica por el mercado de acciones.

**Nota Pedagógica:** Pairs Trading y Métricas de Trading

## ⚠️ ¿Por qué las "Métricas Extras" muestran 0 operaciones si hubo 687 rebalanceos?

El Pairs Trading es una estrategia de POSICIONES MARKET-NEUTRAL. El motor dinámico registra rebalanceos (cambios de pesos), pero no "tickets" individuales de entrada/salida de cada par.
Para esta estrategia, los indicadores relevantes son:

    LOG DE REBALANCEOS: Frecuencia y coste de los ajustes (687 rebalanceos en 10 años = ~69/año).
    BETA: Debería ser cercana a 0 (descorrelación del mercado). ✅ Confirmado: Beta = -0.01.
    ALPHA: Rentabilidad no explicada por el mercado (alpha puro).  Alpha = -0.00.
    MAX DRAWDOWN: Riesgo de ruptura de cointegración. ✅ Confirmado: -7.72%.
    SHARPE: Eficiencia riesgo/retorno (objetivo > 1.0). ❌ Sharpe = -1.57.

## ¿Por qué el Pairs Trading tuvo resultados "matizados"?

Los datos muestran algo contraintuitivo: la estrategia logró ser perfectamente market-neutral (Beta ≈ 0, R² ≈ 0, Max Drawdown -7.7%), pero no generó rentabilidad positiva (CAGR -0.44%, Sharpe -1.57). ¿Por qué?
La respuesta está en los costes de transacción

* Exceso de rotación: 687 rebalanceos en 10 años (~69/año) es una frecuencia excesiva para una estrategia de arbitraje estadístico. Cada rotación del 20% genera un coste del 0.2% (ida y vuelta), lo que suma 1,371 € en 10 años (13.7% del capital inicial).
* Spreads demasiado estrechos: Los pares KO/PEP y EWA/EWC, aunque cointegrados, tienen spreads con amplitud limitada. Cuando el z-score supera 2.0 y se abre la posición, el spread suele revertir rápidamente (z < 0.5), generando ganancias pequeñas que no compensan los costes de transacción.
* Umbrales subóptimos: Los umbrales de entrada (2.0) y salida (0.5) fueron elegidos de forma arbitraria. En la práctica profesional, estos umbrales se optimizan mediante backtesting exhaustivo para cada par específico, considerando su volatilidad residual y los costes de transacción reales.
* Falta de alpha en los pares seleccionados: Aunque KO/PEP y EWA/EWC están cointegrados (p < 0.15), la cointegración no garantiza rentabilidad. Solo garantiza que el spread es estacionario. Para que el arbitraje sea rentable, el spread debe tener suficiente amplitud y velocidad de reversión para compensar los costes.

Pero... las métricas de riesgo son excepcionales  
A pesar de la rentabilidad negativa, la estrategia logró algo valioso:

* Beta ≈ 0: La cartera es completamente indiferente a los movimientos del mercado. En 2020, cuando el SPY cayó un 32.7%, el Pairs Trading solo cayó un 7.7%.
* Volatilidad 90% menor: 1.55% vs 14.96%. La curva de patrimonio es extremadamente suave.
* VaR 95% diario 98% menor: 5.86 € vs 358.40 €. El riesgo de cola diaria es mínimo.
* Max Drawdown 76% menor: -7.72% vs -32.70%. La estrategia protege el capital en crisis.

## La Ventaja Real del Pairs Trading (Matizada)

Los datos de este período (2010-2020) nos obligan a ser honestos sobre las limitaciones del arbitraje estadístico:

| Ventaja real | Evidencia |
|--------------|-----------|
| ✅ **Market-neutral confirmado** | Beta = -0,01 y R² = 0,01, mostrando una descorrelación prácticamente total respecto al mercado. |
| ✅ **Riesgo de caída mínimo** | Max Drawdown de solo -7,72%, muy inferior al observado en SPY. |
| ✅ **Volatilidad extremadamente baja** | 1,55% frente al 14,96% de Buy & Hold. |
| ✅ **VaR diario controlado** | 5,86 € frente a 358,40 €, reduciendo drásticamente el riesgo extremo diario. |
| ❌ **Rentabilidad negativa** | CAGR de -0,44%, insuficiente para preservar el poder adquisitivo del capital. |
| ❌ **Sharpe negativo** | -1,57, indicando una relación rentabilidad-riesgo desfavorable. |
| ❌ **Costes de transacción excesivos** | 1.371 € acumulados, equivalentes al 13,7% del capital inicial. |
| ❌ **Frecuencia de rebalanceo excesiva** | 687 operaciones en 10 años, generando una elevada rotación de cartera. |

**Conclusión matizada:** El Pairs Trading logró ser market-neutral (Beta ≈ 0, R² ≈ 0), pero no generó alpha positivo debido a los costes de transacción. La estrategia es excelente para reducir el riesgo (Max Drawdown -7.7% vs -32.7% del SPY), pero no para generar rentabilidad en este período con estos pares y estos umbrales.

## Cómo Hacer Seguimiento con el Script

### 1. Optimizar los umbrales de entrada/salida

Los umbrales actuales (entrada: 2.0, salida: 0.5) son genéricos. En la práctica profesional, se optimizan para cada par específico mediante:

    Backtesting exhaustivo: Probar diferentes combinaciones de umbrales y seleccionar las que maximicen el Sharpe ratio.
    Análisis de la distribución del z-score: Si el z-score raramente supera 2.5, el umbral de entrada debería ser 2.5, no 2.0.
    Consideración de costes: El umbral de salida debe ser lo suficientemente amplio para que la ganancia media por operación supere los costes de transacción.

### 2. Reducir la frecuencia de rebalanceo

687 rebalanceos en 10 años es excesivo. Se puede reducir la frecuencia evaluando el z-score solo una vez por semana (en lugar de diariamente), lo que reduciría los costes de transacción en ~80%.

### 3. Seleccionar pares con spreads más amplios

KO/PEP y EWA/EWC tienen spreads estrechos. Pares como acciones de tecnología vs. acciones de valor, o ETFs de sectores cíclicos vs. defensivos, suelen tener spreads más amplios y rentables.

### 4. Monitorear la cointegración rolling

La cointegración no es permanente. Se debe re-evaluar el test de Engle-Granger cada 6-12 meses para detectar rupturas estructurales a tiempo.

**Conclusiones**

El análisis del Pairs Trading arroja lecciones matizadas pero valiosas:

* La cointegración es necesaria, pero no suficiente. Un p-valor bajo (p < 0.15) confirma que el spread es estacionario, pero no garantiza que el arbitraje sea rentable después de costes.
* Los costes de transacción son el enemigo silencioso. Con 687 rebalanceos en 10 años y un coste del 0.2% por operación, los costes acumulados (1,371 €) erosionaron completamente cualquier ganancia potencial.
* El Pairs Trading SÍ logra ser market-neutral. Beta ≈ 0, R² ≈ 0, Max Drawdown -7.7%. La estrategia es excelente para reducir el riesgo, pero no para generar rentabilidad con estos parámetros.
* La selección de umbrales es crítica. Los umbrales de entrada (2.0) y salida (0.5) deben optimizarse para cada par específico, considerando su volatilidad residual y los costes de transacción.
* No todos los pares cointegrados son rentables. GLD/GDX fue rechazado correctamente (p = 0.319), pero KO/PEP y EWA/EWC, aunque cointegrados, no generaron alpha positivo debido a spreads estrechos y costes elevados.
* El Pairs Trading es una estrategia de riesgo bajo, no de rentabilidad alta. Con un Max Drawdown del -7.7% y una volatilidad del 1.55%, la estrategia es ideal para inversores conservadores que priorizan la preservación del capital sobre la rentabilidad.
* La disciplina estadística es lo que separa el arbitraje de la especulación. Operar solo pares con p-valor < 0.15, usar z-scores para identificar desviaciones extremas, y cerrar posiciones cuando el spread reverts, es lo que convierte el Pairs Trading en una estrategia sistemática y reproducible.

La filosofía del Pairs Trading, democratizada a través de este motor cuantitativo, demuestra que no necesitas predecir la dirección del mercado. Solo necesitas identificar relaciones estables entre activos y apostar a que esas relaciones se mantendrán... siempre que los costes de transacción no erosionen las ganancias.

## Descargo de esponsabilidad y Advertencia de Riesgos.

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa.
Los Resultados Pasados No Garantizan Resultados Futuros
El backtest presentado es una simulación histórica basada en datos pasados (2010-2020). Que la estrategia Pairs Trading haya generado un CAGR del -0.44% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los mercados financieros son dinámicos y las relaciones de cointegración pueden romperse en cualquier momento.
### Limitaciones del Backtest

* Sesgo de Supervivencia: Los ETFs utilizados (KO, PEP, EWA, EWC, GLD, GDX) son productos consolidados, pero podrían cambiar, fusionarse o ser liquidados en el futuro.
* Costes de Transacción Reales: Hemos asumido un 0.1% de comisión por operación. En la vida real, los costes pueden ser mayores (comisiones del bróker, spreads bid-ask, slippage).
* Fiscalidad: El motor no contempla el impacto de impuestos por ventas a corto plazo. Con 687 rebalanceos en 10 años, los eventos fiscales serían significativos.
* Cointegración inestable: La cointegración no es permanente. Un par que está cointegrado hoy puede romper su relación mañana debido a cambios estructurales (adquisiciones, cambios regulatorios, crisis sectoriales).
* Optimización de parámetros: Los umbrales de entrada (2.0) y salida (0.5) fueron elegidos de forma arbitraria. En la práctica profesional, se optimizan mediante backtesting exhaustivo.

No es Asesoramiento Financiero
Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe:

* Evaluar su propia tolerancia al riesgo (un Max Drawdown del -7.7% es bajo, pero la rentabilidad negativa puede ser psicológicamente difícil de soportar).
* Considerar su horizonte temporal (el Pairs Trading está diseñado para años, no para días).
* Consultar con un asesor financiero independiente antes de tomar decisiones.

### Riesgo de Pérdida de Capital

Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. Aunque el Pairs Trading tiene un Max Drawdown bajo (-7.7%), la rentabilidad negativa (-0.44%) significa que el capital se erosiona lentamente con el tiempo. Un inversor que busque rentabilidad positiva no debería usar esta estrategia con estos parámetros.
Uso del Código
El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de:

* Errores en el código o en los datos descargados de Yahoo Finance.
* Pérdidas económicas derivadas del uso de estas herramientas.
* La exactitud de las métricas calculadas (siempre debes verificar los cálculos críticos de forma independiente).

**🎯 Recuerda**
El Pairs Trading cuantitativo no es "comprar dos empresas similares y esperar que se muevan juntas". Eso es correlación, no cointegración. El Pairs Trading cuantitativo es validar estadísticamente que el spread entre dos activos es estacionario (p < 0.15), operar solo cuando el z-score supera umbrales críticos (|z| > 2.0), y cerrar cuando el spread reverts (|z| < 0.5).
Es una estrategia de disciplina estadística y gestión de costes, no de intuición. Su verdadero valor no está en maximizar el CAGR, sino en ofrecer una Beta cercana a 0 y un Max Drawdown mínimo, actuando como un satélite de bajo riesgo en un modelo Core-Satellite.

**La lección más importante de este capítulo:** la cointegración es necesaria, pero no suficiente. Para que el Pairs Trading sea rentable, necesitas pares con spreads amplios, umbrales optimizados, y costes de transacción controlados. Sin estos tres elementos, la estrategia será market-neutral pero no generará alpha positivo.

**La paciencia, la disciplina estadística y la gestión rigurosa de costes son tus mayores aliados.**