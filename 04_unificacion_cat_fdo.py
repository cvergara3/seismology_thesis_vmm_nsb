# Se debe ejecutar con la versión de pandas 1.4.2
#%%
import pandas as pd
import numpy as np
import os
import shutil
from geopy.distance import geodesic
from sklearn.neighbors import KDTree
from tqdm import tqdm

ruta = r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\resultados_unificacion'
ruta_destino = r'E:\RESULTADOS SISMOTECTONICA\2021_12\Phasenet Picks'
carpeta1 = r'E:\RESULTADOS SISMOTECTONICA\2021_12\merged_2021_12.csv'

df_cat = pd.read_csv('Catalogo Final Tesis.csv')

def unificacion (nombre_archivo):
    
    df_fdo = pd.read_csv(nombre_archivo)

    df_fdo['phase_time'] = pd.to_datetime(df_fdo['phase_time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_fdo['begin_time'] = pd.to_datetime(df_fdo['begin_time'], format='%Y-%m-%d %H:%M:%S.%f')
    df_fdo = df_fdo.sort_values(by=['phase_time'], ascending=True)

    df_cat['FECHA'] = pd.to_datetime(df_cat['FECHA'])

    # modificar dependiendo del delta de tiempo a utilizar
    rango1 = pd.Timedelta(seconds=10)
    rango2 = pd.Timedelta(seconds=60)
    df_cat['Fecha_Inicio'] = df_cat['FECHA'] - rango1
    df_cat['Fecha_Final'] = df_cat['FECHA'] + rango2

    filas_a_unir = []

    # obtener los índices de las filas de df1 que están dentro del rango de fechas de df2
    mask = (df_fdo['phase_time'].values[:, None] >= df_cat['Fecha_Inicio'].values) & (df_fdo['phase_time'].values[:, None] <= df_cat['Fecha_Final'].values)

    # obtener los índices de las filas de df2 que contienen las fechas en df1
    indices_df2 = np.nonzero(mask.any(axis=0))[0]

    # obtener las filas de df1 que están dentro del rango de fechas de df2 y unir con las filas correspondientes de df2
    for idx in indices_df2:
        filas_a_unir.append(pd.concat([df_fdo[mask[:, idx]].reset_index(drop=True), df_cat.iloc[[idx]].reset_index(drop=True)], axis=1))

    # verificar si hay filas a unir
    if not filas_a_unir:
        print(f"No hay filas a unir para {nombre_archivo}. Se pasa al siguiente archivo.")
        return
    
    # unir filas
    df_unido = pd.concat(filas_a_unir, axis=0, ignore_index=True)
    df_unido = df_unido.sort_values(by=['phase_time'], ascending=True)
    df_unido = df_unido.fillna(method='ffill')

    # calcular la diferencia en segundos
    df_unido['dif_segundos'] = abs((df_unido['phase_time'] - df_unido['FECHA']).dt.total_seconds())

    # crear dataframe vacío para almacenar los resultados
    df_resultado = pd.DataFrame(columns=['ID_CAVE', 'phase_type', 'dif_segundos'])

    # recorrer filas del dataframe original
    for idx, fila in df_unido.iterrows():
        # obtener valor de ID de la fila actual
        id_actual = fila['ID_CAVE']

        # filtrar filas con el mismo ID
        df_id = df_unido[df_unido['ID_CAVE'] == id_actual]

        # si solo hay una fila con ese ID, agregarla al resultado sin modificar
        if len(df_id) == 1:
            df_resultado = df_resultado.append(fila, ignore_index=True)
        else:
            # si hay más de una fila con ese ID, continuar con la siguiente condición
            # filtrar filas con el mismo phase_type
            phase_type_actual = fila['phase_type']
            df_phase_type = df_id[df_id['phase_type'] == phase_type_actual]

            if len(df_phase_type) == 1:
                # si solo hay una fila con ese phase_type, agregarla al resultado sin modificar
                df_resultado = df_resultado.append(df_phase_type.iloc[0], ignore_index=True)
            else:
                # si hay más de una fila con ese phase_type, continuar con la siguiente condición
                # obtener fila con el menor valor en dif_segundos
                min_dif_segundos = df_phase_type['dif_segundos'].min()
                df_min = df_phase_type[df_phase_type['dif_segundos'] == min_dif_segundos]

                # agregar fila con el menor valor en dif_segundos al resultado
                df_resultado = df_resultado.append(df_min.iloc[0], ignore_index=True)

    df_resultado_2 = df_resultado.drop_duplicates().sort_values(by=['phase_time']).reset_index(drop=True)

    def remove_duplicates(group):
        if len(group) == 1:
            # si solo hay una fila en el grupo, devolver el grupo sin cambios
            return group
        elif len(group['phase_type'].unique()) == 1:
            # si solo hay un valor en la columna "phase_type", devolver el grupo sin cambios
            return group
        else:
            # si hay dos valores en la columna "phase_type", revisar las fechas
            p_rows = group[group['phase_type'] == 'P']
            s_rows = group[group['phase_type'] == 'S']
            if p_rows['phase_time'].max() > s_rows['phase_time'].min():
                # si la fecha de "phase_type"=="P" es mayor a la de "phase_type"=="S", dejar solo la fila de "phase_type"==P
                group = p_rows
            return group

    df_final = df_resultado_2.groupby('ID_CAVE').apply(remove_duplicates).sort_values(by=['phase_time'], ascending=True).reset_index(drop=True).drop_duplicates().reset_index(drop=True)
    df_final = df_final[['ID_CAVE', 'phase_type', 'CATAL', 'CLASIF', 'FECHA', 'phase_time', 'LAT', 'LONG',
           'MAGN', 'PROF', 'TIPO_MAGN', 'file_name',
           'phase_index', 'phase_score', 'station_id']]
    
    # guardar archivo de salida en la ubicación adecuada
    archivo_salida = 'unido_' + nombre_archivo.split('\\')[4] # Si es otro disco duro puede ser 4
    print (archivo_salida)
    ruta_salida = os.path.join(ruta, archivo_salida)
    df_final.to_csv(ruta_salida, index=False)

# crea una lista de nombres de archivo csv en la carpeta
nombres_archivos = os.listdir(ruta_destino)
nombres_archivos = [f for f in nombres_archivos if f.endswith('.csv')]

# itera sobre la lista de nombres de archivo y procesa cada archivo csv
for nombre_archivo in nombres_archivos:
    nombre_completo = os.path.join(ruta_destino, nombre_archivo)
    unificacion(nombre_completo)

# Lista para almacenar los DataFrames de cada archivo CSV
data_frames = []

# Recorre todos los archivos en la carpeta y carga cada archivo CSV en un DataFrame
for filename in os.listdir(ruta):
    if filename.endswith('.csv'):
        file_path = os.path.join(ruta, filename)
        df = pd.read_csv(file_path)
        data_frames.append(df)

# Combina todos los DataFrames en un solo DataFrame
merged_df = pd.concat(data_frames)

# Guarda el archivo combinado como un archivo CSV
merged_df.to_csv(carpeta1, index=False)

# Eliminar la carpeta existente
shutil.rmtree(ruta)

# Crear una nueva carpeta vacía con el mismo nombre
os.mkdir(ruta)

# %%
