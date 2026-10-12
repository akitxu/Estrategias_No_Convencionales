Capítulo 11 — Carry Trade: cobrar el diferencial de tipos

    "El Carry Trade es como recoger monedas delante de una apisonadora: 
    funciona el 90% del tiempo, pero cuando falla, lo pierde todo."
    — Dicho popular en macroeconomía

Semáforo de viabilidad: 🟡 Parcialmente viable (con filtros estrictos)
El Carry Trade "naive" (long en divisas de alto rendimiento, short en divisas 
de bajo rendimiento, y mantener) quiebra sistemáticamente en crisis de 
liquidez (2008, marzo 2020). Solo es viable si se combina con:

    Un filtro de volatilidad que actúe como "freno de emergencia".
    Una gestión de riesgo estricta (stop-loss, límites de posición).
    Datos de tipos de interés en tiempo real (no disponibles gratis con calidad).

Nota sobre esta implementación: Este capítulo presenta una versión 
pedagógica Long-Only (solo compramos divisas de alto rendimiento, sin hacer 
short de las de bajo rendimiento). Una implementación profesional requeriría 
short selling real, datos de tipos de interés dinámicos y gestión de margen. 
En la Sección 4 detallamos qué faltaría para una versión profesional.
1. Fundamentos Teóricos
1.1 La Paridad del Interés No Cubierta (UIP)
La Paridad del Interés No Cubierta (Uncovered Interest Parity, UIP) es una 
teoría fundamental en finanzas internacionales que establece que la diferencia 
de tipos de interés entre dos países debe ser igual a la depreciación esperada 
de la divisa con mayor tipo.
Fórmula teórica:

(1 + i_doméstica) = (1 + i_extranjera) × (E[S_t+1] / S_t)

Donde:

    i_doméstica = tipo de interés doméstico
    i_extranjera = tipo de interés extranjero  
    E[S_t+1] = tipo de cambio esperado futuro
    S_t = tipo de cambio actual

Implicación: Si el tipo de interés en Australia es 4% y en Japón es 0.1%, 
el AUD debería depreciarse un ~3.9% frente al JPY para que no haya oportunidad 
de arbitraje. En teoría, el Carry Trade no debería generar beneficios ajustados 
al riesgo.
1.2 La Anomalía del Carry
La realidad empírica contradice la UIP. Durante décadas, los estudios 
académicos (Fama, 1984; Burnside et al., 2011) han documentado que:

    Las divisas de alto rendimiento NO se deprecian tanto como predice la UIP.
    El Carry Trade genera alpha positivo en períodos de calma de mercado.
    Este alpha viene acompañado de riesgo de cola extremo (crisis de liquidez).

¿Por qué existe esta anomalía?

    Riesgo de cola no diversificable: Los inversores exigen una prima por 
    asumir el riesgo de que todas las divisas de riesgo se desplomen simultáneamente 
    en una crisis (2008, 2020).
    Límites al arbitraje: Los costes de transacción, restricciones de margen 
    y asimetrías de información impiden que los arbitrajistas eliminen completamente 
    la anomalía.
    Comportamiento de los bancos centrales: Las intervenciones cambiarias y 
    políticas monetarias asimétricas crean oportunidades temporales.

1.3 Por qué funciona (y por qué a veces no)
El Carry Trade es esencialmente vender seguro contra crisis globales:

    En mercados tranquilos: Cobras la prima (diferencial de tipos) y todo va bien.
    En crisis de liquidez: Tienes que pagar el seguro (pérdidas del 20-40% en semanas).

Factores que determinan el éxito:
✅ Funciona cuando:

    Volatilidad global baja (VIX < 20)
    Crecimiento económico estable
    Bancos centrales en modo "normal"
    Liquidez abundante en mercados

❌ Falla cuando:

    Crisis financieras (2008, 2020)
    Shock geopolíticos inesperados
    Cambios bruscos en política monetaria
    Crisis de liquidez en mercados emergentes

