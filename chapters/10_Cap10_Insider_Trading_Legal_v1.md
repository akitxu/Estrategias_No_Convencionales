# Capítulo 10 — Insider Trading Legal: siguiendo al Form 4

> *"Los directivos venden por muchas razones, pero compran solo por una: creen que el precio va a subir."*  
> — Peter Lynch

El **Insider Trading Legal** se refiere a las operaciones de compra y venta de acciones que realizan los directivos, consejeros y empleados con conocimiento privilegiado de su propia empresa, pero que son **reportadas públicamente** a la SEC (Securities and Exchange Commission) mediante el formulario **Form 4**. Estas operaciones son completamente legales siempre que se declaren dentro de los 2 días hábiles siguientes.

En este capítulo, construiremos un sistema que detecta **compras netas significativas** (> $100k) por parte de ejecutivos C-level (CEO, CFO, COO) en mercado abierto, excluyendo las ventas programadas (Rule 10b5-1), y evaluaremos su capacidad para generar alpha en una ventana de 60 días.

**Semáforo de viabilidad:** 🔴 **No viable con datos retail gratuitos**. La lógica es sólida y ampliamente respaldada por la literatura académica, pero los datos gratuitos (como los de `yfinance`) son escasos o incompletos. En un entorno profesional, esta estrategia requiere un feed de datos directo de SEC EDGAR o OpenInsider. Este capítulo utiliza datos sintéticos como *fallback* pedagógico para demostrar la lógica del sistema.

---

## 1. Fundamentos Teóricos: ¿Por qué funciona?

1. **Asimetría informativa:** Los insiders conocen el estado real del negocio (nuevos contratos, márgenes, problemas de cadena de suministro) mucho antes de que se refleje en los informes trimestrales.

2. **Skin in the game:** Una compra abierta en el mercado secundario con dinero propio es la señal de confianza más fuerte que un directivo puede enviar.

3. **Sesgo de venta vs. compra:** Los ejecutivos venden por muchas razones (diversificación, impuestos, compra de una casa). Sin embargo, **solo compran por una razón**: esperan que el precio suba.

---

## 2. Evidencia Académica Clave

### Seyhun (1986) - "The Information Content of Aggregate Insider Trading"
- **Hallazgo:** Las compras agregadas de insiders predicen rentabilidades positivas del mercado a 3-6 meses.
- **Magnitud:** Carteras que compran siguiendo insider buying superan al mercado en 5-10% anual.
- **Limitación:** El efecto se ha debilitado desde los años 80 debido a la mayor regulación y cobertura mediática.

### Lakonishok y Lee (2001) - "Are Insider Trades Informative?"
- **Hallazgo:** Las compras de insiders son informativas, especialmente en small-caps y cuando son múltiples insiders de la misma empresa.
- **Magnitud:** Las acciones con compras de insiders superan a las que tienen ventas en 6-8% al año.
- **Condición:** El efecto es más fuerte cuando la compra representa > 1% del patrimonio del insider.

### Jeng, Metrick y Zeckhauser (2003) - "Estimating the Returns to Insider Trading"
- **Hallazgo:** Las compras de insiders generan alpha de 6-8% anual, pero las ventas NO generan alpha negativo significativo.
- **Interpretación:** Los insiders venden por razones de liquidez, pero compran solo por información.

---

## 3. Reglas Operativas de la Estrategia

1. **Universo:** Acciones de mediana y gran capitalización con liquidez suficiente.
2. **Señal de Entrada:** Compra neta en mercado abierto (Open Market Purchase) por parte de un C-level o Director, con un valor nominal > $100,000.
3. **Filtro de exclusión:** Ignorar ventas programadas bajo la regla 10b5-1 (ya que no reflejan una visión discrecional del mercado).
4. **Asignación de Pesos:** Máximo 8 posiciones simultáneas, con peso dinámico según el monto de la compra.
5. **Salida:** Mantenimiento de la posición durante 60 días o hasta un stop-loss del 8%.

---

## 4. Fuentes de Datos: Opciones y Limitaciones

### Opción 1: SEC EDGAR (Oficial, gratuito)
- **URL:** https://efts.sec.gov/LATEST/search-index
- **Ventajas:** Datos oficiales, completos, gratuitos.
- **Desventajas:** Requiere parsing de JSON/XML complejo, obtener CIK de cada empresa, puede tener retrasos de 1-2 días.
- **Implementación:** ~200 líneas de código para parsing completo.

