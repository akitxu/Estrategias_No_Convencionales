Capítulo 8: Event-Driven — Merger Arbitrage con ETFs

    Versión: 8.1 | Motor: Modular Dinámico v1.0 | Última actualización: 2026-10-05

    "El arbitraje de fusiones real es como ser el casino: ganas en la mayoría de las apuestas, pero cuando pierdes, pierdes grande. Y para jugar en ese casino, necesitas información que el inversor minorista simplemente no tiene."
    — Joel Greenblatt, You Can Be a Stock Market Genius

Si los capítulos anteriores nos enseñaron a explotar patrones de precio, sentimiento y relaciones estadísticas entre activos, el Event-Driven Investing representa un cambio de paradigma radical: dejamos de mirar gráficos y empezamos a mirar eventos corporativos discretos (fusiones, adquisiciones, resultados trimestrales, movimientos de insiders) que crean ineficiencias temporales medibles.
El Merger Arbitrage (arbitraje de fusiones) es la estrategia event-driven por excelencia: cuando una empresa anuncia la adquisición de otra, el precio del target sube pero suele quedarse ligeramente por debajo del precio de oferta. Esa diferencia (el spread) refleja el riesgo de que el deal no se cierre (rechazo regulatorio, financiación fallida, etc.). El arbitrajista compra el target y vende el adquirente, apostando a que el spread se cerrará cuando la operación se complete.
Pero aquí viene la advertencia crítica: el merger arbitrage real requiere datos que Yahoo Finance no proporciona (anuncios de OPAs en tiempo real, spreads de convergencia, análisis de riesgo regulatorio). Por eso, en este capítulo construiremos un proxy pedagógico: una estrategia que detecta "sectores en descuento por miedo a M&A fallido" basándose en caídas bruscas (>25% desde máximos) con volumen anómalo.
Esto NO es merger arbitrage real. Es una aproximación que nos permite entender la lógica del event-driven (entrar en dislocaciones, salir en convergencia) y medir si este tipo de señales genera alpha vs. Buy & Hold.
1. La Lógica del Proxy Merger Arbitrage
El concepto original
En el merger arbitrage puro:

    Evento: Empresa A anuncia la adquisición de Empresa B por $50/acción.
    Reacción: El precio de B sube de $40 a $48 (no a $50, porque hay riesgo de que el deal falle).
    Spread: $2 (4% de descuento sobre el precio de oferta).
    Arbitraje: Comprar B a $48, vender A (si es stock deal), esperar a que el deal cierre y B cotice a $50.
    Riesgo: Si el deal falla, B puede caer a $35 o menos.

Nuestro proxy simplificado
Dado que no tenemos datos de OPAs en tiempo real, construimos un proxy basado en:

    Universo: 5 ETFs de sectores históricamente objetivo de consolidación (XBI biotech, IBB biotech, KBE bancos regionales, XRT retail, SMH semiconductores).
    Detección de "eventos":
        Caída >25% desde máximo histórico de 252 días.
        (Opcional) Volumen >2x la media de 20 días.
    Entrada: Asignar 20% del capital al ETF en descuento (dividido entre los activos con señal).
    Salida: Al recuperar el 50% de la caída O después de 6 meses (126 días), lo que ocurra primero.
    Capital no asignado: Cash (SHY).

Limitaciones documentadas

    No es merger arbitrage real: No hay spreads de convergencia ni análisis de deals específicos.
    Las caídas pueden deberse a otros factores: Crisis sectorial, cambios regulatorios, pánico generalizado.
    El volumen anómalo puede ser ruido: Rebalanceos de fondos, pánico minorista, no necesariamente actividad de M&A.
    Sin análisis regulatorio: No evaluamos probabilidad de cierre de deals.

️ 2. Arquitectura Técnica (Motor Dinámico + Detección de Eventos)
El motor cuantitativo de este libro integra un detector de eventos con el MotorBacktestDinamico. El flujo es:

    Bloque 5: Calcula el máximo histórico rolling (252 días) y detecta caídas >25%. Opcionalmente, filtra por volumen anómalo (>2x media de 20 días).
    Bloque 5 (continuación): El generador de pesos asigna 20% del capital a los ETFs con señal activa, y el resto a SHY (cash).
    Bloque 6: El motor ejecuta el backtest con frecuencia semanal, gestionando entradas y salidas según los criterios de recuperación (50%) o plazo máximo (126 días).
    Bloque 7: Calcula métricas y compara con Buy & Hold.

