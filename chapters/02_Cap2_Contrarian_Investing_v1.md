# Capítulo 11 — Carry Trade: cobrar el diferencial de tipos

> *"El Carry Trade es como recoger monedas delante de una apisonadora: 
> funciona el 90% del tiempo, pero cuando falla, lo pierde todo."*  
> — Dicho popular en macroeconomía

## Semáforo de viabilidad: 🟡 Parcialmente viable (con filtros estrictos)

El Carry Trade "naive" (long en divisas de alto rendimiento, short en divisas 
de bajo rendimiento, y mantener) **quiebra sistemáticamente en crisis de 
liquidez** (2008, marzo 2020). Solo es viable si se combina con:
1. Un filtro de volatilidad que actúe como "freno de emergencia".
2. Una gestión de riesgo estricta (stop-loss, límites de posición).
3. Datos de tipos de interés en tiempo real (no disponibles gratis con calidad).

**Nota sobre esta implementación:** Este notebook presenta una **versión 
pedagógica Long-Only** (solo compramos divisas de alto rendimiento, sin hacer 
short de las de bajo rendimiento). Una implementación profesional requeriría 
short selling real, datos de tipos de interés dinámicos y gestión de margen. 
Al final del capítulo detallamos qué faltaría.

---

## 1. Fundamentos Teóricos

### 1.1 La Paridad del Interés No Cubierta (UIP)
[contenido actual]

### 1.2 La Anomalía del Carry
[contenido actual]

### 1.3 Por qué funciona (y por qué a veces no)
[contenido actual + añadir: el carry trade es esencialmente vender seguro 
contra crisis globales]

---

## 2. Reglas Operativas de ESTA Implementación

### 2.1 Universo
- **Long:** AUD (FXA), GBP (FXB) — divisas históricamente de alto rendimiento
- **Cash:** SHV (iShares Short Treasury) — refugio cuando hay pánico
- **Benchmark:** UUP (Invesco DB US Dollar Index)
- **Filtro de volatilidad:** SPY realized vol 60d > 20% → 100% cash

### 2.2 Señal de Entrada
[contenido actual]

### 2.3 Gestión del Riesgo
[contenido actual + explicar por qué usamos Long-Only en lugar de Long/Short]

---

## 3. Resultados del Backtest (2007-2026)

### 3.1 Métricas Clave
[tabla con CAGR, Sharpe, MaxDD, Beta, correlación SPY, % días en cash]

### 3.2 Interpretación Honesta
- ✅ Lo que funciona: el filtro de volatilidad **protege en crisis** (mostrar 
  gráfico de drawdown comparado con Buy & Hold)
- ⚠️ Lo que no funciona: underperformance en mercados alcistas tranquilos 
  (el filtro saca de mercado demasiado pronto a veces)
- ❌ Limitación estructural: al ser Long-Only, no capturamos el diferencial 
  de tipos completo (eso requeriría short)

### 3.3 Análisis del Filtro de Volatilidad
[tabla con días en cash vs días en FX, y rendimiento en cada régimen]

---

## 4. ⚠️ Lo que FALTA para una Implementación Profesional

Esta es la sección nueva que pediste. La estructuro así:

### 4.1 Short Selling Real (el gap más importante)
**Lo que hicimos:** Long-Only en AUD y GBP.
**Lo que haría un profesional:** Long en AUD/GBP + Short en JPY/CHF, 
aprovechando el diferencial completo.
**Por qué no lo hicimos:**
- El short selling de ETFs requiere cuenta de margen.
- Los costes de préstamo de acciones variables (pueden ser 1-5% anual en JPY).
- Riesgo de "short squeeze" en crisis (cuando todos quieren comprar JPY a la vez).
**Cómo implementarlo:** Usar futuros de divisas (CME) o CFDs con gestión 
de margen estricta.

