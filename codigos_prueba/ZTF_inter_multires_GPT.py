import numpy as np
import pickle
import os
from pathlib import Path
from astropy.io import fits


class ZTFObservation:
    def __init__(self, oid, ra, dec, science_image, class_label, multires_images=None):
        self.oid = oid
        self.ra = ra
        self.dec = dec
        self.science_image = science_image
        self.class_label = class_label
        self.multires_images = multires_images or {}
        #dimensiones imagenes (5 niveles) (resoluciones)
        #reference_image
        #diff_

# Cargar dataset ZTF
ZTF_path = 'dataset_ZTF.pkl'
with open(ZTF_path, "rb") as f:
    data_ZTF = pickle.load(f)

# Ruta a archivos multiresolución
multires_path = 'multiresolution_fits_files'
archivos_multires = {j.stem: j for j in Path(multires_path).iterdir()}

# Crear diccionario final
dict_ZTF_multires = {}

for i in range(len(data_ZTF)):
    oid = data_ZTF['oid'].iloc[i]
    ra = data_ZTF['ra'].iloc[i]
    dec = data_ZTF['dec'].iloc[i]
    class_label = data_ZTF['class'].iloc[i]
    science_image = data_ZTF['science'].iloc[i]

    resoluciones_multires = {}
    
    if oid in archivos_multires:
        specific_multires = archivos_multires[oid]
        if specific_multires.suffix == '.fits':
            with fits.open(specific_multires) as hdul:
                header = hdul[0].header
                data = hdul[0].data
                cdelt1 = header.get('CDELT1', None)
                if data is not None and cdelt1 is not None:
                    resoluciones_multires[cdelt1] = data

    # Ordenar imágenes multiresolución por resolución
    resoluciones_multires = dict(sorted(resoluciones_multires.items(), key=lambda x: x[0]))

    # Crear y almacenar la observación
    observation = ZTFObservation(oid, ra, dec, science_image, class_label, resoluciones_multires)
    dict_ZTF_multires[oid] = observation




# Ruta donde guardar el archivo .pkl
output_path = 'diccionario_ZTF_multires.pkl'

# Contador para mostrar el progreso
total_observaciones = len(dict_ZTF_multires)  # Número total de observaciones en el diccionario

# Abrir el archivo en modo escritura binaria
with open(output_path, 'wb') as f:
    # Iterar sobre los elementos del diccionario y guardar
    for i, (oid, observation) in enumerate(dict_ZTF_multires.items()):
        # Serializar el diccionario y guardarlo en el archivo
        pickle.dump(dict_ZTF_multires, f)
        
        # Imprimir el progreso cada 10 elementos (puedes ajustar este valor)
        if (i + 1) % 10 == 0 or (i + 1) == total_observaciones:
            print(f"Guardado {i + 1} de {total_observaciones} observaciones...")

print(f"Diccionario guardado en: {output_path}")