🚫 3. La limitación crítica: sin datos de volumen
Durante el desarrollo de este capítulo, detectamos que Yahoo Finance no proporciona datos de volumen en el DataFrame de precios ajustados (precios_ajustados). Esto tuvo una consecuencia importante:

🔍 Detectando eventos (caídas >25% + volumen >2x media)...
⚠️  No hay datos de volumen. Usando solo caída como señal.

📊 Eventos detectados: 1696
   • XBI: 617 eventos
   • IBB: 325 eventos
   • KBE: 321 eventos
   • XRT: 247 eventos
   • SMH: 186 eventos

   1696 eventos en 10 años es excesivo (casi 170 eventos por año, o ~3 por semana). Esto significa que el umbral del 25% de caída se activó constantemente durante períodos de estrés (COVID-2020, inflación-2022, correcciones sectoriales). Sin el filtro de volumen, la estrategia entró y salió de posiciones con mucha frecuencia, generando costes de transacción y exponiéndose a caídas que no eran temporales.
📈 4. Análisis de Resultados Reales (2015-2025)
Hemos sometido a backtest la estrategia proxy durante un período de 10 años que incluye la recuperación post-crisis financiera (2015-2019), la Pandemia COVID-19 (2020), la subida de tipos (2022-2023) y el rally de la IA (2023-2025).
Informe de Limpieza de Datos

| Activo | ISIN | Filas | Desde | Hasta | Fuente |
|---------------------------|------|------:|------------|------------|--------|
| SPDR S&P Biotech | XBI | 2670 | 2015-01-02 | 2025-08-14 | CSV |
| iShares Biotechnology | IBB | 2670 | 2015-01-02 | 2025-08-14 | CSV |
| SPDR S&P Bank ETF | KBE | 2670 | 2015-01-02 | 2025-08-14 | CSV |
| SPDR S&P Retail | XRT | 2670 | 2015-01-02 | 2025-08-14 | CSV |
| VanEck Semiconductor | SMH | 2670 | 2015-01-02 | 2025-08-14 | CSV |
| iShares 1-3 Year Treasury | SHY | 2670 | 2015-01-02 | 2025-08-14 | CSV |
| SPDR S&P 500 | SPY | 2670 | 2015-01-02 | 2025-08-14 | CSV |

    💡 Insight clave: Los 7 activos tienen datos completos desde el inicio del período. Sin embargo, la falta de datos de volumen limitó la capacidad del detector de eventos para filtrar señales ruidosas.

5. Métricas de Diagnóstico Comparativo

| Métrica | Event-Driven Proxy | Buy & Hold (SPY) | Interpretación |
|----------|------------------:|-----------------:|----------------|
| Patrimonio Final | 14.234 € | ~36.500 € | ❌ Event-Driven obtiene un patrimonio final un 61% inferior al de SPY. |
| CAGR | 3,38% | 12,69% | ❌ Rentabilidad anualizada 9,31 puntos porcentuales menor. |
| Volatilidad | 5,01% | 21,41% | ✅ Reduce la volatilidad en un 77%. |
| Ratio de Sharpe | 0,28 | 0,50 | ❌ Menor eficiencia en la relación riesgo-rentabilidad. |
| Ratio de Sortino | 0,35 | 0,66 | ❌ Peor comportamiento ajustado al riesgo bajista. |
| Máx. Drawdown | -16,28% | -32,58% | ✅ Reduce la caída máxima aproximadamente un 50%. |
| VaR 95% diario | 69,77 € | 777,73 € | ✅ Menor exposición a eventos extremos de mercado. |
| Alpha | 0,01 | 0,00 | ⚖️ Genera una alfa ligeramente positiva. |
| Beta | 0,15 | 0,00 | ✅ Baja sensibilidad a los movimientos del mercado. |
| R² | 0,28 | 0,00 | ⚠️ Solo el 28% de la variación se explica por SPY. |
| Tracking Error | 0,16 | 0,00 | ⚠️ Diferencia moderada respecto al benchmark. |
| Rebalanceos totales | 208 | 0 | ⚠️ Aproximadamente 21 operaciones de rotación al año. |

🧮 6. Matriz de Correlación del Universo

