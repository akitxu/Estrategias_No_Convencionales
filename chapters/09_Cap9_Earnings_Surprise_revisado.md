# Capítulo 9 — Earnings Surprise: el efecto post-anuncio (PEAD)

> *"El mercado puede ignorar la información durante un tiempo, pero no puede ignorarla para siempre."*  
> — Adaptado de Benjamin Graham

El **Post-Earnings Announcement Drift (PEAD)** es una de las anomalías de mercado más estudiadas de las finanzas cuantitativas. Describe el fenómeno por el cual las acciones que reportan beneficios significativamente superiores a las expectativas de los analistas tienden a seguir moviéndose en esa dirección durante semanas o meses después del anuncio. Fue documentado en los trabajos pioneros de Ball y Brown (1968) y Bernard y Thomas (1989), y desde entonces se ha replicado sobre todo en empresas pequeñas y medianas.

Este capítulo hace algo más que presentar una estrategia: **documenta cómo se construyó, cómo se auditó y qué ocurrió cuando se sometió a pruebas diseñadas para refutarla**. El resultado final es menos espectacular que el del primer borrador, pero mucho más instructivo.

**Semáforo de viabilidad:** 🟡 **Parcialmente backtesteable**. La estrategia es sólida en teoría, pero depende de la calidad y puntualidad de los datos de `earnings_dates` de Yahoo Finance, que a veces presentan retrasos o valores nulos.

**Veredicto de la evidencia:** 🔴 **En el universo y con los datos de este capítulo, el efecto PEAD no es detectable**. Lo que la estrategia aporta (menor riesgo que SPY) se explica por el universo elegido y por estar parcialmente en efectivo, no por la señal de sorpresa. Las secciones 4 y 5 explican cómo se llegó a esta conclusión.

---

## 1. Fundamentos Teóricos: ¿Por qué debería existir el PEAD?

Si los mercados fueran perfectamente eficientes, el precio ajustaría instantáneamente a la nueva información en el momento del anuncio. La literatura propone varias razones por las que no ocurre así:

1. **Infrareacción inicial (underreaction):** los inversores son conservadores y tardan en actualizar sus creencias ante una noticia que contradice la tendencia previa.
2. **Costes de arbitraje:** los límites de capital y el riesgo impiden que los grandes fondos arbitren la ineficiencia de inmediato. Este mecanismo es **más fuerte en empresas pequeñas e ilíquidas** que en las mega-caps de este capítulo, algo que conviene tener presente al interpretar los resultados.
3. **Anclaje de los analistas:** las revisiones de las estimaciones de beneficios son graduales, lo que crea un "viento de cola" (drift) que empuja el precio durante varios trimestres.

La métrica clásica es el **SUE (Standardized Unexpected Earnings)**. Para este backtest retail se utiliza una aproximación directa: el **porcentaje de sorpresa** (`Surprise(%)`) que publica Yahoo Finance. Tiene un defecto conocido: cuando el beneficio esperado está cerca de cero, el porcentaje se dispara. Por eso, en la versión final, se recorta a 50 % solo para ordenar candidatos.

---

## 2. La estrategia final (versión 5)

| Elemento | Regla |
|---|---|
| **Universo** | 21 grandes compañías de EE. UU. (7 tecnología, 4 finanzas, 3 salud, 4 consumo, 3 industriales) |
| **Señal 1: sorpresa** | `Surprise(%)` > 2 % |
| **Señal 2: reacción del precio** | Rentabilidad en exceso sobre SPY entre el cierre de T−1 y el cierre de T+1 > 0 |
| **Señal 3: volumen** | Pico de volumen en T o T+1 > 1,5 × media de las 20 sesiones previas |
| **Entrada** | La señal se activa en el cierre de T+1; el motor aplica los pesos a partir de la sesión siguiente |
| **Tenencia** | Hasta 60 **sesiones** bursátiles, o salida 3 sesiones antes del siguiente anuncio |
| **Tamaño de posición** | Máximo 8 posiciones, 12,5 % cada una; si hay más candidatas, se prioriza por magnitud de sorpresa; el resto queda en efectivo |
| **Stop-loss** | −8 % desde el precio de entrada, evaluado en cada decisión; la acción queda bloqueada hasta el siguiente evento |
| **Rebalanceo** | Semanal (primera sesión de cada semana); coste de 0,1 % sobre la rotación |

