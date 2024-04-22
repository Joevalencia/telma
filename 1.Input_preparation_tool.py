# -*- coding: utf-8 -*-
"""
Proceso de creación códigos python para lectura de ficheros txt


- Prima apparizione della finestra di dialogo         
- Lanciata dopo aver premuto il pulsante "Lanzamiento cierre" nel xlsb

"""
import pandas as pd
import warnings
from tqdm import tqdm
from babel.numbers import parse_decimal
import sys
import numpy as np
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
warnings.simplefilter(action='ignore', category=FutureWarning)


# 0 -> FUL90
# 1 -> PATR
# 2 -> PRESACU
# 3 -> PRIE
# 4 -> ULRECARGOS
# 5 -> ULRECIBOS
# 6 -> ULRESCATES




#ruta_py_file = os.path.dirname(__file__)
#print(ruta_py_file) es C:\Users\jvalenciaf001\Desktop\PwC\Clienti\Generali\Progetto UL\Data\13. Cierre mensual UL\2023

ruta_py_file = r'C:\Users\jvalenciaf001\Desktop\PwC\Clienti\Generali\Progetto UL\Data\13. Cierre mensual UL\2023'

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

    # Resto del código

#   folder_paths_xlsx = MainWindow_xlsx().selectFiles()

data_converted_folder = "data_converted"
ruta_carpeta = os.path.join(os.path.dirname(folder_paths_txt[0]), data_converted_folder)  
if not os.path.exists(ruta_carpeta):
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

#######################################################################################################################
####  FINALIZZAZIONE E CHIUSURA DELLA FINESTRA DI DIALOGO
####  STEP DI DEFINIZIONE DELLE PATH COMPLETATO E DEFINIZIONE DELLE VARIABILI PORTATE A TERMINE
#######################################################################################################################


#####################################################################
###########  CARICAMENTO, PULIZIA ED EXPORTAZIONE DEI FILETTINI   ###
#####################################################################


folder_paths_xlsx = str(folder_paths_xlsx)[2:-2]

# for j in range(len(folder_paths_txt)):
#     folder_paths_txt[j] = folder_paths_txt[j][2:-2]

#folder_paths_txt = str(folder_paths_txt)[2:-2]
mapping_xlsx = pd.read_excel(folder_paths_xlsx, sheet_name=None)

dictionary_header = {}  # es el dict que contiene todas las pestañas con las cabeceras

for n, df in mapping_xlsx.items():
    dictionary_header[n] = df


###################################
###########    FUL90    ###########
###################################



