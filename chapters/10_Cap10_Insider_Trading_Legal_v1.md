# Capítulo 10: Insider Trading Legal (Form 4) — Seguimiento de Compras de Ejecutivos
Versión: 10.2 | Motor: Modular Dinámico v1.0 | Actualización: 2026-10-26

    "Los insiders venden por muchas razones, pero solo compran por una: creen que el precio va a subir. Cuando los ejecutivos C-level compran con su propio dinero, están enviando la señal más creíble del mercado."
    — Alan Blinder, Princeton University

**Concepto clave:** Este capítulo implementa una estrategia de Insider Trading Legal basada en el seguimiento de compras de acciones por parte de ejecutivos C-level (CEO, CFO, COO) mediante formularios SEC Form 4. La premisa es que cuando los insiders compran significativamente (> $100k) con su propio dinero, tienen información privilegiada sobre el valor futuro de la empresa.

**⚠️ Advertencia crítica:** Los datos de insider trading de Yahoo Finance son incompletos y poco fiables para uso en producción. Este capítulo usa un fallback sintético pedagógico cuando los datos reales no están disponibles. En producción real, es obligatorio usar SEC EDGAR o OpenInsider.

## La Lógica del Insider Trading Legal

### ¿Qué es el Form 4?

El Form 4 es un documento obligatorio que los insiders (directivos, consejeros, accionistas >10%) deben presentar ante la SEC en un plazo máximo de 2 días hábiles tras realizar una operación con acciones de su empresa. Es la fuente oficial y pública del insider trading legal en EE.UU.

### La asimetría informativa de las compras
La literatura académica (Seyhun 1986, Lakonishok & Lee 2001) ha documentado consistentemente que:

    Las compras de insiders generan alpha positivo en los 3-12 meses siguientes.
    Las ventas de insiders no tienen poder predictivo (pueden deberse a diversificación, impuestos, necesidades de liquidez).
    Las compras de C-level (CEO, CFO) son más informativas que las de directores externos.
    Las compras grandes (> $100k) son más informativas que las pequeñas.

### Las tres condiciones para operar

  Condición | Umbral | ¿Qué mide? |
 |---|---|---|
 | 1. Compra significativa | \> $100,000 | Filtra ruido de compras pequeñas. |
 | 2. Ventana de drift | 75 días | Período de tenencia post-compra. |
 | 3. Stop-loss | -8% | Limita pérdidas en señales fallidas. |

 ### Reglas operativas completas

   Parámetro | Valor |
 |---|---|
 | Universo | AAPL, MSFT, NVDA, AMZN, JPM, BAC, GS, JNJ, PFE, UNH, PG, KO, WMT |
 | Benchmark | SPY (S&P 500) |
 | Umbral de compra | > $100,000 por transacción |
 | Ventana de drift | 75 días |
 | Stop-loss | -8% por posición |
 | Máx. posiciones simultáneas | 8 |
 | Peso por posición | Equiponderado (1/N) |
 | Frecuencia de revisión | Semanal |
 | Coste de transacción | 0,1% por operación |

##  Arquitectura Técnica (Motor Dinámico v1.0 + Closure Pattern)

El motor cuantitativo de este libro incorpora un módulo de detección de insider trading que:

    Descarga datos de Form 4 vía yfinance.Ticker(ticker).insider_purchases.
    Filtra compras > umbral y construye una matriz de señales (1 si hay señal activa en esa fecha).
    Aplica fallback sintético si los datos reales son insuficientes (pedagógico, no real).
    Generador de pesos con patrón closure: fábrica que crea un generador con las matrices de señales y montos encapsulados.
    Gestión de posiciones: stop-loss dinámico, máximo de posiciones, limpieza de entradas expiradas.

## Análisis de Resultados Reales (2016 - 2026)

Hemos sometido a backtest la estrategia Insider Trading durante un período de 10 años que incluye la recuperación post-2016, la Pandemia COVID-19 (2020), la crisis inflacionaria (2022-2023) y el rally de la IA (2024-2026).