> **Nota sobre el efectivo.** En el motor del proyecto el efectivo no rinde nada (0 %). La versión inicial del capítulo hablaba de refugiarse en SHV; eso no está implementado. Es una de las líneas de mejora de la sección 8.

---

## 3. Evolución del desarrollo: de la idea al diagnóstico

### 3.1 Los dos primeros intentos

**Intento 1: comprar cualquier sorpresa positiva** (`Surprise(%) > 0`). El resultado fue decepcionante. Muchas empresas "superan" las expectativas por márgenes triviales, y eso ya está descontado en el precio.

**Intento 2: umbral estricto y ventana de drift.** Se elevó el umbral a 5 % con ventana de 45 días. La relación señal/ruido mejoró. Esa versión produjo los resultados del borrador original (10 acciones, periodo 2008–2026): CAGR 7,41 %, Sharpe 0,40, drawdown −28,14 %, beta 0,23. Esas cifras proceden de una ejecución anterior que no se ha repetido y **no son comparables** con las actuales (distinto universo y periodo).

### 3.2 Auditoría del código: errores corregidos

Antes de interpretar nada, se revisó el notebook. Se encontraron trece problemas, de tres tipos.

**Errores que impedían ejecutar o falseaban la salida**

| Problema | Corrección |
|---|---|
| `FECHA_INICIO` y `FECHA_FIN` valían `None`; el gráfico y el análisis hacían `None[:4]` y restaban strings (`TypeError`) | Se rellenan con las fechas del menú de estrés; títulos y CAGR usan el índice real de la serie |
| El resumen por activo usaba `mask`, que solo recogía el último evento (y daba `NameError` sin eventos) | Resumen mediante un embudo de filtros por activo |
| "Días con posición" se calculaba como `(patrimonio > 0).sum()`, que da siempre 100 % | La exposición se calcula desde los pesos reales |
| Cabecera del notebook copiada del Capítulo 8 (Merger Arbitrage) | Corregida |

**Errores de lógica de la estrategia**

| Problema | Corrección |
|---|---|
| `STOP_LOSS_PCT` y `estado['posiciones']` se definían pero **nunca se usaban**, aunque el docstring decía lo contrario | Stop-loss real desde el precio de entrada |
| El filtro de volumen se evaluaba **cada día** de la ventana y se sobrescribía entre eventos, lo que hacía la posición intermitente | Un único test por evento: pico de volumen frente a la media de las 20 sesiones previas |
| `earnings_dates` devuelve solo unos 12 trimestres | `get_earnings_dates(limit=100)` (histórico desde 2002) |
| La ventana de 60 "días" eran días naturales (≈ 42 sesiones) | 60 sesiones bursátiles |
| Con una sola señal activa, el 100 % de la cartera iba a una acción | Máximo de 8 posiciones, con peso fijo de 1/8 |

**Look-ahead y diseño**

| Problema | Corrección |
|---|---|
| La señal empezaba el mismo día del anuncio. Si el anuncio sale después del cierre, la cartera "compraba" con información que aún no existía | La señal empieza en T+1, cuando la reacción completa ya es conocida |
| La posición se mantenía durante el siguiente anuncio (riesgo binario) | Salida 3 sesiones antes |
| Gráfico con doble eje Y (las curvas no eran comparables a simple vista) | Un único eje, todo normalizado al capital inicial |
| El texto de conclusiones decía "umbral > 5 %" cuando el código usaba 2 % | Texto generado con los parámetros reales |

### 3.3 Mejoras de diseño

Además de corregir errores, se añadieron tres elementos pensados para mejorar la calidad de la señal:

1. **Confirmación por reacción del precio.** Una sorpresa de beneficios que el mercado no premia suele ser ruido. Solo se entra si la acción supera a SPY alrededor del anuncio.
2. **Prioridad por magnitud de sorpresa** cuando hay más candidatas que posiciones.
3. **Salida antes del siguiente anuncio**, para no asumir el riesgo binario de un nuevo resultado.

### 3.4 Integración con el motor del proyecto (`core`)

Al leer el código del motor `MotorBacktestDinamico` se confirmaron cuatro hechos importantes:

- **No hay look-ahead en el motor.** Los pesos decididos al cierre de *t* se aplican a la rentabilidad de *t+1*.
- **`log_operaciones` nunca se rellena** en el motor dinámico. Por eso Win-rate, Profit Factor y Operaciones Totales salían siempre a 0, con cualquier estrategia. Esas métricas no deben interpretarse; se sustituyeron por estadísticas por evento calculadas en el notebook.
- **El efectivo rinde 0 %**, lo que penaliza a la estrategia frente a SPY cuando está fuera.
- **El "Alpha" del informe** se calcula como `CAGR − beta × CAGR(SPY)`, sin tasa libre de riesgo. Con una beta baja, ese número sale positivo con muy poco esfuerzo: no es una prueba de habilidad.

### 3.5 Un fallo que cambió el resultado: el benchmark ausente

En la primera ejecución con las mejoras, el notebook avisó de que SPY no estaba entre los precios cargados (el motor guarda el benchmark aparte). En consecuencia, el filtro de reacción medía la **rentabilidad absoluta** en vez del exceso sobre el mercado, y dejaba pasar un 61 % de los eventos con datos de precio (522 de 862), una proporción típica de un mercado alcista. Tras descargar SPY y medir el exceso real, el resultado cambió de forma notable con un cambio mínimo en el número de señales:

| Versión | Eventos que pasan el filtro de reacción | Patrimonio final | CAGR | Sharpe | Max Drawdown |
|---|---|---|---|---|---|
| Reacción medida sin ajustar por mercado | 522 | 85.504 € | 16,28 % | 1,15 | −26,15 % |
| Reacción medida en exceso sobre SPY | 505 | 73.869 € | 15,09 % | 1,07 | −27,85 % |

Con solo un 3 % menos de eventos, el patrimonio final cayó un 14 %. Esa fragilidad es, en sí misma, una señal de alarma: un efecto real no debería depender tanto de unas pocas decenas de operaciones.

### 3.6 La batería de validación

Tras esa corrección se diseñaron cuatro pruebas, de menos a más exigentes:

1. **Estadísticas por evento:** rentabilidad y exceso sobre SPY de cada episodio de inversión.
2. **Estudio de eventos:** exceso acumulado a 5, 10, 20, 40 y 60 sesiones, comparado con el exceso *normal* de la misma acción en cualquier fecha. Aísla el efecto de la señal del hecho de que estas acciones, elegidas con información de hoy, han batido a SPY.
3. **Test placebo:** se mantiene el número, la duración y la exposición de los episodios de cada acción, pero se colocan en fechas aleatorias. Si la estrategia real no supera a esa distribución, la señal no aporta información.
4. **Barrido de parámetros:** 27 combinaciones de umbral, ventana y máximo de posiciones, para medir la estabilidad del resultado (no para elegir la mejor, lo que sería *data snooping*).

El placebo tuvo además su propia corrección. La primera versión permitía solapar episodios del mismo activo, así que quedaba menos invertida que la estrategia real y su rentabilidad media salía artificialmente baja (11,4 %). Eso hacía parecer significativo (p = 0,06) un resultado que no lo era. Con los episodios reubicados sin solapes, la exposición de los placebos (81,4 %) pasó a coincidir con la de la estrategia real (80,7 %), y el p-valor subió.

---

## 4. Resultados de la versión final

