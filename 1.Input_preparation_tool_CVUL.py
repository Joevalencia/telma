# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:26:01 2024

@author: jvalenciaf001
"""

import pandas as pd
import warnings
from tqdm import tqdm
from babel.numbers import parse_decimal
import sys
import numpy as np
import glob
import os
import time
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
warnings.simplefilter(action='ignore', category=FutureWarning)

#ruta_py_file = r'C:\Users\jvalenciaf001\Desktop\PwC\Clienti\Generali\Progetto UL\Data\13. Cierre mensual UL\2023'
ruta_percurso = os.path.dirname(__file__)

start_time_all = time.time()

class MainWindow(QMainWindow):
    def __init__(self, file_type):
        super().__init__()
        self.file_type = file_type
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Seleccionar Archivos {self.file_type}")
        self.setGeometry(100, 100, 400, 200)

        self.button = QPushButton(f"Seleccionar Archivos {self.file_type}", self)
        self.button.setGeometry(50, 50, 300, 50)
        self.button.clicked.connect(self.selectFiles)

    def selectFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, 
                                                f"Seleccionar Archivos para cierre en {self.file_type}", 
                                                "", 
                                                f"{self.file_type} Files (*.{self.file_type});;All Files (*)")
        
        self.folder_paths = []  # List on which will be gather the path of txt files
        if files:
            for file in files:
                self.folder_paths.append(file)  # Appending paths to the list
            self.close()  # Closing dialog windows

if __name__ == "__main__":
    app = QApplication(sys.argv)

    txt_dialog = MainWindow("txt")
    txt_dialog.show()
    app.exec_()

    folder_paths_txt = txt_dialog.folder_paths

    xlsx_dialog = MainWindow("xlsx")
    xlsx_dialog.show()
    app.exec_()

    folder_paths_xlsx = xlsx_dialog.folder_paths



data_converted_folder = "data_converted_CVUL"
ruta_carpeta = os.path.join(os.path.dirname(folder_paths_txt[0]), data_converted_folder)  


if not os.path.exists(ruta_carpeta):
    #shutil.rmtree(ruta_carpeta)
    os.makedirs(ruta_carpeta)

## Folder names XLSX
folder_names_xlsx = []

for path in folder_paths_xlsx:
    file_name_with_extension = os.path.basename(path)  # Obtiene el nombre del archivo con extensión
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    # Verifica que la extensión sea '.XLSX' antes de agregarlo a la lista
    if file_extension.upper() == '.XLSX':
        folder_names_xlsx.append(file_name)


## Folder names TXT
folder_names_txt = []

for path in folder_paths_txt:
    file_name_with_extension = os.path.basename(path)  # Obtiene el nombre del archivo con extensión
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    # Verifica que la extensión sea '.XLSX' antes de agregarlo a la lista
    if file_extension.upper() == '.TXT':
        folder_names_txt.append(file_name)


# Percurso de la cabecera 
#folder_paths_xlsx= r'C:\Users\jvalenciaf001\Desktop\PwC\Clienti\Generali\Progetto UL\Data\13. Cierre mensual UL\Headers_mapping.xlsx'

folder_paths_xlsx = str(folder_paths_xlsx)[2:-2]

mapping_xlsx = pd.read_excel(folder_paths_xlsx, sheet_name=None)

dictionary_header = {}  # es el dict que contiene todas las pestañas con las cabeceras

for n, df in mapping_xlsx.items():
    dictionary_header[n] = df
    

cvul_trimestrales = {}

# Ruta donde se guardarán los archivos Feather
#ruta_carpeta = "data_converted_folder"

for ruta in tqdm(folder_paths_txt, desc='Leyendo, limpiando y exportando archivos TXT de CVUL en formato feather y CSV'):

    def replace_and_convert(value):
        if isinstance(value, str):
            value = value.replace('.', '').replace(',', '.')
        return float(value)
    

    nombre_sin_extension = os.path.splitext(os.path.basename(ruta))[0]
    if nombre_sin_extension.startswith("CVUL"):
        try:
            df = pd.read_table(ruta,
                               delim_whitespace=True, skiprows=5,
                               header=None, low_memory=True, dtype=str).iloc[:-6, :]

            df.iloc[:, 3:] = df.iloc[:, 3:].applymap(replace_and_convert)
            cvul_trimestrales[nombre_sin_extension] = df
            for key, df in cvul_trimestrales.items():
                cvul_trimestrales[key].columns = dictionary_header["CVUL"][key].T.loc[1:]

            for key, df in cvul_trimestrales.items():
                
                
                
                # Generar la ruta del archivo Feather utilizando el nombre de la clave
                path_feather_file = os.path.join(ruta_carpeta, f'{key}.feather')
                path_xlsx_file = os.path.join(ruta_carpeta, f'{key}.csv')

                # Eliminar archivo Feather existente si existe
                if os.path.exists(path_feather_file):
                    os.remove(path_feather_file)
                    os.remove(path_xlsx_file)

                # Guardar el DataFrame como archivo Feather
                df['POLIZA'] = pd.to_numeric(df['POLIZA'])
                
                df.to_feather(path_feather_file)
                df_no_comm = df.copy()
                #df.to_csv(path_xlsx_file)
                
                
                def replace_and_convert_inverse(value):
                    if isinstance(value, str):
                        value = value.replace('.',',')
                    return str(value)
                
                
                df_no_comm.iloc[:, 3:] = df_no_comm.iloc[:, 3:].applymap(replace_and_convert_inverse)
                df_no_comm.to_csv(path_xlsx_file)
                
        except Exception as e:
            print(f'\nFalta el fichero {ruta[-12:]} debido a: {e}')


###########################################################################################
######################### FIN EXPORTACION #################################################
###########################################################################################















