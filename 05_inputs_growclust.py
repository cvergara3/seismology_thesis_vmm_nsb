#%%
import pickle
import pandas as pd
from obspy import UTCDateTime
import glob

# carpeta = r'E:/RESULTADOS SISMOTECTONICA/merged/'
# archivos_csv = glob.glob(carpeta + '*.csv')

# datos_combinados = pd.DataFrame()

# for archivo in archivos_csv:
#     df = pd.read_csv(archivo)
#     datos_combinados = pd.concat([datos_combinados, df], ignore_index=True)

# datos_combinados.to_csv(carpeta + '00_merged_total.csv', index=False)
# %%
###################   PROCESAMIENTO ORIGINS   #######################
df = pd.read_csv(r'E:/RESULTADOS SISMOTECTONICA/merged/00_merged_total.csv')
# Escoger solo los que estan por fuera del nido
df = df[df['LONG']<=-73.5]
df = df.drop_duplicates(subset='ID_CAVE')
df['FECHA'] = pd.to_datetime(df['FECHA'])
df['FECHA_obspy'] = df['FECHA'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

origins_CAVE = {}
for index, row in df.iterrows():
    id_cave = row['ID_CAVE']
    fecha = row['FECHA_obspy']
    lat = row['LAT']
    long = row['LONG']
    prof = row['PROF']
    magn = row['MAGN']

    origins_CAVE[id_cave] = (fecha, lat, long, prof, magn, id_cave)

# Crear un nuevo diccionario con las llaves convertidas a enteros y los valores convertidos
new_origins_CAVE = {}

# Iterar a través del diccionario original y realizar la conversión de las llaves y los valores
for key, value in origins_CAVE.items():
    # Convertir la llave a int
    new_key = int(key)
    
    # Convertir los valores de la tupla a los tipos deseados
    new_value = (UTCDateTime(value[0]), *value[1:5], int(value[5]))
    
    # Agregar la nueva llave y valor al diccionario
    new_origins_CAVE[new_key] = new_value

with open(r'E:\RESULTADOS SISMOTECTONICA\CODIGO MF\ev_grad3D\cat_total_SN\origins.pkl', 'wb') as archivo_pkl:
    pickle.dump(new_origins_CAVE, archivo_pkl)

#%%
###################   PROCESAMIENTO PICKS   #######################
df = pd.read_csv(r'E:/RESULTADOS SISMOTECTONICA/merged/00_merged_total.csv')
df = df[df['LONG']<=-73.5]
df['phase_time'] = pd.to_datetime(df['phase_time'])
df['phase_time_obspy'] = df['phase_time'].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
# df['phase_time'] = pd.to_datetime(df['phase_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
# df['phase_time_obspy'] = df['phase_time'].apply(UTCDateTime)
df[['red', 'estacion']] = df['station_id'].str.split('.', n=1, expand=True)
df['estacion'] = df['estacion'].str.split('.').str[0]

picks_CAVE = {}

for _, row in df.iterrows():
    id_cave = row['ID_CAVE']
    phase_type = row['phase_type']
    red = row['red']
    station = row['estacion']
    fecha = row['phase_time_obspy']

    clave_compuesta = (red, station, phase_type)

    if id_cave not in picks_CAVE:
        picks_CAVE[id_cave] = {}

    picks_CAVE[id_cave][clave_compuesta] = fecha

# Crear un nuevo diccionario con claves de tipo int (sin decimales)
new_picks_CAVE = {}

# Iterar a través del diccionario original y realizar la conversión
for clave, subclaves in picks_CAVE.items():
    clave_sin_decimales = int(clave)
    nuevo_subclaves = {}
    for subclave, valor in subclaves.items():
        nuevo_valor = UTCDateTime(valor)
        nuevo_subclaves[subclave] = nuevo_valor
    new_picks_CAVE[clave_sin_decimales] = nuevo_subclaves

with open(r'E:\RESULTADOS SISMOTECTONICA\CODIGO MF\ev_grad3D\cat_total_SN\picks_eqs.pkl', 'wb') as archivo_pkl:
    pickle.dump(new_picks_CAVE, archivo_pkl)
# %%
###################   PROCESAMIENTO STATIONS   #######################
df = pd.read_csv(r'E:\2016\stlist.csv', delimiter=';')

stations_CAVE = {}

for index, row in df.iterrows():
    estacion = row['estacion']
    red = row['red']
    latitud = row['lat']
    longitud = row['long']

    clave_compuesta = (red, estacion)

    stations_CAVE[clave_compuesta] = (latitud, longitud)

with open(r'E:\RESULTADOS SISMOTECTONICA\CODIGO MF\ev_grad3D\cat_total_SN\stats.pkl', 'wb') as archivo_pkl:
    pickle.dump(stations_CAVE, archivo_pkl)
# %%
