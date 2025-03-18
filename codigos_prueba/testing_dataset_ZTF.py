import numpy as np
import pickle
import pandas as pd
from pathlib import Path
import os
from astropy.io import fits


class MMobject:
    def __init__(self, oid, candid, ra, dec, science_image, ref_image, diff_image, class_label, multires_images=None):
        self.oid = oid
        self.candid = candid
        self.ra = ra
        self.dec = dec
        self.science_image = science_image
        self.ref_image = ref_image
        self.diff_image = diff_image
        self.class_label = class_label
        self.multires_images = multires_images or {}  # Llave: resolución, Valor: imagen

    def get_multires_images(self):
        """Devuelve todas las imágenes multiresolución almacenadas."""
        return self.multires_images

    def get_science_image(self):
        """Devuelve la imagen científica asociada a esta observación."""
        return self.science_image

    def to_dict(self):
        """Convierte la instancia de MMobject a un diccionario para poder almacenarla en un DataFrame."""
        return {
            'oid': self.oid,
            'candid': self.candid,
            'ra': self.ra,
            'dec': self.dec,
            'science_image': self.science_image,
            'ref_image': self.ref_image,
            'diff_image': self.diff_image,
            'class_label': self.class_label,  # Confirmar que esto tiene el valor correcto
            'multires_images': self.multires_images  # Aquí guardamos el diccionario directamente
        }


# Paths
ZTF_path = 'dataset_ZTF.pkl'
multires_path = 'multiresolution_fits_files'

print("Cargando el dataset de ZTF...")
with open(ZTF_path, "rb") as f:
    data_ZTF = pickle.load(f)

# Verificar que la columna "class" tiene los valores correctos
print("Valores únicos de la clase en el dataset:", data_ZTF["class"].unique())
print("Conteo de clases en el dataset:")
print(data_ZTF["class"].value_counts())

# Convertir a DataFrame si no lo es
if not isinstance(data_ZTF, pd.DataFrame):
    data_ZTF = pd.DataFrame(data_ZTF)
print(f"Dataset cargado con {len(data_ZTF)} filas.")

print("Leyendo archivos de multiresolución...")
multires_folders = {folder.name: folder for folder in Path(multires_path).iterdir() if folder.is_dir()}
print(f"Se encontraron {len(multires_folders)} carpetas de multiresolución.")

# Lista para almacenar los objetos MMobject
mm_objects = []

print("Procesando objetos...")
for _, row in data_ZTF.iterrows():
    oid = row['oid']
    oid_folder = Path(multires_path) / oid  # Ruta de la carpeta del objeto
    
    if oid_folder.exists() and oid_folder.is_dir():
        resoluciones_multires = {}

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

        # Verificar que la clase esté correctamente asignada
        class_label = row['class']
        print(f"Objeto {oid} tiene la clase {class_label}")

        # Crear objeto MMobject
        observation = MMobject(
            oid=oid,
            candid=row.get('candid', None),
            ra=row['ra'],
            dec=row['dec'],
            science_image=row['science'],
            ref_image=row.get('ref', None),
            diff_image=row.get('diff', None),
            class_label=class_label,  # Confirmamos que se está asignando correctamente
            multires_images=dict(sorted(resoluciones_multires.items(), key=lambda x: x[0]))
        )
        
        mm_objects.append(observation)

# Convertir la lista de objetos a un DataFrame de pandas
# Usamos el método to_dict() para evitar el problema con la clase
mm_objects_dict = [obj.to_dict() for obj in mm_objects]

# Crear DataFrame a partir de los diccionarios
df_mm_objects = pd.DataFrame(mm_objects_dict)

# Guardar como archivo pickle para acceso rápido
df_mm_objects.to_pickle("MMobjects.pkl")

print("Proceso completado. Archivo guardado como MMobjects.pkl")