### Opción 2: OpenInsider (Agregador, gratuito)
- **URL:** http://openinsider.com/
- **Ventajas:** Datos ya procesados, fáciles de scrapear.
- **Desventajas:** No oficial, puede caerse, scraping inestable, cobertura limitada.

### Opción 3: Wharton WRDS (Académico, pago)
- **URL:** https://wrds-www.wharton.upenn.edu/
- **Ventajas:** Base de datos `insider_transactions` completa y limpia.
- **Desventajas:** Requiere afiliación académica, coste ~$5k/año para instituciones.

### Opción 4: Refinitiv/Bloomberg (Profesional, pago)
- **Ventajas:** Datos en tiempo real, históricos completos, API robusta.
- **Desventajas:** Coste $20k+/año, solo para profesionales.

**Para este capítulo**, documentaremos el proceso de obtención de datos con SEC EDGAR, pero usaremos datos sintéticos para demostrar la lógica de la estrategia.

---

## 5. Limitaciones y Riesgos Específicos

1. **Calidad de los datos:** Las bases de datos gratuitas a menudo no distinguen bien entre una compra discrecional y una adquisición por ejercicio de opciones.

2. **Retraso en la publicación:** Aunque la SEC exige la notificación en 2 días, los datos pueden tardar más en estar disponibles en APIs gratuitas, generando *slippage*.

3. **Sesgo de supervivencia:** Al igual que en el Capítulo 9, analizamos empresas que existen hoy.

4. **Falsas señales:** No todas las compras de insiders son informativas. Algunas son parte de programas de compra automáticos (10b5-1 plans) que no reflejan visión actual del mercado.

---

## 6. Demostración de la Lógica (con Datos Sintéticos)

️ **ADVERTENCIA CRÍTICA:** Los datos utilizados en esta sección son **SINTÉTICOS**, generados aleatoriamente para demostrar la lógica de la estrategia. **No reflejan el comportamiento real de las compras de insiders** y **no pueden usarse para conclusiones sobre la eficacia de la estrategia**.

En un entorno profesional, se usarían datos reales de SEC EDGAR (con parsing correcto de CIK y XML) o bases de datos como OpenInsider, Wharton Research Data Services (WRDS), o Refinitiv.

### Código de demostración:
[Ver Bloque 6 del notebook]

---

## 7. Guía para Obtener Datos Reales

### Paso 1: Obtener CIK de cada empresa
```python
import requests
import json

# Descargar archivo de mapeo ticker -> CIK de SEC
url = "https://www.sec.gov/files/company_tickers.json"
headers = {'User-Agent': 'TuNombre tuemail@ejemplo.com'}
response = requests.get(url, headers=headers)
company_tickers = response.json()

# Ejemplo: Apple
cik = company_tickers['aapl']['cik_str']  # 320193
```

Paso 2: Consultar filings Form 4 por CIK
```
# API de SEC EDGAR para filings
url = f"https://data.sec.gov/submissions/CIK{cik:010d}.json"
response = requests.get(url, headers=headers)
filings = response.json()

# Filtrar solo Form 4
form4_filings = [f for f in filings['recent']['form'] if f == '4']
```
Paso 3: Parsear XML de cada filing
```
# Cada filing tiene un XML con las operaciones
# Requiere parsing con xml.etree.ElementTree
# Ver documentación: https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm
```
Alternativa más simple: Usar la librería sec-edgar-downloader:

bash```
pip install sec-edgar-downloader
```
python ```
from sec_edgar_downloader import Downloader
dl = Downloader("TuNombre", "tuemail@ejemplo.com")
dl.get("4", "AAPL", download_details=True)
```
8. Análisis de Viabilidad
Frecuencia esperada de señales

    S&P 500: ~500 empresas × 4 trimestres/año = ~2,000 earnings reports/año
    Insider buying significativo: ~10-20% de las empresas tienen compras > $100k por trimestre
    Señales esperadas: 200-400 eventos/año (5-10 por semana)