| Activo | XBI | IBB | KBE | XRT | SMH | SHY | SPY |
|---------|----:|----:|----:|----:|----:|----:|----:|
| **XBI** | 1,00 | 0,92 | 0,46 | 0,56 | 0,56 | 0,00 | 0,63 |
| **IBB** | 0,92 | 1,00 | 0,47 | 0,54 | 0,58 | -0,01 | 0,69 |
| **KBE** | 0,46 | 0,47 | 1,00 | 0,66 | 0,51 | -0,20 | 0,71 |
| **XRT** | 0,56 | 0,54 | 0,66 | 1,00 | 0,57 | -0,05 | 0,71 |
| **SMH** | 0,56 | 0,58 | 0,51 | 0,57 | 1,00 | -0,07 | 0,82 |
| **SHY** | 0,00 | -0,01 | -0,20 | -0,05 | -0,07 | 1,00 | -0,08 |
| **SPY** | 0,63 | 0,69 | 0,71 | 0,71 | 0,82 | -0,08 | 1,00 |

    💡 Insight clave: Los ETFs sectoriales tienen correlaciones moderadas entre sí (0.46-0.66), lo que sugiere cierta diversificación. SHY (cash) tiene correlación cercana a cero con todos los activos de riesgo, confirmando su rol como refugio. SMH (semiconductores) tiene la mayor correlación con SPY (0.82), lo que indica que es el más sensible al mercado general.

🤖 7. Diagnóstico Automático
El módulo CalculadorMetricas interpreta estos números y genera el siguiente veredicto cualitativo:

    🟡 Ratio de Sharpe aceptable (0.28): Rentabilidad positiva por unidad de riesgo, pero inferior al Buy & Hold.
    🟢 Riesgo de caída controlado (Max DD: 16.3%): Una caída del 16.3% es manejable psicológicamente, mucho mejor que el -32.6% del Buy & Hold.
    ✅ Beta baja (0.15): La cartera está mayoritariamente en cash, con baja exposición al mercado.
    ️ Alpha marginal (0.01): Prácticamente nulo. La estrategia no generó valor añadido significativo.

📌 8. Nota Pedagógica: ¿Por qué el Proxy Falló en Rentabilidad?
⚠️ La respuesta está en los datos
Los resultados muestran algo contraintuitivo: la estrategia logró un Max Drawdown mucho menor (-16.28% vs -32.58%) y una volatilidad 77% menor (5.01% vs 21.41%), pero un CAGR drásticamente inferior (3.38% vs 12.69%). ¿Por qué?
La respuesta está en la estructura de la estrategia:

    La estrategia estuvo mayoritariamente en cash (SHY): Con una Beta de 0.15 y un R² de 0.28, la cartera pasó la mayor parte del tiempo en SHY, perdiéndose el rally alcista del SPY (+265% en 10 años).
    Demasiados eventos detectados (1696): Sin el filtro de volumen, el umbral del 25% de caída se activó constantemente. La estrategia entró y salió de posiciones con mucha frecuencia, generando costes de transacción (208 rebalanceos) y exponiéndose a caídas que no eran temporales.
    Los ETFs sectoriales no recuperaron rápidamente: Algunos sectores (biotech XBI/IBB, bancos KBE) estuvieron en caída libre durante años (2021-2023 para biotech, 2020-2023 para bancos regionales). El criterio de "recuperar 50% de la caída" no se activó, y las posiciones se cerraron por plazo máximo (6 meses) con pérdidas.
    El período 2015-2025 fue alcista para el mercado general: El SPY subió de ~2,000 a ~5,500 puntos (+175%). Cualquier estrategia que esté mayoritariamente en cash tendrá un rendimiento muy inferior.

✅ Pero... la gestión de riesgo funcionó
A pesar del bajo rendimiento, la estrategia logró algo valioso:

    Max Drawdown 50% menor: -16.28% vs -32.58%. En momentos de crisis, la estrategia protegió el capital al estar en cash.
    Volatilidad 77% menor: 5.01% vs 21.41%. La curva de patrimonio es extremadamente suave.
    VaR 95% diario 91% menor: 69.77 € vs 777.73 €. El riesgo de cola diaria es mínimo.
    Beta 0.15: La cartera es casi independiente del mercado.

Esto sugiere que la lógica event-driven (entrar en dislocaciones, salir en convergencia) funciona para reducir el riesgo, pero no para generar rentabilidad en un mercado alcista.
⚖️ 9. La Ventaja Real del Event-Driven Proxy (matizada)
Los datos de este período (2015-2025) nos obligan a ser honestos sobre las capacidades y limitaciones de este proxy:

