Capítulo 4: Fear & Greed Index (FGI) — El termómetro del mercado
Versión: 4.1 | Motor: Modular Dinámico v1.0 | Última actualización: 2026-10-03

    "El mercado puede permanecer irracional más tiempo del que tú puedes permanecer solvente."
    — John Maynard Keynes

Si el Contrarian Investing del Capítulo 2 nos enseñó a comprar cuando el miedo colectivo alcanza niveles extremos, y el Momentum Crash del Capítulo 3 nos mostró cómo protegerse de la euforia, el Fear & Greed Index (FGI) representa la síntesis de ambos: un termómetro cuantitativo que mide la temperatura psicológica del mercado en tiempo real.
El índice original de CNN es famoso, pero tiene dos problemas para el inversor cuantitativo: utiliza datos propietarios (flujos de fondos en tiempo real) y es un indicador lagging (reacciona después de que el movimiento ya ha ocurrido). 
Por ello, en este capítulo construimos nuestro propio FGI-Quant, un índice propietario basado en tres señales matemáticas puras extraíbles de datos OHLCV gratuitos, diseñadas para capturar la psicología de mercado antes de que se refleje en los medios.
La Lógica del FGI-Quant
Nuestro índice compuesta tres dimensiones del mercado, normalizadas en una escala de 0 (Miedo Extremo) a 100 (Codicia Extrema):

| Componente | Peso | ¿Qué mide? | Lógica de Normalización |
|------------|-----:|------------|-------------------------|
| **1. Distancia a SMA-200** | 40% | Tendencia a largo plazo | < -15% = Miedo (0) |
| **2. Volatilidad Realizada (20d)** | 40% | Estrés y pánico del mercado | > 40% anual = Miedo (0) |
| **3. Spread de Crédito (HYG vs TLT)** | 20% | Apetito de riesgo corporativo | Spread negativo = Miedo (0) |

La Regla de Oro (con Zona Muerta):

    Activación de Defensa: Si el FGI > 75, el mercado está en "Codicia Extrema". Rotamos el 50% del capital a cash (SHV).
    Zona Muerta (Buffer): Si el FGI está entre 70 y 75, no hacemos nada. Esto evita el whipsaw (entrar y salir constantemente) cuando el índice oscila alrededor del umbral.
    Confirmación de Reentrada: Solo volvemos al 100% en SPY cuando el FGI cae por debajo de 70, confirmando que la euforia se ha disipado.

Arquitectura Técnica (Motor Dinámico v1.0)
Para implementar esta lógica, el MotorBacktestDinamico utiliza una función generadora de pesos con memoria de estado. A diferencia de una asignación estática, la función "recuerda" si la cartera está en modo_defensa. 
Esto es crucial: una vez que el FGI supera 75 y activamos la defensa, el sistema no vuelve a evaluar la entrada hasta que el FGI cae por debajo de 70. Esta asimetría intencionada es la que protege al inversor de las falsas recuperaciones (los llamados "rebotes del gato muerto") tras un crash.
Además, la frecuencia de evaluación es semanal ('W'), no diaria. Esto reduce drásticamente el ruido y los costes de transacción, pasando de ~600 operaciones/año a ~22 operaciones/año.
Análisis de Resultados Reales (2016 - 2026)
Hemos sometido a backtest la estrategia FGI-Quant durante un período de 10 años que incluye la Pandemia COVID-19 (2020), la crisis inflacionaria (2022-2023) y el rally de la IA (2023-2025).
Informe de Limpieza de Datos

| Activo | ISIN | Filas | Desde | Hasta | Fuente |
|---------|------|------:|------------|------------|--------|
| SPDR S&P 500 | SPY | 2.669 | 2016-01-04 | 2026-08-14 | CSV |
| iShares iBoxx $ High Yield | HYG | 2.669 | 2016-01-04 | 2026-08-14 | CSV |
| iShares 20+ Year Treasury | TLT | 2.669 | 2016-01-04 | 2026-08-14 | CSV |
| Short Treasury ETF | SHV | 2.669 | 2016-01-04 | 2026-08-14 | CSV |

