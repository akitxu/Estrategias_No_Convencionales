# ==========================================================================
# GESTOR PROYECTO (Entorno, Directorios y Menús Base)
# ==========================================================================

import os
import sys
import re
import json
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path

class GestorProyecto:
    MARKER_FILE = ".proyecto_root"
    CARPETAS_NIVEL1 = {"core", "datos", "outputs", "chapters", "logs", "notebooks"}
    CARPETAS_NIVEL2 = {
        "carteras", "datos_csv", "datos_fi_gestora", "datos_fi_investing",
        "datos_fi_myinvestor", "datos_fi_r4", "datos_fi_yahoo",
        "backtest", "figures", "reports",
    }
    COLAB_DRIVE_SUBPATH = "MI_PROYECTO_TFM"

    def __init__(self, base_dir_manual=None):
        self.IN_COLAB = "google.colab" in sys.modules
        self.DIRS = {}
        self.BASE_DIR = self._detectar_raiz(base_dir_manual)
        self._constructor_arbol_directorios()
        self._crear_directorios_si_no_existen()

    def _detectar_raiz(self, base_dir_manual):
        if base_dir_manual:
            print(f"📁 BASE_DIR fijado manualmente -> {base_dir_manual}")
            return os.path.abspath(base_dir_manual)
        elif self.IN_COLAB:
            return self._resolver_base_colab()
        else:
            # SOLUCIÓN 100% ROBUSTA Y PORTABLE:
            # Como este archivo de código está en 'core/', la raíz real del proyecto 
            # está exactamente un nivel por encima de 'core'.
            raiz_real = Path(__file__).resolve().parent.parent
            return str(raiz_real)
    def _normalizar_a_raiz(self, punto_partida):
        """Busca hacia arriba ('parents') hasta encontrar una carpeta que contenga 
        elementos clave del proyecto (como 'core' o 'chapters'), asegurando 
        que nunca se tome la carpeta 'notebooks' como raíz."""
        actual = Path(punto_partida).resolve()
        
        # Comprobamos el directorio actual y todos sus padres hacia arriba
        for parent in [actual] + list(actual.parents):
            # Si encontramos marcadores claros de la raíz del proyecto
            if (parent / "core").exists() or (parent / "chapters").exists() or (parent / self.MARKER_FILE).exists():
                return str(parent)
                
        # Alternativa de seguridad por si no encuentra los marcadores exactos:
        # Si estamos dentro de 'notebooks/...', subimos un nivel extra para salir de ella.
        if "notebooks" in actual.parts:
            # Buscamos el directorio justo antes de entrar a 'notebooks'
            idx = actual.parts.index("notebooks")
            raiz_estimada = Path(*actual.parts[:idx])
            if str(raiz_estimada) != "/" and str(raiz_estimada) != "":
                return str(raiz_estimada)

        return str(actual)

    def _resolver_base_colab(self):
        drive_root = "/content/drive"
        my_drive = os.path.join(drive_root, "MyDrive")
        if not os.path.isdir(my_drive):
            try:
                from google.colab import drive
                print("💽 Montando Google Drive...")
                drive.mount(drive_root)
            except Exception as e:
                print(f"⚠️ No se pudo montar Google Drive ({e}).")
        raiz = os.path.join(my_drive, self.COLAB_DRIVE_SUBPATH) if os.path.isdir(my_drive) else os.path.join("/content", self.COLAB_DRIVE_SUBPATH)
        print(f"ℹ️ Entorno Colab detectado -> raíz: {raiz}")
        return raiz

    def _obtener_directorio_del_notebook(self):
        try:
            import ipykernel
            try:
                from jupyter_server import serverapp as app_module
            except ImportError:
                from notebook import notebookapp as app_module
            connection_file = os.path.basename(ipykernel.get_connection_file())
            match = re.search(r'kernel-(.*)\.json', connection_file)
            if not match: return None
            kernel_id = match.group(1)
            for srv in app_module.list_running_servers():
                try:
                    url = srv['url'] + 'api/sessions'
                    token = srv.get('token', '')
                    headers = {'Authorization': f'token {token}'} if token else {}
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=2) as resp:
                        sessions = json.loads(resp.read())
                    for sess in sessions:
                        if sess.get('kernel', {}).get('id') == kernel_id:
                            ruta_relativa = sess['notebook']['path']
                            ruta_completa = os.path.join(srv['root_dir'], ruta_relativa)
                            return os.path.dirname(os.path.abspath(ruta_completa))
                except Exception:
                    continue
        except Exception:
            pass
        return None

    def _constructor_arbol_directorios(self):
        # (Aquí va tu lógica habitual de construcción de subdirectorios basada en self.BASE_DIR)
        pass

    def _crear_directorios_si_no_existen(self):
        # (Lógica de creación de directorios)
        pass

    def _normalizar_a_raiz(self, path):
        path = os.path.abspath(path)
        nombre = os.path.basename(path)
        if nombre in self.CARPETAS_NIVEL2:
            return os.path.dirname(os.path.dirname(path))
        elif nombre in self.CARPETAS_NIVEL1:
            return os.path.dirname(path)
        return path

    def _constructor_arbol_directorios(self):
        self.DIRS = {
            "CORE": os.path.join(self.BASE_DIR, "core"),
            "CHAPTERS": os.path.join(self.BASE_DIR, "chapters"),
            "LOGS": os.path.join(self.BASE_DIR, "logs"),
            "DATOS": os.path.join(self.BASE_DIR, "datos"),
            "OUTPUTS": os.path.join(self.BASE_DIR, "outputs"),
        }
        # --- TODAS LAS CARPETAS DE DATOS CUELGAN DE 'datos' ---
        self.DIRS.update({
            "CARTERAS": os.path.join(self.DIRS["DATOS"], "carteras"),
            "DATOS_CSV": os.path.join(self.DIRS["DATOS"], "datos_csv"),
            "DATOS_FI_GESTORA": os.path.join(self.DIRS["DATOS"], "datos_fi_gestora"),
            "DATOS_FI_INVESTING": os.path.join(self.DIRS["DATOS"], "datos_fi_investing"),
            "DATOS_FI_MYINVESTOR": os.path.join(self.DIRS["DATOS"], "datos_fi_myinvestor"),
            "DATOS_FI_R4": os.path.join(self.DIRS["DATOS"], "datos_fi_r4"),
            "DATOS_FI_YAHOO": os.path.join(self.DIRS["DATOS"], "datos_fi_yahoo"),
        })
        self.DIRS.update({
            "OUTPUTS_BACKTEST": os.path.join(self.DIRS["OUTPUTS"], "backtest"),
            "OUTPUTS_FIGURES": os.path.join(self.DIRS["OUTPUTS"], "figures"),
            "OUTPUTS_REPORTS": os.path.join(self.DIRS["OUTPUTS"], "reports"),
        })

    def _crear_directorios_si_no_existen(self):
        for dir_path in self.DIRS.values():
            os.makedirs(dir_path, exist_ok=True)
        marcador = os.path.join(self.BASE_DIR, self.MARKER_FILE)
        if not os.path.isfile(marcador):
            with open(marcador, "w") as f:
                f.write("Marcador de raíz del proyecto — no borrar.\n")

    def menu_limpieza_directorios(self):
        print("\n" + "="*65 + "\n📂 GESTIÓN DE ESPACIO DE TRABAJO\n" + "="*65)
        directorios_borrables = {k: v for k, v in self.DIRS.items() if k not in ["DATOS", "OUTPUTS"]}
        dir_keys = list(directorios_borrables.keys())
        for i, key in enumerate(dir_keys, 1):
            path = directorios_borrables[key]
            if os.path.exists(path):
                count = len(os.listdir(path))
                status = f"✅ Existe ({count} elementos)" if count > 0 else "📭 Existe (vacío)"
            else:
                status = "🆕 No existe"
            print(f"  {i}. {key:<20} -> {status}")

        user_input = input("\n¿Qué directorios deseas VACIAR? (ej: 3,5,7 / 'todos' / 'ninguno'): ").strip().lower()
        dirs_to_empty = []
        if user_input == 'todos':
            dirs_to_empty = dir_keys
        elif user_input not in ['', 'ninguno', 'no', 'n']:
            try:
                for idx in [int(x.strip()) for x in user_input.split(',')]:
                    if 1 <= idx <= len(dir_keys): dirs_to_empty.append(dir_keys[idx - 1])
            except ValueError:
                print("⚠️ Formato no reconocido. No se vaciará nada.")

        if dirs_to_empty:
            print("\n🧹 Iniciando limpieza...")
            for key in dirs_to_empty:
                path = directorios_borrables[key]
                if os.path.exists(path):
                    print(f"   🗑️  Vaciando '{key}'...")
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        try:
                            if os.path.isfile(item_path) or os.path.islink(item_path): os.unlink(item_path)
                            elif os.path.isdir(item_path): shutil.rmtree(item_path)
                        except Exception as e:
                            print(f"      ⚠️ No se pudo borrar {item_path}: {e}")
                    print(f"      ✅ '{key}' limpiado.")

    def menu_stress_testing(self):
        print("\n" + "="*70 + "\n📉 ANÁLISIS DE ESTRÉS (STRESS TESTING)\n" + "="*70)
        print("  1. Crisis Punto Com (2000-2002)\n  2. Crisis Financiera Mundial (2007-2009)")
        print("  3. Crisis Deuda Soberana (2010-2012)\n  4. Crisis Financiera China (2015-2016)")
        print("  5. Crisis COVID-19 (2020)\n  6. Subida Tipos / Inflación (2022-2023)")
        print("  7. Periodo Personalizado\n  8. Histórico Completo (1999-Hoy)\n")
        opt = input("Introduce tu elección (1-8) [Por defecto 8]: ").strip() or "8"
        periods = {
            '1': ('2000-03-01', '2002-12-31', 'Crisis Punto Com'),
            '2': ('2007-10-01', '2009-03-31', 'Crisis Financiera Mundial'),
            '3': ('2010-04-01', '2012-07-31', 'Crisis Deuda Soberana'),
            '4': ('2015-06-01', '2016-06-30', 'Crisis Financiera China'),
            '5': ('2020-02-01', '2020-12-31', 'Crisis COVID-19'),
            '6': ('2022-01-01', '2023-12-31', 'Subida Tipos / Inflación'),
            '8': ('1999-01-01', datetime.now().strftime('%Y-%m-%d'), 'Histórico Completo')
        }
        if opt == '7':
            start = input("  Fecha inicio (YYYY-MM-DD): ").strip()
            end = input("  Fecha fin (YYYY-MM-DD): ").strip()
            name = "Periodo Personalizado"
        else:
            start, end, name = periods.get(opt, periods['8'])
        print(f"\n🎯 Evento: {name} | Inicio: {start} | Fin: {end}\n")
        return start, end, name

    def imprimir_resumen(self):
        print("\n" + "="*65 + "\n🔍 ENTORNO CONFIGURADO\n" + "="*65)
        print(f"📂 Base: {self.BASE_DIR}")
        for k, v in self.DIRS.items():
            print(f"📁 {k:<20}: {v}")