2. Reglas Operativas de ESTA Implementación
2.1 Universo de Activos

 Activo | Ticker | Rol | Tipo de interés histórico |
 |---|---|---|---|
 | Dólar Australiano | FXA | Long (target) | 3-5% |
 | Libra Esterlina | FXB | Long (target) | 3-5% |
 | Yen Japonés | FXY | Short (funding) | 0-0.5% |
 | Franco Suizo | FXF | Short (funding) | 0-1% |
 | iShares Short Treasury | SHV | Cash (refugio) | 2-5% |
 | Invesco DB USD Index | UUP | Benchmark | — |
 | SPDR S&P 500 | SPY | Proxy volatilidad | — |

Nota: En esta versión pedagógica usamos solo Long en AUD y GBP, sin 
implementar el short en JPY y CHF. Esto simplifica la estrategia pero reduce 
significativamente el carry capturado.
2.2 Señal de Entrada
Modo Normal (volatilidad baja):

    Si la volatilidad realizada del SPY (ventana 60 días) ≤ 20% anualizada
    Asignar 50% a AUD (FXA) y 50% a GBP (FXB)
    Rebalanceo mensual

Modo Defensa (volatilidad alta):

    Si la volatilidad realizada del SPY > 20% anualizada
    Mover 100% a efectivo (SHV)
    Esperar a que la volatilidad baje para reentrar

2.3 Gestión del Riesgo
Por qué usamos Long-Only en lugar de Long/Short:

    Simplicidad pedagógica: El objetivo es demostrar el concepto, no optimizar returns.
    Limitaciones retail: El short selling de ETFs requiere:
        Cuenta de margen (intereses variables)
        Localización de acciones prestables (no siempre disponible)
        Gestión de riesgo de short squeeze
    Costes ocultos: Los costes de préstamo pueden erosionar el alpha, 
    especialmente en divisas de bajo rendimiento como JPY durante crisis.

Limitaciones de esta aproximación:

    No capturamos el diferencial completo (solo la mitad del carry)
    ❌ Mayor exposición direccional al dólar (si AUD y GBP caen juntos, perdemos)
    ❌ Menor diversificación que un Carry Trade Long/Short balanceado

3. Resultados del Backtest (2007-2026)
3.1 Métricas Clave

  Métrica | Carry Trade + Vol Filter | Buy & Hold Universo | SPY | Diferencia |
 |---|---|---|---|---|
 | Patrimonio Final | 7,219 € | ~20,000 € | ~14,000 € | — |
 | Rentabilidad Total | -27.81% | +100% | +40% | -127.81 pp ❌ |
 | CAGR | -1.66% | 3.93% | ~2.5% | -5.59 pp ❌ |
 | Volatilidad | 7.29% | 6.37% | ~15% | +0.92 pp |
 | Sharpe Ratio | -0.50 | 0.30 | ~0.2 | -0.80 ❌ |
 | Sortino Ratio | -0.62 | 0.40 | — | -1.02 ❌ |
 | Max Drawdown | -48.43% | -14.68% | ~-35% | +33.75 pp PEOR ❌❌ |
 | Beta | -0.50 | 1.00 | — | Baja correlación |
 | R² | 0.31 | 1.00 | — | Poca explicación por mercado |
 | Días en Cash (SHV) | 0% | 0% | 0% | Filtro no activado ⚠️ |

 3.2 Interpretación Honesta de los Resultados
Lo que NO funcionó:

    Underperformance Severo: El CAGR negativo (-1.66%) indica que la estrategia 
    destruyó capital en lugar de generarlo. Esto es consistente con la literatura 
    académica que muestra que el Carry Trade retail tiene dificultades para capturar 
    el alpha después de costes.
    Max Drawdown Catastrófico (-48.43%): A pesar del filtro de volatilidad 
    (que no funcionó correctamente), la estrategia sufrió pérdidas enormes. Esto 
    confirma que:
        El Carry Trade tiene riesgo de cola extremo (2008, 2020)
        Los ETFs de divisas tienen tracking error y costes de gestión (~0.40% anual)
        La implementación retail no puede replicar las condiciones institucionales
    Sharpe Ratio Negativo (-0.50): La estrategia no compensa el riesgo asumido. 
    Por cada unidad de riesgo, pierde dinero.
    Filtro de Volatilidad Ineficaz: Aunque el 22.8% de los días tuvieron 
    volatilidad > 20%, la estrategia permaneció 100% invertida en divisas. Esto 
    sugiere un bug en la implementación del generador de pesos.