| Ventaja / Limitación | Evidencia |
|----------------------|-----------|
| ✅ Max Drawdown menor | -16,28% frente a -32,58% (50% menos caída máxima) |
| ✅ Volatilidad reducida | 5,01% frente a 21,41% (77% menos volatilidad) |
| ✅ VaR diario controlado | 69,77 € frente a 777,73 € (91% menos riesgo de cola) |
| ✅ Beta baja | 0,15 (baja correlación con el mercado) |
| ❌ CAGR muy inferior | 3,38% frente a 12,69% (9,31 puntos porcentuales menos) |
| ❌ Sharpe peor | 0,28 frente a 0,50 (44% peor eficiencia riesgo-rentabilidad) |
| ❌ Demasiados eventos | 1.696 eventos en 10 años (sin filtro de volumen) |
| ⚠️ Alpha marginal | 0,01 (prácticamente nulo) |

    Conclusión matizada: El proxy de Merger Arbitrage logró reducir drásticamente el riesgo (drawdown, volatilidad, VaR), pero no generó rentabilidad competitiva frente al Buy & Hold. La estrategia pasó la mayor parte del tiempo en cash, perdiéndose el rally alcista del mercado. El valor real de este capítulo está en entender la lógica event-driven (entrar en dislocaciones, salir en convergencia), no en los resultados del proxy.

🛠️ 10. Cómo Hacer Seguimiento con el Script
1. Añadir datos de volumen
Para filtrar señales ruidosas, es crítico incluir el filtro de volumen (>2x la media de 20 días). Esto requiere modificar el GestorDatos para incluir datos de volumen en el DataFrame, o descargar los datos de volumen por separado desde Yahoo Finance.
2. Ajustar el umbral de caída
El umbral del 25% de caída generó 1696 eventos en 10 años. Prueba umbrales más estrictos:

    30% de caída: Menos eventos, señales más fuertes.
    40% de caída: Solo crisis severas, muy pocos eventos.

3. Ampliar el plazo máximo
El plazo máximo de 6 meses (126 días) puede ser demasiado corto para sectores que tardan años en recuperarse (ej. biotech 2021-2023). Prueba:

    12 meses (252 días): Más tiempo para la recuperación.
    Sin plazo máximo: Solo salir por recuperación del 50%.

4. Añadir análisis fundamental
Para un proxy más sofisticado, añade filtros fundamentales:

    PER sectorial: Solo entrar si el PER del sector está por debajo de la media histórica.
    Deuda/EBITDA: Evitar sectores con alto apalancamiento (más riesgo de quiebra).
    Flujo de caja: Solo entrar si el sector genera flujo de caja positivo.

5. Validar con datos de M&A reales
Para merger arbitrage real, necesitas:

    Datos de SEC EDGAR: Form 8-K (anuncios de OPAs), Form 14D-9 (respuesta del target).
    Spreads de convergencia: Diferencia entre precio del target y precio de oferta.
    Análisis de riesgo regulatorio: Probabilidad de aprobación antitrust.

11. Conclusiones del Capítulo 8: Event-Driven
📌 Lecciones clave de este capítulo

    El merger arbitrage real requiere infraestructura profesional. Sin datos de OPAs en tiempo real, spreads de convergencia y análisis regulatorio, solo podemos construir proxies simplificados. Este capítulo es pedagógico, no una estrategia ejecutable en real.
    La lógica event-driven es sólida, pero difícil de implementar. Entrar en dislocaciones (caídas bruscas) y salir en convergencia (recuperación parcial) es una lógica válida, pero identificar qué caídas son por M&A y cuáles por otros factores requiere contexto fundamental que este proxy no tiene.
    El volumen anómalo es una señal ruidosa sin contexto. Volumen >2x la media puede indicar actividad institucional, pero también pánico minorista, rebalanceos de fondos, o ruido aleatorio. Sin análisis fundamental, es difícil filtrar señal de ruido.
    El plazo máximo es crítico para gestionar el riesgo. Limitar la exposición a 6 meses evita quedar atrapado en caídas estructurales (no temporales). Es una red de seguridad contra el "value trap".
    La diversificación sectorial reduce riesgo, pero no lo elimina. Monitorizar 5 ETFs de sectores diferentes (biotech, bancos, retail, semis) reduce la dependencia de un solo sector, pero no elimina el riesgo de correlación en crisis sistémicas.
    Estar mayoritariamente en cash tiene un coste de oportunidad enorme. En un mercado alcista (+265% en 10 años), una estrategia que pasa el 85% del tiempo en cash tendrá un rendimiento muy inferior, independientemente de lo bien que gestione el riesgo.
    La honestidad intelectual es obligatoria. Documentar las limitaciones del proxy (no es merger arbitrage real, sin datos de volumen, sin análisis fundamental) es más valioso que presentar resultados inflados.

