#!/usr/bin/env python
# coding: utf-8

# # 📓 Navegador de Notebooks — Estrategias No Convencionales
# 
# Explora los notebooks del proyecto organizados por bloques temáticos.
# 
# Este notebook te permite:
# - 📂 Detectar automáticamente el entorno (local o Google Colab)
# - 📥 Clonar el repositorio en Colab si es necesario
# - 🔍 Escanear todos los notebooks `.ipynb` del proyecto
# - 🚀 Abrir cualquier notebook directamente en Google Colab
# - 🐙 Ver el código fuente en GitHub
# - 📊 Ver estadísticas del proyecto

# #  Configuración común y detección de entorno

# In[1]:


# Celda 1: Imports, detección de entorno y clonación automática en Colab
from pathlib import Path
from urllib.parse import quote
import os
import sys
import subprocess
import json
import pandas as pd
from IPython.display import display, HTML, Markdown

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
GITHUB_USER = "akitxu"
GITHUB_REPO = "Estrategias_No_Convencionales"
GITHUB_BRANCH = "main"
GITHUB_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}.git"

# =============================================================================
# DETECCIÓN DE ENTORNO
# =============================================================================
def esta_en_colab():
    try:
        import google.colab  # noqa: F401
        return True
    except ImportError:
        return False

IN_COLAB = esta_en_colab()

print("🔍 Detectando entorno y preparando proyecto...")
print("=" * 70)

if IN_COLAB:
    print("✅ Entorno: Google Colab")
else:
    print("✅ Entorno: Local (Jupyter)")

# =============================================================================
# PREPARACIÓN DEL PROYECTO
# =============================================================================
def encontrar_raiz_local():
    """
    Busca la raíz del repositorio empezando en el directorio actual
    y recorriendo sus padres.
    """
    actual = Path.cwd().resolve()

    for candidato in [actual, *actual.parents]:
        if (
            (candidato / "notebooks").is_dir()
            or (candidato / "chapters").is_dir()
            or (candidato / ".git").exists()
        ):
            return candidato

    return actual


def preparar_proyecto():
    """
    Devuelve la raíz del proyecto tanto en local como en Google Colab.
    """
    if IN_COLAB:
        raiz = Path("/content") / GITHUB_REPO

        if not raiz.exists():
            print(f"📥 Clonando repositorio desde GitHub...")
            print(f"   URL: {GITHUB_URL}")

            resultado = subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    "--branch",
                    GITHUB_BRANCH,
                    GITHUB_URL,
                    str(raiz),
                ],
                capture_output=True,
                text=True,
            )

            if resultado.returncode != 0:
                raise RuntimeError(
                    "No se pudo clonar el repositorio:\n"
                    f"{resultado.stderr}"
                )

            print(f"✅ Repositorio clonado exitosamente en: {raiz}")

        elif not (raiz / ".git").exists():
            raise RuntimeError(
                f"La ruta {raiz} existe, pero no parece ser un repositorio Git."
            )
        else:
            print(f"✅ Repositorio encontrado en: {raiz}")

        return raiz

    # Local
    raiz = encontrar_raiz_local()
    print(f"✅ Usando directorio local: {raiz.absolute()}")
    return raiz


PROJECT_ROOT = preparar_proyecto()

# =============================================================================
# CONFIGURAR RUTAS
# =============================================================================
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
CHAPTERS_DIR = PROJECT_ROOT / "chapters"
CORE_DIR = PROJECT_ROOT / "core"

print(f"\n PROJECT_ROOT: {PROJECT_ROOT}")
print(f"📓 Notebooks: {NOTEBOOKS_DIR}")
print(f"📚 Capítulos: {CHAPTERS_DIR}")
print(f"🧠 Core: {CORE_DIR}")
print(f"\n✅ Notebooks existe: {NOTEBOOKS_DIR.is_dir()}")
print(f"✅ Capítulos existe: {CHAPTERS_DIR.is_dir()}")
print(f"✅ Core existe: {CORE_DIR.is_dir()}")

# =============================================================================
# AÑADIR CORE AL SYS.PATH (¡ESTO ES LO QUE FALTABA!)
# =============================================================================
if CORE_DIR.is_dir():
    # Añadimos el directorio PADRE de 'core' al sys.path
    sys.path.insert(0, str(PROJECT_ROOT))
    print(f"✅ 'core' añadido al sys.path: {PROJECT_ROOT}")
else:
    print(f"⚠️  La carpeta 'core' no existe en {CORE_DIR}")
    print(f"   Verifica que el repositorio se clonó correctamente.")

print("=" * 70)


# # Escaneo de notebooks

# In[2]:


# Celda 2: Escaneo automático de notebooks
import re


