# ⚠️ Advertencia Legal y de Uso

## Opciones para Obtener Datos Históricos de Precios

Para trabajar con datos históricos de fondos o activos, tienes dos opciones principales:

### 🔹 Opción A: Descargar datos desde las gestoras oficiales

Descarga los datos directamente desde las páginas web de las gestoras (ej: Renta 4, Vanguard, iShares, Amundi, etc.). Son datos oficiales y precisos, sin diferencias respecto a la fuente, y su uso no conlleva riesgos legales. Guárdalos en una carpeta específica (ej: `Datos_fondos_csv/`) para mantener el proyecto organizado.

###  Opción B: Uso de plataformas públicas (Yahoo Finance + yfinance)

Este proyecto utiliza la librería `yfinance` (licencia Apache 2.0) para automatizar la descarga de datos financieros desde Yahoo Finance.

**⚠️ Precauciones y limitaciones de yfinance:**

- **No oficial:** `yfinance` es una herramienta no oficial y no está afiliada, avalada ni respaldada por Yahoo Inc.
- **Términos de Servicio:** El uso de `yfinance` puede violar los Términos de Servicio de Yahoo. El usuario es el único responsable de cumplirlos.
- **Uso permitido:** Los datos descargados a través de este código son exclusivamente para uso educativo o personal. No está permitido redistribuirlos, venderlos o usarlos con fines comerciales.
- **Precisión:** Estos datos pueden presentar pequeñas diferencias con respecto a las fuentes oficiales. Para decisiones críticas de inversión, se recomienda contrastar la información con la documentación oficial de la gestora.
- **Limitaciones del proyecto:** Algunas estrategias de este libro requieren datos que Yahoo Finance no proporciona (datos de opciones, Form 4 de SEC EDGAR, datos on-chain de criptomonedas, etc.). En esos casos, el código utiliza PROXYS SIMPLIFICADOS que no replican fielmente las estrategias profesionales reales.

---

## 🚫 Exención de Responsabilidad

El código, la documentación y los resultados generados en este proyecto se proporcionan exclusivamente con fines **educativos y de investigación cuantitativa** (incluyendo, a modo de ejemplo, proyectos académicos como un Trabajo Fin de Máster - TFM). Bajo ninguna circunstancia constituyen asesoramiento financiero, de inversión, fiscal ni de ningún otro tipo.

Tenga en cuenta las siguientes consideraciones antes de utilizar esta herramienta:

### Uso del Código
El software proporcionado se entrega **"TAL CUAL" (AS IS)**, sin garantía de ningún tipo. El autor no se hace responsable de errores en el código, en los datos descargados de Yahoo Finance, ni de pérdidas económicas derivadas del uso de estas herramientas.

### Riesgo de capital
Operar en mercados financieros conlleva inherentemente riesgo de pérdida de capital. Algunas estrategias de este proyecto (Bloque VII: Alto Riesgo) requieren conocimientos avanzados, capital elevado o infraestructura profesional.

### Rentabilidad pasada
La rentabilidad histórica de las estrategias analizadas **no garantiza ni predice la rentabilidad futura**. Los mercados financieros son dinámicos y los patrones del pasado pueden no repetirse.

### Pruebas previas
Recomendamos encarecidamente realizar siempre tus propias pruebas en entornos simulados (paper trading) durante al menos 6-12 meses antes de implementar ninguna estrategia con capital real.

### Responsabilidad
Cualquier decisión de inversión tomada a partir de la lectura o ejecución de este proyecto debe ser bajo la **exclusiva responsabilidad del inversor**.

### Limitaciones específicas del ML
Las estrategias de Machine Learning (Capítulo 7) son particularmente susceptibles a:
- **Overfitting:** El modelo puede memorizar el pasado sin aprender patrones generalizables.
- **Concept Drift:** Los patrones de mercado cambian con el tiempo.
- **Ratio señal/ruido baja:** Los mercados financieros tienen una ratio señal/ruido muy baja (~0.05).

### Limitaciones de los proxies
Algunas estrategias de este proyecto son PROXYS SIMPLIFICADOS:
- **Merger Arbitrage (Cap. 8):** No utiliza datos reales de OPAs, sino un proxy basado en caídas sectoriales.
- **Statistical Arbitrage (Cap. 6):** Utiliza pesos igualitarios en lugar de pesos por capitalización real.
- **Crypto Yield Farming (Cap. 23):** No simula yield farming real (requiere datos on-chain).

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **Creative Commons Atribución – No Comercial – Compartir Igual 4.0 Internacional (CC BY‑NC‑SA 4.0)**.

Copyright © 2026 Enrique Fueyo Vega

**Permisos:**
- ✅ Puedes usar el contenido con fines personales, educativos o de investigación.
- ✅ Puedes compartirlo en cualquier medio o formato.
- ✅ Puedes adaptarlo o modificarlo, siempre que mantengas la misma licencia.

**Condiciones:**
- **Atribución (BY):** Debes citar al autor original, incluir un enlace a esta licencia e indicar si realizaste cambios.
- **No Comercial (NC):** No puedes usar este proyecto, su código o sus datos con fines comerciales.
- **Compartir Igual (SA):** Si adaptas o modificas el proyecto, debes distribuir tu versión bajo la misma licencia CC BY‑NC‑SA 4.0.

---

**Última actualización:** Octubre 2026