def read_and_export_file(file_path, export_path, header_name):
   
    with tqdm(total=100, desc=f"Leyendo, limpiando y exportando {header_name}") as pbar:
               
        df = pd.read_table(file_path, delim_whitespace=True, 
                           low_memory=False, skiprows=2,
                           parse_dates=True)
        pbar.update(50)         

        # Exportar el archivo a formato feather
        df.columns = dictionary_header.get(header_name).T.iloc[0, 1:]
        # Cambio a NaN donde llenaba con C y P
        df['FONDO'] = df['FONDO'].replace(['C', 'P'], np.nan)
        df['VALORADO'] = pd.Series([np.nan if x is None else x for x in df.VALORADO])
        df['CTA_DES'] = pd.Series([np.nan if x is None else x for x in df.CTA_DES])
        df['GENERADO'] = pd.Series([np.nan if x is None else x for x in df.GENERADO])
        df['FMOVTO'] = pd.to_datetime(df.FMOVTO, dayfirst=True)
        df['FVALOR'] = pd.to_datetime(df.FVALOR, dayfirst=True)
        
        fech1 = str(input('\nDigitar a partir de que fecha de movimientos considerar (FMOVTO): Ejemplo 2023-01-01\n'))
        print('\n')
        print('Fecha de movimiento (FMOVTO) seleccionada:\n ', fech1)
        print('\n')
        df = df[df['FMOVTO'] >= fech1]
        # df_copy = df.copy()
        # no_import = df_copy[df_copy.PROMOV.isin(['RT', 'RP'])].query('RAZMOV == "VU"').query('IMPORT == "-"').POLIZA.unique() ## Numero di poliza que no tienen un importe numerico
        # print(f'Número de pólizas a partir del {fech1} en venta de unidades eliminadas que no tienen un importe númerico: ', str(len(no_import)))
        # print('\n')
        df['IMPORT'] = pd.to_numeric(df.IMPORT, errors='coerce')
        df = df.dropna()       
        
        df_no_mov = df[~df.duplicated(subset='IMPORT', keep=False)]
        df_no_mov = df_no_mov[df_no_mov.PROMOV.isin(['TT', 'TP'])]
        df_no_mov = df_no_mov[df_no_mov.RAZMOV.isin(['VU', 'CU'])]
        print(f'Número de pólizas a partir del {fech1} que no tienen un fondo de CU/VU destino: ', str(len(df_no_mov.POLIZA.unique())))
        #no_fondo = df[df.duplicated(subset='IMPORT', keep=False)]
        
        df['FMOVTO'] = pd.to_datetime(df['FMOVTO'])
        df = df.iloc[:, :-4]    
        
        df.to_feather(export_path)
        
        df_no_mov.to_csv(os.path.join(ruta_carpeta, 'FUL90_movimientos_no_fondo_destino.csv'))

        pbar.update(50) 
        

try:
    read_and_export_file(folder_paths_txt[0], os.path.join(ruta_carpeta, 'FUL90.feather'), 'FUL90')
except Exception:
    print('NO GENERACION Y EXPORTACIÓN DEL FICHERO FUL90')




###################################
###########    PATRMUL  ###########
###################################

def read_and_export_file_with_progress(file_path, export_path, header_name):

    with tqdm(total=100, desc=f"Leyendo, limpiando y exportando {header_name}") as pbar:
        
        
        # Funciones para limpiar el archivo
        def to_number_for_python(valore):
            try:
                return parse_decimal(valore, locale='es')
            except Exception:
                return valore
        
        def to_number_to_float(df):
            try:
                return pd.to_numeric(df)
            except Exception:
                return df
        
        #file = r'C:\Users\jvalenciaf001\Desktop\PwC\Clienti\2050\PATR0124.txt'
        #file = r'C:\Users\jvalenciaf001\Desktop\PwC\Clienti\Generali\Progetto UL\Data\13. Cierre mensual UL\2023\PATR1223.txt'
        data = pd.read_csv(file_path, sep=';', decimal= ',' , low_memory=False, header=None)
        pbar.update(50)  # Actualiza la barra de progreso después de leer el archivo
        ## Cleaning formatting
        data[[k for k in range(6, 14)]] = data[[k for k in range(6, 14)]].applymap(to_number_for_python)
        data[[21, 22, 27,30, 44]] = data[[21, 22, 27, 30, 44]].applymap(to_number_for_python)
        data[[k for k in range(15, 19)]] = data[[k for k in range(15, 19)]].applymap(to_number_for_python)
        
        ## Cleaning Deciminal
        data[[k for k in range(6, 14)]] = data[[k for k in range(6, 14)]].applymap(to_number_to_float)
        data[[k for k in range(15, 19)]] = data[[k for k in range(15, 19)]].applymap(to_number_to_float)
        data[[21, 22, 27, 30, 44]] = data[[21, 22, 27, 30, 44]].applymap(to_number_to_float)

        
        
        #df = pd.read_table(file_path, sep=';', decimal= ',' , low_memory=False, header=None)
        data.columns = dictionary_header.get("PATR").T.iloc[0, 1:]   

        
        data.to_feather(export_path)

        pbar.update(50)  

try:
    read_and_export_file_with_progress(folder_paths_txt[1], os.path.join(ruta_carpeta, 'PATRIMONIO_UL.feather'), 'PATRIMUL')