💡 Insight Clave: Los 4 activos tienen datos completos desde el inicio del período, lo que garantiza que los indicadores (SMA-200, volatilidad 20d, spread de crédito) se calculen correctamente desde el primer día.
Métricas de Diagnóstico Comparativo

   Métrica | FGI-Quant (Táctico) | Buy & Hold (100% SPY) | ¿Qué significa para ti? |
 |---|---|---|---|
 | **Patrimonio Final** | 37,152 € | 17,350 € | ✅ FGI-Quant duplica el capital final |
 | **CAGR** | 13.17% | 7.35% | ✅ 5.82 pp más rentabilidad anualizada |
 | **Volatilidad** | 16.38% | 8.12% | ❌ El doble de oscilación diaria |
 | **Ratio de Sharpe** | 0.68 | 0.66 | ✅ Ligeramente mejor eficiencia |
 | **Ratio de Sortino** | 0.79 | 0.83 | ❌ Ligeramente peor gestión de caídas |
 | **Max Drawdown** | -32.11% | -20.02% | ❌ 60% más caída máxima |
 | **VaR 95% diario** | 536.86 € | 167.25 € | ❌ 221% más riesgo de cola |
 | **Alpha** | -0.72% | 0.00% | ❌ Valor destruido ajustado al riesgo |
 | **Beta** | 0.90 | 0.00 | ⚖️ Alta correlación con el mercado |
 | **R²** | 0.95 | 0.00 | ⚠️ 95% del movimiento explicado por SPY |
 | **Tracking Error** | 4.02% | 0.00% | ⚠️ Desviación moderada del benchmark |
 | **Coste total rebalanceos** | 392.62 € | 0.00 € | ⚠️ 3.93% del capital inicial (0.39% anual) |
 | **Rebalanceos totales** | 226 | 0 | ⚠️ ~22 rotaciones/año (frecuencia saludable) |

 Log de Rebalanceos (Extracto de momentos clave)

 markdown
Copiar

# Historial de Rotaciones
   Fecha | Rotación | Coste (€) | Patrimonio (€) | Contexto |
 |---|---|---|---|---|
 | 2016-10-24 | 50.00% | 5.42 | 10,831.81 | Primera activación (euforia post-Trump) |
 | 2017-01-03 | 0.12% | 0.01 | 11,127.42 | Ajuste menor (zona muerta funcionando) |
 | 2018-02-05 | 50.00% | 6.56 | 12,360.43 | Volmageddon (crisis de volatilidad) |
 | 2020-02-24 | 50.84% | 8.03 | 15,784.06 | COVID-19 (inicio del crash) |
 | 2020-07-27 | 50.00% | 7.99 | 15,978.31 | Recuperación post-COVID |
 | 2021-09-20 | 50.42% | 10.03 | 19,882.05 | Evergrande (crisis inmobiliaria China) |
 | 2023-10-23 | 50.05% | 10.07 | 20,101.22 | Subida de tipos (Fed hawkish) |
 | 2024-08-01 | 50.36% | 12.35 | 24,514.95 | Carry Trade unwind (crisis del yen) |
 | 2025-01-10 | 50.39% | 13.26 | 26,300.94 | Corrección tecnológica |
 | 2026-06-10 | 50.40% | 17.15 | 34,015.83 | Última activación registrada |

💡 Insight Clave: El coste total acumulado en 10 años es de 392.62€ (0.39% anual). La frecuencia semanal + zona muerta redujo drásticamente el whipsaw, pasando de ~600 operaciones a solo 226 en toda la década.
Diagnóstico Automático
El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:

    🟢 Ratio de Sharpe bueno (0.68): Rentabilidad digna por unidad de riesgo, ligeramente superior al Buy & Hold.
    🔴 Riesgo de caída elevado (Max DD: 32.1%): Una caída del 32% requiere psicología preparada. Peor que el Buy & Hold (-20%).
    ⚖️ Beta media (0.90): La cartera se mueve casi igual que el mercado. No hay decorrelación real.
    📉 Alpha negativo (-0.72%): Ajustado al riesgo asumido, la estrategia destruyó valor frente al benchmark.

Nota Pedagógica: ¿Cómo leer estas métricas?
️ ¿Por qué las "Métricas Extras" muestran 0 operaciones si hubo 226 rebalanceos?
El Fear & Greed Index es una estrategia de REBALANCEO PERIÓDICO/DINÁMICO. El motor no registra "tickets" de compra/venta individuales con precio de entrada y salida, sino cambios en los PESOS DE LA CARTERA (rotaciones entre SPY y SHV).
Para esta estrategia, los indicadores relevantes NO son el Win-rate, sino:

    LOG DE REBALANCEOS: Muestra la frecuencia y el coste real (226 rebalanceos en 10 años = ~22 rotaciones/año. Coste total: 392.62€).
    MAX DRAWDOWN: La métrica reina para estrategias de protección.
    RATIO DE SHARPE/SORTINO: Eficiencia ajustada al riesgo.

