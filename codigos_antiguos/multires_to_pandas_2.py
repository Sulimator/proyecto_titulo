import pickle
import pandas as pd
from pathlib import Path
from astropy.io import fits

# Paths
multires_path = 'multires_fits_files/multiresolution_fits_files'
output_pickle = 'multires_image_paths.pkl'

# Cargar los OID de referencia desde dataset_ZTF.pkl
ZTF_path = 'dataset_ZTF.pkl'
print("Cargando el dataset de ZTF...")
with open(ZTF_path, "rb") as f:
    data_ZTF = pickle.load(f)

# Asegurar que sea un DataFrame
if not isinstance(data_ZTF, pd.DataFrame):
    data_ZTF = pd.DataFrame(data_ZTF)

# Obtener todos los OID
oid_subset = data_ZTF['oid'].astype(str)  # Asegurar que sean strings

# Definir tamaño de las tandas y límite de procesamiento
batch_size = 50  # Procesar de 50 en 50 objetos
max_processed = 36000  # Detenerse después de 6000 objetos procesados

# Intentar cargar progreso previo
try:
    with open(output_pickle, "rb") as f:
        df_multires = pickle.load(f)
    processed_oids = set(df_multires['oid'].astype(str))  # Convertir a strings
    print(f"Se cargaron {len(df_multires)} objetos previamente procesados.")
except (FileNotFoundError, EOFError):
    df_multires = pd.DataFrame()
    processed_oids = set()
    print("No se encontró un archivo previo. Se comenzará desde cero.")

# Lista para almacenar los datos nuevos
data_list = []
print("Procesando imágenes multiresolución en tandas...")

processed_count = len(processed_oids)

for i, oid in enumerate(oid_subset):
    if processed_count >= max_processed:
        print("Se ha alcanzado el límite de procesamiento de 6000 objetos. Deteniendo ejecución.")
        break
    
    oid = str(oid)  # Asegurar que el OID sea string
    if oid in processed_oids:
        continue  # Saltar objetos ya procesados
    
    oid_folder = Path(multires_path) / oid  # Carpeta del objeto en PS1
    resoluciones_multires = {}
    
    if oid_folder.exists() and oid_folder.is_dir():
        for fits_file in oid_folder.glob("*.fits"):
            try:
                with fits.open(fits_file) as hdul:
                    header = hdul[0].header
                    cdelt1 = header.get('CDELT1', None)  # Extraer resolución en grados
                    
                    if cdelt1 is not None:
                        resoluciones_multires[f"{cdelt1:.6f}"] = str(fits_file)  # Guardar la ruta del archivo
            except Exception as e:
                print(f"Error al abrir {fits_file}: {e}")
    
    # Agregar a la lista
    if resoluciones_multires:
        data_entry = {'oid': oid, **resoluciones_multires}  # Expandir las resoluciones como atributos
        data_list.append(data_entry)
        processed_count += 1
    
    # Guardar en tandas
    if (i + 1) % batch_size == 0 or (i + 1) == len(oid_subset):
        df_batch = pd.DataFrame(data_list)
        df_multires = pd.concat([df_multires, df_batch], ignore_index=True)
        with open(output_pickle, "wb") as f:
            pickle.dump(df_multires, f)
        print(f"Guardado parcial: {len(df_multires)} objetos procesados.")
        data_list = []  # Reiniciar la lista

print(f"Proceso completado. Archivo final guardado como {output_pickle}.")