### 4.2 Datos de Tipos de Interés Dinámicos
**Lo que hicimos:** Asumimos que AUD/GBP son siempre "high yield" y JPY/CHF 
siempre "funding".
**Lo que haría un profesional:** Recalcular el carry diario usando tipos 
oficiales de cada banco central.
**Por qué no lo hicimos:**
- Los tipos cambian (ej: el Fed Funds pasó de 5.25% a 0% en 2008).
- Necesitaríamos API de FRED o datos de Bloomberg/Refinitiv.
**Cómo implementarlo:**
```python
# Ejemplo con FRED (gratuito, requiere clave API)
import pandas_datareader.data as web
fed_funds = web.DataReader('FEDFUNDS', 'fred', start, end)
boj_rate = web.DataReader('IR3TIB01JPM156N', 'fred', start, end)
# Calcular carry diario = tipo_long - tipo_short

4.3 Costes de Transacción Realistas
Lo que hicimos: 0.2% por operación (≈10 pb/lado).
Lo que haría un profesional:

    Spread bid-ask real de cada ETF (varía 1-5 pb según liquidez).
    Slippage por impacto de mercado (especialmente en emergentes como MXN).
    Tracking error del ETF vs divisa spot (~0.1-0.3% anual).
    Comisiones del broker.
    Cómo implementarlo: Modelar cada componente por separado y sumarlos.

4.4 Gestión de Margen y Riesgo de Cola
Lo que hicimos: Stop-loss del 8% y filtro de volatilidad.
Lo que haría un profesional:

    VaR (Value at Risk) diario con límites estrictos.
    Stress testing con escenarios históricos (2008, 2020, 2015 CHF shock).
    Límites de exposición por divisa y por correlación.
    Hedging con opciones (comprar puts OTM como seguro).
    Cómo implementarlo:
    ```
    # Ejemplo de VaR histórico
var_95 = np.percentile(rentabilidades, 5)
if var_95 < -0.02:  # Si el VaR 95% supera -2%, reducir exposición
    reducir_posiciones()
    ```
4.5 Universo Más Amplio
Lo que hicimos: 4 divisas G10 (AUD, GBP, JPY, CHF).
Lo que haría un profesional:

    Incluir emergentes de alto carry (MXN, BRL, ZAR, TRY) — mayor alpha, mayor riesgo.
    Incluir divisas europeas (EUR, NOK, SEK).
    Ponderar por liquidez y por carry (no equitativo).
    Cómo implementarlo: Expandir UNIVERSO_FX y ajustar pesos por 
    carry_score / volatilidad.

4.6 Datos en Tiempo Real y Ejecución
Lo que hicimos: Backtest con datos históricos diarios.
Lo que haría un profesional:

    Datos intradía para timing preciso.
    Ejecución algorítmica (VWAP, TWAP) para minimizar slippage.
    Monitoreo 24/7 (el mercado FX no cierra).
    Cómo implementarlo: Plataformas como Interactive Brokers API, 
    Alpaca, o QuantConnect.

5. Conclusión Pedagógica
El Carry Trade es una de las estrategias más estudiadas en finanzas 
cuantitativas, pero también una de las más traicioneras para el 
inversor retail. Este capítulo demuestra que:

    La lógica económica es sólida (las divisas de alto rendimiento 
    tienden a apreciarse en períodos de calma).
    El riesgo de cola es real y devastador (2008, 2020).
    Un filtro de volatilidad mejora el perfil riesgo-retorno, pero 
    no elimina el problema.
    Una implementación profesional requiere infraestructura que excede 
    las capacidades retail gratuitas.

Veredicto: 🟡 Estrategia viable como satélite táctico (10-20% del 
patrimonio), pero NO como estrategia core. Requiere disciplina de hierro 
para cortar pérdidas cuando la volatilidad se dispara.
6. Descargo de Responsabilidad
[contenido actual + añadir:]
Esta implementación es una versión pedagógica simplificada. No incluye 
short selling real, datos de tipos dinámicos, ni gestión de margen 
profesional. Los resultados del backtest no son directamente replicables 
en un entorno real sin las adaptaciones descritas en la Sección 4.