Periodo: **2012-05-18 → 2026-08-14** (14,2 años). El inicio lo marca Meta, que no cotizaba antes: el motor usa solo el periodo en que todos los activos tienen datos.

### 4.1 Métricas clave

| Métrica | Earnings Surprise | Buy & Hold (universo) | SPY |
|---|---|---|---|
| **Patrimonio final** | 73.869 € | — | — |
| **Rentabilidad total** | 638,69 % | 5.583,66 % | 668,36 % |
| **CAGR** | 15,09 % | 32,83 % | ≈ 15,4 % |
| **Volatilidad anual** | 12,18 % | 29,18 % | — |
| **Sharpe** | 1,07 | 1,06 | 0,80 |
| **Sortino** | 1,33 | 1,37 | — |
| **Max Drawdown** | −27,85 % | −53,97 % | −33,7 % |
| **Beta** | 0,51 | — | — |
| **R²** | 0,50 | — | — |
| **Exposición real media** | 73,0 % (mín. 0 %, máx. 100 %) | 100 % | 100 % |
| **Rebalanceos** | 720 | — | — |

### 4.2 Cómo leer estas cifras

- **Frente a SPY, la estrategia consigue el mismo retorno con menos riesgo.** CAGR parecido (15,1 % frente a 15,4 %), pero Sharpe 1,07 frente a 0,80 y drawdown de −28 % frente a −34 %.
- **La beta de 0,51 es coherente con una exposición media del 73 %** y con una cesta que incluye muchas defensivas (PG, KO, JNJ, WMT, PFE).
- **El Buy & Hold del universo no es un rival realista.** Rinde un 32,8 % anual porque contiene a NVDA, TSLA y META, ganadoras que se eligieron con información de hoy (sesgo de supervivencia). Comparar contra esa curva infravalora cualquier estrategia; el comparador justo es SPY.
- **El embudo de señales** (1.955 anuncios → 1.360 con sorpresa > 2 % → 505 con reacción positiva → 434 con volumen anómalo) muestra que el umbral de sorpresa casi no filtra: el 70 % de los anuncios lo supera, porque las empresas baten el consenso con mucha frecuencia.

---

## 5. ¿Existe el PEAD en este universo? Resultados de las pruebas

### 5.1 Estadísticas por evento

434 episodios, de 57 sesiones de media. Acierto: 70,7 %. Rentabilidad media: 5,51 % (mediana 4,68 %). Exceso medio sobre SPY: 2,34 %, con acierto frente a SPY del 55,5 % (t = 4,4). El 25,3 % de los episodios habría tocado el stop de −8 %, y aplicarlo reduce la rentabilidad media por episodio al 4,86 %.

Estas cifras parecen buenas, pero **no aíslan el PEAD**: incluyen el hecho de que las 21 acciones superaron a SPY. Además, el t-stat sobrestima la significación porque los eventos se agrupan en las mismas temporadas de resultados.

| Año de entrada | Rentabilidad media | Exceso medio vs SPY |
|---|---|---|
| 2012 | 4,67 % | −1,09 % |
| 2013 | 12,46 % | 7,06 % |
| 2014 | 4,47 % | 2,05 % |
| 2015 | −0,48 % | 2,00 % |
| 2016 | 10,03 % | 5,21 % |
| 2017 | 7,81 % | 2,13 % |
| 2018 | 2,07 % | 1,91 % |
| 2019 | 8,95 % | 3,38 % |
| 2020 | 7,39 % | 4,41 % |
| 2021 | 6,15 % | 2,61 % |
| 2022 | −2,64 % | 0,13 % |
| 2023 | 5,81 % | 0,77 % |
| 2024 | 8,89 % | 3,29 % |
| 2025 | 4,02 % | 1,22 % |
| 2026 | 0,73 % | −2,80 % |

### 5.2 Estudio de eventos: la prueba decisiva

