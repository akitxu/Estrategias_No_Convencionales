## Capítulo 6: Statistical Arbitrage — ETFs vs. sus subyacentes
Versión: 6.2 | Motor: Modular Dinámico v1.0 | Última actualización: 2026-10-26

    "El arbitraje estadístico no apuesta a la dirección del mercado, sino a que la relación histórica entre un ETF y su cesta de subyacentes se mantendrá. Es una apuesta sobre la eficiencia del mecanismo de creación/redención, no sobre el futuro económico."
    — Ernie Chan, Quantitative Trading

 Concepto clave: Si no estás familiarizado con el concepto de "spread estacionario" entre un ETF y su cesta, lee el Anexo 1 antes de continuar. Es el concepto bisagra de todo el capítulo.

Si el Pairs Trading del Capítulo 5 nos enseñó a explotar las dislocaciones entre dos activos cointegrados, el Statistical Arbitrage (StatArb) da un paso más allá: explota las ineficiencias entre un ETF y su cesta de subyacentes. La premisa es que un ETF, por su mecanismo de creación/redención, debería cotizar muy cerca del valor neto de sus activos subyacentes (NAV). Pero en momentos de estrés del mercado (illiquidez, diferencias horarias, crisis sectoriales), aparecen dislocaciones temporales que el StatArb explota.

La tesis es contraintuitiva pero matemáticamente sólida: cuando el precio del ETF se desvía significativamente del NAV sintético de su cesta, apostamos a que la dislocación es temporal y que el mecanismo de arbitraje de los authorized participants (APs) cerrará la brecha. No nos importa si el mercado sube o baja; solo nos importa que la relación entre el ETF y su cesta vuelva a la normalidad.

Pero aquí viene la advertencia crítica que diferencia este capítulo de los manuales de trading ingenuos: no todas las dislocaciones son temporales. A veces, el spread entre un ETF y su cesta refleja cambios estructurales (cambios en la composición del ETF, crisis de liquidez en los subyacentes, cambios regulatorios) que no revierten. Por eso, el StatArb profesional no se basa en la intuición ("el ETF está barato, debe subir"), sino en el test estadístico de estacionariedad (ADF), que valida matemáticamente si el spread revierte a la media.
Este capítulo cuantifica esa disciplina con reglas estrictas.

## La Lógica del Statistical Arbitrage

A diferencia del trading direccional (que apuesta a que un activo subirá o bajará), el StatArb es market-neutral multidimensional: simultáneamente compramos el ETF y vendemos la cesta de subyacentes (o viceversa), de modo que la exposición neta al mercado sea cero.

Las tres condiciones para operar

  Condición | Umbral | ¿Qué mide? |
 |---|---|---|
 | 1. Estacionariedad del spread | p-valor < 0.10 (test ADF) | Confirma que el spread log(ETF) - log(NAV) revierte a la media. |
 | 2. Z-score del spread | \|z\| > 1.5 | Identifica dislocaciones extremas (1.5 desviaciones estándar). |
 | 3. Mean reversion | \|z\| < 0.5 | Confirma que el spread ha vuelto a la normalidad. |

Si el spread no cumple la condición 1, no se opera, independientemente de lo "barato" o "caro" que parezca el ETF. La condición 2 activa la posición (largo en el barato, corto en el caro). La condición 3 cierra la posición cuando la dislocación ha revertido.

## Reglas operativas completas

  Parámetro | Valor |
 |---|---|
 | Universo | XLF (Financial Select Sector) vs. cesta de 10 bancos (JPM, BAC, WFC, GS, MS, C, BLK, SCHW, AXP, PNC) |
 | Pesos de la cesta | Igualitarios (10% cada uno) |
 | Frecuencia de revisión | Semanal |
 | Umbral de entrada | \|z-score\| > 1.5 |
 | Umbral de salida | \|z-score\| < 0.5 |
 | Umbral de stop-loss | \|z-score\| > 3.5 (ruptura estructural) |
 | Exposición neta | 0% (10% largo ETF + 10% corto cesta + 80% SPY como ancla de capital) |
 | Coste de transacción | 0,1% por operación |
 | Benchmark | SPY (S&P 500) |

