'''

CODIGO PARA GENERACION DE EXTRACCIÓN DATOS EXCEL


'''

import pandas as pd
import warnings
from tqdm import tqdm
import sys
import shutil
import os
warnings.simplefilter(action='ignore', category=FutureWarning)



#ruta_script = r'C:\Users\jvalenciaf001\Desktop\PwC\Clienti\Generali\Progetto UL\Data\13. Cierre mensual UL\2023\data_converted' 
#\FUL90.feather'



# ######### DEFINICION De directiorios #####
ruta_script = os.path.dirname(__file__)
#print(ruta_script) es C:\Users\jvalenciaf001\Desktop\PwC\Clienti\Generali\Progetto UL\Data\13. Cierre mensual UL\2023

new_folder = "Resultado_cierre"

# Folder agregación | Acumulado y no acumulado
mes_no_acc_cu = 'Mensual CU'
mes_agg_cu = 'Mensual acumulado CU'
mes_no_acc_vu = 'Mensual VU'
mes_agg_vu = 'Mensual acumulado VU'


ruta_new_folder =  os.path.join(ruta_script, new_folder)
ruta_feather_files = os.path.join(ruta_script, "data_converted")

# Directorios  

try:
    shutil.rmtree(os.path.join(ruta_new_folder, mes_no_acc_cu))
    shutil.rmtree(os.path.join(ruta_new_folder, mes_agg_cu))
    shutil.rmtree(os.path.join(ruta_new_folder, mes_no_acc_vu))
    shutil.rmtree(os.path.join(ruta_new_folder, mes_agg_vu))
except:
    pass


# Compras
ruta_mes_no_acc_cu = os.path.join(ruta_new_folder, mes_no_acc_cu)
os.makedirs(ruta_mes_no_acc_cu)
ruta_mes_agg_cu = os.path.join(ruta_new_folder, mes_agg_cu)
os.makedirs(ruta_mes_agg_cu)

# Ventas
ruta_mes_no_acc_vu = os.path.join(ruta_new_folder, mes_no_acc_vu)
os.makedirs(ruta_mes_no_acc_vu)
ruta_mes_agg_vu = os.path.join(ruta_new_folder, mes_agg_vu)
os.makedirs(ruta_mes_agg_vu)


#### LECTURA de los Files en formato feather #####
#df = pd.read_feather(feather_file_path)
ful90_feather = "FUL90.feather"
ruta_ful90_feather = os.path.join(ruta_feather_files, ful90_feather)
#ruta_ful90_feather = rf"{ruta_feather_files}\{ful90_feather}"
#print(ruta_ful90_feather)


# Fichero Feather

print('Leyendo el FICHERO en formato feather para limpieza y agregación...')
df = pd.read_feather(ruta_ful90_feather)


print('Importación acabada.')
print('Definición de dictionarios python para exportación en EXCEL...')


# Diccionario vacío para almacenar los DataFrames por mes.
# Es decir habrán 12 matrices de los movimientos, cada una representa los movimientos en ese mes Mes_1 = ENERO, Mes_2 = FEBRERO.
df_por_mes = {}

for mes in range(1, 13):
    # Filtra el DataFrame original por el mes actual
    df_mes_actual = df[df['FMOVTO'].dt.month == mes]
    df_por_mes[f'Mes_{mes}'] = df_mes_actual
df.sort_values(by='FMOVTO')
df = df[df.CIA.isin(['G', '1', '5'])]
df_mov_2023 = df  ### df_mov_2023 contiene todos los movimiento del 2023
df_mov_2023 = df_mov_2023[df_mov_2023.CIA.isin(['G', '1', '5'])] #  Obtengo df G, 1, 5, movimientos 2023


# Diccionario para almacenar meses del año de modo acumulado
df_acumulado_por_mes = {}

for mes in range(1, 13):
    
    # Filtracion del DataFrame original hasta el mes actual
    df_hasta_mes = df[df['FMOVTO'].dt.month <= mes]
    df_acumulado_por_mes[f'Mes_{mes}'] = df_hasta_mes


print('Finalización de la creación de los diccionarios.')
print(f'Inicialiazación de la creación de archivos en formato EXCEL Mensual en la carpeta {mes_no_acc_cu}...')