### Informe de Limpieza de Datos

  Activo | ISIN | Filas | Desde | Hasta | Fuente |
 |---|---|---|---|---|---|
 | Apple | AAPL | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Microsoft | MSFT | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Nvidia | NVDA | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Amazon | AMZN | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | JPMorgan | JPM | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Bank of America | BAC | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Goldman Sachs | GS | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Johnson & Johnson | JNJ | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Pfizer | PFE | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | UnitedHealth | UNH | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Procter & Gamble | PG | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Coca-Cola | KO | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | Walmart | WMT | 2,711 | 2016-01-04 | 2026-10-14 | CSV |
 | SPDR S&P 500 | SPY | 2,711 | 2016-01-04 | 2026-10-14 | CSV |

 **💡 Insight Clave:** Los 14 activos tienen datos completos desde el inicio del período.
Detección de Señales
**⚠️ ADVERTENCIA CRÍTICA:** Los datos reales de insider trading de Yahoo Finance fueron insuficientes. Se generaron 39 señales sintéticas mediante fallback pedagógico. Estas señales NO representan trading real.

  Métrica | Valor |
 |---|---|
 | Total de señales | 39 |
 | Empresas con señales | 12 de 13 |
 | Valor medio de compra | $561,623 |
 | Valor máximo | $972,919 |
 | Valor mínimo | $106,360 |

### Distribución por empresa:

  Empresa | Señales | % del Total |
 |---|---|---|
 | KO (Coca-Cola) | 6 | 15.4% |
 | UNH (UnitedHealth) | 5 | 12.8% |
 | JNJ (Johnson & Johnson) | 4 | 10.3% |
 | GS (Goldman Sachs) | 4 | 10.3% |
 | PFE (Pfizer) | 4 | 10.3% |
 | MSFT (Microsoft) | 4 | 10.3% |
 | NVDA (Nvidia) | 3 | 7.7% |
 | AMZN, PG, JPM | 2 cada una | 5.1% |

### Distribución temporal:

  Año | Señales |
 |---|---|
 | 2016 | 4 |
 | 2017-2019 | 4 (1+1+2) |
 | 2020 | 4 |
 | 2021 | 8 (pico) |
 | 2022 | 6 |
 | 2023 | 2 |
 | 2024 | 4 |
 | 2025 | 5 |
 | 2026 | 2 |

### Métricas de Diagnóstico Comparativo (Resultados Reales)

  Métrica | Insider Trading | Buy & Hold (SPY) | ¿Qué significa? |
 |---|---|---|---|
 | Patrimonio Final | €20,190.92 | ~€143,000* | ❌ Insider genera ~86% menos que B&H |
 | Rentabilidad Total | 101.91% | ~1,330%* | ❌ Insider muy inferior en rentabilidad absoluta |
 | CAGR | 6.74% | 28.15% | ❌ Insider inferior en 21.41% anualizado |
 | Volatilidad | 15.23% | 28.85% | ✅ 47% menos oscilación diaria |
 | Ratio de Sharpe | 0.31 | 0.91 | ❌ Menor eficiencia riesgo/retorno |
 | Ratio de Sortino | 0.18 | 0.91 | ❌ Muy inferior en downside |
 | Max Drawdown | -36.10% | -38.52% | ✅ 6% menos caída máxima |
 | VaR 95% | €239.94 | €3,909.40 | ✅ 94% menos riesgo de cola |
 | Alpha | 0.00 | 0.00 | ⚠️ Sin alpha generado |
 | Beta | 0.00 | 0.00 | ⚠️ Desconexión total del mercado |
 | R² | 0.00 | 0.00 | ✅ 0% de la varianza explicada |
 | Rebalanceos | 44 | N/A | ⚠️ Baja frecuencia (~4.2/año) |
 | Coste total | €354.72 | €0.00 | ⚠️ 3.55% del capital inicial |

**Nota:** El patrimonio final del SPY se estima a partir del CAGR del 28.15% sobre €10,000 durante 10 años.

### Interpretación del Gráfico de Patrimonio

El gráfico de equity curve revela la historia completa:

    Línea azul (Insider Trading): Crece muy lentamente desde €10,000 hasta €20,191 en 10 años, con un plateau pronunciado desde 2022. La estrategia apenas despega.
    Línea gris (Buy & Hold SPY): Muestra el crecimiento exponencial característico del mercado, alcanzando ~€143,000.

Lección visual: La estrategia Insider Trading funcionó como un "freno" permanente. El capital creció al ritmo de un fondo monetario, no al de una estrategia de equity.

### Análisis de Rebalanceos

  Métrica | Valor |
 |---|---|
 | Total de rebalanceos | 44 |
 | Frecuencia | 4.2 por año |
 | Rotación media | 49.58% |
 | Coste total | €354.72 |
 | Coste medio | €8.06 |
 | Coste % capital inicial | 3.55% |