| Horizonte (sesiones) | Eventos | Exceso del evento | Exceso normal de la acción | **Exceso extra** | t-stat |
|---|---|---|---|---|---|
| 5 | 434 | 0,37 % | 0,15 % | **0,22 %** | 1,25 |
| 10 | 432 | 0,56 % | 0,30 % | **0,26 %** | 1,13 |
| 20 | 428 | 0,71 % | 0,61 % | **0,10 %** | 0,34 |
| 40 | 425 | 1,53 % | 1,26 % | **0,27 %** | 0,66 |
| 60 | 425 | 2,30 % | 1,96 % | **0,34 %** | 0,63 |

Si existiera drift PEAD, el exceso extra debería ser claramente positivo y concentrarse en los primeros horizontes. No ocurre: va de +0,10 % a +0,34 %, con t-stats entre 0,3 y 1,3, sin patrón. A 60 sesiones, el evento rinde un 2,30 % sobre SPY, pero las mismas acciones rinden un 1,96 % en cualquier fecha: **cerca del 85 % del exceso aparente pertenece al universo, y solo un 15 % a la señal**. Ese 1,96 % por 60 sesiones equivale a un 8 % anual sobre SPY, que es el sesgo de supervivencia convertido en número.

### 5.3 Test placebo

| Métrica | Estrategia real | Media de placebos | p5 – p95 | p-valor |
|---|---|---|---|---|
| CAGR | 15,09 % | 14,19 % | 11,19 % – 18,24 % | 0,307 |
| Sharpe | 1,07 | 0,95 | 0,73 – 1,22 | 0,198 |

(100 placebos; exposición real 80,7 % frente a 81,4 % en los placebos; p-valores unilaterales.)

La estrategia real queda en la zona media-alta de la distribución, pero no se distingue de elegir fechas al azar dentro de las mismas acciones. El Sharpe medio de los placebos (0,95) ya supera al de SPY (0,80): **invertir en estas acciones, con el mismo tope de posiciones y el mismo stop, ya produce el perfil de riesgo observado**.

### 5.4 Barrido de parámetros

Sharpe medio (promediado sobre el máximo de posiciones):

| Umbral de sorpresa | Ventana 20 sesiones | Ventana 40 sesiones | Ventana 60 sesiones |
|---|---|---|---|
| > 2 % | 0,58 | 0,66 | 1,08 |
| > 5 % | 0,55 | 0,66 | 1,08 |
| > 10 % | 0,38 | 0,47 | 0,81 |

- El Sharpe de las 27 combinaciones va de 0,20 a 1,15 (mediana 0,65). Solo 8 de 27 superan a SPY en Sharpe (0,80), y solo 2 de 27 en CAGR.
- **El resultado depende sobre todo de la ventana y de cuánto tiempo se está invertido**, no del umbral de sorpresa. Si el efecto fuera un drift tras el anuncio, las ventanas cortas deberían funcionar al menos tan bien como las largas; ocurre lo contrario, que es lo que se espera si lo que se captura es simplemente exposición a estas acciones.
- Umbrales mayores (> 10 %) empeoran el resultado, pero también reducen mucho la exposición (del 81 % al 46 %).
- Las mejores combinaciones (60 sesiones y 5 posiciones, CAGR ≈ 20 %) tienen un drawdown de −34 % a −35 %, similar al de SPY: más retorno a cambio de más riesgo, no un free lunch.

---

## 6. Limitaciones y riesgos específicos

