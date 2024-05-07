#%%
# Ejecutar con ambiente base. No con ambiente 'obspy'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#%%
df_sgc1 = pd.read_csv(r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\catalogos\SGC1_final.csv', encoding = 'latin-1', delimiter =';')
df_sgc2 = pd.read_csv(r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\catalogos\SGC2_final.csv', encoding = 'latin-1', delimiter =';')
df_isc = pd.read_csv(r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\catalogos\ISC_final.csv', encoding = 'latin-1', delimiter =';')
df_lbs = pd.read_csv(r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\catalogos\LBS_final.csv', encoding = 'latin-1', delimiter =';')
# %%
# Procesamiento SGC1
df_sgc1_final = df_sgc1[['FECHA', 'HORA', 'LAT', 'LONG', 'PROF', 'MAGN_ML', 'ID_CAVE']]

# Combinar las columnas de fecha y hora
df_sgc1_final['FECHA_HORA'] = pd.to_datetime(df_sgc1_final['FECHA'] + ' ' + df_sgc1_final['HORA'], format='%d/%m/%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')

# Renombrar las columnas
df_sgc1_final = df_sgc1_final.rename(columns={'MAGN_ML': 'MAGN'})
df_sgc1_final['TIPO_MAGN'] = 'Ml'
df_sgc1_final['CATAL'] = 'SGC1'

# Ordenar el DataFrame por la columna de fecha
df_sgc1_final = df_sgc1_final.sort_values(by='FECHA_HORA')
df_sgc1_final['CLASIF'] = ['Somero' if x<=50 else 'Profundo' for x in df_sgc1_final['PROF']]
df_sgc1_final = df_sgc1_final[['FECHA_HORA','HORA','LAT','LONG','PROF','MAGN','TIPO_MAGN','CLASIF','CATAL','ID_CAVE']]

# %%
# Procesamiento SGC2
df_sgc2_final = df_sgc2[['FECHA_HORA', 'HORA', 'LAT', 'LONG', 'PROF', 'MAGN', 'TIPO_MAGN', 'ID_CAVE']]
df_sgc2_final = df_sgc2_final.rename(columns={'FECHA_HORA': 'FECHA'})

# Combinar las columnas de fecha y hora
df_sgc2_final['FECHA_HORA'] = pd.to_datetime(df_sgc2_final['FECHA'] + ' ' + df_sgc2_final['HORA'], format='%d/%m/%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
df_sgc2_final['CATAL'] = 'SGC2'

# Ordenar el DataFrame por la columna de fecha
df_sgc2_final = df_sgc2_final.sort_values(by='FECHA_HORA')
df_sgc2_final['CLASIF'] = ['Somero' if x<=50 else 'Profundo' for x in df_sgc2_final['PROF']]
df_sgc2_final = df_sgc2_final[['FECHA_HORA','HORA','LAT','LONG','PROF','MAGN','TIPO_MAGN','CLASIF','CATAL','ID_CAVE']]

# %%
# Procesamiento LBS
df_lbs_final = df_lbs[['FECHA', 'HORA', 'LAT', 'LONG', 'PROF', 'MAGN', 'TIPO_MAGN', 'ID_CAVE']]

# Combinar las columnas de fecha y hora
df_lbs_final['FECHA_HORA'] = pd.to_datetime(df_lbs_final['FECHA'] + ' ' + df_lbs_final['HORA'], format='%d/%m/%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
df_lbs_final['CATAL'] = 'LBS'

# Ordenar el DataFrame por la columna de fecha
df_lbs_final = df_lbs_final.sort_values(by='FECHA_HORA')
df_lbs_final['CLASIF'] = ['Somero' if x<=50 else 'Profundo' for x in df_lbs_final['PROF']]
df_lbs_final = df_lbs_final[['FECHA_HORA','HORA','LAT','LONG','PROF','MAGN','TIPO_MAGN','CLASIF','CATAL','ID_CAVE']]

# %%
# Procesamiento ISC
df_isc_final = df_isc[['DATE', 'HORA', 'LAT', 'LONG', 'DEPTH', 'MAG', 'TYPE1', 'ID']]
df_isc_final = df_isc_final.rename(columns={'DATE': 'FECHA', 'DEPTH': 'PROF', 'MAG': 'MAGN', 'TYPE1': 'TIPO_MAGN', 'ID': 'ID_CAVE'})

# Combinar las columnas de fecha y hora
df_isc_final['FECHA_HORA'] = pd.to_datetime(df_isc_final['FECHA'] + ' ' + df_isc_final['HORA'], format='%d/%m/%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
df_isc_final['CATAL'] = 'ISC'

# Ordenar el DataFrame por la columna de fecha
df_isc_final = df_isc_final.sort_values(by='FECHA_HORA')
df_isc_final['CLASIF'] = ['Somero' if x<=50 else 'Profundo' for x in df_isc_final['PROF']]
df_isc_final = df_isc_final[['FECHA_HORA','HORA','LAT','LONG','PROF','MAGN','TIPO_MAGN','CLASIF','CATAL','ID_CAVE']]

# %%
# Catalogo final con duplicados
# Concatenar los DataFrames
df_parcial = pd.concat([df_sgc1_final, df_sgc2_final, df_lbs_final, df_isc_final])
df_parcial = df_parcial.reset_index(drop=True)
df_parcial['FECHA_HORA'] = pd.to_datetime(df_parcial['FECHA_HORA'])
df_parcial = df_parcial.sort_values('FECHA_HORA')
#df_parcial.to_csv(r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\Catalogo Final Tesis_con duplicados.csv', index=False) 
time_diff = df_parcial['FECHA_HORA'].diff()
mask = time_diff.dt.total_seconds() >= 120 #Se consideran duplicados si están dentro de 2 minutos de ventana

# Catalogo final sin duplicados
df_final = df_parcial[mask]
df_final = df_final.rename(columns={'FECHA_HORA': 'FECHA'})
#df_final.to_csv(r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\Catalogo Final Tesis.csv', index=False) 

####################### Marzo 2024
# Crear el DataFrame con los datos proporcionados
df = df_parcial

# Convertir la columna 'FECHA_HORA' a tipo datetime
df['FECHA_HORA'] = pd.to_datetime(df['FECHA_HORA'])

# Redondear los valores de 'FECHA_HORA' al minuto más cercano
df['FECHA_HORA_ROUND'] = df['FECHA_HORA'].dt.round('T')

# Encontrar los duplicados basados en 'FECHA_HORA_ROUND'
duplicates = df[df.duplicated(subset='FECHA_HORA_ROUND', keep=False)]

# Crear un índice único basado en los duplicados encontrados
duplicates['DUPLICATE_INDEX'] = duplicates.groupby('FECHA_HORA_ROUND').cumcount() + 1

# Usar pivot_table para combinar columnas hacia la derecha
combined_duplicates = duplicates.pivot_table(index='FECHA_HORA_ROUND', columns='DUPLICATE_INDEX', values=['LAT', 'LONG', 'PROF', 'MAGN', 'TIPO_MAGN', 'CLASIF', 'CATAL', 'ID_CAVE'], aggfunc='first')

# Eliminar el multi-índice en las columnas
combined_duplicates.columns = ['_'.join(map(str, col)) for col in combined_duplicates.columns]

combined_duplicates.to_csv('combined_duplicates.csv')
# %%
df['FECHA'] = pd.to_datetime(df['FECHA'])

# Extrae el año de la fecha
df['YEAR'] = df['FECHA'].dt.year

# Agrupa los datos por año y categoría y cuenta las frecuencias
frecuencias = df.groupby(['YEAR', 'CATAL']).size().reset_index(name='Frecuencia')
# %%
# Crea el histograma con barras apiladas
fig = go.Figure()

# Itera sobre cada categoría y crea una barra apilada correspondiente
for categoria in df['CATAL'].unique():
    data = frecuencias[frecuencias['CATAL'] == categoria]
    fig.add_trace(go.Bar(
        x=data['YEAR'],
        y=data['Frecuencia'],
        name=categoria
    ))

# Personaliza el histograma y el rango del eje x
fig.update_layout(
    title='Histograma de fechas por año y categoría',
    xaxis_title='Año',
    yaxis_title='Frecuencia',
    barmode='stack',  # Configura las barras apiladas
    xaxis=dict(
        tickmode='linear',
        dtick=1
    ),
    width=900  # Ajusta el ancho de la figura según tus necesidades
)

# Muestra el histograma
fig.show()
# %%
