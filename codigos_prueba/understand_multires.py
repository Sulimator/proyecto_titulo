import os
from astropy.io import fits
import matplotlib.pyplot as plt

# Carpeta donde están los archivos FITS
carpeta = "multiresolution_fits_files/ZTF19aakpyrv"

# Listar archivos FITS
archivos_fits = [f for f in os.listdir(carpeta) if f.endswith('.fits')]

# Diccionario para almacenar resoluciones e imágenes
resoluciones_imagenes = []

# Procesar cada archivo FITS
for archivo in archivos_fits:
    ruta_archivo = os.path.join(carpeta, archivo)
    
    with fits.open(ruta_archivo) as hdul:
        # Leer datos y resolución (CDELT1 o CDELT2)
        header = hdul[0].header
        data = hdul[0].data
        cdelt1 = header.get('CDELT1', None)  # Tamaño del píxel en grados
        
        if data is not None and cdelt1 is not None:
            # Guardar resolución y datos
            resoluciones_imagenes.append((cdelt1, data))

# Ordenar por resolución (CDELT1, de mayor a menor nivel de detalle)
resoluciones_imagenes.sort(key=lambda x: x[0])

# Graficar todas las resoluciones
plt.figure(figsize=(15, 15))
for i, (resolucion, imagen) in enumerate(resoluciones_imagenes):
    plt.subplot(1, len(resoluciones_imagenes), i + 1)
    plt.imshow(imagen, cmap='gray', origin='lower')
    plt.title(f'Res: {resolucion:.6f}°')
    plt.axis('off')

plt.tight_layout()
plt.show()


with fits.open(ruta_archivo) as hdul:
    header = hdul[0].header
    # Convertir el generador a lista
    keys = list(header.keys())
    print(keys)