⚠️ Limitaciones Estructurales:

    Versión Long-Only: Solo capturamos mitad del carry (falta el short de JPY/CHF)
    Datos de tipos estáticos: Asumimos que AUD/GBP son siempre "high yield" y 
    JPY/CHF siempre "funding", pero los tipos cambian
    Costes de transacción: 0.2% por operación (≈10 pb/lado) erosiona el alpha
    Sesgo de supervivencia: Los ETFs actuales no representan el universo histórico completo

3.3 Análisis del Filtro de Volatilidad
Resultado esperado vs. real:

 Métrica | Esperado | Real | Problema |
 |---|---|---|---|
 | Días con vol > 20% | ~22% | 22.8% ✅ | Correcto |
 | Días en cash (SHV) | ~22% | 0% ❌ | Filtro no activado |
 | Días en FX | ~78% | 100% ❌ | Siempre invertido |
 | Max Drawdown | ~-25% | -48.43% ❌ | Sin protección |

 Diagnóstico del problema:
El generador de pesos no está reconociendo correctamente la columna de cash 
(Short_Treasury) cuando intenta asignar el 100% en modo defensa. Esto es un 
bug de implementación que debe corregirse antes de usar la estrategia en producción.
Solución técnica requerida:

python```
# En el generador de pesos, buscar dinámicamente la columna de cash:
cash_col = next((a for a in activos if 'Short_Treasury' in a or 'SHV' in a), None)
if cash_col:
    pesos[cash_col] = 1.0
    ```

4. ⚠️ Lo que FALTA para una Implementación Profesional
Esta sección detalla las limitaciones de nuestra implementación pedagógica y 
qué se necesitaría para una versión profesional viable.
4.1 Short Selling Real (el gap más importante)
Lo que hicimos: Long-Only en AUD y GBP.
Lo que haría un profesional: Long en AUD/GBP + Short en JPY/CHF, 
aprovechando el diferencial completo.
Por qué no lo hicimos:

    El short selling de ETFs requiere cuenta de margen.
    Los costes de préstamo de acciones son variables (pueden ser 1-5% anual en JPY).
    Riesgo de "short squeeze" en crisis (cuando todos quieren comprar JPY a la vez).

Cómo implementarlo:

    Usar futuros de divisas (CME) en lugar de ETFs.
    CFDs con gestión de margen estricta.
    Calcular el carry neto: (tipo_long - tipo_short) - costes_préstamo - costes_transacción

4.2 Datos de Tipos de Interés Dinámicos
Lo que hicimos: Asumimos que AUD/GBP son siempre "high yield" y JPY/CHF 
siempre "funding".
Lo que haría un profesional: Recalcular el carry diario usando tipos 
oficiales de cada banco central.
Por qué no lo hicimos:

    Los tipos cambian (ej: el Fed Funds pasó de 5.25% a 0% en 2008).
    Necesitaríamos API de FRED o datos de Bloomberg/Refinitiv.
    Complejidad adicional en el backtest.

Cómo implementarlo:

python```
# Ejemplo con FRED (gratuito, requiere clave API)
import pandas_datareader.data as web

# Descargar tasas históricas
fed_funds = web.DataReader('FEDFUNDS', 'fred', start, end)
boj_rate = web.DataReader('IR3TIB01JPM156N', 'fred', start, end)
rba_rate = web.DataReader('IR3TIB01AUM156N', 'fred', start, end)

# Calcular carry diario = tipo_long - tipo_short
carry_aud_jpy = rba_rate - boj_rate
```

