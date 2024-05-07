import os
import shutil
import pandas as pd

# OJO: ELIMINAR ANTES DE CORRER LA INFORMACION QUE ESTA EN 'CSV' Y EN 'RESULTS'
output_directory = r'D:\RESULTADOS SISMOTECTONICA\2016_01\mseed Unificados'
ruta_destino = r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\PhaseNet\test_data\mseed'
nombre_salida = r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\PhaseNet\comandos.txt'
carpeta2 = r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\PhaseNet\test_data\csv'
output_directory2 = r'C:\Users\carlo\OneDrive\Documentos\CARLOS VERGARA\Python VSC\TESIS\results'
ruta_destino2 = r'D:\RESULTADOS SISMOTECTONICA\2016_01_libro\Phasenet Picks' 

# Eliminar carpeta existente en la ruta de destino
shutil.rmtree(ruta_destino)

# Copiar los archivos
shutil.copytree(output_directory, ruta_destino)

nombres_archivos = []
for archivo in os.listdir(output_directory):
    nombre_archivo, extension = os.path.splitext(archivo)
    if extension == ".mseed":
        nombres_archivos.append(nombre_archivo)

# Abrir el archivo en modo escritura
with open(nombre_salida, 'w') as archivo:
    # Recorrer la lista de nombres de archivos
    for nombre in nombres_archivos:
        # Construir el comando completo
        comando = "python PhaseNet/phasenet/predict.py --model=PhaseNet/model/190703-214543 --data_list=PhaseNet/test_data/csv/" + nombre + ".csv --data_dir=PhaseNet/test_data/mseed --format=mseed --result_fname=" + nombre + " --plot_figure"
        # Guardar el comando en el archivo
        archivo.write(comando + '\n')

# Iterar sobre los nombres de archivo y guardarlos en la carpeta "mis_archivos"
for nombre in nombres_archivos:
    data = {'fname': [nombre + ".mseed"]}
    df = pd.DataFrame(data)
    ruta_archivo = os.path.join(carpeta2, nombre + ".csv")
    df.to_csv(ruta_archivo, index=False)

with open(nombre_salida, 'r') as f:
    comandos = f.readlines()

for comando in comandos:
    comando = comando.strip()  # elimina los saltos de línea al final
    print(f'Ejecutando comando: {comando}')
    os.system(comando)

# Copiar los archivos
shutil.copytree(output_directory2, ruta_destino2)

# crea una lista de nombres de archivo csv en la carpeta
nombres_archivos = os.listdir(ruta_destino2)
nombres_archivos = [f for f in nombres_archivos if f.endswith('.csv')]