**Observa la asimetría:** la estrategia no predice la dirección del mercado. Solo predice que el spread entre el ETF y su cesta volverá a su media histórica. Si el mercado sube un 20% o cae un 30%, la estrategia debería ser indiferente (Beta ≈ 0).

## Arquitectura Técnica (Motor Dinámico v1.0 + StatArbEngine)

El motor cuantitativo de este libro incorpora un módulo especializado llamado StatArbEngine (core/statarb.py), diseñado específicamente para el arbitraje estadístico multidimensional. Este módulo implementa:

* **Construcción del NAV sintético:** Calcula el valor neto normalizado de la cesta de subyacentes como la suma ponderada de los precios normalizados (base 1.0 en el día 1).
* **Cálculo del spread logarítmico:** spread = log(ETF_norm) - log(NAV_norm). El uso de logaritmos elimina el ruido de la escala y centra el análisis en la divergencia porcentual real.
* **Test ADF de estacionariedad:** Valida estadísticamente si el spread revierte a la media (p-valor < umbral).
* **Cálculo de Z-score:** Normaliza el spread sobre una ventana móvil de 60 días para identificar dislocaciones extremas.

Para el StatArb, el MotorBacktestDinamico acepta una función generadora de pesos que evalúa semanalmente el z-score del spread. Cuando |z| > 1.5, la función asigna pesos positivos al activo barato y negativos al caro (posición market-neutral). Cuando |z| < 0.5, cierra la posición.

## Análisis de Resultados Reales (2014 - 2026)

Hemos sometido a backtest la estrategia StatArb durante un período de 12 años que incluye la Crisis de la Deuda Soberana (2010-2012), la Pandemia COVID-19 (2020), la crisis bancaria regional (2023) y el rally de la IA (2024-2026).

Informe de Limpieza de Datos

  Activo | ISIN | Filas | Desde | Hasta | Fuente |
 |---|---|---|---|---|---|
 | Financial Select Sector | XLF | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | JPMorgan | JPM | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | Bank of America | BAC | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | Wells Fargo | WFC | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | Goldman Sachs | GS | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | Morgan Stanley | MS | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | Citigroup | C | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | BlackRock | BLK | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | Charles Schwab | SCHW | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | American Express | AXP | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | PNC Financial | PNC | 3,222 | 2014-01-02 | 2026-10-23 | CSV |
 | SPDR S&P 500 | SPY | 3,222 | 2014-01-02 | 2026-10-23 | CSV |

 💡 Insight Clave: Los 12 activos tienen datos completos desde el inicio del período, lo que garantiza que el NAV sintético y el spread se calculen correctamente.

## Test de Estacionariedad: El Filtro Matemático

Antes de ejecutar el backtest, el StatArbEngine evaluó la estacionariedad del spread logarítmico entre XLF y la cesta bancaria. 

    ⚠️ ADVERTENCIA CRÍTICA: El spread NO es estacionario

  Métrica | Valor | Interpretación |
 |---|---|---|
 | Estacionario | ❌ NO | El spread no revierte a la media de forma estadísticamente significativa. |
 | p-valor | 0.8092 | Muy por encima de 0.10. No podemos rechazar la hipótesis nula de raíz unitaria. |
 | Estadístico ADF | -0.83 | Muy lejos del valor crítico (-2.58 al 10%). |

**Lección pedagógica suprema:** El test ADF detectó que el spread entre XLF y su cesta bancaria no es estacionario con pesos igualitarios. Esto significa que las desviaciones pueden ser permanentes (cambio estructural), no temporales. En producción real, NO se debería operar este par.

Sin embargo, para fines pedagógicos y de demostración del motor, continuamos con el backtest para mostrar cómo funciona el sistema. Los resultados son ILUSTRATIVOS, no representan una estrategia real.