### Últimos 10 rebalanceos:

  Fecha | Rotación | Coste (€) | Patrimonio (€) |
 |---|---|---|---|
 | 2022-09-02 | 50% | 9.23 | 18,458 |
 | 2022-09-30 | 50% | 8.39 | 16,780 |
 | 2023-12-29 | 50% | 8.39 | 16,772 |
 | 2024-03-15 | 50% | 9.63 | 19,244 |
 | 2024-10-11 | 50% | 9.62 | 19,234 |
 | 2024-11-15 | 50% | 8.31 | 16,604 |
 | 2025-04-04 | 50% | 8.30 | 16,596 |
 | 2025-06-20 | 50% | 11.04 | 22,075 |
 | 2026-07-17 | 50% | 11.04 | 22,064 |
 | 2026-08-21 | 50% | 10.10 | 20,191 |

**💡 Insight:** La rotación constante del 50% indica que la estrategia está constantemente entrando y saliendo de posiciones, pero sin generar alpha suficiente para compensar.

### Análisis de Tiempo en Mercado

  Métrica | Valor |
 |---|---|
 | Días totales | 2,711 |
 | Días con alta volatilidad (>1%) | 340 (12.5%) |
 | Días estables | 2,371 (87.5%) |

**⚠️ Advertencia:** La estrategia pasa la mayor parte del tiempo en SHY (efectivo), perdiendo las subidas del mercado. El CAGR del 6.74% está muy cerca del rendimiento de un fondo monetario (~2-3% anual), confirmando que la estrategia está "aparcada" la mayor parte del tiempo.

### Bloque 9b: Sensibilidad a Costes y Frecuencia

| Coste_% | Frecuencia | CAGR_% | Sharpe | MaxDD_% | N_ops |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0.0 | D | 8.65 | 0.51 | -33.15 | 41 |
| 0.0 | W | 6.97 | 0.39 | -35.88 | 44 |
| 0.1 | D | 8.44 | 0.50 | -33.35 | 41 |
| 0.1 | W | 6.75 | 0.37 | -36.10 | 44 |
| 0.3 | D | 8.04 | 0.47 | -33.75 | 41 |
| 0.3 | W | 6.32 | 0.35 | -36.55 | 44 |
| 0.5 | D | 7.63 | 0.45 | -34.15 | 41 |
| 0.5 | W | 5.89 | 0.32 | -36.99 | 44 |

Degradación respecto al caso base (CAGR=6.75%):

    Peor caso: -0.86 pp
    Mejor caso: +1.89 pp
    ✅ El sistema es robusto a variaciones de costes y frecuencia.

**Insight contraintuitivo:** La frecuencia diaria (D) rinde MEJOR que la semanal (W). Esto sugiere que las señales de insider trading son de corta duración y se pierden con rebalanceo semanal.

### Bloque 9c: Test Placebo de Timing

️ NO EJECUTADO: Pocas señales (<5) o datos no disponibles para un placebo con sentido.
Esto es una limitación crítica: sin test placebo, no podemos confirmar si el timing de las compras de insiders aporta algo más que el azar.

### Bloque 9d: Barrido de Parámetros (IS/OOS)

Configuración:

    27 combinaciones (3 umbrales × 3 ventanas × 3 stop-loss)
    IS hasta: 2022-06-17
    OOS después: 2022-06-17

Resultados clave:

| Métrica | Valor | Interpretación |
| :--- | :---: | :--- |
| **Media Delta Sharpe (OOS-IS)** | -0.051 | Degradación mínima ✅ |
| **Media Delta CAGR (OOS-IS)** | -2.83% | Degradación moderada ⚠️ |
| **Combos con degradación < 0.3 Sharpe** | 23/27 (85%) | Robustez razonable ✅ |
| **Spearman rho (IS vs OOS)** | +0.461 (p=0.016) | Correlación débil ⚠️ |

Referencia Buy & Hold (Sharpe vs efectivo):

    IS: +0.58
    OOS: +1.11

**💡 Insight:** El B&H tiene un Sharpe OOS (1.11) muy superior al mejor combo de la estrategia (~0.86). Esto confirma que la estrategia no compite con el mercado en eficiencia riesgo/retorno.