Costes de transacción estimados

    Comisión: 0.1% por operación (retail)
    Slippage: 0.05-0.10% (large-caps líquidas)
    Coste total: 0.15-0.20% por operación
    Impacto en CAGR: Con 200 operaciones/año, coste anual = 30-40% del patrimonio (si se renueva toda la cartera)

Universo viable

    Large-caps (S&P 500): Alta liquidez, datos fiables, pero efecto PEAD débil (mercado eficiente)
    Mid-caps (Russell 1000): Menor cobertura de analistas, efecto más fuerte, pero menor liquidez
    Small-caps (Russell 2000): Efecto más fuerte, pero problemas de liquidez y datos

Recomendación: Universo de S&P 500 + Russell 1000 (~1,500 empresas) para balance entre señal y liquidez.
9. Integración con Capítulo 9 (Estrategia Híbrida)
La combinación de Earnings Surprise (PEAD) + Insider Buying puede ser más robusta que cada señal sola:
Lógica de la estrategia híbrida:

    Señal 1: Earnings Surprise > 5% (Capítulo 9)
    Señal 2: Insider buying > $100k por C-level en los últimos 30 días (este capítulo)
    Entrada: Comprar solo si AMBAS señales están activas simultáneamente
    Peso: Distribución equitativa entre señales que cumplen ambos criterios

Ventajas esperadas:

    Mayor selectividad: Menos señales, pero de mayor calidad
    Confirmación cruzada: El insider buying valida que la sorpresa de beneficios es genuina
    Reducción de falsas señales: Filtra sorpresas de beneficios que no convencen a los insiders

Limitaciones:

    Frecuencia muy baja: Puede haber solo 20-50 señales/año (1 por semana)
    Datos complejos: Requiere integrar dos fuentes de datos diferentes
    Backtest difícil: Necesita datos históricos de ambas señales sincronizados

10. Conclusiones Pedagógicas
Lo que sabemos (evidencia académica):

    El insider buying es una señal válida: Múltiples estudios académicos (Seyhun 1986, Lakonishok & Lee 2001) demuestran que las compras de insiders predicen rentabilidades positivas.
    Magnitud: 5-10% de alpha anual en carteras que siguen insider buying.
    Condiciones óptimas: small-caps, múltiples insiders, >1% patrimonio.
    El efecto se ha debilitado desde los años 80 debido a mayor regulación y cobertura mediática.

Lo que no podemos validar (limitaciones retail):

    Datos históricos: Sin acceso a SEC EDGAR (parsing complejo) o bases de datos de pago (WRDS, Refinitiv), no podemos obtener datos fiables para backtestear.
    Resultados sintéticos: Los datos generados aleatoriamente no tienen validez estadística.
    Costes reales: No podemos estimar con precisión el slippage y el impacto de mercado sin datos de order book.

Recomendación práctica:

    No usar como estrategia standalone: El insider trading legal es una señal de confirmación, no una estrategia completa.
    Integrar con otras señales: Combinar con Earnings Surprise (Capítulo 9), momentum, o análisis fundamental.
    Usar como satélite táctico: Asignar 10-20% del patrimonio a esta señal, no el 100%.
    Invertir en datos: Si quieres implementar esta estrategia seriamente, necesitas datos profesionales (WRDS, Refinitiv) o implementar el parsing completo de SEC EDGAR.

Lección pedagógica clave:
En quant finance, los datos son el 80% del trabajo. Este capítulo demuestra que incluso con una señal teóricamente sólida (insider buying), la implementación práctica requiere infraestructura de datos que excede las capacidades retail gratuitas. Esta es una lección fundamental: sin datos de calidad, no hay estrategia.
11. Descargo de Responsabilidad
Este capítulo y el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa. Los datos de insider trading utilizados en la demostración son SINTÉTICOS y no reflejan la realidad del mercado. En un entorno real, se usarían datos de SEC EDGAR (con parsing correcto de CIK y XML) o bases de datos profesionales como OpenInsider, Wharton Research Data Services (WRDS) o Refinitiv. El backtest asume ejecución en T+2, ignorando el slippage real y los delays de publicación. El rendimiento pasado (incluso con datos reales) no garantiza resultados futuros. Operar basándose en insider trading conlleva riesgos específicos (liquidez, concentración, regulación). Realiza siempre tus propias pruebas (paper trading) y consulta con un asesor financiero independiente.