def resumen_no_acc_cu(df, mes):
    
    filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['PU', 'PI',
                                                    'CA', 'EE', 
                                                'AE', 'EI'])].query('RAZMOV =="CU"').groupby(['PRODUCTO', 'PROMOV',
                                                                                              'FONDO']).agg({'IMPORT':'sum'}).reset_index()
                                                                                             
                                                                                             
                                                                                             
    print(f"\nExportando ficheros CSV de FUL90 en la carpeta {mes_no_acc_cu}.")
    filtro1.to_excel(ruta_mes_no_acc_cu+f"\\FUL90_resumen_{mes}.xlsx")
    sys.stdout.flush()
    

[resumen_no_acc_cu(df_por_mes, mes) for mes in tqdm(df_por_mes.keys())]


                                                                                            
#resumen_no_acc(df_por_mes, 'Mes_1')

print('Finalización de la creación de archivos en formato EXCEL Mensual COMPRAS.')
#########################################################################

print(f'Inicialización de la creación de archivos en formato EXCEL Mensual Acumulado en la carpeta {mes_agg_cu}...')


def resumen_agg_cu(df, mes):
    
    filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['PU', 'PI',
                                                    'CA', 'EE', 
                                                'AE', 'EI'])].query('RAZMOV =="CU"').groupby(['PRODUCTO', 'PROMOV',
                                                                                              'FONDO']).agg({'IMPORT':'sum'}).reset_index()
                                                                                             
                                                                                             
                                                                                             
    print(f"\nExportando ficheros CSV de FUL90 en la carpeta {mes_agg_cu}.")
    filtro1.to_excel(ruta_mes_agg_cu+f"\\FUL90_resumen_acumulado_{mes}.xlsx")
    sys.stdout.flush()
    
     
    
[resumen_agg_cu(df_acumulado_por_mes, mes) for mes in tqdm(df_acumulado_por_mes.keys())]
  

print('Finalización de la creación de archivos en formato EXCEL Mensual Acumulado COMPRAS. ')


#########################################################################
##                Fichero excel reporting Ventas                       ##
#########################################################################


print(f'Inicialización de la creación de archivos en formato EXCEL Mensual Acumulado en la carpeta {mes_no_acc_vu}...')

def resumen_no_acc_vu(df, mes):
    
    filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['RT', 'RP'])].query('RAZMOV == "VU"').groupby(['PRODUCTO', 'PROMOV',
                                                                                              'FONDO']).agg({'IMPORT':'sum'}).reset_index()
                                                                                             
                                                                                             
                                                                                             
    print(f"\nExportando ficheros CSV de FUL90 en la carpeta {mes_no_acc_vu}.")
    filtro1.to_excel(ruta_mes_no_acc_vu+f"\\FUL90_resumen_{mes}.xlsx")
    sys.stdout.flush()
    
[resumen_no_acc_vu(df_por_mes, mes) for mes in tqdm(df_por_mes.keys())]


print('Finalización de la creación de archivos en formato EXCEL Mensual VENTAS.')

#############################################################################################################################################


print(f'Inicialización de la creación de archivos en formato EXCEL Mensual Acumulado en la carpeta {mes_agg_vu}...')

def resumen_agg_vu(df, mes):
    
    filtro1 = df.get(mes)[df.get(mes).PROMOV.isin(['RT', 'RP'])].query('RAZMOV == "VU"').groupby(['PRODUCTO', 'PROMOV',
                                                                                              'FONDO']).agg({'IMPORT':'sum'}).reset_index()
                                                                                             
                                                                                             
                                                                                             
    print(f"\nExportando ficheros CSV de FUL90 en la carpeta {mes_agg_vu}.")
    filtro1.to_excel(ruta_mes_agg_vu+f"\\FUL90_resumen_{mes}.xlsx")
    sys.stdout.flush()
  
[resumen_agg_vu(df_acumulado_por_mes, mes) for mes in tqdm(df_acumulado_por_mes.keys())]

print('Finalización de la creación de archivos en formato EXCEL Mensual Acumulado VENTAS. ')





######################################################################### 
    
    
    
    
    
    
    
    
    