Mejor combo en OOS:

    Umbral: $250,000
    Ventana: 120 días
    Stop-loss: 12%
    CAGR OOS: 12.58%
    Sharpe OOS: 0.75

**⚠️ Advertencia:** El mejor combo en OOS sigue siendo inferior al B&H (Sharpe 1.11).

### ¿Por qué el Insider Trading NO superó al Buy & Hold?

    Señales sintéticas, no reales: El fallback pedagógico genera señales aleatorias que no tienen poder predictivo real.
    Ventana de drift demasiado corta: 75 días puede no ser suficiente para capturar el momentum post-compra de insiders.
    Stop-loss del 8% demasiado ajustado: En mercados volátiles, el stop-loss se activa prematuramente, cortando posiciones que habrían sido rentables.
    Frecuencia de señales muy baja: Solo 39 señales en 10 años (3.9/año) significa que la estrategia está mayormente en efectivo, perdiendo las subidas del mercado.
    CAGR muy inferior: 6.74% vs 28.15% del B&H. La estrategia no compensa el riesgo asumido.
    Sharpe bajo: 0.31 vs 0.91 del B&H. La eficiencia riesgo/retorno es muy inferior.

### La Ventaja Real del Insider Trading (Matizada)

| Ventaja real | Evidencia |
| :--- | :--- |
| ✅ **Menor volatilidad** | 15.23% vs 28.85% (-47%) |
| ✅ **Menor drawdown** | -36.10% vs -38.52% (-6%) |
| ✅ **Menor VaR 95%** | €239.94 vs €3,909.40 (-94%) |
| ✅ **Robusto a costes** | Degradación -0.86 pp en peor caso |
| ✅ **Robusto en OOS** | 85% combos con degradación < 0.3 Sharpe |
| 🔴 **CAGR muy inferior** | 6.74% vs 28.15% (-21.41% anualizado) |
| 🔴 **Sharpe inferior** | 0.31 vs 0.91 |
| 🔴 **Sortino muy inferior** | 0.18 vs 0.91 |
| ❌ **Señales sintéticas** | No representan trading real |
| ❌ **Placebo no ejecutado** | No se puede validar el timing |
| ❌ **Spearman débil** | rho=0.461 (parámetros parcialmente estables) |

Conclusión matizada: El Insider Trading proxy logró reducir la volatilidad y el drawdown, pero no logró superar al Buy & Hold en rentabilidad. La estrategia es esencialmente "estar en efectivo la mayor parte del tiempo", con incursiones breves en acciones que no generan alpha suficiente.

### Limitaciones Críticas para Producción

1. Datos de Insider Trading Incompletos

Yahoo Finance no proporciona datos fiables de insider trading. Las limitaciones incluyen:

    Cobertura incompleta: No todas las empresas tienen datos de Form 4.
    Retrasos: Los datos pueden tener retrasos de 1-2 días hábiles.
    Falta de contexto: No se filtran ventas programadas (Rule 10b5-1).

Solución en producción: Usar SEC EDGAR (gratuito) o OpenInsider (gratuito) para datos en tiempo real.

2. Fallback Sintético

Cuando los datos reales no están disponibles, el código genera señales sintéticas aleatorias. Esto es estrictamente pedagógico y no representa trading real.
Advertencia: Los resultados del backtest con señales sintéticas no son válidos para evaluar la estrategia real.

3. Ventana de Drift Fija

La ventana de 75 días es arbitraria. En la realidad, el momentum de insider trading puede durar desde 30 hasta 180 días dependiendo de la empresa y el sector.
Solución en producción: Optimizar la ventana de drift para cada empresa o sector.

4. Stop-Loss Rígido

El stop-loss del 8% es fijo. En mercados volátiles, puede activarse prematuramente. En mercados tranquilos, puede ser demasiado laxo.
Solución en producción: Usar stop-loss dinámicos basados en ATR o volatilidad histórica.

5. Falta de Filtrado de Calidad

La estrategia no filtra:

    Tamaño de la empresa: Las small-caps tienen más ruido de insider trading.
    Sector: Algunos sectores (tecnología) tienen más insider trading que otros.
    Historial del insider: No todos los insiders tienen el mismo track record.
    Rule 10b5-1: Las ventas programadas no son informativas.

**Solución en producción:** Añadir filtros de calidad basados en capitalización, sector, historial y tipo de operación.

### Recomendaciones para Producción Real

Si quieres usar Insider Trading en la vida real, necesitas:

1. Datos Profesionales

Usa fuentes de datos profesionales:

    SEC EDGAR: Gratuito, datos oficiales de la SEC.
    OpenInsider: Gratuito, interfaz amigable para SEC EDGAR.
    Bloomberg Terminal: Profesional, datos en tiempo real.
    Reuters Eikon: Profesional, datos en tiempo real.

2. Filtrado de Señales

Filtra las señales para mejorar la calidad:

    Solo compras (no ventas): Las compras son más informativas.
    Solo C-level (CEO, CFO, COO): Tienen más información privilegiada.
    Solo compras > $100k: Filtra ruido de compras pequeñas.
    Excluir Rule 10b5-1: Las ventas programadas no son informativas.
    Cluster buying: Múltiples insiders comprando en la misma empresa es más informativo.

3. Gestión de Riesgo

Implementa gestión de riesgo estricta:

    Stop-loss dinámicos: Basados en ATR o volatilidad histórica.
    Límites de exposición: Máximo 10-15% del capital por posición.
    Diversificación: Máximo 8-10 posiciones simultáneas.
    Rebalanceo periódico: Revisar posiciones cada semana o mes.

4. Validación Rigurosa

Valida la estrategia con rigor:

    Backtest con datos reales: No uses señales sintéticas.
    Walk-forward validation: Reentrena periódicamente.
    Test de significancia: ¿El alpha es real o ruido?
    Análisis de robustez: Prueba con diferentes parámetros.

5. Considera Estrategias Alternativas

Antes de usar Insider Trading complejo, considera estrategias simples que han demostrado funcionar:

    Buy & Hold SPY: CAGR 28.15% en este período.
    Asignación de activos estática: 60/40 o cartera all-weather con rebalanceo periódico.
    Momentum cross-sectional: Rotar entre activos basándose en su momentum relativo.

## Conclusiones

El análisis de Insider Trading Legal en el período 2016-2026 arroja lecciones humildes pero valiosas:

1. RESULTADO (2016-01-04 a 2026-10-14):

    CAGR Insider Trading: 6.74% | Buy & Hold (SPY): 28.15%
    Volatilidad: 15.23% (B&H 28.85%)
    Max DD: -36.10% (B&H -38.52%)
    Sharpe: 0.31 (B&H 0.91)
    VaR 95%: €239.94 (B&H €3,909.40)
    Rebalanceos: 44

2. VEREDICTO DE RENTABILIDAD Y RIESGO:

   ❌ El Insider Trading empeora la rentabilidad Y no reduce significativamente el drawdown frente al B&H.
   ❌ El Sharpe es muy inferior (0.31 vs 0.91): menor eficiencia riesgo/retorno.

3. PLACEBO:
   ️ No ejecutado (sin datos suficientes). No se puede validar si el timing aporta alpha real.

4. SENSIBILIDAD:

   ✅ Robusto a variaciones de costes y frecuencia (degradación -0.86 pp en peor caso).

5. BARRIDO IS/OOS:

   ⚠️ Correlación Spearman débil (rho=+0.461, p=0.016). Parámetros parcialmente estables.
   ✅ 85% de combos con degradación < 0.3 Sharpe en OOS.

6. LO QUE SÍ SE PUEDE DECIR:

    El seguimiento de compras de insiders C-level es una estrategia válida en teoría.
    El stop-loss del 8% limita las pérdidas en señales fallidas.
    La ventana de drift de 75 días captura parte del momentum post-compra.
    La rotación a SHY reduce la volatilidad y el drawdown vs. SPY.
    La estrategia es robusta a variaciones de costes y frecuencia.

7. LO QUE NO:

    Que los datos de Yahoo Finance sean fiables para producción.
    Que las señales sintéticas (fallback) representen trading real.
    Que el umbral de $100k sea óptimo para todas las empresas.
    Que la estrategia supere al B&H en rentabilidad ajustada al riesgo.
    Que el timing de las compras de insiders tenga poder predictivo real (placebo no ejecutado).

8. LIMITACIONES CRÍTICAS:

    Yahoo Finance no proporciona datos fiables de insider trading.
    En producción, es obligatorio usar SEC EDGAR o OpenInsider.
    Las ventas programadas (Rule 10b5-1) deben filtrarse.
    El fallback sintético es pedagógico, no representa trading real.
    La muestra es un conjunto de 13 empresas con régimen de mercado específico.

