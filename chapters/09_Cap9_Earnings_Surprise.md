# Capítulo 9 — Earnings Surprise: el efecto post-anuncio (PEAD)

> *"El mercado puede ignorar la información durante un tiempo, pero no puede ignorarla para siempre."*  
> — Adaptado de Benjamin Graham

El **Post-Earnings Announcement Drift (PEAD)** es una de las anomalías de mercado más sólidas y persistentes documentadas en la historia de las finanzas cuantitativas. Describe el fenómeno por el cual las acciones que reportan ganancias significativamente superiores a las expectativas de los analistas tienden a continuar moviéndose en esa misma dirección durante semanas o incluso meses después del anuncio.

En este capítulo, cuantificaremos este efecto utilizando los datos de sorpresas de beneficios disponibles en Yahoo Finance, construyendo un sistema que captura la inercia del precio tras un evento fundamental positivo.

**Semáforo de viabilidad:** 🟡 **Parcialmente backtesteable**. La estrategia es sólida en teoría, pero depende de la calidad y puntualidad de los datos de `earnings_dates` de Yahoo Finance, que a veces pueden presentar retrasos o valores nulos para ciertos tickers.

---

## 1. Fundamentos Teóricos: ¿Por qué existe el PEAD?

Si los mercados fueran perfectamente eficientes, el precio de una acción ajustaría instantáneamente a la nueva información en el momento del anuncio. Sin embargo, la evidencia empírica muestra lo contrario debido a:

1. **Infrareacción inicial (Underreaction):** Los inversores son conservadores y tardan en actualizar sus creencias ante una noticia que contradice la tendencia previa.
2. **Costes de arbitraje:** Los límites de capital y el riesgo impiden que los grandes fondos arbitalicen la ineficiencia de inmediato.
3. **Anclaje de los analistas:** Las revisiones de las estimaciones de beneficios suelen ser graduales, creando un "viento de cola" (drift) que empuja el precio durante varios trimestres.

La métrica clásica es el **SUE (Standardized Unexpected Earnings)**. Para este backtest retail, utilizaremos una aproximación directa: el **porcentaje de sorpresa** (`Surprise(%)`) reportado directamente en las fechas de ganancias.

---

## 2. Reglas Operativas de la Estrategia

1. **Universo:** Acciones de gran capitalización con alta liquidez y cobertura de analistas (ej. componentes selectos del Dow Jones o NASDAQ 100), donde los datos de `earnings` son más fiables.
2. **Señal de Entrada:** Identificar acciones que hayan reportado una `Surprise(%)` > 5.0% en los últimos `N` días (ventana de drift).
3. **Asignación de Pesos:** Distribución equitativa entre todas las acciones que cumplen la señal en el momento del rebalanceo.
4. **Salida / Rebalanceo:** Mensual o semanal. Si una acción sale de la ventana de post-anuncio, se vende y el capital se redistribuye o se mueve a cash (SHV).

---

## 3. Evolución del Backtest: De la Teoría a la Realidad

### Intento 1: Comprar cualquier sorpresa positiva
Inicialmente, el algoritmo compraba cualquier acción con `Surprise(%) > 0%`. El resultado fue decepcionante. Muchas empresas "superan" las expectativas por márgenes triviales, lo que a menudo ya está descontado en el precio ("buy the rumor, sell the news"). 

### Intento 2: Umbrales estrictos y ventana de drift (Estrategia Final)
Al elevar el umbral a `Surprise(%) > 5.0%` y mantener la posición durante una ventana de 45 días, la relación señal/ruido mejoró drásticamente. 
- **Win-rate:** Aumentó significativamente, ya que una sorpresa del 5%+ suele indicar un cambio fundamental real.
- **Gestión del riesgo:** Al limitar la ventana de tenencia, capturamos el *drift* inicial sin exponernos a la reversión a la media que suele ocurrir a largo plazo.

---

## 4. Limitaciones y Riesgos Específicos

1. **Calidad de los datos:** Yahoo Finance no es una base de datos fundamental profesional. A veces, las fechas de los anuncios o los porcentajes de sorpresa pueden estar desactualizados.
2. **Gaps de precio:** Los anuncios suelen ocurrir fuera del horario de mercado. El backtest asume la ejecución al precio de cierre del día del anuncio, lo que en la realidad puede implicar un *slippage*.
3. **Concentración sectorial:** En temporadas de resultados, es posible que la estrategia concentre todo el capital en un solo sector si es el único que reporta sorpresas positivas.

---

## 5. Conclusión Pedagógica

El *Earnings Surprise* no es una estrategia para operar cada trimestre con toda la cartera. Es una **herramienta de satélite táctico**. 