1. **Sesgo de supervivencia.** El universo son compañías grandes y actuales, seleccionadas con información de hoy. Es la limitación más importante del capítulo, y la que más probablemente infla cualquier resultado.
2. **Calidad de los datos.** Yahoo Finance no es una base de datos fundamental profesional: fechas y sorpresas pueden estar desactualizadas, y no se garantiza la hora del anuncio. Un sistema profesional usaría Compustat, I/B/E/S o Refinitiv, con constituyentes *point-in-time*.
3. **Timing de la ejecución.** El borrador original asumía ejecutar al cierre del día del anuncio, lo que puede usar información que aún no existía. La versión final entra en T+1.
4. **Periodo efectivo corto.** El motor trabaja solo con el periodo común a todos los activos, así que Meta recorta la muestra a 2012–2026 y deja fuera la crisis de 2008.
5. **Pocas observaciones independientes.** Los 434 episodios se agrupan en las mismas temporadas de resultados, lo que reduce la potencia estadística. Con esta muestra solo se detectan efectos grandes: **no se puede distinguir un efecto cero de uno pequeño pero real** (por ejemplo, 1–2 % por trimestre).
6. **Efectivo al 0 %.** Penaliza a la estrategia en los periodos fuera del mercado.
7. **Pruebas múltiples.** Probar 27 combinaciones sobre los mismos datos y quedarse con la mejor sería *data snooping*; por eso el barrido se interpreta como medida de estabilidad.
8. **Concentración sectorial.** En temporadas de resultados la cartera puede cargarse de un único sector. No se ha medido.

---

## 7. Conclusiones

### 7.1 Conclusión sobre la estrategia

Con los datos y el universo de este capítulo, **no hay evidencia de que la señal de sorpresa de beneficios aporte valor**. Las tres pruebas apuntan en la misma dirección: el exceso extra tras el anuncio es pequeño y no significativo, la estrategia no se distingue de colocar los mismos periodos de inversión en fechas al azar, y el rendimiento depende de la exposición, no de la señal.

Lo que sí es cierto es que la cartera resultante tiene mejor perfil de riesgo que SPY. Pero ese perfil se explica por el universo y por la exposición parcial. Por eso **no se recomienda presentar esta estrategia como "alpha de PEAD" ni como satélite justificado por la señal**. Si se quiere una cesta defensiva de grandes compañías, existen formas más simples y baratas de construirla.

### 7.2 Conclusión sobre lo que no se puede concluir

La conclusión rigurosa es **"no detectable en este universo"**, no "el PEAD no existe". La literatura sitúa el efecto sobre todo en empresas pequeñas y medianas, y en grandes compañías muy seguidas se ha debilitado mucho. Este capítulo, con 21 mega-caps y 14 años, no tiene potencia para descartarlo.

### 7.3 Lecciones metodológicas

1. **Un backtest bonito no es evidencia.** Hay que compararlo contra un placebo con la misma exposición.
2. **Comparar con SPY no basta.** Hay que comparar cada evento con el comportamiento normal de la misma acción, para separar la señal del sesgo del universo.
3. **Desconfía de las métricas de resumen.** El "Alpha" del informe estándar era positivo y no significaba nada; el Win-rate salía a 0 por un registro vacío.
4. **Audita antes de interpretar.** Trece errores de código, varios de ellos silenciosos, estaban condicionando los números.
5. **Mide la exposición real.** Una cartera 73 % invertida no puede compararse sin más con una 100 % invertida.
6. **Una corrección pequeña puede mover mucho el resultado.** Un 3 % menos de señales redujo el patrimonio final un 14 %: señal de fragilidad.

**Veredicto:** 🔴 **Efecto PEAD no demostrado en este universo.** 🟡 La infraestructura (señales, validación, placebo) es reutilizable para probar el efecto en condiciones más favorables.

---

## 8. Líneas de investigación futura

### 8.1 Mejoras rápidas (con la infraestructura actual)

| Idea | Qué aporta | Estado |
|---|---|---|
| **Sensibilidad del stop** (−12 %, −15 %, sin stop) | El stop lo toca el 25 % de los episodios y recorta exposición sin evidencia de que proteja | Pendiente |
| **Ampliar el periodo** con `EXCLUIR_TICKERS = ['META', 'TSLA', 'V']` | Llega a 2007, incluye 2008 y reduce el sesgo de ganadoras elegidas ex post | Pendiente (parámetro ya disponible) |
| **Umbrales intermedios** (3 % y 7 %) | El barrido cubrió 2 %, 5 % y 10 %; falta ver si hay un punto de inflexión | Parcial |
| **Gráfico de drawdown comparativo** (estrategia, SPY, universo) | Muestra cuándo protege la estrategia y cuándo no | Pendiente |
| **Tabla de rentabilidad anual** de la estrategia frente a SPY | Identifica en qué años gana o pierde. Hoy solo existe el desglose por episodio (sección 5.1) | Pendiente |