except Exception:
    print('NO GENERACION Y EXPORTACIÓN CORRECTA DE PATRIMONIO UL')

###################################
###########  PRESACU    ###########
###################################

# ####               REVISARRRRRR
# # Acordarse de hacer añadir cabecera y shiftar de 1 las filas del df.
# start_time = time.time()
# presacu = pd.read_table(folder_paths_txt[6],
#                         encoding='unicode-escape', 
#                         delim_whitespace=True)

# presacu_fil = pd.Series(np.ones((1,presacu.shape[1])).ravel()).T
# presacu = pd.concat([presacu_fil, presacu], ignore_index=True)
# presacu_cabecera = ["X"+str(i) for i in range(presacu_fil.shape[0])]
# end_time = time.time()
# elapsed_time = end_time -start_time
# print(f"Execution time for PRESACU: {elapsed_time} seconds")



def read_and_export_presacu(file_path, export_path):
    
    with tqdm(total =100, desc= 'Leyendo, limpiando y exportando PRESACU') as pbar:
        pbar.update(50)
        try: 
            
            presacu = pd.read_table(file_path,   encoding='unicode-escape',  delim_whitespace=True)
            presacu.columns = ["Columna"+str(i) for i in range(29)]
            
            presacu.to_feather(export_path)
            #presacu.to_feather(os.path.join(ruta_carpeta, 'PRESACU.feather'))
            
        
        except Exception:
            print('No hay fichero PRESACU')
        pbar.update(50)
        
try:
    read_and_export_presacu(folder_paths_txt[2], os.path.join(ruta_carpeta, 'PRESACU.feather'))
    
except Exception:
    print('\nNO CREACIÓN Y EXPORTACIÓN DE FICHERO PRESACU')
###################################
###########  PRIE    ##############
###################################


def read_and_export_file_with_progress(file_path, export_path, header_name):
    
    with tqdm(total=100, desc=f"Leyendo, limpiando y exportando {header_name}") as pbar:
        def to_number_for_python(valore):
            try:
                return parse_decimal(valore, locale='es')
            except Exception:
                return valore
    
        try: 
            # Lee el archivo
            df = pd.read_table(file_path, sep=";", header=None)
            df.columns = dictionary_header.get(header_name).T.iloc[0, 1:]  
            df.iloc[:, 11:18] = df.iloc[:, 11:18].applymap(to_number_for_python)
            #df['F. VENCIMIENTO'] = pd.to_datetime(df['F. VENCIMIENTO'], )
            pbar.update(50)
            df.to_feather(export_path)

        except Exception:
            
            print(f'\nNo Se pudo Limpiar bien el archivo {header_name}')
        pbar.update(50)  

try:
    read_and_export_file_with_progress(folder_paths_txt[3], os.path.join(ruta_carpeta, 'PRIE.feather'), 'PRIE')
except Exception:
    print('\nNO CREACIÓN Y EXPORTACIÓN DE FICHERO PRIE')




###################################
###########  ULRE    ##############
###################################

def read_and_export_ulrecargos(file_path, export_path, header_name):
    # Lee el archivo con tqdm para mostrar la barra de progreso
    with tqdm(total=100, desc=f"Leyendo, limpiando y exportando {header_name}") as pbar:
       
       

        # Lee el archivo
        try:
            df = pd.read_table(file_path, delim_whitespace=True, header=None)#.iloc[:, :116]
            df.iloc[:, 1:] = (df.iloc[:, 1:].replace(',', '.', regex=True).replace('%', '', 
                                                                         regex=True).replace('EUR', '', regex=True).astype(float))
            pbar.update(50)  # Actualiza la barra de progreso después de leer el archivo
            df.to_feather(export_path)
        except Exception:
            
            print(f'\nNo Se puedo Limpiar bien el archivo {header_name}') 
        

        pbar.update(50) 