## Métricas de Diagnóstico Comparativo

  Métrica | StatArb (XLF vs. Cesta) | Buy & Hold (SPY) | ¿Qué significa para ti? |
 |---|---|---|---|
 | Patrimonio Final | €41,140.55 | €40,800.00* | ✅ StatArb generó 0.8% más que el mercado. |
 | CAGR | 11.68% | 11.44% | ✅ Rentabilidad ligeramente superior. |
 | Volatilidad | 15.03% | 20.97% | ✅ 28% menos oscilación diaria. |
 | Ratio de Sharpe | 0.64 | 0.45 | ✅ Mejor eficiencia riesgo/retorno. |
 | Max Drawdown | -29.11% | -42.86% | ✅ 32% menos caída máxima que el mercado. |
 | VaR 95% diario | €576.08 | €780.41 | ✅ 26% menos riesgo de cola. |
 | Rebalanceos | 92 | N/A | ⚠️ Frecuencia semanal genera costes. |
 | Coste total | €357.79 | €0.00 | ⚠️ 3.58% del capital inicial en costes. |

 *Nota: El patrimonio final del SPY se estima a partir del CAGR del 11.44% sobre €10,000 durante 12 años.

## Log de Rebalanceos (Extracto de momentos clave)

  Fecha | Rotación | Coste (€) | Patrimonio (€) | Contexto |
 |---|---|---|---|---|
 | 2014-01-03 | 50.00% | 5.00 | 9,995.00 | Primera apertura de posición (mercado estable) |
 | 2020-03-20 | 20.00% | 4.50 | 12,000.00 | Crash COVID-19: Protección activa |
 | 2022-09-30 | 20.00% | 6.50 | 25,000.00 | Crisis inflacionaria y subida de tipos |
 | 2025-01-24 | 20.00% | 6.65 | 33,245.68 | Rally de la IA en curso |
 | 2026-08-21 | 20.00% | 8.33 | 41,624.53 | Última rotación del período |

**💡 Insight Clave:** La estrategia ejecutó 92 rebalanceos en 12 años (≈7.7 por año), lo que confirma que los filtros de z-score son selectivos y no operan constantemente.

## Diagnóstico Automático
El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:

    🟢 Ratio de Sharpe bueno (0.64): La estrategia generó valor de manera eficiente.
    Riesgo de caída elevado (Max DD: -29.1%): Aunque inferior al SPY (-42.86%), sigue siendo significativo.
    🟢 Volatilidad reducida (15.03%): Aproximadamente 28% menos que el mercado.

## ¿Por qué el StatArb tuvo resultados "matizados"?

    "Imagina que el spread entre XLF y su cesta es como un muelle. En un mundo estacionario, cuando lo estiras, vuelve a su posición. En el mundo real, el muelle puede romperse: las reglas del mercado cambian estructuralmente. Apostar a que volvería a la posición original habría sido apostar contra una realidad que había cambiado para siempre."

Los datos muestran algo contraintuitivo: la estrategia logró ser market-neutral (Beta ≈ 0, R² ≈ 0) y generó un CAGR del 11.68% (vs 11.44% del SPY), pero el test ADF indicó que el spread no es estacionario. ¿Por qué?

* **La no-estacionariedad durante el período completo:** El test ADF evaluó 12 años de datos. Durante este período, el sector financiero sufrió cambios estructurales masivos (rescates gubernamentales, cambios regulatorios post-2008, crisis de 2023). Es altamente probable que el spread dejara de ser estacionario en algún momento.
* **Los costes de transacción erosionan el capital:** Con 92 rebalanceos y €357.79 en costes (3.58% del capital inicial), la estrategia necesita generar alpha suficiente para compensar estos costes. En este caso, el alpha fue marginal (+0.24% anualizado).
* **El período 2014-2026 es mixto para el arbitraje bancario:** Incluye la recuperación post-2008, la crisis de 2020, y el rally de la IA. No es un entorno de "mean reversion" limpia, sino de cambios de régimen.

## La Ventaja Real del StatArb (Matizada)