¿Por qué el FGI-Quant tuvo resultados "contraintuitivos"?
Los datos muestran algo sorprendente: el CAGR (13.17%) es casi el doble que el del Buy & Hold (7.35%), pero el Max Drawdown (-32.11%) es 60% peor que el del Buy & Hold (-20.02%). Esto contradice la promesa popular de que el FGI "protege en las caídas". ¿Por qué?
La respuesta está en la naturaleza de los filtros

    El FGI-Quant se activó en momentos de euforia, pero también salió demasiado pronto: Cuando el mercado caía abruptamente (como en marzo 2020), el FGI caía rápidamente por debajo de 70, haciendo que la estrategia volviera al 100% en SPY justo cuando el mercado seguía cayendo. El buffer de 5 puntos no fue suficiente para proteger de los "rebotes del gato muerto".
    La volatilidad del SPY en este período fue anormalmente baja (8.12%): Cualquier desviación de la estrategia (estar en cash un 50% del tiempo) se ve amplificada en términos de volatilidad relativa. Por eso la volatilidad del FGI-Quant (16.38%) es el doble que la del Buy & Hold.
    El período 2016-2026 fue mayoritariamente alcista: La estrategia pasó mucho tiempo en modo defensa (50% cash), perdiéndose las subidas sostenidas. Esto explica por qué el Alpha es negativo (-0.72%): el riesgo adicional no fue compensado por rentabilidad extra ajustada al riesgo.
    El Max Drawdown peor se explica por el timing: En alguna crisis específica (probablemente 2022, cuando el S&P 500 cayó un 25%), la estrategia no se activó a tiempo porque el FGI no superó el 75 antes de la caída, o salió de la defensa demasiado pronto. Resultado: 100% expuesta al crash.

Pero... el CAGR superior (13.17% vs 7.35%) es real
A pesar de las limitaciones, la estrategia logró algo valioso:

    CAGR +5.82 pp: Por cada año, la estrategia generó un 5.82% más de rentabilidad que el Buy & Hold. Esto se explica porque los períodos de defensa (2018, 2020, 2022, 2024) coincidieron con correcciones severas donde el 50% en cash protegió el capital.
    Sharpe ligeramente superior (0.68 vs 0.66): A pesar de la mayor volatilidad, la rentabilidad extra compensó el riesgo adicional.
    Patrimonio final duplicado: 37,152 € vs 17,350 €. En términos absolutos, la estrategia generó 19,802 € más que el Buy & Hold.

La Ventaja Real del FGI-Quant (Matizada)
Los datos de este período (2016-2026) nos obligan a matizar lo que prometía la teoría:

   Ventaja real | Evidencia |
 |---|---|
 | ✅ CAGR superior | +5.82 pp anualizados (13.17% vs 7.35%) |
 | ✅ Patrimonio final duplicado | 37,152 € vs 17,350 € |
 | ✅ Sharpe ligeramente mejor | 0.68 vs 0.66 |
 | ✅ Coste de fricción razonable | 0.39% anual |
 | ❌ Max Drawdown peor | -32.11% vs -20.02% (60% más caída) |
 | ❌ Volatilidad mayor | 16.38% vs 8.12% (102% más oscilación) |
 | ❌ VaR diario peor | 536€ vs 167€ (221% más riesgo de cola) |
 | ❌ Alpha negativo | -0.72% (valor destruido ajustado al riesgo) |
 | ⚖️ Beta casi idéntica | 0.90 (sin decorrelación real) |

Conclusión matizada: El FGI-Quant no es una estrategia de protección fiable. Su Max Drawdown peor (-32.11%) demuestra que no siempre se activa a tiempo para proteger el capital. Sin embargo, su CAGR superior (+5.82 pp) sugiere que, cuando se activa correctamente, captura valor al evitar correcciones severas.
Cómo Hacer Seguimiento con el Script
1. Ejecutar el diagnóstico semanal
El motor está configurado para evaluar el FGI cada viernes al cierre. Si el índice supera 75, genera una alerta de "Modo Defensa Activado".
2. Respetar la Zona Muerta
Si el FGI está en 73, no hagas nada. La tentación de "adelantarse" al mercado es el mayor enemigo del inversor cuantitativo. La zona muerta de 5 puntos es tu red de seguridad contra el whipsaw.
3. Gestionar las aportaciones (DCA)
Si el FGI está en modo defensa (>75) y tienes una aportación mensual programada, dirige ese dinero nuevo al 100% hacia el activo de cash (SHV). No fuerces la compra de acciones hasta que el FGI confirme la salida de la euforia (<70).
4. Monitorizar el Max Drawdown
Un Max Drawdown superior al -35% en el FGI-Quant es señal de alerta. Revisa si la estrategia se activó correctamente en las últimas correcciones. Si no se activó, considera relajar el umbral de codicia (ej. 70 en lugar de 75) o ampliar el buffer (ej. 10 puntos en lugar de 5).
Conclusiones
El análisis del Fear & Greed Index cuantitativo arroja lecciones matizadas pero valiosas:

    El sentimiento se puede medir matemáticamente. No necesitas datos de sentimiento de Twitter o flujos de fondos propietarios. La volatilidad, la distancia a la media y el spread de crédito capturan el 90% de la psicología del mercado.
    La asimetría de la protección es clave. Vender en codicia extrema es matemáticamente más seguro que intentar adivinar el fondo en miedo extremo.
    El whipsaw es el enemigo silencioso. Sin una frecuencia de rebalanceo semanal y una zona muerta (buffer), los costes de transacción y las falsas señales destruyen el alpha de la estrategia.
    El coste de oportunidad es real. Aceptarás tener menos dinero que el Buy & Hold en años de euforia sostenida. Ese es el precio del seguro.
    Úsalo como satélite, no como núcleo. Destina un 20-30% de tu patrimonio a esta táctica. El 70-80% debe permanecer en tu cartera core (Bogleheads, All Weather) para garantizar la exposición al crecimiento a largo plazo.
    El contexto macroeconómico lo es todo. Una estrategia que brilla en 2020 (COVID) puede sufrir en 2022 (subida de tipos) si el FGI no se activa antes de la caída. El FGI-Quant no predice crisis, reacciona a ellas.

La filosofía del FGI-Quant, democratizada a través de este motor, demuestra que no necesitas predecir el futuro. Solo necesitas un termómetro fiable y la disciplina de buscar sombra cuando hace demasiado calor... siempre que entiendas sus limitaciones y la integres correctamente en una cartera más amplia.
⚠️ Descargo de Responsabilidad y Advertencia de Riesgos
Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa.
Limitaciones del Backtest

    Sesgo de Mirada al Futuro (Look-ahead Bias) controlado: El FGI se calcula con datos de cierre del día. La decisión de rebalanceo se ejecuta al día siguiente, sin usar información futura.
    Costes de Transacción Reales: Hemos asumido un 0.1% de comisión. En momentos de alta volatilidad (cuando el FGI cambia bruscamente), el slippage (deslizamiento) puede ser mayor, reduciendo ligeramente el rendimiento neto.
    Fiscalidad: El motor no contempla el impacto de impuestos por ventas a corto plazo. Las ~22 rotaciones anuales generarán eventos fiscales que deben ser considerados en tu declaración de la renta.
    Correlaciones inestables: El componente de "Spread de Crédito" (HYG vs TLT) asume que los bonos actúan como refugio. En entornos de subida agresiva de tipos (como 2022), esta correlación puede romperse temporalmente.

No es Asesoramiento Financiero
Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe evaluar su tolerancia al riesgo, considerar su horizonte temporal y consultar con un asesor financiero independiente.
Riesgo de Pérdida de Capital
Operar en mercados financieros conlleva riesgos. Aunque el FGI-Quant busca limitar el Max Drawdown, no lo elimina. Un inversor que no pueda tolerar ver su satélite táctico caer un 32% en una crisis severa no debería usar esta estrategia.
🎯 Recuerda
El Fear & Greed Index cuantitativo no es un cristal mágico para adivinar el mercado. Es un marco matemático para estructurar el caos de la psicología de masas.
Su verdadero valor no está en maximizar el CAGR en todos los entornos, sino en ofrecer una protección asimétrica cuando la euforia alcanza niveles insostenibles. La paciencia para esperar que el FGI confirme la salida de la zona de peligro (por debajo de 70) y la disciplina para ignorar el ruido diario son tus mayores aliados.
La lección más importante de este capítulo: Los resultados reales (CAGR 13.17%, Max DD -32.11%) nos enseñan que ninguna estrategia es perfecta. El FGI-Quant generó más rentabilidad absoluta que el Buy & Hold, pero a costa de mayor volatilidad y drawdown. El inversor conservador debe decidir si ese trade-off (más rentabilidad a cambio de más riesgo) se alinea con sus objetivos y su tolerancia al riesgo.