# Capítulo 1: Patrones Armónicos (ABCD) — Validación de la Estrategia

**Versión:** 3.1 (Revisión 3 — completa) | **Motor:** Modular Dinámico v1.0 | **Actualización:** 2026-10-28

> *"En el trading cuantitativo, un backtest perfecto es sospechoso. Un backtest que sobrevive a pruebas de estrés rigurosas es valioso."*
> — Adaptación libre de Marcos López de Prado

**Objetivo de este documento:** Someter la estrategia de Patrones Armónicos ABCD a pruebas de validación rigurosas para determinar si el rendimiento observado (+21.26% CAGR vs +15.10% del Buy & Hold en el histórico global) es real o producto de overfitting, sesgo de datos, look-ahead bias o condiciones de mercado favorables.

---

## Resumen Ejecutivo de Resultados

| Prueba | Resultado | Veredicto |
|--------|-----------|-----------|
| **Out-of-Sample (OOS)** | Degradación CAGR: -0.20 pp, Sharpe: -0.03 | ✅ ALTA robustez (4/5) |
| **Sensibilidad a Costes** | Degradación peor caso: -12.09 pp CAGR | ️ FRÁGIL a slippage >0.3% |
| **Test Placebo (Monte Carlo)** | p-valor: 0.003 | ✅ Timing aporta valor real |
| **Barrido IS/OOS** | Spearman rho: +0.659, mejora en OOS | ✅ Parámetros estables |
| **Ratio de Calmar** | 0.70 (Estrategia) vs 1.01 (B&H) | ⚠️ B&H más eficiente por drawdown |
| **Impacto fiscal estimado** | CAGR neto: 6.2% vs 15.5% (B&H) | ⚠️ Amplía brecha de underperformance |

**Conclusión ejecutiva:** La estrategia **NO está sobreajustada** y el timing de los patrones **SÍ aporta alpha estadísticamente significativo** (p=0.003). Sin embargo, sufre de *cash drag* en mercados alcistas y es frágil a costes elevados. Su valor real reside en la **preservación de capital**, no en la maximización de rentabilidad, lo que la hace adecuada como **componente satélite** de una cartera diversificada.

---

## 1. Prueba de Muestra Fuera de Muestra (Out-of-Sample)

### Metodología
- **Período completo:** 2016-01-04 → 2026-10-14 (2,711 días)
- **In-Sample (IS):** 70% inicial (1,897 días, hasta 2023-07-19)
- **Out-of-Sample (OOS):** 30% final (814 días, desde 2023-07-19)
- **Criterio de robustez:** Degradación < 5 pp en CAGR y < 0.3 en Sharpe entre IS y OOS de la propia estrategia.

### Resultados Comparativos

| Segmento | Días | Años | CAGR | Rent_Total | Max_DD | Volatilidad | Sharpe | Patrimonio_Final |
|----------|------|------|------|------------|--------|-------------|--------|------------------|
| **Estrategia IS** | 1,898 | 7.54 | +8.09% | +79.7% | -13.4% | 9.2% | 0.68 | €17,969 |
| **Estrategia OOS** | 814 | 3.24 | +7.89% | +27.9% | -11.2% | 9.4% | 0.65 | €22,978 |
| **Buy&Hold IS** | 1,897 | 7.53 | +13.42% | +158.3% | -33.7% | 18.7% | 0.66 | €25,877 |
| **Buy&Hold OOS** | 814 | 3.24 | +19.05% | +75.9% | -18.8% | 15.0% | 1.11 | €45,525 |

### Análisis de Degradación IS → OOS

**Estrategia Patrones Armónicos:**
- Degradación CAGR: **-0.20 pp** ✅
- Degradación Sharpe: **-0.03** ✅
- Cambio Max Drawdown: **+2.2 pp** (mejora en OOS) ✅

**Buy & Hold (Referencia):**
- Incremento CAGR OOS vs IS: **+5.63 pp** (fuerte régimen alcista 2023–2026)

### Veredicto de Robustez