try:
    read_and_export_ulrecargos(folder_paths_txt[4], os.path.join(ruta_carpeta, 'ULRECARGOS.feather'), 'ULRECARGOS')
except Exception:
    print('\nNO CREACIÓN Y EXPORTACIÓN CORRECTA DEL FICHERO UL RECARGOS')



# print(f"Execution time for ULRECIBOS: {elapsed_time} seconds")
def read_and_export_ulrecibos(file_path, export_path, header_name):
    # Lee el archivo con tqdm para mostrar la barra de progreso
    with tqdm(total=100, desc=f"Leyendo, limpiando y exportando {header_name}") as pbar:
        
        

        # Lee el archivo
        try: 
            # df = pd.read_table(file_path, delim_whitespace=True,
            #                skiprows=1)
            df = pd.read_csv(file_path).iloc[:, :116]
            pbar.update(50)  
            df.to_feather(export_path)
            pbar.update(50)  
        except Exception:
            print(f'\nNo se pudo guardar bien el archivo {header_name}')

        

try:
    read_and_export_ulrecibos(folder_paths_txt[5], os.path.join(ruta_carpeta, 'ULRECIBOS.feather'), 'ULRECIBOS')
except Exception:
    print('\nNO CREACIÓN Y EXPORTACIÓN DEL FICHERO UL RECIBOS')


# Acordarse de hacer añadir cabecera y shiftar de 1 las filas del df.

def read_and_export_ulrescates(file_path, export_path, header_name):
    
    with tqdm(total=100, desc=f"Leyendo, limpiando y exportando {header_name}") as pbar:
        
        

        try:
            df = pd.read_table(file_path, delim_whitespace=True)
            pbar.update(50)  # Actualiza la barra de progreso después de leer el archivo
            df.to_feather(export_path)
        except Exception:
            print(f'\nNo se puedo Cargar bien el archivo {header_name}')
        ## Poner
        

        pbar.update(50)  # Actualiza la barra de progreso después de exportar el archivo

       
try:
    read_and_export_ulrescates(folder_paths_txt[6], os.path.join(ruta_carpeta, 'ULRESCATES.feather'), 'ULRESCATES')
except Exception:
    print('\nNO CREACIÓN Y EXPORTACIÓN DEL FICHERO UL RESCATES')



end_time_all = time.time()
elapsed_time = end_time_all - start_time_all
print(f"\nTiempo total de ejecución para el modulo 1.Input_Preparation: {elapsed_time: .2f} segundos")




# encabezados = ['PRODUCTO',
#     "CESTA",
#     "CIA",
#     "RAMO",
#     "POLIZA",
#     "APLICACION",
#     "NPARTCINI",
#     "VALORPARTCINI",
#     "VALORPATRIMONIOINI",
#     "COMPRAUDS",
#     "APORTRESCATADAS",
#     "APORTGASTOS",
#     "APORTTRASPASOS",
#     "SINIESTROS",
#     "APORTRESOLUCIONES",
#     "AJUSTES",
#     "NPARTC",
#     "VALORPARTC",
#     "VALORPATRIMONIO",
#     "SEXO",
#     "FNACIMIENTO",
#     "PRIMASPAGADAS",
#     "PRIMASRESCATADAS",
#     "FANULACION",
#     "CAUSAANUL",
#     "FVTO",
#     "GTOG1",
#     "GTOG2",
#     "GTOGT",
#     "GTOGC",
#     "GTOGR",
#     "GTOGP",
#     "GTOGS",
#     "FEFECTO",
#     "FSUSPENSION",
#     "DURACION",
#     "TIPOCRECPRIMA",
#     "%CRECPRIMA",
#     "INTE",
#     "TABLAMORT",
#     "CARTERAACT",
#     "CODAGEXT",
#     "CODSUC",
#     "CANAL",
#     "CAPFALL",
#     "RAMO CONT",
#     "Garantía Fallecimiento",
#     "X1"
# ]