def extraer_metadatos_notebook(ruta):
    """
    Extrae título y descripción de un notebook .ipynb.
    """
    titulo = ruta.stem
    descripcion = ""

    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            notebook = json.load(archivo)

        for celda in notebook.get("cells", []):
            if celda.get("cell_type") != "markdown":
                continue

            texto = "".join(celda.get("source", []))
            lineas = texto.splitlines()

            # Extraer título (primera línea con #)
            encabezado = next(
                (
                    linea.strip().lstrip("#").strip()
                    for linea in lineas
                    if linea.strip().startswith("#")
                ),
                None,
            )

            if encabezado:
                titulo = encabezado

            # Extraer descripción (primeras líneas tras el título)
            descripcion_lineas = []
            despues_titulo = False

            for linea in lineas:
                linea = linea.strip()

                if linea.startswith("#"):
                    despues_titulo = True
                    continue

                if despues_titulo and linea and not linea.startswith("**"):
                    descripcion_lineas.append(linea)

                if len(descripcion_lineas) >= 2:
                    break

            descripcion = " ".join(descripcion_lineas)[:200]
            break

    except Exception as error:
        descripcion = f"Error leyendo notebook: {error}"

    return titulo, descripcion


def escanear_notebooks():
    """
    Escanea recursivamente todos los notebooks .ipynb dentro de notebooks/.
    Clasifica cada notebook según su carpeta contenedora (Bloque_*).
    """
    if not NOTEBOOKS_DIR.is_dir():
        print(f"❌ No existe el directorio: {NOTEBOOKS_DIR}")
        return pd.DataFrame(
            columns=[
                "titulo",
                "descripcion",
                "archivo",
                "ruta_completa",
                "ruta_relativa",
                "bloque",
            ]
        )

    registros = []

    for ruta in sorted(NOTEBOOKS_DIR.rglob("*.ipynb")):
        # Excluir checkpoints y archivos temporales
        if (
            ruta.name.startswith(".")
            or ruta.name.startswith("~")
            or ".ipynb_checkpoints" in ruta.parts
        ):
            continue

        titulo, descripcion = extraer_metadatos_notebook(ruta)
        ruta_relativa = ruta.relative_to(PROJECT_ROOT)

        # Determinar el bloque a partir de la ruta relativa
        partes = ruta.relative_to(NOTEBOOKS_DIR).parts

        if len(partes) > 1:
            bloque = partes[0]
        else:
            bloque = "Sin bloque"

        registros.append(
            {
                "titulo": titulo,
                "descripcion": descripcion,
                "archivo": ruta.name,
                "ruta_completa": ruta,
                "ruta_relativa": ruta_relativa,
                "bloque": bloque,
            }
        )

    return pd.DataFrame(registros)


df_notebooks = escanear_notebooks()

if df_notebooks.empty:
    print("⚠️ No se encontraron notebooks.")
else:
    print(f"✅ Se encontraron {len(df_notebooks)} notebooks organizados por bloques\n")
    print("Distribución por bloque:")
    for bloque in sorted(df_notebooks["bloque"].unique()):
        count = len(df_notebooks[df_notebooks["bloque"] == bloque])
        print(f"   • {bloque}: {count} notebooks")

    display(
        df_notebooks[["titulo", "bloque", "archivo"]]
        .sort_values(["bloque", "archivo"])
        .reset_index(drop=True)
    )


# # Menú visual interactivo con enlaces

# In[3]:


# Celda 3: Menú visual interactivo con botones "Abrir en Colab" y "Ver en GitHub"
# Celda 3: Menú visual con opciones Local, GitHub y Colab

from html import escape
from urllib.parse import quote
from IPython.display import display, HTML


def construir_enlaces_notebook(ruta_relativa):
    """
    Construye los enlaces para ejecutar o visualizar un notebook.

    - Local: abre el archivo relativo al directorio del proyecto.
    - GitHub: muestra el notebook en GitHub.
    - Colab: abre el notebook en Google Colab.
    """
    ruta_posix = ruta_relativa.as_posix()
    ruta_url = quote(ruta_posix, safe="/")

    github_url = (
        f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"
        f"/blob/{GITHUB_BRANCH}/{ruta_url}"
    )

    colab_url = (
        f"https://colab.research.google.com/github/"
        f"{GITHUB_USER}/{GITHUB_REPO}"
        f"/blob/{GITHUB_BRANCH}/{ruta_url}"
    )

    # En Jupyter local, la ruta relativa permite abrir el notebook
    # desde el directorio raíz del proyecto.
    local_url = quote(ruta_posix, safe="/")

    return local_url, github_url, colab_url