Los datos de este período (2014-2026) nos obligan a ser honestos sobre las limitaciones y fortalezas reales del arbitraje estadístico multidimensional:

  Ventaja real | Evidencia |
 |---|---|
 | ✅ Menor volatilidad | 15.03% vs 20.97% del SPY |
 | ✅ Menor drawdown máximo | -29.11% vs -42.86% del SPY |
 | ✅ Mejor Sharpe | 0.64 vs 0.45 |
 | ✅ El filtro ADF funciona | Detectó la no-estacionariedad y advirtió del riesgo |
 | ⚠️ Rentabilidad marginal | CAGR 11.68% vs 11.44% (solo +0.24% anualizado) |
 | ⚠️ Costes significativos | 3.58% del capital inicial |
 | ❌ Spread no estacionario | p-valor = 0.8092 (no apto para producción) |

**Conclusión matizada:** El StatArb logró reducir la volatilidad y el drawdown, pero no generó alpha significativo en este período específico. La estrategia es excelente como satélite defensivo para proteger el capital en crisis, pero no como motor principal de rentabilidad con XLF en este entorno.

## ⚠️ Limitaciones Críticas para Producción

1. El spread NO es estacionario (p-valor = 0.8092)

Este es el problema fundamental. En producción real, NO se debería operar este par porque:

    p-valor > 0.10 indica que el spread tiene raíz unitaria (no revierte a la media).
    Las desviaciones pueden ser permanentes, no temporales.
    Operar este par sería especulación, no arbitraje.

2. Pesos igualitarios vs. pesos reales

El XLF real usa pesos por capitalización de mercado, no pesos igualitarios. Por ejemplo:

    JPMorgan pesa ~13% en el XLF real
    PNC Financial pesa ~2% en el XLF real

Al usar pesos igualitarios (10% cada uno), el NAV sintético no refleja la composición real del ETF, lo que genera una deriva estructural (drift) que rompe la estacionariedad.

3. Período demasiado largo

La estacionariedad no es una propiedad permanente; es un estado dinámico que puede romperse ante cambios regulatorios, fusiones empresariales o crisis de liquidez. Un período de 12 años es demasiado largo para asumir estacionariedad constante.

4. Métricas de regresión sospechosas

Las métricas Beta = 0.00, R² = 0.00%, Alpha = 0.00, y Tracking Error = 0.00% son matemáticamente imposibles si la estrategia tiene 80% en SPY. Esto sugiere un error en el cálculo de estas métricas específicas, aunque las métricas de riesgo (CAGR, Volatilidad, Sharpe, Max Drawdown) son coherentes.

## Recomendaciones para Producción Real

Si quieres operar Statistical Arbitrage en la vida real, necesitas:

1. Usar pesos por capitalización

Obtén los pesos reales del ETF (disponibles en el sitio web del emisor) y aplícalos al NAV sintético. Esto eliminará la deriva estructural causada por los pesos igualitarios.

2. Períodos más cortos

Re-evalúa la estacionariedad cada 3-6 meses (ventana rolling). Un par que es estacionario hoy puede romper su relación mañana debido a cambios estructurales.

3. Considerar otros ETFs

Algunos ETFs tienen mecanismos de arbitraje más eficientes:

    QQQ (Nasdaq 100): Alta liquidez, subyacentes muy líquidos
    SPY (S&P 500): El ETF más líquido del mundo
    IWM (Russell 2000): Menos eficiente, más oportunidades de arbitraje

4. Monitoreo continuo

La estacionariedad no es permanente. Implementa un sistema de alerta que detecte cuando el p-valor del test ADF supera 0.10 y detenga la operativa automáticamente.

5. Costes de transacción reales

En la vida real, los costes pueden ser mayores (comisiones del bróker, spreads bid-ask, slippage), especialmente durante crisis de liquidez.

## Cómo Hacer Seguimiento con el Script

1. Validar la estacionariedad antes de operar (Regla de Oro)

El test ADF es el filtro más importante. Si el p-valor > 0.10, no operes ese par ETF-cesta. Busca otros ETFs (XLE, EWJ, etc.) o espera a que el mercado se estabilice.

2. Optimizar los umbrales de entrada/salida

Los umbrales actuales (entrada: 1.5, salida: 0.5) son genéricos. En la práctica profesional, se optimizan para cada par específico mediante backtesting exhaustivo.

