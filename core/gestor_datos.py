"""
GESTOR DATOS (Importación, Carteras y Descargas)
"""
from pathlib import Path
from typing import Optional, Callable, Dict
import pandas as pd
import numpy as np
import re
import yfinance as yf
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

class GestorDatos:
    def __init__(self, diccionario_datos=None, ruta_cartera_excel=None,
                 fecha_inicio="2010-01-01", fecha_fin=None, dir_base=".", gestor_proyecto=None):
        self.fecha_inicio = pd.to_datetime(fecha_inicio)
        self.fecha_fin = pd.to_datetime(fecha_fin) if fecha_fin else pd.Timestamp.now()
        
        # --- COMPATIBILIDAD CON GESTOR PROYECTO ---
        if gestor_proyecto:
            self.dir_base = Path(gestor_proyecto.BASE_DIR)
            self.dir_datos = Path(gestor_proyecto.DIRS["DATOS_CSV"])
            self.dirs_fuentes = {
                'gestora': Path(gestor_proyecto.DIRS["DATOS_FI_GESTORA"]),
                'r4': Path(gestor_proyecto.DIRS["DATOS_FI_R4"]),
                'myinvestor': Path(gestor_proyecto.DIRS["DATOS_FI_MYINVESTOR"]),
                'investing': Path(gestor_proyecto.DIRS["DATOS_FI_INVESTING"]),
                'yahoo': Path(gestor_proyecto.DIRS["DATOS_FI_YAHOO"]),
            }
            self.dir_figures_png = Path(gestor_proyecto.DIRS["OUTPUTS_FIGURES"])
            self.dir_carteras = Path(gestor_proyecto.DIRS["CARTERAS"])
        else:
            self.dir_base = Path(dir_base)
            self.dir_raiz_datos = self.dir_base / "datos"
            self.dir_raiz_datos.mkdir(parents=True, exist_ok=True)
            self.dir_datos = self.dir_raiz_datos / "datos_csv"
            self.dir_datos.mkdir(parents=True, exist_ok=True)
            self.ORDEN_PRIORIDAD_FUENTE = ['gestora', 'r4', 'myinvestor', 'investing', 'yahoo']
            self.dirs_fuentes = {}
            for fuente in self.ORDEN_PRIORIDAD_FUENTE:
                self.dirs_fuentes[fuente] = self.dir_raiz_datos / f"datos_fi_{fuente}"
                self.dirs_fuentes[fuente].mkdir(parents=True, exist_ok=True)
            self.dir_outputs = self.dir_base / "outputs"
            self.dir_figures_png = self.dir_outputs / "figures" / "png"
            self.dir_figures_png.mkdir(parents=True, exist_ok=True)
            self.dir_carteras = self.dir_raiz_datos / "carteras"
            self.dir_carteras.mkdir(parents=True, exist_ok=True)
        
        self.ruta_db = self.dir_datos / "san_database.db"
        self.db_engine = create_engine(f"sqlite:///{self.ruta_db.as_posix()}", echo=False)
        
        if ruta_cartera_excel and Path(ruta_cartera_excel).exists():
            self.valores_seleccionados = self._procesar_cartera_excel(ruta_cartera_excel)
        elif diccionario_datos:
            self.valores_seleccionados = self._procesar_diccionario(diccionario_datos)
        else:
            raise ValueError("Debe aportarse un 'diccionario_datos' o una 'ruta_cartera_excel'.")
        
        self.datos_cargados = {}
        self.cartera_activa_df = None
        self.precios_ajustados = None
        self.rentabilidades_diarias = None
    
    def _procesar_diccionario(self, diccionario_datos):
        datos_planos = []
        for cat, fondos in diccionario_datos.items():
            for nombre, info in fondos.items():
                if isinstance(info, dict) and 'isin' in info and 'ticker' in info:
                    datos_planos.append({
                        'categoria': cat,
                        'nombre': nombre,
                        'isin': str(info['isin']).strip(),
                        'ticker': str(info['ticker']).strip()
                    })
        return pd.DataFrame(datos_planos)
    
    def _procesar_cartera_excel(self, ruta_excel):
        df = pd.read_excel(ruta_excel)
        datos_planos = []
        for _, row in df.iterrows():
            isin = str(row.get('isin', '')).strip()
            if isin and isin != 'nan':
                datos_planos.append({
                    'categoria': str(row.get('bucket', 'GENERAL')).strip(),
                    'nombre': str(row.get('nombre', 'Desconocido')).strip(),
                    'isin': isin,
                    'ticker': str(row.get('ticker', '')).strip()
                })
        return pd.DataFrame(datos_planos).drop_duplicates(subset=['isin'])
    
    def _limpiar_numero_universal(self, serie):
        def limpiar(v):
            v = str(v).strip()
            if v in ('', 'nan', 'None'):
                return np.nan
            if ',' in v:
                v = v.replace('.', '').replace(',', '.')
            elif v.count('.') > 1:
                partes = v.split('.')
                v = ''.join(partes[:-1]) + '.' + partes[-1]
            return v
        return serie.apply(limpiar)
    
    @staticmethod
    def _is_vliq_r4(filepath: Path) -> bool:
        try:
            with open(filepath, encoding='utf-8', errors='ignore') as f:
                for _ in range(10):
                    line = f.readline()
                    if not line:
                        break
                    parts = line.strip('\r\n').split(';')
                    if len(parts) >= 3 and parts[1]:
                        try:
                            pd.to_datetime(parts[1], format='%d/%m/%Y')
                            float(parts[2].replace(',', '.'))
                            return True
                        except (ValueError, TypeError):
                            continue
        except Exception:
            pass
        return False
    
    def _parse_vliq_r4(self, filepath: Path) -> pd.DataFrame:
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        rows = []
        for line in lines:
            parts = line.strip('\r\n').split(';')
            if len(parts) < 3:
                continue
            date_str, val_str = parts[1].strip(), parts[2].strip()
            try:
                date = pd.to_datetime(date_str, format='%d/%m/%Y')
                val = float(val_str.replace(',', '.'))
                rows.append((date, val))
            except (ValueError, TypeError):
                continue
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=['Date', 'Close']).set_index('Date')
        df = df[~df.index.duplicated(keep='last')].sort_index()
        df['Open'] = df['High'] = df['Low'] = df['Close']
        df['Volume'] = 0.0
        if hasattr(self, 'fecha_inicio') and self.fecha_inicio is not None:
            df = df[df.index >= self.fecha_inicio]
        if hasattr(self, 'fecha_fin') and self.fecha_fin is not None:
            df = df[df.index <= self.fecha_fin]
        return df
    
    def _load_csv_robusto(self, filepath: Path) -> pd.DataFrame:
        filepath = Path(filepath)
        if self._is_vliq_r4(filepath):
            df = self._parse_vliq_r4(filepath)
            if not df.empty:
                return df
        for sep in [',', ';', '\t']:
            for dec in ['.', ',']:
                for enc in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(filepath, sep=sep, decimal=dec, encoding=enc)
                        date_col = next((c for c in df.columns if re.search(r'date|fecha', c, re.I)), None)
                        if date_col is None and len(df.columns) > 0:
                            date_col = df.columns[0]
                        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                        df = df.dropna(subset=[date_col]).set_index(date_col).sort_index()
                        close_col = next((c for c in df.columns if re.search(r'close|nav|valor|precio|ultimo|último', c, re.I)), None)
                        if close_col is None and not df.empty:
                            close_col = df.columns[0]
                        if close_col and close_col != 'Close':
                            df.rename(columns={close_col: 'Close'}, inplace=True)
                        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
                        df = df.dropna(subset=['Close'])
                        if not df.empty and df['Close'].notna().mean() >= 0.5:
                            for col in ['Open', 'High', 'Low']:
                                if col not in df.columns:
                                    df[col] = df['Close']
                            if 'Volume' not in df.columns:
                                df['Volume'] = 0.0
                            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
                            if hasattr(self, 'fecha_inicio') and self.fecha_inicio is not None:
                                df = df[df.index >= self.fecha_inicio]
                            if hasattr(self, 'fecha_fin') and self.fecha_fin is not None:
                                df = df[df.index <= self.fecha_fin]
                            return df
                    except Exception:
                        continue
        return pd.DataFrame()
    
    def importar_ficheros_r4(self):
        carpeta_r4 = self.dirs_fuentes['r4']
        archivos = list(carpeta_r4.glob('*.csv'))
        if not archivos:
            print(f"📭 No hay archivos CSV en {carpeta_r4}")
            return
        print(f"\n📥 Procesando {len(archivos)} ficheros desde Renta 4...")
        archivos_importados, archivos_omitidos = 0, 0
        for f in archivos:
            stem = f.stem
            isin = stem[5:-4] if stem.startswith('vliq_') and stem.endswith('_r4') else stem
            df = self._load_csv_robusto(f)
            if not df.empty:
                ruta_destino = self.dir_datos / f"{isin}.csv"
                df.to_csv(ruta_destino, sep=',', decimal='.', date_format='%Y-%m-%d')
                print(f"✅ {isin}.csv importado y normalizado (fuente: {f.name})")
                archivos_importados += 1
            else:
                print(f"⚠️ No se pudieron extraer datos válidos de {f.name}")
                archivos_omitidos += 1
        print(f"\n📊 Resumen: {archivos_importados} importados, {archivos_omitidos} omitidos")
    
    def gestionar_descarga_cotizaciones(self):
        print(f"\n🗑️ Limpiando CSVs antiguos y descargando desde Yahoo Finance...")
        for archivo in self.dir_datos.glob("*.csv"):
            archivo.unlink()
        if self.valores_seleccionados is None or self.valores_seleccionados.empty:
            print("\n⚠️ No hay activos configurados para descargar.")
            return
        print(f"\n📊 Procesando {len(self.valores_seleccionados)} activos...")
        descargados, omitidos = 0, 0
        for _, row in self.valores_seleccionados.iterrows():
            isin = str(row.get('isin', '')).strip()
            ticker = str(row.get('ticker', '')).strip()
            nombre = str(row.get('nombre', isin)).strip()
            if ticker.lower() == 'nan':
                ticker = ''
            if isin.lower() == 'nan':
                isin = ''
            print(f"\n   📊 {nombre}")
            descargado = False
            if ticker and ticker not in ['', 'nan']:
                try:
                    df = yf.download(ticker, start=self.fecha_inicio.strftime('%Y-%m-%d'),
                                    end=self.fecha_fin.strftime('%Y-%m-%d'),
                                    progress=False, auto_adjust=True)
                    if not df.empty:
                        if isinstance(df.columns, pd.MultiIndex):
                            df.columns = df.columns.get_level_values(0)
                        df.index.name = "Date"
                        df.to_csv(self.dir_datos / f"{isin}.csv")
                        print(f"      ✅ Descargado con ticker: {ticker}")
                        descargado, descargados = True, descargados + 1
                except Exception as e:
                    print(f"      ❌ Error con ticker {ticker}: {e}")
            if not descargado and isin and isin not in ['', 'nan']:
                try:
                    df = yf.download(isin, start=self.fecha_inicio.strftime('%Y-%m-%d'),
                                    end=self.fecha_fin.strftime('%Y-%m-%d'),
                                    progress=False, auto_adjust=True)
                    if not df.empty:
                        if isinstance(df.columns, pd.MultiIndex):
                            df.columns = df.columns.get_level_values(0)
                        df.index.name = "Date"
                        df.to_csv(self.dir_datos / f"{isin}.csv")
                        print(f"      ✅ Descargado con ISIN: {isin}")
                        descargado, descargados = True, descargados + 1
                except Exception as e:
                    print(f"      ❌ Error con ISIN {isin}: {e}")
            if not descargado:
                print(f"      ⚠️ No se pudo descargar {nombre}.")
                omitidos += 1
        print(f"\n📊 Resumen: {descargados} descargados, {omitidos} omitidos")
    
    def normalizar_csv_directorio(self):
        for ruta in sorted(self.dir_datos.glob("*.csv")):
            df = self._load_csv_robusto(ruta)
            if not df.empty:
                df.to_csv(ruta, sep=',', decimal='.', date_format='%Y-%m-%d')
    
    def descargar_csv_especifico(self, isin, ticker):
        """Descarga un CSV específico solo si no existe o no cubre el rango completo."""
        ruta_csv = self.dir_datos / f"{isin}.csv"
        
        if ruta_csv.exists():
            try:
                df_check = pd.read_csv(ruta_csv, index_col=0, parse_dates=True)
                if not df_check.empty:
                    fecha_min = df_check.index.min()
                    fecha_max = df_check.index.max()
                    tolerancia = pd.Timedelta(days=7)
                    
                    # Verificar AMBOS extremos del rango
                    cubre_inicio = fecha_min <= self.fecha_inicio + tolerancia
                    cubre_fin = fecha_max >= self.fecha_fin - tolerancia
                    
                    if cubre_inicio and cubre_fin:
                        return  # Ya está bien, no hace falta re-descargar
            except:
                pass  # Si hay error leyendo, mejor re-descargar
        
        if not ticker or ticker in ['nan', 'None', '']:
            return
        
        try:
            df = yf.download(
                ticker,
                start=self.fecha_inicio.strftime('%Y-%m-%d'),
                end=self.fecha_fin.strftime('%Y-%m-%d'),
                progress=False,
                auto_adjust=True
            )
            if df.empty:
                return
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df.index.name = "Date"
            df.to_csv(ruta_csv)
        except:
            pass
    
    def preparar_datos_motor(self):
        df_precios = pd.DataFrame()
        if self.cartera_activa_df is None:
            print("⚠️ No hay cartera cargada.")
            return
        informe_limpieza = []
        for _, row in self.cartera_activa_df.iterrows():
            isin = str(row['isin'])
            ticker = str(row.get('ticker', ''))
            if not (self.dir_datos / f"{isin}.csv").exists():
                self.descargar_csv_especifico(isin, ticker)
            df = self._load_csv_robusto(self.dir_datos / f"{isin}.csv")
            if not df.empty:
                nombre = row['nombre']
                nombre_limpio = str(nombre).replace(" ", "_").replace(".", "").replace(",", "")
                df_close = df[['Close']].copy()
                df_precios = pd.merge(df_precios, df_close.rename(columns={'Close': nombre_limpio}),
                                     left_index=True, right_index=True, how='outer')
                informe_limpieza.append({
                    'Activo': nombre[:35],
                    'ISIN': isin,
                    'Filas': len(df),
                    'Desde': df.index.min().strftime('%Y-%m-%d'),
                    'Hasta': df.index.max().strftime('%Y-%m-%d'),
                    'Fuente': 'CSV'
                })
        self.precios_ajustados = df_precios.ffill().dropna()
        self.rentabilidades_diarias = self.precios_ajustados.pct_change().dropna()
        if informe_limpieza:
            print(f"\n{'='*75}\n🧼 INFORME DE LIMPIEZA DE DATOS\n{'='*75}")
            df_informe = pd.DataFrame(informe_limpieza)
            try:
                from IPython.display import display
                display(df_informe)
            except ImportError:
                print(df_informe.to_string(index=False))
            print(f"{'='*75}\n✅ {len(self.precios_ajustados.columns)} activos alineados para el Motor Backtest.\n{'='*75}\n")
    
    def _cartera_por_defecto(self):
        if self.valores_seleccionados.empty:
            return
        print("📝 No hay Excel cargado. Generando cartera automática (60/40) desde el diccionario...")
        filas = []
        for i, row in self.valores_seleccionados.iterrows():
            peso = 0.60 if i == 0 else 0.40
            filas.append({
                'nombre': row['nombre'],
                'isin': row['isin'],
                'ticker': row['ticker'],
                'fichero_csv': f"{row['isin']}.csv",
                'bucket': row['categoria'],
                'cantidad_invertida': 10000 * peso,
                'num_participaciones': 0
            })
        self.cartera_activa_df = pd.DataFrame(filas)
    
    def crear_cartera_interactiva(self):
        print("\n" + "═" * 60 + "\n 💼 CREAR NUEVA CARTERA DE INVERSIÓN\n" + "═" * 60)
        nombre_cartera = input("  > Introduce el nombre para esta cartera (ej. Cartera_Bogleheads): ").strip() or "cartera_generada"
        nombre_archivo = "".join(c for c in nombre_cartera if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        print("\nActivos disponibles:")
        for i, row in self.valores_seleccionados.iterrows():
            print(f"  {i}. {row['nombre']} ({row['isin']})")
        sel = input("\nEscribe los índices de los activos a incluir (ej: 0,1): ")
        try:
            isins = [self.valores_seleccionados.iloc[int(x.strip())]['isin'] for x in sel.split(',')]
        except:
            print("❌ Error.")
            return
        filas = []
        for isin in isins:
            info = self.valores_seleccionados[self.valores_seleccionados['isin'] == isin].iloc[0]
            print(f"\n--- Activo: {info['nombre']} ({isin}) ---")
            fecha_inv = input("  > Fecha inversión (YYYY-MM-DD): ").strip()
            try:
                cantidad = float(input("  > Cantidad invertida (€): ").strip())
            except:
                cantidad = 0.0
            self.descargar_csv_especifico(isin, info['ticker'])
            cotiz_inv = 0.0
            df = self._load_csv_robusto(self.dir_datos / f"{isin}.csv")
            if not df.empty:
                try:
                    idx = df.index.get_indexer([pd.to_datetime(fecha_inv)], method='nearest')[0]
                    cotiz_inv = float(df.iloc[idx]['Close'])
                except:
                    pass
            num_partic = cantidad / cotiz_inv if cotiz_inv > 0 else 0.0
            filas.append({
                'nombre': info['nombre'],
                'isin': isin,
                'ticker': info['ticker'],
                'fichero_csv': f"{isin}.csv",
                'concepto': 'Suscripción',
                'fecha_inversion': fecha_inv,
                'cotiz_fecha_inv': cotiz_inv,
                'cantidad_invertida': cantidad,
                'num_participaciones': num_partic,
                'bucket': info['categoria'],
                'bucket_alpha': '*',
                'peso': '*',
                'valor_actual': '*',
                'beneficio': '*',
                'plusvalia_pct': '*',
                'peso_pct': '*',
                'peso_actual': '*',
                'fecha_actual': '*',
                'bucket_comercial': '*',
                'bucket_flag': '*'
            })
        self.cartera_activa_df = pd.DataFrame(filas)
        self.valores_seleccionados = self.cartera_activa_df.copy()
        self.actualizar_y_guardar_cartera(nombre_archivo)
    
    def listar_y_cargar_cartera(self):
        archivos = list(self.dir_carteras.glob("*.xlsx"))
        if not archivos:
            print(f"\n❌ No hay carteras guardadas en {self.dir_carteras.resolve()}")
            return
        print(f"\n📂 Carteras disponibles en la carpeta '{self.dir_carteras.name}/':")
        for i, arch in enumerate(archivos):
            print(f"  {i}. {arch.name}")
        sel = input("\nSelecciona el número de la cartera a cargar (o 'n' para cancelar): ").strip()
        if sel.lower() == 'n':
            return
        try:
            idx = int(sel)
            if 0 <= idx < len(archivos):
                self.cargar_cartera_existente(archivos[idx])
            else:
                print("❌ Número fuera de rango.")
        except ValueError:
            print("❌ Entrada no válida.")
    
    def cargar_cartera_existente(self, ruta_excel):
        print(f"\n📂 Cargando cartera: {ruta_excel.name}")
        self.cartera_activa_df = pd.read_excel(ruta_excel)
        if 'ticker' in self.cartera_activa_df.columns:
            self.valores_seleccionados = self.cartera_activa_df.copy()
        self.actualizar_y_guardar_cartera(Path(ruta_excel).stem)
    
    def actualizar_y_guardar_cartera(self, nombre_archivo):
        if self.cartera_activa_df is None:
            return
        print("\n🔄 Actualizando valores de la cartera...")
        if 'Fecha_actual' in self.cartera_activa_df.columns:
            self.cartera_activa_df = self.cartera_activa_df.drop(columns=['Fecha_actual'])
        self.cartera_activa_df.columns = [str(c).lower().strip() for c in self.cartera_activa_df.columns]
        c_isin = 'isin'
        c_ticker = 'ticker'
        c_cantidad = 'cantidad_invertida'
        c_num_part = 'num_participaciones'
        c_valor = 'valor_actual'
        c_benef = 'beneficio'
        c_plusv = 'plusvalia_pct'
        c_peso_pct = 'peso_pct'
        c_peso_act = 'peso_actual'
        c_fecha_inv = 'fecha_inversion'
        c_cotiz_inv = 'cotiz_fecha_inv'
        c_fecha_act = 'fecha_actual'
        columnas_necesarias = [c_ticker, c_cantidad, c_num_part, c_valor, c_benef,
                               c_plusv, c_peso_pct, c_peso_act, c_fecha_inv, c_cotiz_inv, c_fecha_act]
        for col in columnas_necesarias:
            if col not in self.cartera_activa_df.columns:
                self.cartera_activa_df[col] = np.nan if col != c_ticker else ''
        if c_isin not in self.cartera_activa_df.columns:
            print("❌ Error crítico: El Excel no contiene la columna 'isin'.")
            return
        columnas_float = [c_cantidad, c_num_part, c_valor, c_benef, c_plusv,
                          c_peso_pct, c_peso_act, c_cotiz_inv]
        for col in columnas_float:
            if col in self.cartera_activa_df.columns:
                self.cartera_activa_df[col] = pd.to_numeric(
                    self.cartera_activa_df[col], errors='coerce'
                ).fillna(0.0).astype(float)
        if c_fecha_act in self.cartera_activa_df.columns:
            self.cartera_activa_df[c_fecha_act] = self.cartera_activa_df[c_fecha_act].astype(object)
        if c_fecha_inv in self.cartera_activa_df.columns:
            self.cartera_activa_df[c_fecha_inv] = self.cartera_activa_df[c_fecha_inv].astype(object)
        valor_total = 0.0
        def safe_float(val):
            try:
                if val is None or str(val).strip() in ['*', '', 'nan', 'None'] or pd.isna(val):
                    return 0.0
                return float(val)
            except (ValueError, TypeError):
                return 0.0
        for i, row in self.cartera_activa_df.iterrows():
            isin = str(row[c_isin]).strip()
            ticker = str(row.get(c_ticker, '')).strip()
            if not (self.dir_datos / f"{isin}.csv").exists():
                if not ticker or ticker == 'nan':
                    dict_info = self.valores_seleccionados[self.valores_seleccionados['isin'] == isin]
                    if not dict_info.empty:
                        ticker = dict_info.iloc[0]['ticker']
                self.descargar_csv_especifico(isin, ticker)
            valor_actual = 0.0
            df = self._load_csv_robusto(self.dir_datos / f"{isin}.csv")
            if not df.empty:
                num_part_val = safe_float(row.get(c_num_part, 0.0))
                if num_part_val == 0:
                    invertido = safe_float(row[c_cantidad])
                    cotiz_inv = 0.0
                    try:
                        fecha_obj = pd.to_datetime(str(row[c_fecha_inv]), errors='coerce')
                        if pd.notna(fecha_obj):
                            idx = df.index.get_indexer([fecha_obj], method='nearest')[0]
                            cotiz_inv = float(df.iloc[idx]['Close'])
                            self.cartera_activa_df.at[i, c_cotiz_inv] = round(cotiz_inv, 4)
                    except Exception:
                        pass
                    if cotiz_inv > 0:
                        num_part_val = invertido / cotiz_inv
                        self.cartera_activa_df.at[i, c_num_part] = num_part_val
                valor_actual = float(df['Close'].iloc[-1]) * num_part_val
                self.cartera_activa_df.at[i, c_fecha_act] = df.index[-1].strftime('%Y-%m-%d %H:%M:%S')
            invertido = safe_float(row.get(c_cantidad, 0.0))
            self.cartera_activa_df.at[i, c_valor] = round(valor_actual, 2)
            self.cartera_activa_df.at[i, c_benef] = round(valor_actual - invertido, 2)
            self.cartera_activa_df.at[i, c_plusv] = round(((valor_actual - invertido) / invertido) * 100, 2) if invertido > 0 else 0.0
            valor_total += valor_actual
        for i in self.cartera_activa_df.index:
            val = self.cartera_activa_df.at[i, c_valor]
            self.cartera_activa_df.at[i, c_peso_pct] = round((val / valor_total) * 100, 4) if valor_total > 0 else 0.0
            self.cartera_activa_df.at[i, c_peso_act] = self.cartera_activa_df.at[i, c_peso_pct]
        try:
            ruta_salida = self.dir_carteras / f"{nombre_archivo}.xlsx"
            self.cartera_activa_df.to_excel(ruta_salida, index=False)
            print(f"✅ Guardado en: {ruta_salida.resolve()}")
        except Exception as e:
            print(f"❌ Error al guardar el Excel (¿lo tienes abierto?): {e}")
    
    def calcular_correlacion(self):
        if self.rentabilidades_diarias is None:
            print("⚠️ No hay datos de rentabilidades para calcular la correlación.")
            return
        corr_matrix = self.rentabilidades_diarias.corr()
        print("\n" + "="*50 + "\n📊 TABLA DE CORRELACIONES (Retornos Diarios)\n" + "="*50)
        print(corr_matrix.round(2).to_string())
        print("="*50 + "\n")
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
        plt.title("Matriz de Correlación")
        plt.tight_layout()
        plt.show()
    
    def menu(self):
        while True:
            print("\n" + "=" * 55 + "\n SISTEMA: IMPORTAR · NORMALIZAR · CARTERAS\n" + "=" * 55)
            print("1. Descargar/Actualizar cotizaciones (Yahoo)")
            print("2. Importar ficheros Renta 4")
            print("3. Normalizar CSVs del directorio")
            print("4. Crear cartera interactiva (Pide nombre y descarga CSVs)")
            print("5. Cargar cartera existente (Lista carteras guardadas)")
            print("6. Ejecutar Estrategia (Continuar al Backtest)")
            print("7. Salir")
            print("8. 🔄 Sincronizar datos con período actual (re-descarga si es necesario)")
            opcion = input("Selecciona una opción (1-8): ").strip()
            if opcion == '1': self.gestionar_descarga_cotizaciones()
            elif opcion == '2': self.importar_ficheros_r4()
            elif opcion == '3': self.normalizar_csv_directorio()
            elif opcion == '4': self.crear_cartera_interactiva()
            elif opcion == '5': self.listar_y_cargar_cartera()
            elif opcion == '6':
                # NUEVO: Validar que los datos coincidan con el período antes de ejecutar
                if not self._validar_datos_con_periodo():
                    print("\n⚠️  Los datos en disco no coinciden con el período solicitado.")
                    print("   Usa la opción 8 para sincronizar, o la opción 1 para re-descargar todo.")
                    input("\nPresiona Enter para continuar...")
                    continue
                if self.cartera_activa_df is None: self._cartera_por_defecto()
                if self.cartera_activa_df is not None:
                    self.preparar_datos_motor()
                    return True
            elif opcion == '7': return False
            elif opcion == '8':
                self.sincronizar_con_periodo_actual()
            else: print("❌ Opción no válida.")
            if opcion not in ['6', '7']: input("\nPresiona Enter para continuar...")

    # ============================================================================
    # MÉTODO: Validar que los datos en disco coincidan con el período solicitado
    # ============================================================================
    def _validar_datos_con_periodo(self) -> bool:
        """
        Verifica que los CSVs existentes cubran el rango [fecha_inicio, fecha_fin].
        ACEPTA datos parciales: si un ETF no tiene datos desde el inicio (porque no existía),
        lo acepta pero informa al usuario.
        """
        if self.valores_seleccionados is None or self.valores_seleccionados.empty:
            return True
        
        problemas_criticos = []  # Datos que faltan al FINAL (crítico)
        advertencias_parciales = []  # Datos que faltan al INICIO (aceptable)
        
        for _, row in self.valores_seleccionados.iterrows():
            isin = str(row.get('isin', '')).strip()
            ruta_csv = self.dir_datos / f"{isin}.csv"
            
            if not ruta_csv.exists():
                problemas_criticos.append(f"{row['nombre']}: CSV no existe")
                continue
            
            try:
                df_full = pd.read_csv(ruta_csv, index_col=0, parse_dates=True)
                if df_full.empty:
                    problemas_criticos.append(f"{row['nombre']}: CSV vacío")
                    continue
                
                fecha_min_csv = df_full.index.min()
                fecha_max_csv = df_full.index.max()
                tolerancia = pd.Timedelta(days=7)
                
                # CRÍTICO: Verificar que cubre el FINAL del período
                if fecha_max_csv < self.fecha_fin - tolerancia:
                    problemas_criticos.append(
                        f"{row['nombre']}: datos hasta {fecha_max_csv.date()}, "
                        f"pero se pide hasta {self.fecha_fin.date()}"
                    )
                
                # ADVERTENCIA: Verificar que cubre el INICIO del período
                # (aceptable si el ETF no existía antes)
                if fecha_min_csv > self.fecha_inicio + tolerancia:
                    advertencias_parciales.append(
                        f"{row['nombre']}: datos desde {fecha_min_csv.date()} "
                        f"(el ETF no existía antes)"
                    )
            except Exception as e:
                problemas_criticos.append(f"{row['nombre']}: error leyendo CSV ({e})")
        
        # Si hay problemas críticos (datos que faltan al FINAL), abortar
        if problemas_criticos:
            print(f"\n❌ PROBLEMAS CRÍTICOS detectados:")
            print(f"   • Período solicitado: {self.fecha_inicio.date()} → {self.fecha_fin.date()}")
            print(f"   • Problemas: {len(problemas_criticos)}")
            for p in problemas_criticos[:5]:
                print(f"      • {p}")
            if len(problemas_criticos) > 5:
                print(f"      ... y {len(problemas_criticos) - 5} más")
            return False
        
        # Si solo hay advertencias parciales (datos que faltan al INICIO), aceptar pero informar
        if advertencias_parciales:
            print(f"\n⚠️  DATOS PARCIALES detectados:")
            print(f"   • Período solicitado: {self.fecha_inicio.date()} → {self.fecha_fin.date()}")
            print(f"   • Activos con datos parciales: {len(advertencias_parciales)}")
            for a in advertencias_parciales[:5]:
                print(f"      • {a}")
            if len(advertencias_parciales) > 5:
                print(f"      ... y {len(advertencias_parciales) - 5} más")
            print(f"\n💡 El backtest usará solo el período donde TODOS los activos tienen datos.")
            print(f"   Esto puede reducir el rango efectivo de análisis.")
        
        print(f"\n✅ Datos aceptados para el backtest.")
        return True


    # ============================================================================
    # MÉTODO: Sincronizar datos con el período actual (re-descarga inteligente)
    # ============================================================================
    def sincronizar_con_periodo_actual(self):
        """
        Re-descarga solo los CSVs que no cubren el rango [fecha_inicio, fecha_fin].
        Más eficiente que 'gestionar_descarga_cotizaciones()' que borra todo.
        """
        if self.valores_seleccionados is None or self.valores_seleccionados.empty:
            print("\n⚠️ No hay activos configurados para sincronizar.")
            return
        
        print(f"\n🔄 SINCRONIZANDO DATOS CON EL PERÍODO ACTUAL")
        print(f"   • Rango solicitado: {self.fecha_inicio.date()} → {self.fecha_fin.date()}")
        
        sincronizados, re_descargados, omitidos = 0, 0, 0
        
        for _, row in self.valores_seleccionados.iterrows():
            isin = str(row.get('isin', '')).strip()
            ticker = str(row.get('ticker', '')).strip()
            nombre = str(row.get('nombre', isin)).strip()
            ruta_csv = self.dir_datos / f"{isin}.csv"
            
            necesita_descarga = False
            motivo = ""
            
            if not ruta_csv.exists():
                necesita_descarga = True
                motivo = "CSV no existe"
            else:
                try:
                    df_check = pd.read_csv(ruta_csv, index_col=0, parse_dates=True)
                    if df_check.empty:
                        necesita_descarga = True
                        motivo = "CSV vacío"
                    else:
                        fecha_min_csv = df_check.index.min()
                        fecha_max_csv = df_check.index.max()
                        tolerancia = pd.Timedelta(days=7)
                        
                        if fecha_min_csv > self.fecha_inicio + tolerancia:
                            necesita_descarga = True
                            motivo = f"datos desde {fecha_min_csv.date()}, falta desde {self.fecha_inicio.date()}"
                        elif fecha_max_csv < self.fecha_fin - tolerancia:
                            necesita_descarga = True
                            motivo = f"datos hasta {fecha_max_csv.date()}, falta hasta {self.fecha_fin.date()}"
                        else:
                            sincronizados += 1
                            continue
                except Exception as e:
                    necesita_descarga = True
                    motivo = f"error: {e}"
            
            if necesita_descarga:
                print(f"\n   📊 {nombre}")
                print(f"      ⚠️ {motivo}")
                print(f"      🔄 Re-descargando...")
                
                try:
                    if ticker and ticker not in ['', 'nan']:
                        df = yf.download(
                            ticker,
                            start=self.fecha_inicio.strftime('%Y-%m-%d'),
                            end=self.fecha_fin.strftime('%Y-%m-%d'),
                            progress=False,
                            auto_adjust=True
                        )
                        if not df.empty:
                            if isinstance(df.columns, pd.MultiIndex):
                                df.columns = df.columns.get_level_values(0)
                            df.index.name = "Date"
                            df.to_csv(ruta_csv)
                            print(f"      ✅ Re-descargado con ticker: {ticker}")
                            re_descargados += 1
                            continue
                except Exception as e:
                    print(f"      ❌ Error con ticker {ticker}: {e}")
                
                # Fallback al ISIN
                try:
                    if isin and isin not in ['', 'nan']:
                        df = yf.download(
                            isin,
                            start=self.fecha_inicio.strftime('%Y-%m-%d'),
                            end=self.fecha_fin.strftime('%Y-%m-%d'),
                            progress=False,
                            auto_adjust=True
                        )
                        if not df.empty:
                            if isinstance(df.columns, pd.MultiIndex):
                                df.columns = df.columns.get_level_values(0)
                            df.index.name = "Date"
                            df.to_csv(ruta_csv)
                            print(f"      ✅ Re-descargado con ISIN: {isin}")
                            re_descargados += 1
                            continue
                except Exception as e:
                    print(f"      ❌ Error con ISIN {isin}: {e}")
                
                print(f"      ⚠️ No se pudo re-descargar {nombre}")
                omitidos += 1
        
        print(f"\n📊 RESUMEN DE SINCRONIZACIÓN:")
        print(f"   • ✅ Ya sincronizados: {sincronizados}")
        print(f"   • 🔄 Re-descargados: {re_descargados}")
        print(f"   • ❌ No se pudieron sincronizar: {omitidos}")


    def clasificar_y_asignar_pesos(self, metodo='clasificacion_estatica', **kwargs):
        if self.precios_ajustados is None or self.precios_ajustados.empty:
            raise ValueError("❌ No hay precios ajustados. Ejecuta preparar_datos_motor() primero.")
        metodos = {
            'clasificacion_estatica': self._clasificacion_rv_rf,
            'sma_200': self._filtro_sma_200,
            'ema_cross': self._filtro_ema_cross,
            'tortuga_coja': self._estrategia_tortuga_coja,
            'momentum_cross_sectional': self._momentum_cross_sectional
        }
        if metodo not in metodos:
            raise ValueError(f" Método '{metodo}' no reconocido. Opciones: {list(metodos.keys())}")
        print(f"\n🎯 Método seleccionado: {metodo}")
        return metodos[metodo](**kwargs)
    
    def _clasificacion_rv_rf(self, pct_rv=0.60, pct_rf=0.40):
        cols = list(self.precios_ajustados.columns)
        mapa_categoria = {}
        for _, row in self.valores_seleccionados.iterrows():
            nombre_limpio = str(row['nombre']).replace(" ", "_").replace(".", "").replace(",", "")
            mapa_categoria[nombre_limpio] = str(row.get('categoria', '')).lower()
        kw_rv = ['variable', 'stock', 'world', 'emerging', 'rv']
        rv_cols, rf_cols = [], []
        for col in cols:
            cat = mapa_categoria.get(col, '')
            if cat:
                (rv_cols if any(k in cat for k in kw_rv) else rf_cols).append(col)
            else:
                (rv_cols if any(k in col.lower() for k in kw_rv) else rf_cols).append(col)
        pesos_dict = {}
        if rv_cols:
            w = pct_rv / len(rv_cols)
            pesos_dict.update({c: w for c in rv_cols})
        if rf_cols:
            w = pct_rf / len(rf_cols)
            pesos_dict.update({c: w for c in rf_cols})
        if not pesos_dict:
            pesos_dict = {c: 1.0/len(cols) for c in cols}
        tot = sum(pesos_dict.values())
        pesos_dict = {k: v/tot for k, v in pesos_dict.items() if v > 0}
        print(f"✅ Clasificación estática: {len(rv_cols)} RV / {len(rf_cols)} RF")
        return pesos_dict
    
    def _filtro_sma_200(self, periodo=200, ticker=None):
        ticker = ticker or self.precios_ajustados.columns[0]
        precios = self.precios_ajustados[ticker]
        sma = precios.rolling(window=periodo).mean()
        pesos = (precios > sma).astype(float)
        pesos.name = 'peso_cartera'
        print(f"📊 Filtro SMA {periodo} aplicado a {ticker}")
        print(f"   • Días invertido: {(pesos == 1).sum()}")
        print(f"   • Días en refugio: {(pesos == 0).sum()}")
        print(f"   • % tiempo invertido: {(pesos.mean() * 100):.1f}%")
        return pesos
    
    def _filtro_ema_cross(self, short_period=50, long_period=200, ticker=None):
        ticker = ticker or self.precios_ajustados.columns[0]
        precios = self.precios_ajustados[ticker]
        ema_short = precios.ewm(span=short_period, adjust=False).mean()
        ema_long = precios.ewm(span=long_period, adjust=False).mean()
        pesos = (ema_short > ema_long).astype(float)
        pesos.name = 'peso_cartera'
        print(f"📊 Cruce EMAs {short_period}/{long_period} aplicado a {ticker}")
        print(f"   • Días invertido: {(pesos == 1).sum()}")
        print(f"   • Días en refugio: {(pesos == 0).sum()}")
        print(f"   • % tiempo invertido: {(pesos.mean() * 100):.1f}%")
        return pesos
    
    def _estrategia_tortuga_coja(self, **kwargs):
        from estrategias.tortuga_coja import EstrategiaTortugaCoja
        if not hasattr(self, 'datos_ohlcv') or self.datos_ohlcv is None:
            raise ValueError("❌ La Tortuga Coja requiere datos OHLCV. Usa cargar_datos_ohlcv() primero.")
        estrategia = EstrategiaTortugaCoja(
            ticker=self.precios_ajustados.columns[0],
            df_ohlcv=self.datos_ohlcv,
            **kwargs
        )
        estrategia.calcular_indicadores()
        estrategia.generar_señales()
        estrategia.ejecutar_backtest()
        estrategia.calcular_metricas_motor()
        print(f"🐢 Estrategia Tortuga Coja ejecutada")
        print(f"   • Operaciones realizadas: {len(estrategia.df_operaciones)}")
        print(f"   • Capital final: {estrategia.capital_final:,.2f}€")
        return {
            'pesos': estrategia.df_cartera,
            'operaciones': estrategia.df_operaciones,
            'metricas': estrategia.metricas,
            'estrategia': estrategia
        }
    
    def _momentum_cross_sectional(self, periodo_momentum=12, top_n=5, rebalanceo='mensual'):
        precios = self.precios_ajustados.copy()
        momentum = precios.pct_change(periodo_momentum * 21)
        if rebalanceo == 'mensual':
            fechas_rebalanceo = precios.resample('M').last().index
        elif rebalanceo == 'semanal':
            fechas_rebalanceo = precios.resample('W').last().index
        else:
            fechas_rebalanceo = precios.index
        pesos = pd.DataFrame(index=fechas_rebalanceo, columns=precios.columns, data=0.0)
        for fecha in fechas_rebalanceo:
            if fecha in momentum.index:
                mom_fecha = momentum.loc[fecha].dropna().sort_values(ascending=False)
                top_activos = mom_fecha.head(top_n).index
                peso_individual = 1.0 / len(top_activos) if len(top_activos) > 0 else 0.0
                for activo in top_activos:
                    pesos.loc[fecha, activo] = peso_individual
        print(f"📊 Momentum Cross-Sectional ({periodo_momentum}M, top {top_n})")
        print(f"   • Activos disponibles: {len(precios.columns)}")
        print(f"   • Fechas de rebalanceo: {len(fechas_rebalanceo)}")
        print(f"   • Frecuencia: {rebalanceo}")
        return pesos
    
    # ============================================================================
    # MÉTODO 6: Contrarian Ranking (Capítulo 2 del libro 2)
    # ============================================================================
    def contrarian_ranking(
        self,
        top_n: int = 5,
        umbral_drawdown: float = -0.30,
        umbral_rsi: float = 30.0,
        holding_meses: int = 6,
        cash_ticker: Optional[str] = None
    ) -> Callable:
        """
        Genera una función generadora de pesos para MotorBacktestDinamico
        que implementa la estrategia Contrarian del Capítulo 2.
        """
        precios = self.precios_ajustados.copy()
        activos = list(precios.columns)
        
        # Identificar la columna de cash por nombre limpio (no por ticker)
        cash_columna = None
        if cash_ticker:
            for _, row in self.valores_seleccionados.iterrows():
                if str(row.get('ticker', '')).strip().upper() == cash_ticker.upper():
                    nombre_limpio = str(row['nombre']).replace(" ", "_").replace(".", "").replace(",", "").replace("(", "").replace(")", "")
                    if nombre_limpio in activos:
                        cash_columna = nombre_limpio
                        break
            if cash_columna is None:
                for col in activos:
                    if cash_ticker.upper() in col.upper():
                        cash_columna = col
                        break
        
        if cash_columna:
            print(f"   • Columna cash detectada: '{cash_columna}'")
        else:
            print(f"   • ⚠️ No se detectó columna cash para '{cash_ticker}'. Se usará todo el universo.")
        
        candidatos = [a for a in activos if a != cash_columna]
        
        estado = {
            'posiciones_activas': {},
            'ultima_rotacion': None,
            'cash_columna': cash_columna
        }
        
        def _calcular_rsi(serie: pd.Series, periodo: int = 14) -> float:
            if len(serie) < periodo + 1:
                return 50.0
            delta = serie.diff()
            ganancia = delta.where(delta > 0, 0.0)
            perdida = -delta.where(delta < 0, 0.0)
            ganancia_media = ganancia.rolling(window=periodo).mean().iloc[-1]
            perdida_media = perdida.rolling(window=periodo).mean().iloc[-1]
            if perdida_media == 0:
                return 100.0
            rs = ganancia_media / perdida_media
            return 100 - (100 / (1 + rs))
        
        def _calcular_drawdown_max_52s(serie: pd.Series) -> float:
            ventana = serie.iloc[-252:] if len(serie) >= 252 else serie
            maximo = ventana.max()
            actual = serie.iloc[-1]
            if maximo == 0:
                return 0.0
            return (actual / maximo) - 1
        
        def _rentabilidad_12m(serie: pd.Series) -> float:
            if len(serie) < 252:
                return 0.0
            return (serie.iloc[-1] / serie.iloc[-252]) - 1
        
        def generador_pesos(
            fecha_actual: pd.Timestamp,
            precios_hist: pd.DataFrame,
            rent_hist: pd.DataFrame,
            estado_estrategia: Dict
        ) -> tuple:
            pesos = {a: 0.0 for a in activos}
            
            ultima = estado_estrategia.get('ultima_rotacion')
            toca_rotar = (
                ultima is None or
                (fecha_actual.year - ultima.year) * 12 + (fecha_actual.month - ultima.month) >= holding_meses
            )
            
            if toca_rotar:
                estado_estrategia['posiciones_activas'] = {}
                
                ranking = []
                for activo in candidatos:
                    if activo not in precios_hist.columns:
                        continue
                    serie = precios_hist[activo].dropna()
                    if len(serie) < 252:
                        continue
                    
                    ret_12m = _rentabilidad_12m(serie)
                    dd = _calcular_drawdown_max_52s(serie)
                    rsi = _calcular_rsi(serie)
                    
                    ranking.append({
                        'activo': activo,
                        'ret_12m': ret_12m,
                        'drawdown': dd,
                        'rsi': rsi
                    })
                
                if not ranking:
                    estado_estrategia['ultima_rotacion'] = fecha_actual
                    return pesos, estado_estrategia
                
                ranking.sort(key=lambda x: x['ret_12m'])
                
                seleccionados = []
                for r in ranking:
                    if len(seleccionados) >= top_n:
                        break
                    if r['drawdown'] <= umbral_drawdown and r['rsi'] <= umbral_rsi:
                        seleccionados.append(r)
                
                if seleccionados:
                    peso_individual = 1.0 / len(seleccionados)
                    for s in seleccionados:
                        pesos[s['activo']] = peso_individual
                        estado_estrategia['posiciones_activas'][s['activo']] = fecha_actual
                
                estado_estrategia['ultima_rotacion'] = fecha_actual
            
            else:
                n_activos = len(estado_estrategia.get('posiciones_activas', {}))
                if n_activos > 0:
                    peso_individual = 1.0 / n_activos
                    for activo in estado_estrategia['posiciones_activas']:
                        if activo in pesos:
                            pesos[activo] = peso_individual
            
            return pesos, estado_estrategia
        
        print(f"🎯 Estrategia Contrarian configurada:")
        print(f"   • Top perdedores: {top_n}")
        print(f"   • Umbral drawdown: {umbral_drawdown:.0%}")
        print(f"   • Umbral RSI: {umbral_rsi}")
        print(f"   • Holding period: {holding_meses} meses")
        print(f"   • Cash ticker: {cash_ticker or 'NINGUNO'}")
        print(f"   • Candidatos válidos: {len(candidatos)} activos")
        
        return generador_pesos