### 8.2 Cambios de diseño de la estrategia

1. **Universo más favorable al PEAD:** mid-caps y small-caps líquidas, o un índice amplio (S&P 400/600, Russell). Es la prueba más importante: el efecto debería ser mayor donde los costes de arbitraje son altos.
2. **Selección relativa en vez de umbral absoluto:** quedarse con el decil o quintil superior de sorpresa dentro de cada temporada de resultados, en lugar de un umbral fijo que el 70 % de los anuncios supera.
3. **SUE estandarizado** en lugar del porcentaje de sorpresa, que es inestable cuando el beneficio esperado es cercano a cero.
4. **Reacción del precio como señal principal:** en grandes compañías el ajuste puede ocurrir en los primeros días, de modo que ventanas muy cortas en torno al anuncio merecen su propio estudio.
5. **Efectivo con rendimiento** (por ejemplo SHV o un ETF monetario) en lugar de 0 %.
6. **Frecuencia diaria de decisión** (si el motor la admite) para que el stop y la salida previa al anuncio no tengan hasta una semana de retraso.
7. **Referencia justa:** comparar contra el universo equiponderado y rebalanceado, no contra un Buy & Hold dominado por las ganadoras.

### 8.3 Rigor estadístico

1. **Bootstrap por bloques de temporada** para tener en cuenta que los eventos se agrupan.
2. **Más simulaciones placebo** (500–1.000) y p-valores bilaterales.
3. **Regresión sobre factores** (mercado, tamaño, valor, momentum): el PEAD está muy ligado al momentum, y es posible que la señal solo replique un factor ya conocido.
4. **Separación en muestras:** definir los parámetros con una parte del periodo y evaluarlos en otra, o ajustar el Sharpe por pruebas múltiples.

### 8.4 Datos

1. Datos profesionales de consenso y sorpresas (I/B/E/S, Compustat, Refinitiv) con hora exacta del anuncio.
2. Constituyentes históricos *point-in-time* para eliminar el sesgo de supervivencia.
3. Sistema alternativo de ISIN reales en el diccionario del universo (hoy el campo `isin` contiene el ticker).

### 8.5 Conexión con el siguiente capítulo

El Capítulo 10 estudia el *insider trading* legal (formulario 4 de la SEC). Una posible línea de trabajo es usar las compras de directivos como **confirmación independiente** de la sorpresa de beneficios: dos señales con fuentes distintas podrían filtrar mejor que una sola.

---

## 9. Descargo de responsabilidad

*Este capítulo y el código asociado tienen fines exclusivamente educativos y de investigación cuantitativa. Los datos de `earnings_dates` de `yfinance` pueden contener errores o retrasos. El rendimiento pasado no garantiza resultados futuros. Operar acciones individuales alrededor de eventos de resultados conlleva un riesgo de volatilidad extremo. Realiza siempre tus propias investigaciones y consulta con un asesor financiero profesional antes de tomar decisiones de inversión.*

---

## Apéndice: historial de versiones del notebook

| Versión | Cambios principales |
|---|---|
| Original | 21 acciones, umbral 2 %, ventana de 60 días naturales, señal desde el día del anuncio, sin stop real |
| v2 | Corrección de 13 errores; confirmación por reacción, volumen por evento, máximo de 8 posiciones, salida pre-anuncio, stop real |
| v3 | Descarga de SPY para medir la reacción en exceso; estadísticas por evento |
| v4 | Test placebo y barrido de parámetros; parámetro `EXCLUIR_TICKERS`; exposición real media |
| v5 | Placebo sin solapes (corrige el sesgo a favor de la estrategia); estudio de eventos; gráfico del barrido legible |