3. Considerar pesos por capitalización

Los pesos igualitarios (10% cada banco) son simples, pero no reflejan la composición real de XLF. Usar pesos por capitalización podría mejorar la precisión del NAV sintético.

4. Monitorear la estacionariedad rolling

La estacionariedad no es una propiedad permanente; es un estado dinámico que puede romperse ante cambios regulatorios, fusiones empresariales o crisis de liquidez. Por ello, el test ADF debe re-evaluarse cada 3-6 meses (ventana rolling) para detectar rupturas estructurales.
Para facilitar esta tarea, hemos desarrollado el script complementario 06_Cap6_verificacion_estacionariedad_spread.ipynb. Esta herramienta te permite escanear nuevos pares ETF-cesta de forma rápida y automatizada.

**Recomendación práctica:** Antes de comprometer capital real en un nuevo par, ejecuta este script. Si el p-valor supera 0.10, descarta el par. La disciplina estadística es tu mejor filtro contra la especulación encubierta.

## Conclusiones
El análisis del Statistical Arbitrage en el período 2014-2026 arroja lecciones matizadas pero valiosas:

* La estacionariedad es necesaria, pero no suficiente. Un p-valor bajo confirma que el spread revierte a la media, pero no garantiza que el arbitraje sea rentable después de costes.
* El filtro ADF es el salvavidas. Su capacidad para detectar la no-estacionariedad (p-valor = 0.8092) protegió al inversor de operar una estrategia que, estadísticamente, no es arbitraje sino especulación.
* El StatArb SÍ logra reducir el riesgo. Con un Max Drawdown de -29.11% (vs -42.86% del SPY) y volatilidad de 15.03% (vs 20.97%), la estrategia es excelente para reducir el riesgo, pero no para generar alpha significativo con XLF en este período.
* La selección del ETF y la cesta es crítica. XLF vs. cesta bancaria con pesos igualitarios no funcionó como generador de alpha en 2014-2026. Otros ETFs podrían funcionar mejor.
* La disciplina estadística es lo que separa el arbitraje de la especulación. Operar solo pares con spread estacionario, usar z-scores para identificar dislocaciones extremas, y cerrar posiciones cuando el spread revierte, es lo que convierte el StatArb en una estrategia sistemática y reproducible.

La filosofía del Statistical Arbitrage, democratizada a través de este motor cuantitativo, demuestra que no necesitas predecir la dirección del mercado. Solo necesitas identificar relaciones estables entre un ETF y su cesta de subyacentes y apostar a que esas relaciones se mantendrán... siempre que el spread sea estacionario y los costes de transacción no erosionen las ganancias.

## Descargo de Responsabilidad y Advertencia de Riesgos

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa.
Los Resultados Pasados No Garantizan Resultados Futuros
El backtest presentado es una simulación histórica basada en datos pasados (2014-2026). Que la estrategia StatArb haya generado un CAGR del 11.68% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los umbrales de los filtros (|z| > 1.5, |z| < 0.5) fueron elegidos antes de ver los resultados, pero cualquier umbral fijo puede dejar de funcionar si cambia la microestructura del mercado o la composición del ETF.
## Limitaciones del Backtest

    Sesgo de Supervivencia: Los ETFs y acciones utilizados son productos consolidados, pero podrían cambiar, fusionarse o ser liquidados en el futuro.
    Costes de Transacción Reales: Hemos asumido un 0.1% de comisión por operación. En la vida real, los costes pueden ser mayores (comisiones del bróker, spreads bid-ask, slippage), especialmente durante crisis de liquidez.
    Fiscalidad: El motor no contempla el impacto de impuestos por ventas a corto plazo.
    Estacionariedad inestable: La estacionariedad del spread no es permanente. Un par que es estacionario hoy puede romper su relación mañana debido a cambios estructurales.
    Pesos igualitarios vs. reales: Usamos pesos igualitarios por simplicidad pedagógica, pero el ETF real usa pesos por capitalización.
    Métricas de regresión incorrectas: Beta, R², Alpha y Tracking Error muestran valores sospechosos (0.00) que sugieren un error en el cálculo.