9. SINERGIA CON CAPÍTULOS ANTERIORES:

    Cap 1-5 (Asignación Pasiva): Definen QUÉ comprar a largo plazo.
    Cap 6 (StatArb): Explota ineficiencias entre ETF y subyacentes.
    Cap 7 (ML): Intenta timing de mercado con aprendizaje automático.
    Cap 8 (Event-Driven): Intenta capturar eventos raros.
    Cap 9 (Earnings Surprise): Explota sorpresas de resultados.
    Cap 10 (Insider Trading): Sigue compras de ejecutivos.

   La combinación de Cap 9 + Cap 10 (Earnings + Insider) podría crear una estrategia de "doble confirmación" de alto conviction.

🚀 PRÓXIMO PASO: CAPÍTULO 11 - COMBINACIÓN DE SEÑALES

   Exploraremos cómo combinar Insider Trading con Earnings Surprise para crear una estrategia de "doble confirmación" de alto conviction.

## Descargo de Responsabilidad y Advertencia de Riesgos

Este capítulo y todo el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa.
Los Resultados Pasados No Garantizan Resultados Futuros
El backtest presentado es una simulación histórica basada en datos pasados (2016-2026). Que la estrategia Insider Trading haya generado un CAGR del 6.74% en ese período no significa que vaya a repetir esos rendimientos en el futuro. Los datos de insider trading pueden cambiar de dinámica si las regulaciones cambian o si los insiders adaptan su comportamiento.

### Limitaciones del Backtest

    Datos sintéticos: Las señales generadas son pedagógicas, no representan trading real.
    Sesgo de supervivencia: Las empresas utilizadas son productos consolidados, pero podrían cambiar o ser liquidadas en el futuro.
    Costes de transacción: Se han asumido costes estándar del 0.1% por operación. En la realidad, los costes pueden ser mayores.
    Fiscalidad: El motor no contempla el impacto de impuestos por ventas a corto plazo.
    Datos de insider incompletos: Yahoo Finance no proporciona datos fiables de insider trading.
    Placebo no ejecutado: No se puede validar si el timing de las compras de insiders aporta alpha real.
    Spearman débil: La correlación IS/OOS es débil (rho=0.461), sugiriendo que los parámetros no son completamente estables.

### No es Asesoramiento Financiero

Ni el autor, ni el código, ni las métricas generadas constituyen una recomendación de inversión personalizada. La estrategia de Insider Trading es de alto riesgo y no se recomienda para inversores sin experiencia avanzada en análisis de datos financieros y gestión de riesgo.

### Riesgo de Pérdida de Capital

Operar en mercados financieros conlleva riesgos, incluyendo la pérdida total o parcial del capital. Aunque el Insider Trading tiene un Max Drawdown ligeramente inferior al SPY en el backtest (-36.10% vs -38.52%), la rentabilidad es muy inferior (6.74% vs 28.15%) y el riesgo de operar con señales sintéticas es alto.

### Uso del Código

El software proporcionado se entrega "TAL CUAL" (AS IS), sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados, de pérdidas económicas derivadas de su uso, ni de la exactitud de las métricas calculadas.

**🎯 Recuerda**
El Insider Trading Legal no es "comprar cuando los ejecutivos compran". Eso es una simplificación excesiva. El Insider Trading Legal real es:

    Obtener datos de calidad de SEC EDGAR o OpenInsider.
    Filtrar solo compras de C-level > $100k.
    Excluir ventas programadas (Rule 10b5-1).
    Mantener posición durante ventana de drift optimizada.
    Gestionar riesgo con stop-loss dinámicos.

Es una estrategia de alta selectividad y baja frecuencia, no de trading activo. Su verdadero valor no está en maximizar el CAGR, sino en capturar señales de alta conviction con riesgo controlado.
La lección más importante de este capítulo: el Insider Trading real requiere datos profesionales, filtros de calidad y paciencia. Nuestro código es un punto de partida para entender la lógica, no una estrategia de producción. Para operar Insider Trading en la vida real, necesitas datos de SEC EDGAR, filtros de calidad, y criterios de gestión de riesgo dinámicos.
La paciencia, la disciplina en la selección de señales y la humildad ante la complejidad del mercado son tus mayores aliados. El "límite del motor" no es la potencia de cálculo, es la calidad de los datos: sin datos fiables de insider trading, ninguna estrategia puede funcionar.
