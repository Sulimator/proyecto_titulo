import os
from astropy.io import fits
import matplotlib.pyplot as plt


carpeta = "multiresolution_fits_files/ZTF19aakpyrv"


archivos_fits = [f for f in os.listdir(carpeta) if f.endswith('.fits')]


print("Archivos FITS disponibles:", archivos_fits[:5])

for archivo in archivos_fits[:5]: 
   
    ruta_archivo = os.path.join(carpeta, archivo)
    
 
    with fits.open(ruta_archivo) as hdul:
       
        print(f"Información del archivo {archivo}:")
        hdul.info()


    
        for i, hdu in enumerate(hdul):
            #list_images = []
            print(f"Extensión {i}: {hdu.header}")
        
    
        
        

    
        imagen_fits = hdul[0].data
        print(hdul[0].header)
        # Visualizar la imagen
        plt.figure(figsize=(8, 8))
        plt.imshow(imagen_fits, cmap="gray", origin="lower")
        plt.title(f"Imagen - {archivo}")
        plt.colorbar()  # Para mostrar la barra de colores
        plt.axis("off")  # No mostrar los ejes 
        plt.show()







import os
from astropy.io import fits

# Ruta de la carpeta principal
carpeta_principal = "multiresolution_fits_files"

# Inicializar contador de imágenes
contador_imagenes = 0

# Recorrer las subcarpetas y archivos FITS
for subcarpeta, _, archivos in os.walk(carpeta_principal):
    for archivo in archivos:
        if archivo.endswith('.fits'):
            ruta_archivo = os.path.join(subcarpeta, archivo)
            
            # Abrir el archivo FITS
            with fits.open(ruta_archivo) as hdul:
                # Verificar cuántas extensiones tienen datos válidos
                for hdu in hdul:
                    if hdu.data is not None:  # Si hay datos en la extensión
                        contador_imagenes += 1

# Mostrar el total de imágenes
print(f"El conjunto de datos contiene {contador_imagenes} imágenes.")
print(hdul[0].header)