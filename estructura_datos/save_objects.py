import numpy as np
import pickle
import pandas as pd
from pathlib import Path
import os
from astropy.io import fits
from clases import MMObject, MMobjects  # Importar las clases definidas en clases.py

# Paths
ZTF_path = 'dataset_ZTF.pkl'
multires_path = 'multires/multiresolution_fits_files'
output_pickle = 'MMobjects.pkl'

# Cargar el dataset de ZTF
print("Cargando el dataset de ZTF...")
with open(ZTF_path, "rb") as f:
    data_ZTF = pickle.load(f)

# Asegurar que sea un DataFrame
if not isinstance(data_ZTF, pd.DataFrame):
    data_ZTF = pd.DataFrame(data_ZTF)

print(f"Dataset cargado con {len(data_ZTF)} filas.")
print("Conteo de clases en el dataset:")
print(data_ZTF["class"].value_counts())

# Leer archivos de multiresolución
multires_folders = {folder.name: folder for folder in Path(multires_path).iterdir() if folder.is_dir()}
print(f"Se encontraron {len(multires_folders)} carpetas de multiresolución.")

# Crear contenedor de MMObjects
mmobjects_container = MMobjects()

print("Procesando objetos...")
for _, row in data_ZTF.iterrows():
    oid = row['oid']
    oid_folder = Path(multires_path) / oid  # Carpeta del objeto en PS1

    # Leer imágenes multiresolución si existen
    resoluciones_multires = {}
    if oid_folder.exists() and oid_folder.is_dir():
        for fits_file in oid_folder.glob("*.fits"):
            try:
                with fits.open(fits_file) as hdul:
                    header = hdul[0].header
                    data = hdul[0].data
                    cdelt1 = header.get('CDELT1', None)  # Extraer resolución

                    if data is not None and cdelt1 is not None:
                        resoluciones_multires[cdelt1] = data
            except Exception as e:
                print(f"Error al abrir {fits_file}: {e}")

    # Crear objeto MMObject
    mm_object = MMObject(
        oid=oid,
        candid=row.get('candid', None),
        ra=row['ra'],
        dec=row['dec'],
        science_image=row['science'],
        ref_image=row.get('ref', None),
        diff_image=row.get('diff', None),
        multires_images=dict(sorted(resoluciones_multires.items(), key=lambda x: x[0])),
        class_label=row['class']
    )

    # Agregar al contenedor
    mmobjects_container.add_object(mm_object)

print(f"Se han creado {len(mmobjects_container.objs)} objetos MMObject.")

# Guardar en un archivo pickle
with open(output_pickle, "wb") as f:
    pickle.dump(mmobjects_container, f)

print(f"Proceso completado. Archivo guardado como {output_pickle}.")
