from obspy import read
from obspy.clients.fdsn.mass_downloader.domain import RectangularDomain
from obspy.clients.fdsn.mass_downloader import Restrictions
from obspy.clients.fdsn.mass_downloader import RectangularDomain, \
    Restrictions, MassDownloader
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import URL_MAPPINGS
from obspy import UTCDateTime
from obspy import read
import obspy
import glob
from tqdm import tqdm
from obspy import read, Trace, Stream
import os
import pandas as pd
import numpy as np
import os

ruta1 = r'D:\RESULTADOS SISMOTECTONICA\2021_12\primera_parte'
ruta2 = r'D:\RESULTADOS SISMOTECTONICA\2021_12\segunda_parte'
# Los unificados guardarlos en la carpeta trimestral
output_directory = r'D:\RESULTADOS SISMOTECTONICA\2021_12\mseed Unificados'
ruta = r'D:\RESULTADOS SISMOTECTONICA\2017_12'

client = Client("http://sismo.sgc.gov.co:8080")
domain = RectangularDomain(minlatitude=4.3, maxlatitude=9.3,
                           minlongitude=-76, maxlongitude=-72)
restrict = Restrictions(
    starttime=UTCDateTime("2016-07-01T00:00:00"),
    endtime=UTCDateTime("2016-07-02T00:00:00"), network ='CM', reject_channels_with_gaps=False, chunklength_in_sec=86400)

mdl = MassDownloader(providers=[client])
mdl.download(domain, restrict, mseed_storage=ruta,
              stationxml_storage="stations_final")

# Directorio donde se guardarán los archivos unificados
if not os.path.exists(output_directory):
    os.mkdir(output_directory)  

#Iterar sobre todos los archivos en el directorio y subdirectorios
for root, dirs, files in os.walk(ruta1):
    # Crear un diccionario para almacenar los canales por día y estación
    data_dict = {}
    for file in tqdm(files, desc='Processing'):
        if file.endswith('.mseed'):
            try:
                # Leer el archivo y obtener la estación, fecha y hora de inicio
                st = read(os.path.join(root, file))
                station = st[0].stats.station
                date = st[0].stats.starttime.date

                # Si no existe una entrada en el diccionario para la estación y fecha, crear una
                if (station, date) not in data_dict:
                    data_dict[(station, date)] = Stream()

                # Agregar las trazas del archivo a la entrada correspondiente del diccionario
                for tr in st:
                    if tr.stats.station == station and tr.stats.starttime.date == date:
                        data_dict[(station, date)] += tr.copy()
            
            except Exception:
                continue
    
    # Escribir los archivos unificados para cada estación y fecha
    for key, value in data_dict.items():
        station, date = key
        output_filename = f'{station}_{date}.mseed'
        output_path = os.path.join(output_directory, output_filename)
        value.write(output_path, format='MSEED')

#Iterar sobre todos los archivos en el directorio y subdirectorios
for root, dirs, files in os.walk(ruta2):
    # Crear un diccionario para almacenar los canales por día y estación
    data_dict = {}
    for file in tqdm(files, desc='Processing'):
        if file.endswith('.mseed'):
            try:
                # Leer el archivo y obtener la estación, fecha y hora de inicio
                st = read(os.path.join(root, file))
                station = st[0].stats.station
                date = st[0].stats.starttime.date

                # Si no existe una entrada en el diccionario para la estación y fecha, crear una
                if (station, date) not in data_dict:
                    data_dict[(station, date)] = Stream()

                # Agregar las trazas del archivo a la entrada correspondiente del diccionario
                for tr in st:
                    if tr.stats.station == station and tr.stats.starttime.date == date:
                        data_dict[(station, date)] += tr.copy()
            
            except Exception:
                continue
    
    # Escribir los archivos unificados para cada estación y fecha
    for key, value in data_dict.items():
        station, date = key
        output_filename = f'{station}_{date}.mseed'
        output_path = os.path.join(output_directory, output_filename)
        value.write(output_path, format='MSEED')