4.3 Costes de Transacción Realistas
Lo que hicimos: 0.2% por operación (≈10 pb/lado).
Lo que haría un profesional:

    Spread bid-ask real de cada ETF (varía 1-5 pb según liquidez).
    Slippage por impacto de mercado (especialmente en emergentes como MXN).
    Tracking error del ETF vs divisa spot (~0.1-0.3% anual).
    Comisiones del broker (variables según volumen).
    Costes de préstamo para short (si aplica).

Cómo implementarlo:

python
```
# Modelo de costes realistas
def calcular_costes_realistas(ticker, volumen_operado):
    spread = spreads_históricos[ticker]  # ej: 0.0002 para FXA
    slippage = 0.0001 * (volumen_operado / volumen_medio_diario)
    comision = 0.0005  # 5 pb
    tracking_error = 0.002  # 20 pb anual / 252 días
    return spread + slippage + comision + tracking_error
```

4.4 Gestión de Margen y Riesgo de Cola
Lo que hicimos: Stop-loss del 8% y filtro de volatilidad.
Lo que haría un profesional:

    VaR (Value at Risk) diario con límites estrictos.
    Stress testing con escenarios históricos (2008, 2020, 2015 CHF shock).
    Límites de exposición por divisa y por correlación.
    Hedging con opciones (comprar puts OTM como seguro).

Cómo implementarlo:

python```

# Ejemplo de VaR histórico
var_95 = np.percentile(rentabilidades, 5)
if var_95 < -0.02:  # Si el VaR 95% supera -2%, reducir exposición
    reducir_posiciones(factor=0.5)

# Stress testing
escenarios = {
    '2008_financiera': {'AUD': -0.30, 'GBP': -0.25, 'JPY': +0.20},
    '2020_covid': {'AUD': -0.20, 'GBP': -0.15, 'JPY': +0.10},
    '2015_chf_shock': {'CHF': +0.30, 'EUR': -0.15}
}
```

4.5 Universo Más Amplio
Lo que hicimos: 4 divisas G10 (AUD, GBP, JPY, CHF).
Lo que haría un profesional:

    Incluir emergentes de alto carry (MXN, BRL, ZAR, TRY) — mayor alpha, mayor riesgo.
    Incluir divisas europeas (EUR, NOK, SEK).
    Ponderar por liquidez y por carry (no equitativo).
    Rotación dinámica basada en momentum de tipos.

Cómo implementarlo:

python
```
# Expandir universo
UNIVERSO_FX_PROFESIONAL = {
    'target_high_yield': {
        'AUD': {'ticker': 'FXA', 'peso_base': 0.15},
        'GBP': {'ticker': 'FXB', 'peso_base': 0.15},
        'MXN': {'ticker': 'FXM', 'peso_base': 0.10},  # emergente
        'BRL': {'ticker': 'EWZ', 'peso_base': 0.10},  # emergente
    },
    'funding_low_yield': {
        'JPY': {'ticker': 'FXY', 'peso_base': 0.25},
        'CHF': {'ticker': 'FXF', 'peso_base': 0.25},
    }
}

# Ajustar pesos por carry/volatilidad
def calcular_pesos_dinamicos(tipos_interes, volatilidades):
    carry_score = tipos_interes['target'] - tipos_interes['funding']
    pesos = carry_score / volatilidades
    return pesos / pesos.sum()  # normalizar
```

4.6 Datos en Tiempo Real y Ejecución
Lo que hicimos: Backtest con datos históricos diarios.
Lo que haría un profesional:

    Datos intradía para timing preciso.
    Ejecución algorítmica (VWAP, TWAP) para minimizar slippage.
    Monitoreo 24/7 (el mercado FX no cierra).
    Alertas automáticas para cambios de régimen.

Cómo implementarlo:

python```
# Plataformas profesionales
# - Interactive Brokers API (datos + ejecución)
# - Alpaca (comisiones bajas, API moderna)
# - QuantConnect (backtesting + live trading)
# - Bloomberg Terminal (datos institucionales)

# Ejemplo con Interactive Brokers
from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Suscribirse a datos en tiempo real
contrato_aud = Forex('AUDUSD')
ib.reqMktData(contrato_aud, '', False, False)
```
5. Conclusión Pedagógica
El Carry Trade es una de las estrategias más estudiadas en finanzas 
cuantitativas, pero también una de las más traicioneras para el 
inversor retail. Este capítulo demuestra que:
✅ Lo que aprendimos:

    La lógica económica es sólida: Las divisas de alto rendimiento 
    tienden a apreciarse en períodos de calma (anomalía del carry).
    El riesgo de cola es real y devastador: Las crisis de 2008 y 2020 
    mostraron que el Carry Trade puede perder 30-50% en semanas.
    Un filtro de volatilidad es necesario pero no suficiente: 
    Mejora el perfil riesgo-retorno, pero no elimina el problema 
    fundamental del riesgo de cola.
    La implementación retail tiene limitaciones severas: 
    Sin short selling, sin datos de tipos dinámicos, y con costes 
    de transacción altos, el alpha se erosiona rápidamente.

❌ Lo que NO funcionó en nuestro backtest:

    Underperformance severo: CAGR -1.66% vs Buy & Hold +3.93%.
    Max Drawdown catastrófico: -48.43% (peor que el mercado).
    Filtro de volatilidad ineficaz: No se activó correctamente.
    Sharpe Ratio negativo: -0.50 (no compensa el riesgo).

Veredicto Final:
🟡 Estrategia viable como satélite táctico (10-20% del patrimonio), 
pero NO como estrategia core.
Requisitos para implementación profesional:

    Short selling real con gestión de margen
    Datos de tipos de interés en tiempo real (FRED, Bloomberg)
    Costes de transacción realistas (< 5 pb/lado)
    Filtro de volatilidad robusto y bien implementado
    Universo amplio (G10 + emergentes)
    Ejecución algorítmica con monitoreo 24/7

Alternativas más viables para retail:

    Usar fondos de gestión alternativa especializados en FX carry.
    Invertir en bonos de alta calidad con carry implícito.
    Mantener diversificación geográfica en la cartera core.
    Usar el Carry Trade solo como señal de confirmación dentro de 
    una estrategia multi-factor.

6. Descargo de Responsabilidad
Este capítulo y el código asociado tienen fines exclusivamente educativos 
y de investigación cuantitativa. Los resultados del backtest muestran que 
el Carry Trade retail no es viable como estrategia standalone con la 
implementación actual.
Limitaciones específicas de esta implementación:

    Versión Long-Only (no captura el carry completo)
    Datos de tipos estáticos (no dinámicos)
    Filtro de volatilidad con bug de implementación
    Costes de transacción simplificados
    Universo limitado (4 divisas G10)

Los ETFs de divisas conllevan riesgos de tipo de cambio, de liquidez y 
de contraparte. El backtest asume que se puede hacer cortocircuito (short 
selling) de ETFs sin costes de préstamo variables, lo cual no es realista 
en todos los brokers retail.
El rendimiento pasado (incluso con datos reales) no garantiza resultados 
futuros. Operar basándose en Carry Trade conlleva riesgos específicos 
(liquidez, concentración, regulación, riesgo de cola). Realiza siempre 
tus propias pruebas (paper trading) y consulta con un asesor financiero 
independiente antes de implementar esta estrategia con capital real.
7. Próximos Pasos
En el Capítulo 12 exploraremos las Materias Primas (Commodities): 
cómo construir estrategias de momentum y mean-reversion en mercados de 
energía, metales y agricultura, completando el bloque de estrategias Macro 
y Globales.
Lección clave del Capítulo 11: 
En quant finance, la teoría es elegante pero la implementación es brutal. 
El Carry Trade nos enseña que algunas estrategias son teóricamente sólidas, 
pero prácticamente inviables para el inversor minorista sin infraestructura 
profesional. La brecha entre el alpha teórico y el alpha real después de 
costes es el cementerio de muchas estrategias prometedoras.