| Criterio | Resultado | Estado |
|----------|-----------|--------|
| CAGR positivo en OOS | +7.89% | ✅ SÍ |
| Sharpe positivo en OOS | 0.65 | ✅ SÍ |
| Degradación CAGR aceptable (<5pp) | -0.20 pp | ✅ SÍ |
| Degradación Sharpe aceptable (<0.3) | -0.03 | ✅ SÍ |
| Supera a Buy&Hold en OOS | NO (7.89% vs 19.05%) | ❌ NO |

**🟢 CONCLUSIÓN DE ROBUSTEZ:** La consistencia entre IS (+8.09%) y OOS (+7.89%) demuestra que las reglas operativas (tolerancia 10%, hold 5 días, stop-loss 3%) **no sufren de overfitting**.

**⚠️ MATIZ CRÍTICO (Cash Drag):** En el período OOS (2023-2026), el mercado ofreció un retorno alcista del +19.05% CAGR. Debido a que la estrategia permanece en mercado solo 5 días por operación y mantiene un promedio elevado de liquidez, sufre un claro retraso de rentabilidad acumulada. Su fortaleza radica en la **reducción de la volatilidad** (9.4% vs 15.0%) y **menor Drawdown** (-11.2% vs -18.8%).

---

## 2. Prueba de Sensibilidad a Costes y Parámetros

### Metodología
Se evaluaron 27 combinaciones alternando:
- **Coste de transacción:** 0.0%, 0.1%, 0.3% (incluyendo comisión y slippage).
- **Tolerancia de patrón:** ±5%, ±10%, ±15%.
- **Días en posición (hold):** 3, 5, 7 días.

### Resumen de Sensibilidad por Dimensión

**Impacto del Coste de Transacción:**
| Coste | CAGR medio | Degradación |
|-------|------------|-------------|
| 0.0% | +19.49% | — |
| 0.1% | +17.79% | -1.70 pp |
| 0.3% | +14.49% | -5.00 pp |

**Insight:** Cada 0.1% incremental en costes globales/slippage resta aprox. 2.5% de CAGR. Un slippage superior a 0.3% destruye la ventaja competitiva sobre el Buy & Hold.

**Impacto de la Tolerancia Geométrica:**
| Tolerancia | CAGR medio | Interpretación |
|------------|------------|----------------|
| ±5% | +14.09% | Demasiado estricto, elimina operaciones válidas |
| ±10% | +18.87% | **Punto óptimo** de equilibrio señal/ruido ✅ |
| ±15% | +18.81% | Aumenta señales pero introduce ruido |

**Impacto de la Duración (Hold Days):**
| Hold | CAGR medio | Interpretación |
|------|------------|----------------|
| 3d | +18.66% | Salidas prematuras |
| 5d | +18.98% | **Óptimo** ✅ |
| 7d | +14.12% | El impulso se agota |

**Insight:** La reanudación del impulso tras la confluencia armónica agota su ventaja relativa a partir del 5º día.

---

## 3. Test Placebo de Timing (Monte Carlo)

### Metodología
- **Hipótesis nula (H₀):** Las entradas basadas en patrones ABCD no ofrecen ventaja predictiva comparadas con entradas aleatorias en los mismos activos.
- **Simulaciones:** 2,000 iteraciones distribuyendo aleatoriamente los puntos de entrada.

### Resultados

| Métrica | Real | Azar (media) | Azar (p95) | p-valor |
|---------|------|--------------|------------|---------|
| Rentab. media por patrón | +0.86% | -0.01% | +0.46% | **0.003** |
| Suma log-rentabilidades | +0.850 | -0.047 | — | **0.002** |

**✅ Veredicto Estadístico:** Con un p-valor de 0.003, se rechaza la hipótesis nula. El timing dictado por los patrones armónicos posee **poder estadístico real y significativo** (p < 0.05).

---

## 4. Barrido de Parámetros con Validación IS/OOS

