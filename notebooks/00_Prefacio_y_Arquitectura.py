#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import sys
import csv
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
import numpy as np

# --- 1. Instalación automática de dependencias ---
try:
    import yfinance as yf
    from sqlalchemy import create_engine
except ImportError:
    print("Instalando dependencias necesarias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yfinance", "sqlalchemy"])
    import yfinance as yf
    from sqlalchemy import create_engine


class EntornoImportacion:
    FUENTES_AGRESIVAS = {'yahoo', 'investing'}

    def __init__(self, diccionario_datos: Dict, fecha_inicio: str = "2010-01-01", fecha_fin: Optional[str] = None, dir_base: str = "."):
        if not diccionario_datos or not isinstance(diccionario_datos, dict):
            raise ValueError("Se debe aportar un 'diccionario_datos' válido en la invocación.")
            
        self.fecha_inicio = pd.to_datetime(fecha_inicio)
        self.fecha_fin = pd.to_datetime(fecha_fin) if fecha_fin else None

        self.dir_datos = Path(dir_base) / "Datos_fondos_csv"
        self.dir_datos.mkdir(parents=True, exist_ok=True)

        self.ORDEN_PRIORIDAD_FUENTE = ['gestora', 'r4', 'myinvestor', 'investing', 'yahoo']
        self.dirs_fuentes: Dict[str, Path] = {}
        for fuente in self.ORDEN_PRIORIDAD_FUENTE:
            carpeta = Path(dir_base) / f"datos_fi_{fuente}"
            carpeta.mkdir(parents=True, exist_ok=True)
            self.dirs_fuentes[fuente] = carpeta

        self.dir_backup = self.dir_datos / "_originales"
        self.dir_backup.mkdir(parents=True, exist_ok=True)

        self.ruta_db = self.dir_datos / "san_database.db"
        self.db_engine = create_engine(f"sqlite:///{self.ruta_db}", echo=False)

        self.valores_seleccionados = self._procesar_diccionario(diccionario_datos)
        self.datos_cargados: Dict[str, pd.DataFrame] = {}
        self.fuente_datos: Dict[str, str] = {}

        self._imprimir_resumen()

        # --- NUEVA ESTRUCTURA PARA ESTRATEGIA E INFORMES ---
        self.dir_outputs = Path(dir_base) / "outputs"
        self.dir_backtest = self.dir_outputs / "backtest"
        self.dir_figures = self.dir_outputs / "figures"
        self.dir_figures_png = self.dir_figures / "png"
        self.dir_figures_pdf = self.dir_figures / "pdf"
        self.dir_reports = self.dir_outputs / "reports"
        self.dir_reports_pdf = self.dir_reports / "pdf"
        self.dir_logs = Path(dir_base) / "logs"

        # Crear todas las carpetas de golpe
        for d in [self.dir_backtest, self.dir_figures_png, self.dir_figures_pdf, 
                  self.dir_reports_pdf, self.dir_logs]:
            d.mkdir(parents=True, exist_ok=True)
            
    def _procesar_diccionario(self, diccionario_datos: Dict) -> pd.DataFrame:
        datos_planos = []
        for categoria, fondos in diccionario_datos.items():
            for nombre, info in fondos.items():
                if isinstance(info, dict) and 'ISIN' in info and 'ticker' in info:
                    datos_planos.append({
                        'categoria': categoria,
                        'nombre': nombre,
                        'ISIN': str(info['ISIN']).strip(),
                        'ticker': str(info['ticker']).strip()
                    })
        return pd.DataFrame(datos_planos)

    def _imprimir_resumen(self):
        n_valores = len(self.valores_seleccionados)
        print("\n" + "═" * 55)
        print("  🚀 CONFIGURACIÓN ENTORNO COMPLETADA")
        print("═" * 55)
        print(f"  📊 Nº de valores en diccionario : {n_valores}")
        print(f"  📅 Rango de fechas análisis     : {self.fecha_inicio.strftime('%Y-%m-%d')} al ({self.fecha_fin.strftime('%Y-%m-%d') if self.fecha_fin else 'Actualidad'})")
        print(f"  📁 Ruta datos normalizados      : {self.dir_datos.resolve()}")
        print(f"  📥 Carpetas de entrada por fuente:")
        for fuente, carpeta in self.dirs_fuentes.items():
            print(f"     · {fuente:<11} -> {carpeta.resolve()}")
        print("═" * 55 + "\n")

    def _prioridad_fuente(self, fuente: str) -> int:
        try:
            return self.ORDEN_PRIORIDAD_FUENTE.index(fuente)
        except ValueError:
            return len(self.ORDEN_PRIORIDAD_FUENTE)

    def _limpiar_numero_universal(self, serie: pd.Series) -> pd.Series:
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

    def _parse_vliq_r4(self, filepath: Path) -> pd.DataFrame:
        rows = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) < 2:
                    continue
                for i in range(len(row) - 1):
                    date_str = row[i].strip()
                    if not re.match(r'\d{2}/\d{2}/\d{4}', date_str):
                        continue
                    val_str = row[i + 1].strip()
                    if '|' in val_str:
                        val_str = val_str.replace('|', '').replace(' ', '')
                    else:
                        val_str = re.sub(r'[^0-9.,-]', '', val_str)
                        if ',' in val_str and '.' in val_str:
                            val_str = val_str.replace('.', '').replace(',', '.')
                        elif ',' in val_str:
                            val_str = val_str.replace(',', '.')
                    try:
                        date = pd.to_datetime(date_str, format='%d/%m/%Y')
                        val = float(val_str)
                        rows.append((date, val))
                        break
                    except ValueError:
                        continue
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows, columns=['Date', 'Close']).set_index('Date')
        df = df[~df.index.duplicated(keep='last')].sort_index()
        df['Open'] = df['High'] = df['Low'] = df['Close']
        df['Volume'] = 0.0
        return df

    def _load_csv_robusto(self, filepath: Path) -> pd.DataFrame:
        filepath = Path(filepath)
        for sep in [',', ';', '\t']:
            for enc in ['utf-8', 'latin-1']:
                try:
                    df = pd.read_csv(filepath, sep=sep, encoding=enc, dtype=str, on_bad_lines='skip', engine='c')
                    if len(df.columns) > 1:
                        date_col = next((c for c in df.columns if re.search(r'date|fecha', c, re.I)), df.columns[0])
                        df[date_col] = df[date_col].astype(str).str.replace(';', ' ').str.split(' ').str[0].str.strip()
                        df[date_col] = pd.to_datetime(df[date_col], errors='coerce', format='mixed', dayfirst=True)
                        df = df.dropna(subset=[date_col]).set_index(date_col).sort_index()

                        close_col = next((c for c in df.columns if re.search(r'close|nav|valor|precio|ultimo|último|adj close', c, re.I)), df.columns[1])
                        if close_col != 'Close':
                            df.rename(columns={close_col: 'Close'}, inplace=True)

                        df['Close'] = self._limpiar_numero_universal(df['Close'])
                        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
                        df = df.dropna(subset=['Close'])

                        if not df.empty:
                            for col in ['Open', 'High', 'Low']:
                                if col not in df.columns:
                                    df[col] = df['Close']
                            if 'Volume' not in df.columns:
                                df['Volume'] = 0.0
                            
                            # Acotar por rango de fechas si procede
                            if self.fecha_inicio is not None:
                                df = df[df.index >= self.fecha_inicio]
                            if self.fecha_fin is not None:
                                df = df[df.index <= self.fecha_fin]

                            return df[['Open', 'High', 'Low', 'Close', 'Volume']]
                except Exception:
                    continue

        df_r4 = self._parse_vliq_r4(filepath)
        if not df_r4.empty:
            if self.fecha_inicio is not None:
                df_r4 = df_r4[df_r4.index >= self.fecha_inicio]
            if self.fecha_fin is not None:
                df_r4 = df_r4[df_r4.index <= self.fecha_fin]
        return df_r4

    def descargar_y_cargar_precios(self, forzar_descarga: bool = False):
        print(f"{'=' * 55}\n🔄 Modo: {'Forzar descarga (Yahoo)' if forzar_descarga else 'Cargar local'}\n{'=' * 55}\n")
        for _, row in self.valores_seleccionados.iterrows():
            isin, ticker = row['ISIN'], row['ticker']
            if not ticker:
                continue
            ruta_csv = self.dir_datos / f"{isin}.csv"
            fuente_descarga = None
            
            if not forzar_descarga and ruta_csv.exists():
                df = self._load_csv_robusto(ruta_csv)
            else:
                try:
                    df_yf = yf.download(
                        ticker, 
                        start=self.fecha_inicio.strftime('%Y-%m-%d'), 
                        end=self.fecha_fin.strftime('%Y-%m-%d') if self.fecha_fin else None, 
                        progress=False, 
                        auto_adjust=True
                    )
                    if df_yf.empty:
                        continue
                    if isinstance(df_yf.columns, pd.MultiIndex):
                        df_yf.columns = df_yf.columns.get_level_values(0)
                    df_yf.index = pd.to_datetime(df_yf.index)
                    df_yf.index.name = "Date"
                    if "Close" not in df_yf.columns and "Adj Close" in df_yf.columns:
                        df_yf.rename(columns={"Adj Close": "Close"}, inplace=True)
                    df_yf.to_csv(ruta_csv)
                    df = df_yf
                    fuente_descarga = 'yahoo'
                except Exception:
                    continue

            if not df.empty and "Close" in df.columns:
                df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
                df.dropna(subset=["Close"], inplace=True)
                self.datos_cargados[isin] = df
                if fuente_descarga:
                    self.fuente_datos[isin] = fuente_descarga
                elif isin not in self.fuente_datos:
                    self.fuente_datos[isin] = 'yahoo'

    def importar_csv_externos(self):
        codigos_sin_isin = {'EP2', 'F1467'}
        total_importados = 0
        conflictos = []

        for fuente in self.ORDEN_PRIORIDAD_FUENTE:
            carpeta = self.dirs_fuentes[fuente]
            archivos = list(carpeta.glob('*.csv'))
            if not archivos:
                continue

            print(f"\n{'='*55}\n📥 IMPORTANDO '{fuente.upper()}' ({len(archivos)}) desde {carpeta.name}\n{'='*55}")
            for f in archivos:
                stem = f.stem.replace('vliq_', '').strip()
                for sufijo in ('_r4', '_investing', '_myinvestor', '_yahoo', '_gestora'):
                    if stem.lower().endswith(sufijo):
                        stem = stem[: -len(sufijo)]
                        break
                while stem.lower().endswith('.csv'):
                    stem = stem[:-4]
                isin = stem

                es_isin_valido = bool(re.match(r'^[A-Z]{2}[A-Z0-9]{9}\d$', isin))
                es_codigo_conocido = isin in codigos_sin_isin
                if not es_isin_valido and not es_codigo_conocido:
                    continue

                if isin in self.fuente_datos:
                    fuente_existente = self.fuente_datos[isin]
                    if self._prioridad_fuente(fuente_existente) <= self._prioridad_fuente(fuente):
                        conflictos.append((isin, fuente_existente, fuente))
                        continue

                df = self._load_csv_robusto(f)
                if not df.empty:
                    backup_path = self.dir_backup / f"{fuente}_{f.name}"
                    if not backup_path.exists():
                        shutil.copy2(f, backup_path)
                    path_destino = self.dir_datos / f"{isin}.csv"
                    df.index.name = 'Date'
                    df.to_csv(path_destino, sep=',', decimal='.', date_format='%Y-%m-%d')
                    self.fuente_datos[isin] = fuente
                    total_importados += 1
                    print(f"✅ Guardado: {isin}.csv")

        print(f"\n{'='*55}\n✅ {total_importados} ficheros importados a '{self.dir_datos.name}'.")
        if conflictos:
            print(f"⚠️ {len(conflictos)} conflicto(s) de ISIN resueltos por prioridad.")
        print(f"{'='*55}\n")

    def normalizar_csv_directorio(self):
        csvs = sorted(self.dir_datos.glob("*.csv"))
        if not csvs:
            return
        print(f"\n{'=' * 55}\n🧹 NORMALIZANDO {len(csvs)} ARCHIVOS CSV\n{'=' * 55}\n")
        for ruta in csvs:
            if ruta.parent == self.dir_backup:
                continue
            df = self._load_csv_robusto(ruta)
            if not df.empty:
                df.index.name = 'Date'
                df = df[~df.index.duplicated(keep='last')].sort_index()
                df.to_csv(ruta, sep=',', decimal='.', date_format='%Y-%m-%d')

    def depurar_datos(self, umbral_generico: float = 0.15,
                        umbrales_por_categoria: Dict[str, float] = None,
                        min_dias_planos: int = 5, verbose: bool = True) -> pd.DataFrame:
        reporte = []
        mapeo_categoria = (self.valores_seleccionados.set_index('ISIN')['categoria'].to_dict()
                            if 'categoria' in self.valores_seleccionados.columns else {})

        for isin, df in self.datos_cargados.items():
            if 'Close' not in df.columns or df.empty:
                continue
            df = df.sort_index().copy()
            n_original = len(df)
            fuente = self.fuente_datos.get(isin, 'desconocida')
            es_agresiva = fuente in self.FUENTES_AGRESIVAS

            df['Close'] = df['Close'].replace(0, np.nan)

            racha = 0
            if es_agresiva:
                precios = df['Close'].ffill()
                for igual in precios.diff().eq(0).iloc[::-1]:
                    if igual:
                        racha += 1
                    else:
                        break
                if racha >= min_dias_planos:
                    df = df.loc[:df.index[-(racha + 1)]]
                else:
                    racha = 0

            categoria = mapeo_categoria.get(isin)
            umbral = (umbrales_por_categoria or {}).get(categoria, umbral_generico)
            if not es_agresiva:
                umbral *= 1.5

            rets = df['Close'].pct_change()
            outliers = rets.abs() > umbral
            n_outliers = int(outliers.sum())
            if n_outliers:
                df.loc[outliers, 'Close'] = np.nan

            df['Close'] = df['Close'].interpolate(method='time').ffill().bfill()

            for col in ['Open', 'High', 'Low']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    if df[col].equals(df['Close']):
                        df[col] = df['Close']

            self.datos_cargados[isin] = df
            reporte.append({
                'ISIN': isin, 'fuente': fuente, 'categoria': categoria,
                'dias_originales': n_original, 'dias_finales': len(df),
                'cola_cortada': racha, 'outliers_corregidos': n_outliers,
                'umbral_usado': round(umbral, 4)
            })

        reporte_df = pd.DataFrame(reporte)
        if verbose and not reporte_df.empty:
            print("\n" + "=" * 55)
            print("🧹 LIMPIEZA PROFUNDA — INFORME")
            print("=" * 55)
            print(reporte_df.to_string(index=False))
            print("=" * 55 + "\n")
        return reporte_df

    def seleccionar_activos(self) -> List[str]:
        csvs_disponibles = sorted(self.dir_datos.glob("*.csv"))
        isins_disponibles = [p.stem for p in csvs_disponibles]
        if not isins_disponibles:
            return []
        mapeo_info = self.valores_seleccionados.set_index('ISIN')['nombre'].to_dict()
        for i, isin in enumerate(isins_disponibles, 1):
            print(f"   {i:>2}. {mapeo_info.get(isin, 'Externo')} — ISIN: {isin}")
        sel = input("\nNúmeros separados por coma o 'todos': ").strip()
        if sel.lower() == 'todos':
            return isins_disponibles
        try:
            return [isins_disponibles[int(x) - 1] for x in sel.split(',')]
        except Exception:
            return []

    def cargar_seleccion(self, isins: List[str]):
        for isin in isins:
            df = self._load_csv_robusto(self.dir_datos / f"{isin}.csv")
            if not df.empty:
                self.datos_cargados[isin] = df

    def menu(self):
        while True:
            print("\n" + "=" * 55)
            print(" SISTEMA: IMPORTAR · NORMALIZAR · DEPURAR · SELECCIONAR")
            print("=" * 55)
            print("1. Descargar/Actualizar cotizaciones (Yahoo Finance)")
            print("2. Importar CSVs por fuente (r4, myinvestor, etc.)")
            print("3. Normalizar CSVs del directorio")
            print("4. Seleccionar y cargar activos en memoria")
            print("5. Depurar datos en memoria")
            print("6. Salir")
            print("=" * 55)

            opcion = input("Selecciona una opción (1-6): ").strip()

            if opcion == '1':
                self.descargar_y_cargar_precios(input("¿Forzar? (s/n): ").lower() == 's')
            elif opcion == '2':
                self.importar_csv_externos()
            elif opcion == '3':
                self.normalizar_csv_directorio()
            elif opcion == '4':
                isins = self.seleccionar_activos()
                if isins:
                    self.cargar_seleccion(isins)
            elif opcion == '5':
                self.depurar_datos()
            elif opcion == '6':
                print("Cerrando sistema.")
                break
            else:
                print("❌ Opción no válida.")

            if opcion != '6':
                input("\n✅ Tarea finalizada. Presiona Enter para continuar...")