def mostrar_notebooks(filtro_bloque=None, filtro_busqueda=None):
    """
    Muestra los notebooks con botones para:

    - Ejecutar/abrir localmente.
    - Ver en GitHub.
    - Abrir en Google Colab.
    """
    if df_notebooks.empty:
        print("⚠️ No hay notebooks disponibles para mostrar.")
        print("   Ejecuta primero la celda de escaneo.")
        return

    df = df_notebooks.copy()

    # Aplicar filtro por bloque
    if filtro_bloque and filtro_bloque != "Todos":
        df = df[df["bloque"] == filtro_bloque]

    # Aplicar filtro por texto
    if filtro_busqueda:
        termino = str(filtro_busqueda)

        mask = (
            df["titulo"].str.contains(
                termino,
                case=False,
                na=False,
                regex=False,
            )
            |
            df["descripcion"].str.contains(
                termino,
                case=False,
                na=False,
                regex=False,
            )
            |
            df["archivo"].str.contains(
                termino,
                case=False,
                na=False,
                regex=False,
            )
        )

        df = df[mask]

    html = """
    <style>
        .nb-card {
            background: linear-gradient(
                135deg,
                #667eea 0%,
                #764ba2 100%
            );
            color: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.10);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .nb-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.20);
        }

        .nb-titulo {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 8px;
        }

        .nb-bloque {
            font-size: 0.85em;
            opacity: 0.95;
            background: rgba(255, 255, 255, 0.22);
            padding: 4px 10px;
            border-radius: 12px;
            display: inline-block;
            margin-bottom: 10px;
        }

        .nb-descripcion {
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 15px;
        }

        .nb-archivo {
            font-size: 0.8em;
            color: #f1f1f1;
            font-family: monospace;
            margin-bottom: 14px;
            word-break: break-word;
        }

        .nb-botones {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }

        .nb-btn {
            display: inline-block;
            padding: 9px 16px;
            border-radius: 6px;
            text-decoration: none !important;
            font-weight: bold;
            font-size: 0.90em;
            cursor: pointer;
            border: 1px solid transparent;
            transition: background-color 0.2s, color 0.2s;
            white-space: nowrap;
        }

        /* Botón local */
        .nb-btn-local {
            background: #f37626;
            color: #ffffff !important;
            border-color: #f37626;
        }

        .nb-btn-local:hover {
            background: #d85f16;
            color: #ffffff !important;
        }

        /* Botón GitHub: fondo claro y texto oscuro */
        .nb-btn-github {
            background: #e9dff7;
            color: #3f2860 !important;
            border-color: #d2bde9;
        }

        .nb-btn-github:hover {
            background: #f4edfb;
            color: #2d1c48 !important;
            border-color: #bda0da;
        }

        /* Botón Colab */
        .nb-btn-colab {
            background: #f9ab00;
            color: #241900 !important;
            border-color: #f9ab00;
        }

        .nb-btn-colab:hover {
            background: #ffc247;
            color: #241900 !important;
        }

        h2 {
            color: #2c3e50;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
    </style>
    """

    html += (
        f"<h2>📓 Notebooks del Proyecto "
        f"({len(df)} encontrados)</h2>"
    )

    if df.empty:
        html += (
            "<p>No se encontraron notebooks con los filtros aplicados.</p>"
        )
        display(HTML(html))
        return

    for _, fila in df.iterrows():
        ruta_relativa = fila["ruta_relativa"]

        local_url, github_url, colab_url = (
            construir_enlaces_notebook(ruta_relativa)
        )

        titulo = str(fila["titulo"]).strip()
        descripcion = str(fila["descripcion"]).strip()
        archivo = str(fila["archivo"]).strip()
        bloque = str(fila["bloque"]).strip()

        # Evitar mostrar "nan"
        if descripcion.lower() == "nan":
            descripcion = ""

        html += f"""
        <div class="nb-card">
            <div class="nb-titulo">
                {escape(titulo)}
            </div>

            <div class="nb-bloque">
                {escape(bloque)}
            </div>

            <div class="nb-descripcion">
                {escape(descripcion or "Sin descripción disponible")}
            </div>

            <div class="nb-archivo">
                📄 {escape(archivo)}
            </div>

            <div class="nb-botones">
                <a
                    href="{escape(local_url)}"
                    target="_blank"
                    class="nb-btn nb-btn-local"
                    title="Abrir el notebook en Jupyter local"
                >
                    ▶️ Ejecutar en local
                </a>

                <a
                    href="{escape(github_url)}"
                    target="_blank"
                    class="nb-btn nb-btn-github"
                    title="Ver el notebook en GitHub"
                >
                    🐙 Ver en GitHub
                </a>

                <a
                    href="{escape(colab_url)}"
                    target="_blank"
                    class="nb-btn nb-btn-colab"
                    title="Abrir el notebook en Google Colab"
                >
                    🚀 Abrir en Colab
                </a>
            </div>
        </div>
        """

    display(HTML(html))


# Mostrar todos los notebooks
mostrar_notebooks()


# #  Filtros disponibles

# In[4]:


# Celda 4: Filtros disponibles
print("FILTROS DISPONIBLES")
print("=" * 70)

if df_notebooks.empty:
    print("No hay notebooks disponibles para filtrar.")
else:
    print("\nBloques disponibles:")
    for i, bloque in enumerate(["Todos"] + list(df_notebooks["bloque"].unique()), 1):
        if bloque == "Todos":
            count = len(df_notebooks)
        else:
            count = len(df_notebooks[df_notebooks["bloque"] == bloque])
        print(f"   {i}. {bloque} ({count} notebooks)")

    print("\nFunciones disponibles:")
    print("   • mostrar_notebooks()")
    print("   • mostrar_notebooks(filtro_bloque='Bloque_I_Comportamiento')")
    print("   • mostrar_notebooks(filtro_busqueda='Momentum')")


# # Estadísticas del proyecto

# In[5]:


# Celda 5: Estadísticas de notebooks
def estadisticas_notebooks():
    """
    Muestra estadísticas de los notebooks del proyecto.
    """
    if df_notebooks.empty:
        print("No hay notebooks disponibles para estadísticas.")
        return

    print("📊 ESTADÍSTICAS DE NOTEBOOKS")
    print("=" * 70)

    print("Distribución por bloque:")
    for bloque in sorted(df_notebooks["bloque"].unique()):
        count = len(df_notebooks[df_notebooks["bloque"] == bloque])
        print(f"   • {bloque}: {count} notebooks")

    print(f"\nTotal de notebooks: {len(df_notebooks)}")
    print(f"Total de bloques: {df_notebooks['bloque'].nunique()}")

    total_celdas = 0
    total_codigo = 0
    total_markdown = 0

    for _, fila in df_notebooks.iterrows():
        try:
            ruta = fila["ruta_completa"]
            with open(ruta, "r", encoding="utf-8") as f:
                nb = json.load(f)
            celdas = nb.get("cells", [])
            total_celdas += len(celdas)
            total_codigo += sum(1 for c in celdas if c.get("cell_type") == "code")
            total_markdown += sum(1 for c in celdas if c.get("cell_type") == "markdown")
        except Exception:
            pass

    print(f"\nTotal de celdas en todos los notebooks: {total_celdas}")
    print(f"   • Celdas de código: {total_codigo}")
    print(f"   • Celdas de markdown: {total_markdown}")
    print("=" * 70)


estadisticas_notebooks()


# #  Diagnóstico de estructura

# In[6]:


# Celda 6: Diagnóstico de estructura
print("🔍 DIAGNÓSTICO DE ESTRUCTURA")
print("=" * 70)
print(f"\n📂 PROJECT_ROOT: {PROJECT_ROOT}")
print(f"   Existe: {PROJECT_ROOT.exists()}")

if PROJECT_ROOT.exists():
    print(f"\n   Contenido de PROJECT_ROOT:")
    for item in sorted(PROJECT_ROOT.iterdir()):
        tipo = "📁" if item.is_dir() else "📄"
        print(f"      {tipo} {item.name}")

    if NOTEBOOKS_DIR.exists():
        print(f"\n📁 Contenido de notebooks/:")
        for item in sorted(NOTEBOOKS_DIR.iterdir()):
            if item.is_dir():
                print(f"      📁 {item.name}/")
                archivos = list(item.glob("*.ipynb"))
                print(f"         ({len(archivos)} notebooks)")
            else:
                print(f"      📄 {item.name}")
    else:
        print(f"\n❌ No existe la carpeta notebooks/")
        print("   Estructura esperada:")
        print("   Estrategias_No_Convencionales/")
        print("   └── notebooks/")
        print("       ├── Bloque_I_Comportamiento/")
        print("       ├── Bloque_II_Cuantitativas/")
        print("       └── ...")
else:
    print(f"\n❌ PROJECT_ROOT no existe: {PROJECT_ROOT}")

print("=" * 70)


# # Guía de uso rápido

# In[7]:


# Celda 7: Guía de uso rápido
print("""
📓 GUÍA DE USO RÁPIDA
=====================

Funciones disponibles:

1. mostrar_notebooks()
   → Muestra el menú visual interactivo con todos los notebooks.

2. mostrar_notebooks(filtro_bloque='Bloque_I_Comportamiento')
   → Muestra solo los notebooks de un bloque específico.

3. mostrar_notebooks(filtro_busqueda='Momentum')
   → Filtra notebooks por título o descripción.

4. estadisticas_notebooks()
   → Muestra estadísticas del proyecto (notebooks, celdas, etc.).

EJEMPLOS DE USO:
    mostrar_notebooks()
    mostrar_notebooks(filtro_bloque='Bloque_II_Cuantitativas')
    mostrar_notebooks(filtro_busqueda='Arbitrage')
    estadisticas_notebooks()
""")