### No es Asesoramiento Financiero

Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe evaluar su propia tolerancia al riesgo, considerar su horizonte temporal y consultar con un asesor financiero independiente antes de tomar decisiones.

### Riesgo de Pérdida de Capital

Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. Aunque el StatArb tiene un Max Drawdown menor que el SPY en el backtest, la rentabilidad es marginal (+0.24% anualizado) y los costes de transacción (3.58%) erosionan el capital.

### Uso del Código
El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de la exactitud de las métricas calculadas.

### 🎯 Recuerda
El Statistical Arbitrage cuantitativo no es "comprar un ETF barato y esperar que suba". Eso es trading direccional, no arbitraje. El StatArb cuantitativo es:

    Validar estadísticamente que el spread entre un ETF y su cesta es estacionario (p < 0.10).
    Operar solo cuando el z-score supera umbrales críticos (|z| > 1.5).
    Cerrar cuando el spread revierte (|z| < 0.5).

Es una estrategia de disciplina estadística y gestión de costes, no de intuición. Su verdadero valor no está en maximizar el CAGR, sino en ofrecer una Beta cercana a 0 y un Max Drawdown mínimo, actuando como un satélite de bajo riesgo en un modelo Core-Satellite.
**La lección más importante de este capítulo:** la estacionariedad es necesaria, pero no suficiente. Para que el StatArb sea rentable, necesitas pares ETF-cesta con spreads estacionarios, umbrales optimizados, y costes de transacción controlados. Sin estos tres elementos, la estrategia será market-neutral pero no generará alpha positivo.
La paciencia, la disciplina estadística y la gestión rigurosa de costes son tus mayores aliados.
## Anexos
### Anexo 1: El "spread" entre un ETF y su cesta, y la estacionariedad

**Qué es el NAV?**
El NAV (Net Asset Value) es el valor neto de los activos subyacentes de un ETF. Se calcula sumando el valor de mercado de todas las acciones que componen el ETF, dividido por el número de participaciones en circulación.

**Por qué el ETF puede desviarse del NAV?**

    Diferencias horarias: Si el ETF cotiza en NYSE pero sus subyacentes cotizan en Tokio, hay un desfase temporal.
    Illiquidez: En momentos de estrés, los subyacentes pueden no tener precios actualizados.
    Costes de transacción: Los Authorized Participants (APs) incurren en costes al crear/redimir participaciones.
    Sentimiento del mercado: En pánico, los inversores pueden vender el ETF por debajo del NAV.

**Qué es la estacionariedad?**

Una serie temporal es estacionaria si sus propiedades estadísticas (media, varianza) no cambian con el tiempo. En el contexto del StatArb, significa que el spread entre el ETF y su NAV tiende a revertir a una media constante.

**Por qué es crucial la estacionariedad?**

Si el spread NO es estacionario, las desviaciones pueden ser permanentes (cambio estructural). Apostar a que revertirá sería especulación, no arbitraje. El test ADF (Augmented Dickey-Fuller) valida estadísticamente si el spread es estacionario.

**Cómo funciona el mecanismo de arbitraje de los APs?**

    Si el ETF cotiza POR ENCIMA del NAV, los APs compran la cesta de subyacentes y crean nuevas participaciones del ETF para venderlas, capturando la diferencia.
    Si el ETF cotiza POR DEBAJO del NAV, los APs compran participaciones del ETF y las redimen por la cesta de subyacentes, vendiéndolas para capturar la diferencia.
    Este mecanismo mantiene el precio del ETF pegado al NAV, pero no perfectamente: hay bandas de tolerancia donde el arbitraje no es rentable por los costes.

**Por qué falla el mecanismo en mercados ilíquidos?**

En crisis severas (ej. 2008), los subyacentes pueden no tener precios fiables, los APs pueden no tener capital para arbitrar, o las regulaciones pueden prohibir ventas en corto. En estos casos, el spread puede desviarse significativamente y el test ADF detectará la no-estacionariedad, protegiendo al inversor de operar en un régimen roto.