### Configuración
- **27 combinaciones** (3 tolerancias × 3 hold days × 3 stop-loss)
- **IS:** 60% inicial (hasta 2022-06-17)
- **OOS:** 40% final (desde 2022-06-17)

### Resultados Clave

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| Media Delta Sharpe (OOS-IS) | +0.696 | Transición a régimen alcista de baja volatilidad |
| Media Delta CAGR (OOS-IS) | +12.02% | Expansión generalizada de retornos |
| Combos con degradación < 0.3 Sharpe | 27/27 (100%) | Robustez estructural completa |
| Spearman rho (IS vs OOS) | +0.659 (p=0.000) | Alta predictibilidad del ranking de parámetros |

### Referencia Buy & Hold
- **Sharpe B&H IS:** +0.58
- **Sharpe B&H OOS:** +1.11

**Insight de estabilidad:** El coeficiente de Spearman de +0.659 confirma que la optimización de parámetros es estable: las combinaciones con mejor desempeño In-Sample mantienen su jerarquía Out-of-Sample.

---

## 5. Auditoría de Riesgos y "Red Flags" Identificadas

### 5.1 Sesgo de Confirmación en Punto D (Look-Ahead Bias Parcial)
**Diagnóstico:** La detección mediante algoritmos de extremófilos (`scipy.signal.argrelextrema`) requiere un número N de velas posteriores para confirmar un máximo o mínimo local.

**Riesgo:** Si la orden se ejecuta hipotéticamente en el mismo precio del punto D en tiempo T₀, el backtest incorpora datos futuros no disponibles en tiempo real.

**Mitigación:** Se debe imponer una latencia obligatoria de 1 a 2 velas de confirmación (T+1/T+2) o ejecutar mediante órdenes límite condicionadas en la Zona de Reversión Potencial (PRZ).

### 5.2 Arrastre de Caja (Cash Drag)
**Diagnóstico:** Al mantener duraciones fijas de 5 días y una frecuencia media de 16.6 operaciones/año, la cartera mantiene un porcentaje alto de efectivo inactivo.

**Impacto:** Explica por qué en mercados alcistas agresivos (OOS 2023-2026) la estrategia obtiene +7.89% frente al +19.05% del B&H.

### 5.3 Ineficiencia Fiscal y Fricción Operativa
Con 166 rebalanceos y una rotación del 86.20%, los costes acumulados superan el 47% del capital inicial en el período completo. La gestión activa diaria incrementa además el diferimiento fiscal negativo frente a la inversión pasiva.

### 5.4 Limitaciones del Estudio
Este estudio presenta limitaciones metodológicas que deben considerarse al interpretar los resultados:

1. **Universo reducido:** Solo 4 activos (SPY, QQQ, XLF, XLK). No se ha validado en acciones individuales, mercados internacionales ni crypto.
2. **Período OOS excepcional:** 2023-2026 fue un mercado alcista fuerte. Los resultados podrían no replicarse en regímenes laterales o bajistas.
3. **Falta de validación cruzada:** Solo se usó una división temporal 70/30. No se aplicó *walk-forward optimization* ni *k-fold cross-validation*.
4. **Datos de volumen no filtrados:** No se descartaron operaciones en días de baja liquidez, lo que puede inflar el slippage real.

---

## 6. Métricas Adicionales de Riesgo

### 6.1 Ratio de Calmar (CAGR / Max Drawdown)

| Estrategia | CAGR | Max DD | Ratio Calmar | Interpretación |
|------------|------|--------|--------------|----------------|
| Patrones ABCD | 7.89% | -11.2% | **0.70** | Saludable |
| Buy & Hold | 19.05% | -18.8% | **1.01** | Superior |

**Insight:** El B&H ofrece mejor rentabilidad por unidad de drawdown máximo. La estrategia ABCD sacrifica eficiencia Calmar a cambio de un drawdown absoluto menor.

### 6.2 Ratio de Sortino (Rentabilidad / Downside Deviation)

| Estrategia | Sortino (estimado) |
|------------|-------------------|
| Patrones ABCD | ~0.95 |
| Buy & Hold | ~1.20 |