# mi_diccionario_fondos = {
#     "Fondos indexados": {
#         "Vanguard Global Stock Index Fund EUR Acc": {"ISIN": "IE00B03HD191", "ticker": "0P00000WLG.F"},
#         "Fidelity S&P 500 Index Fund": {"ISIN": "IE00BYX5MS15", "ticker": "0P0001CJH0"},
#         "Vanguard Emerging Markets Stock Index Inv EUR Acc": {"ISIN": "IE0031786696", "ticker": "0P00012I6A.F"},
#         "Amundi Core Euro Govt Bd Etf Ae-C": {"ISIN": "LU1437018598", "ticker": "LU1437018598.SG"}
#     },
#     "Renta variable": {
#         "Renta 4 Europa Acciones, Fi": {"ISIN": "ES0173322001", "ticker": "0P0000M5GJ.F"},
#         "Renta 4 Global Acciones, Fi Clase R": {"ISIN": "ES0173128002", "ticker": "0P00016DRZ.F"},
#         "Vanguard Global Small-Cap Index Fund EUR Dist": {"ISIN": "IE00BDCXSH02", "ticker": "0P0001CXIY.F"},
#         "Vanguard Emerging Markets Stock Index Fund EUR Acc": {"ISIN": "IE0031786142", "ticker": "0P000060MS.F"},
#         "Vanguard Glb Small-Cp Idx € Acc": {"ISIN": "IE00B42W4L06", "ticker": "0P0000XR9M.F"}
#     },
#     "Renta fija/Otros": {
#         "Vanguard Global Bond Index EUR Hedged Acc": {"ISIN": "IE00B18GC888", "ticker": "0P00012I69.F"},
#         "Vanguard Global Short-Term Bond EUR Hedged Acc": {"ISIN": "IE00BH65QP47", "ticker": "0P00012NJH.F"},
#         "Renta 4 Renta Fija Euro FI Clase A": {"ISIN": "ES0173319007", "ticker": "0P0001RCAQ.F"},
#         "Renta 4 Renta Fija 6 Meses, Fi": {"ISIN": "ES0128520006", "ticker": "0P0000KY8J.F"},
#         "Renta 4 Renta Fija, Fi Clase R": {"ISIN": "ES0176954008", "ticker": "0P0000YLAY.F"}
#     },
#     "Renta fija corto plazo": {
#         "Amundi Money Market Euro Short Term": {"ISIN": "LU1687465945", "ticker": "AMEA.PA"} 
#     },
#     "Renta fija medio plazo": {
#         "iShares Euro Govt Bond 3-5yr UCITS ETF": {"ISIN": "IE00BDBRDM35", "ticker": "IBGM"},
#         "Vanguard Euro Government Bond UCITS ETF": {"ISIN": "IE0007472990", "ticker": "0P00000RQE.F"}
#     },
#     "Renta fija largo plazo": {
#         "iShares Euro Govt Bond 15-30yr UCITS ETF": {"ISIN": "IE00B1DFXH74", "ticker": "IBGL"}
#     },
#     "Fondos monetarios": {
#         "RENTA 4 FONCUENTA AHORRO, F.I.": {"ISIN": "ES0173222003", "ticker": "0P00019MZZ.F"},
#         "Groupama Trèsorerie": {"ISIN": "FR0000989626", "ticker": "0P00000LRT.F"},
#         "AXA Trésor Court Terme C": {"ISIN": "FR0000447823", "ticker": "0P00000F24.F"}        
#     },
#     "Fondos ultra corto plazo": {
#         "DWS Euro Ultra Short Fixed": {"ISIN": "LU0080237943", "ticker": "DI4C.F"},
#         "Groupama Ultra Short Term Bond": {"ISIN": "FR0013346079", "ticker": "0P0001FSY0.F"},
#         "OstrumSRI Credit Ultra Short": {"ISIN": "FR001400CFA4", "ticker": "0P0001QKUD.F"},
#         "Amundi Ultra Short Term Bond": {"ISIN": "FR0011365212", "ticker": "0P0000XPCY.F"},
#         "Invesco Euro Ultra Short": {"ISIN": "LU0102737730", "ticker": "IUGF.F"}
#     },
#     "Fondos retorno absoluto": {
#         "JPMorgan Absolute Return Multi-Asset Fund": {"ISIN": "IE00B2S4RL16", "ticker": "0P0000Y6GY.F"} 
#     },
#     "Índices": {
#         "STOXX Europe 600": {"ISIN": "DE0002635307", "ticker": "EXSA.DE"},
#         "MSCI World": {"ISIN": "IE00B4L5Y983", "ticker": "URTH"},
#         "S&P 500": {"ISIN": "US78378X1072", "ticker": "^GSPC"},
#         "Ibex 35": {"ISIN": "ESI143420005", "ticker": "^IBEX"},
#         "iShares Euro Govt Bond 1-3yr UCITS ETF": {"ISIN": "IE00B4WXJJ64", "ticker": "IBGS"}
#     }
# }
# 