🔧 Herramientas nuevas que has aprendido a usar

    Detección de eventos basados en caídas desde máximos históricos.
    Gestión de posiciones con plazo máximo y criterio de recuperación parcial.
    Construcción de proxies cuando faltan datos en tiempo real.
    Documentación honesta de limitaciones metodológicas.
    Análisis de correlación entre ETFs sectoriales y cash.

💡 Interpretación honesta
La estrategia logró un Max Drawdown 50% menor (-16.28% vs -32.58%) y una volatilidad 77% menor (5.01% vs 21.41%), pero un CAGR drásticamente inferior (3.38% vs 12.69%). Esto no invalida la lógica event-driven, pero sí demuestra que:

    (a) Sin datos de volumen, el detector de eventos genera demasiadas señales ruidosas.
    (b) Sin análisis fundamental, es difícil distinguir caídas temporales de estructurales.
    (c) Estar mayoritariamente en cash tiene un coste de oportunidad enorme en mercados alcistas.

🚪 Próximo paso
En el Capítulo 9 veremos el "Earnings Surprise": cómo construir una cartera que se beneficie de las sorpresas de resultados trimestrales, usando datos de earnings dates y momentum fundamental. A diferencia del merger arbitrage, el earnings surprise tiene datos más accesibles (earnings dates públicos, consensus estimates de analistas) y puede generar alpha real sin infraestructura profesional.

    🎯 Recuerda
    El Event-Driven real (merger arbitrage, earnings plays, insider trading) requiere infraestructura de datos que Yahoo Finance no proporciona. Este capítulo es una introducción pedagógica a la lógica, no una estrategia ejecutable. Para implementarlo en real, necesitarías:

        Bloomberg Terminal o Reuters Eikon.
        Datos de SEC EDGAR para Form 8-K (anuncios de OPAs).
        Datos de earnings dates y consensus estimates.
        Análisis de riesgo regulatorio y probabilidades de cierre.

    La honestidad intelectual es tu mayor activo como inversor cuantitativo.

️ Descargo de Responsabilidad y Advertencia de Riesgos
Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa.
Esto no es Merger Arbitrage Real
La estrategia presentada es un proxy simplificado. El merger arbitrage real requiere datos de OPAs en tiempo real, spreads de convergencia, y análisis de riesgo regulatorio que este motor no puede proporcionar. Los resultados del backtest no son replicables en un entorno de trading real.
Los resultados pasados no garantizan resultados futuros
El backtest es una simulación histórica basada en datos pasados (2015-2025). Las caídas con volumen anómalo no siempre preceden a oportunidades de M&A. Los patrones detectados pueden no repetirse.
Limitaciones específicas del proxy

    Sin datos de volumen: La estrategia usó solo caídas como señal, generando 1696 eventos en 10 años (excesivo).
    Sin análisis fundamental: No se evaluó PER, deuda, flujo de caja, ni otros indicadores de salud sectorial.
    Sin análisis regulatorio: No se evaluó probabilidad de aprobación antitrust ni riesgos legales.
    Plazo máximo arbitrario: 6 meses puede ser demasiado corto para sectores que tardan años en recuperarse.

No es asesoramiento financiero
Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. Cada inversor debe:

    Evaluar su propia tolerancia al riesgo: Un Max Drawdown del -16.28% es bajo, pero el CAGR del 3.38% puede no cumplir objetivos de rentabilidad.
    Considerar su horizonte temporal: El event-driven está diseñado para meses, no para días.
    Consultar con un asesor financiero independiente antes de tomar decisiones.

Riesgo de pérdida de capital
Operar en mercados financieros conlleva riesgos. Las caídas bruscas pueden no revertir, generando pérdidas permanentes. El proxy no garantiza que las posiciones entren en "oportunidades de M&A" ni que salgan en "convergencia".
Uso del código
El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de:

    Errores en el código o en los datos descargados de Yahoo Finance.
    Pérdidas económicas derivadas del uso de estas herramientas.
    La exactitud de las métricas calculadas (siempre debes verificar los cálculos críticos de forma independiente).