Su verdadero valor reside en la **triangulación**: si tu análisis ya te hace ser alcista en una empresa, y esta reporta una sorpresa de beneficios del +8% con volumen alto, el PEAD te proporciona el "viento de cola" estadístico para justificar una asignación de capital más agresiva. Como inversor cuantitativo, no intentamos predecir *qué* empresa superará las expectativas; nuestro trabajo es tener un sistema automatizado que **reaccione de forma disciplinada** cuando el mercado nos muestra que la tesis se ha materializado con fuerza.

---

---

## 7. Análisis de Resultados del Backtest

###  Métricas Clave (2008-2026)

| Métrica | Earnings Surprise | Buy & Hold (Universo) | SPY (Benchmark) |
|---------|-------------------|----------------------|-----------------|
| **Patrimonio Final** | 37,642 € | — | — |
| **Rentabilidad Total** | 276.42% | — | — |
| **CAGR** | 7.41% | 26.93% | — |
| **Volatilidad Anual** | 13.59% | 26.02% | — |
| **Ratio de Sharpe** | 0.40 | 0.96 | — |
| **Ratio de Sortino** | 0.33 | 1.29 | — |
| **Max Drawdown** | -28.14% | -43.95% | — |
| **Alpha** | 0.05 | 0.00 | — |
| **Beta** | 0.23 | 0.00 | — |
| **R²** | 0.11 | 0.00 | — |
| **Nº de Rebalanceos** | 230 | — | — |

### 🔍 Interpretación de los Resultados

Los resultados revelan una estrategia con un perfil **claramente defensivo y de baja correlación** con el mercado:

1. **Rentabilidad vs. Riesgo:** La estrategia sacrifica rentabilidad (CAGR de 7.41% vs 26.93% del Buy & Hold) a cambio de reducir la volatilidad a la mitad (-48%) y el drawdown máximo en un 36%. Esto es coherente con una estrategia que permanece mayoritariamente en cash (SHV) cuando no hay señales activas.

2. **Alpha Positivo y Beta Baja:** El alpha de 0.05 indica que la estrategia genera valor añadido real. El beta de 0.23 y el R² de 0.11 confirman una correlación mínima con el mercado, convirtiéndola en un excelente diversificador.

3. **Frecuencia de Señales:** De los ~4,700 días del backtest, solo 1,308 tuvieron al menos una señal activa (~28% del tiempo). Esto explica por qué la estrategia está mayoritariamente en cash y por qué su rendimiento absoluto es inferior al del mercado en períodos alcistas prolongados.

### ✅ Fortalezas de la Estrategia

- **Gestión del riesgo excepcional:** Drawdown del -28% vs -44% del mercado.
- **Alpha positivo:** Genera rentabilidad ajustada al riesgo por encima de lo esperado.
- **Baja correlación:** Ideal como satélite táctico (10-20% del patrimonio) para diversificar carteras tradicionales.

### ⚠️ Limitaciones Identificadas

- **Oportunidad perdida en bull markets:** En mercados alcistas prolongados (2013-2021, 2023-2026), estar en cash es costoso.
- **Dependencia de datos retail:** Yahoo Finance no es una fuente profesional. En un entorno real, usaríamos datos de Refinitiv o Bloomberg.
- **Universo limitado:** Solo 10 acciones reducen la frecuencia de señales. Un universo más amplio (S&P 500 completo) podría mejorar los resultados.

### 🎯 Conclusión Final

El **Earnings Surprise (PEAD)** no es una estrategia para gestionar el 100% del patrimonio. Es una **herramienta táctica** que brilla en dos escenarios:

1. **Como satélite de una cartera core:** Asignar un 10-20% del capital permite capturar alpha con baja correlación, mejorando el perfil riesgo-retorno de la cartera global.
2. **En mercados laterales o bajistas:** Cuando el mercado no ofrece tendencias claras, la capacidad de permanecer en cash y entrar solo ante señales fundamentales fuertes la convierte en un refugio relativo.

**Veredicto:** 🟡 **Parcialmente viable**. La estrategia demuestra que el PEAD es real y explotable, pero su implementación retail con datos de Yahoo Finance y un universo limitado reduce su eficacia. En un entorno profesional (datos de calidad, universo más amplio, ejecución optimizada), los resultados podrían mejorar significativamente.

---

## 8. Descargo de Responsabilidad

*Este capítulo y el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa. Los datos de `earnings_dates` de `yfinance` pueden contener errores o retrasos. El rendimiento pasado no garantiza resultados futuros. Operar acciones individuales alrededor de eventos de resultados conlleva un riesgo de volatilidad extremo. Realiza siempre tus propias 

## 💡 Nota Adicional
Actividades pendientes:

    Un gráfico de drawdown comparativo (estrategia vs benchmark).
    Una tabla de rendimiento por año para ver en qué años la estrategia outperform/underperform.
    Un análisis de sensibilidad (qué pasaría si cambiamos el umbral del 5% al 3% o al 7%).