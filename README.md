# seismology_thesis_vmm_nsb
El presente repositorio integra los códigos de Python utilizados para el desarrollo del trabajo de grado titulado "SISMICIDAD E IMPLICACIONES SISMOTECTÓNICAS DE UNA ZONA DEL CENTRO – ORIENTE DE LA CUENCA DEL VALLE MEDIO DEL MAGDALENA (VMM) Y NIDO SÍSMICO DE BUCARAMANGA", así como los archivos de salida y resultados del proyecto de investigación con enfoque en la relocalización relativa de sismos. A continuación se explica el contenido de cada uno de los algoritmos, incluyendo PhaseNet y la geración de archivos de entrada para ejecutar GrowClust.

#### 01_procesamiento_catalogos.py
Este código se implementa para la unificación y eliminación de eventos duplicados entre catálogos del SGC y el ISC para la zona de estudio. Asimismo, se grafica un histograma del catálogo final por año y tipo de catálogo. La fuente de donde se descargó la información sismológica a nivel nacional es: http://bdrsnc.sgc.gov.co/paginas1/catalogo/index.php; y el catálogo internacional se descargó de: http://www.isc.ac.uk/iscbulletin/.

#### 02_descarga_unificacion.py
Se utilizó este código para la descarga masiva de formas de onda de todas las estaciones en la zona de estudio. Además, se agrupan los sismogramas en archivos independientes por estación y fecha. Los archivos finales son tipo .mseed. La fuente de información de donde se obtienen las formas de onda es: http://sismo.sgc.gov.co:8080/fdsnws/dataselect/1/builder. 

#### 03_comando_auto_phasenet.py
Este código corresponde a una modificación realizada al código original de PhaseNet, con el fin de poder ejecutar el algoritmo masivamente para cada uno de los archivos descargados y unificados de la fase 2. El algoritmo PhaseNet se tomó del siguiente repositorio de GitHub: https://github.com/AI4EPS/PhaseNet/blob/master/docs/README.md.

#### 04_unificacion_cat_fdo.py
El código permite la integración del catálogo final de sismicidad (Catalogo Final Tesis.csv en el presente repositorio) con los tiempos de arribo detectados automáticamente con PhaseNet. Se asignan ventanas de tiempo para poder amarrar ambas bases de datos y generar el catálogo de sismicidad input a GrowClust. El archivo final después de correr GrowClust corresponde a catalogo_reloc_total.csv en el presente repositorio).

#### 05_inputs_growclust.py
El código se subdivide en tres secciones: Procesamiento Origins, Procesamiento Picks y Procesamiento Stations. Se encarga de procesar los catálogos, encontrando pares de eventos cercanos detectados en estaciones en común, generar correlaciones cruzadas y sintetizar las estaciones sismológicas en formato .pkl. Estos archivos son el input para la ejecución final de GrowClust en Fortran.

Por último, se adjuntan en la carpeta 'Bases de datos' el catálogo unificado de sismicidad con información de sismos entre 1980 y 2023 en la zona de estudio (Valle Medio del Magdalena y Nido Sísmico de Bucaramanga) y el catálogo relocalizado (salida de GrowClust) con datos entre 2016 y 2021.