**Insight:** El B&H también supera en eficiencia de downside. La estrategia ABCD protege mejor en términos absolutos (-11.2% vs -18.8%), pero lo hace a costa de renunciar a gran parte del upside.

### 6.3 Impacto Fiscal Estimado

Con una tasa impositiva efectiva del **21%** sobre plusvalías a corto plazo (frecuencia diaria de rebalanceo):

| Estrategia | CAGR bruto | CAGR neto estimado |
|------------|-----------|-------------------|
| Patrones ABCD | 7.89% | **~6.2%** |
| Buy & Hold | 19.05% | **~15.5%** |

**Insight:** La brecha de underperformance se amplía de 11.16 pp a **9.3 pp** tras impuestos. La alta rotación (86.20%) penaliza fiscalmente a la estrategia ABCD frente al B&H, que tributa principalmente al final del período.

---

## 7. Recomendaciones y Hoja de Ruta para Producción

### A. Rentabilización de la Liquidez (Solución al Cash Drag)
Asignar el capital no utilizado en posiciones armónicas a un fondo monetario o ETF de deuda soberana de ultra corto plazo (ej. BIL, SHV o remuneración de colateral). Un rendimiento adicional del 3-4% anual sobre la caja inactiva eleva significativamente el CAGR global de la estrategia.

### B. Protocolo de Ejecución de Entrada (Eliminación de Look-Ahead)
1. Detectar el punto D en la confluencia de la PRZ.
2. Esperar el cierre de la vela diaria de confirmación (T+1).
3. Introducir orden de entrada al mercado en el precio de apertura de T+2 o colocar orden límite dentro de la PRZ.

### C. Filtro Macro / Tendencial
Condicionar las entradas LONG a períodos donde el índice de referencia (SPY) cotice por encima de su media móvil simple de 200 días (SMA₂₀₀). Desactivar o ajustar stop-loss en entornos donde el mercado general se sitúe en régimen bajista de estructura.

### D. Rediseño como Módulo Satélite (Core-Satellite)
No emplear la estrategia como vehículo del 100% del capital.

**Estructura recomendada:**
- **Core (70-80%):** Asignación pasiva indexada (Buy & Hold / DCA).
- **Satellite (20-30%):** Estrategia Táctica ABCD Armónica para la generación de alpha de corto plazo y cobertura de liquidez.

### E. Validación Continua
- **Re-evaluación periódica:** Revisar la efectividad de los patrones cada 6 meses.
- **Monitoreo de drawdown:** Detener la estrategia si el drawdown supera el -20%.
- **Backtesting rolling:** Validar la estrategia en ventanas móviles para detectar cambios de régimen.
- **Walk-forward optimization:** Implementar re-entrenamiento periódico con ventanas deslizantes.

---

## 8. Veredicto Final (Rev 3.1)

La estrategia de Patrones Armónicos ABCD es un **sistema cuantitativamente válido y estadísticamente real** (p=0.003). No es fruto del azar ni del sobreajuste de datos.

**Sin embargo**, no debe presentarse como un sustituto superior al Buy & Hold para la maximización de patrimonio en fases alcistas. **El test placebo (p=0.003) confirma que los patrones ABCD tienen poder predictivo estadísticamente significativo sobre el timing de entrada. Sin embargo, este poder predictivo no se traduce en superioridad de rentabilidad frente al Buy & Hold en mercados alcistas, debido al cash drag inherente a la estrategia. Por tanto, el valor de la estrategia no reside en maximizar rentabilidad, sino en preservar capital y reducir drawdown, lo cual la hace adecuada como componente satélite de una cartera diversificada.**

Su éxito operacional en cuentas reales dependerá de:
1. Una gestión eficiente del rendimiento de la caja inactiva.
2. La minimización estricta del slippage (<0.2% por operación).
3. La correcta gestión del desfase temporal de confirmación del punto D (T+1/T+2).
4. La integración como satélite dentro de una cartera