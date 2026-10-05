# 📊 Estrategias No Convencionales de Inversión Cuantitativa

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![Jupyter Lab](https://img.shields.io/badge/Jupyter-Lab-orange.svg)
![License CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)
![Motor v1.0](https://img.shields.io/badge/Motor-v1.0-purple.svg)
![33 Estrategias](https://img.shields.io/badge/Estrategias-33-red.svg)

Laboratorio cuantitativo para el análisis, backtesting y comparación de **33 estrategias de inversión no convencionales**, desde arbitraje estadístico hasta machine learning, organizadas en 8 bloques temáticos progresivos.

---

## 📖 Descripción

**Estrategias No Convencionales** es un framework educativo y de investigación que implementa 33 estrategias de inversión avanzadas, organizadas en 8 bloques temáticos de complejidad creciente.

El proyecto está construido sobre un **Motor Modular Dinámico v1.0** reutilizable que garantiza consistencia, reproducibilidad y portabilidad entre entornos locales (Linux/Windows/Mac) y Google Colab.

###  Filosofía del proyecto

- **Honestidad intelectual:** Documentamos las limitaciones de cada estrategia antes que sus ventajas.
- **Reproducibilidad:** Todo el código es ejecutable con datos gratuitos de Yahoo Finance (cuando es posible).
- **Semáforo de viabilidad:** Cada estrategia indica claramente si es 🟢 totalmente backtesteable, 🟡 parcialmente backtesteable o 🔴 solo documentable.
- **No es asesoramiento financiero:** Este proyecto es educativo. Los resultados pasados no garantizan resultados futuros.

---

## ✨ Características Principales

- 🧠 **Motor Modular Dinámico v1.0:** Arquitectura desacoplada (`GestorProyecto`, `GestorDatos`, `MotorBacktestDinamico`, `CalculadorMetricas`, `GeneradorInformes`, `Gemelologo`, `StatArbEngine`).
- 📊 **33 estrategias implementadas:** Organizadas en 8 bloques temáticos progresivos.
- 🔄 **Rebalanceo configurable:** Diario, Semanal, Mensual, Trimestral o Anual.
- 💾 **Caché local de CSVs:** Descarga datos una vez, analiza muchas veces (ahorro de tiempo y límites de API).
- 📈 **Métricas profesionales:** CAGR, Sharpe, Sortino, Max Drawdown, VaR, Alpha, Beta, R², Tracking Error.
-  **Visualización automática:** Equity curves, mapas de drawdown, heatmaps de correlación, feature importance (ML).
- ⚙️ **Parámetros estandarizados:** Nomenclatura unificada (`FREQ_REBALANCEO`, `COSTE_TRANSACCION`) en todos los notebooks.
-  **Semáforo de viabilidad:** Indicador visual de qué estrategias son backtesteables con datos gratuitos.

---

## 📚 Estrategias Implementadas

### 🟢 Bloque I — Comportamiento y Psicología de Masas (Capítulos 1-4)
*Explotamos los sesgos cognitivos colectivos con reglas cuantitativas.*

| Cap | Estrategia | Filosofía | Semáforo |
|-----|-----------|-----------|----------|
| 1 | Arquitectura Común | Motor invisible reutilizable | 🟢 |
| 2 | Contrarian Investing | Comprar cuando nadie quiere | 🟢 |
| 3 | Momentum Crash | Apostar contra la euforia |  |
| 4 | Fear & Greed Index | Temporizador táctico de sentimiento |  |

### 🟢 Bloque II — Cuantitativas y Arbitraje Estadístico (Capítulos 5-7)
*Relaciones matemáticas entre activos para generar alpha puro.*

| Cap | Estrategia | Filosofía | Semáforo |
|-----|-----------|-----------|----------|
| 5 | Pairs Trading | La danza de los correlacionados | 🟢 |
| 6 | Statistical Arbitrage | ETFs vs. sus subyacentes | 🟡 |
| 7 | Algorithmic Trading con IA/ML | El límite del motor | 🟢 |

### 🟡 Bloque III — Estrategias Basadas en Eventos (Capítulos 8-10)
*Ineficiencias temporales por eventos corporativos.*

| Cap | Estrategia | Filosofía | Semáforo |
|-----|-----------|-----------|----------|
| 8 | Merger Arbitrage (Proxy) | Arbitraje de fusiones con ETFs | 🟡 |
| 9 | Earnings Surprise | Efecto post-anuncio | 🟡 |
| 10 | Insider Trading Legal | Siguiendo al Form 4 | 🟡 |

### 🟢 Bloque IV — Macro y Globales (Capítulos 11-13)
*De empresas a países: divisas, tipos, commodities.*

| Cap | Estrategia | Filosofía | Semáforo |
|-----|-----------|-----------|----------|
| 11 | Carry Trade | Cobrar el diferencial de tipos | 🟢 |
| 12 | Volatility Arbitrage | Vender el miedo caro | 🟡 |
| 13 | Global Macro | El estilo Soros |  |

### 🟡 Bloque V — Alternativas y Exóticas (Capítulos 14-16)
*Estrategias defensivas, temáticas o de provisión de liquidez.*

| Cap | Estrategia | Filosofía | Semáforo |
|-----|-----------|-----------|----------|
| 14 | Tail Risk Hedging | El seguro de Nassim Taleb | 🟡 |
| 15 | Liquidity Provision | Ser el mercado | 🟡 |
| 16 | Thematic Investing | Apostar a megatendencias | 🟢 |

### 🟡 Bloque VI — Nicho y Tácticas Específicas (Capítulos 17-20)
*Pequeños edges, tácticas fiscales, patrones estacionales.*

| Cap | Estrategia | Filosofía | Semáforo |
|-----|-----------|-----------|----------|
| 17 | Dividend Capture | Cobrar y salir | 🟡 |
| 18 | Short Selling con ETFs Inversos | Apostar a la caída |  |
| 19 | Tax-Loss Harvesting | La deducción silenciosa | 🟡 |
| 20 | Seasonal Strategies | El calendario como edge | 🟢 |

###  Bloque VII — Alto Riesgo (Solo para Expertos) (Capítulos 21-23)
*⚠️ Requieren conocimientos avanzados, capital elevado o infraestructura profesional.*

| Cap | Estrategia | Filosofía | Semáforo |
|-----|-----------|-----------|----------|
| 21 | Options Butterfly Spread | Apostar al rango | 🔴 |
| 22 | Credit Default Swaps | Asegurar deuda | 🟡 |
| 23 | Crypto Yield Farming | El nuevo carry trade | 🔴 |

###  Bloque VIII — Indicadores Técnicos No Convencionales (Capítulos 24-33)
*Capas de confirmación cuantitativa sobre las estrategias anteriores.*

| Cap | Estrategia | Filosofía | Semáforo |
|-----|-----------|-----------|----------|
| 24 | Fibonacci Moving Averages | La sucesión como soporte dinámico | 🟢 |
| 25 | Bollinger Bands Alternativas | Variantes aumentadas |  |
| 26 | Stochastic RSI | El oscilador del oscilador |  |
| 27 | Dynamic RSI | El oscilador adaptativo | 🟢 |
| 28 | Estocásticos Combinados | Panel de sobrecompra/sobreventa | 🟢 |
| 29 | Fractal Indicator de Williams | Soportes y resistencias dinámicos | 🟢 |
| 30 | Indicadores de Rango de Volatilidad | CHOP, Bollinger-Keltner squeeze | 🟢 |
| 31 | Contrarian Indicators Agregados | El miedo cuantificado | 🟢 |
| 32 | Moving Average Contrarian | El cruce inverso |  |
| 33 | Integración Maestra | Dashboard de indicadores | 🟢 |

---

## 🏗️ Arquitectura del Motor Modular Dinámico v1.0