# In[2]:


# 1. Definimos el diccionario de valores (ejemplo con renta variable y monetarios)
mi_diccionario_fondos = {
    "Monetario": {
        "Renta 4 Renta Fija 6 Meses, Fi": {"ISIN": "ES0128520006", "ticker": "0P0000KY8J.F"},
        "Renta 4 Renta Fija, Fi Clase R": {"ISIN": "ES0176954008", "ticker": "0P0000YLAY.F"},
        "Vanguard Global Short-Term Bond EUR Hedged Acc": {"ISIN": "IE00BH65QP47", "ticker": "0P00012NJH.F"},
        "Vanguard Global Bond Index EUR Hedged Acc": {"ISIN": "IE00B18GC888", "ticker": "0P00012I69.F"},
        "DWS EO Ultra Short Fix.Income I": {"ISIN": "LU0080237943", "ticker": "DI4C.F"}
    },
    "Renta fija": {
        "Vanguard Euro Government Bond UCITS ETF": {"ISIN": "IE0007472990", "ticker": "VGEB"}
    },
    "Renta variable": {
        "Vanguard Global Stock Index Fund EUR Acc": {"ISIN": "IE00B03HD191", "ticker": "0P00000WLG.F"},
        "Vanguard Emerging Markets Stock Index Inv EUR Acc": {"ISIN": "IE0031786696", "ticker": "0P00012I6A.F"},
        "Vanguard Global Stock Index Inv EUR Acc": {"ISIN": "IE00B03HCZ61", "ticker": "0P00000RQC.F"},
        "Amundi MSCI Emerging Markets Swap UCITS ETF EUR Acc": {"ISIN": "LU1681045370", "ticker": "AEEM.PA"},
        "Renta Variable Global Small Caps": {"ISIN": "IE00B42W4L06", "ticker": "0P0000XR9M.F"},
        "Vanguard Emerging Markets Stock Index Fund EUR Acc": {"ISIN": "IE0031786142", "ticker": "0P000060MS.F"}
    }
}


# In[3]:


# 1. Importamos la clase desde el script externo
# (Asegúrate de cambiar "entorno_importacion_ve" por "entorno_importacion_v3" si es el nombre exacto del archivo)
#from entorno_importacion_ve import EntornoImportacion 



# 2. Invocamos la clase fijando el diccionario y el rango de fechas para el análisis
gestor = EntornoImportacion(
    diccionario_datos=mi_diccionario_fondos,
    fecha_inicio="2018-01-01",  # Fecha de inicio del análisis
    fecha_fin="2026-01-01",     # Fecha fin (opcional, si es None coge hasta hoy)
    dir_base="."                # Directorio base actual
) 


# ## Descargar cotizaciones directamente desde Yahoo Finance
# Respetando las fechas configuradas

# In[ ]:


gestor.descargar_y_cargar_precios(forzar_descarga=False)


# ## Importar ficheros CSV externos que tengas en tus carpetas (datos_fi_r4, datos_fi_myinvestor, etc.)

# In[ ]:


gestor.importar_csv_externos()


# ## Seleccionar interactivamente qué activos cargar en memoria

# In[ ]:


isins_seleccionados = gestor.seleccionar_activos()
gestor.cargar_seleccion(isins_seleccionados)


# ## Ejecutar la limpieza y depuración profunda (con informe detallado)

# In[ ]:


# Puedes definir umbrales personalizados por categoría si lo deseas
umbrales = {
    'MONETARIO': 0.02,
    'RENTA_VARIABLE': 0.15
}

reporte_limpieza = gestor.depurar_datos(
    umbrales_por_categoria=umbrales, 
    min_dias_planos=5
)


# ## lanzar el menú interactivo clásico por consola dentro del notebook
# Se cargane en Es un diccionario de Python donde la clave es el ISIN del activo (ej. 'IE00B4L5Y983') y el valor es un pd.DataFrame con la serie temporal de precios y volumen ya depurada y filtrada por el rango de fechas.

# In[8]:


gestor.menu()


# ## Acceso a los archivos seleccionados y cargados
# Los archivos seleccionados y cargados quedan almacenados en la memoria interna de la instancia de la clase a través del diccionario: 

# gestor.datos_cargados

# ## Ver qué activos hay cargados

# In[ ]:


print(list(gestor.datos_cargados.keys()))


# ## Acceder al DataFrame de un activo específico

# In[ ]:


df_fondo = gestor.datos_cargados['IE00B4L5Y983']
df_fondo.head()


# In[ ]:





# In[ ]:




