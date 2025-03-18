import numpy as np
import pickle
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import os
from astropy.io import fits


#La idea seria crear un archivo almacenado en formato pandas en donde se guarde cada objeto creado de la clas MMobject

class MMobject:
    def __init__(self, oid, candid, ra, dec, science_image, ref_image, diff_image class_label, multires_images=None):
        self.oid = oid
        self.candid = candid
        self.ra = ra
        self.dec = dec
        self.science_image = science_image
        self.ref_image = ref_image
        self.diff_image = diff_image
        self.class_label = class_label
        self.multires_images = multires_images or {} #aqui la llave del diccionario puede ser la resolucion y el contenido a imagen 


    def get_multires_images(self):
        """
        Devuelve todas las imágenes multiresolución almacenadas.
        """
        return self.multires_images

    def get_science_image(self):
        """
        Devuelve la imagen científica asociada a esta observación.
        """
        return self.science_image

#Crear funcion que permita mostrar directamente el gráfico de cada una de las imagenes ZTF, science, ref, dif y multires al mismo tiempo 
    def get_image_comparation(self):

        #toma las imaganes de cada parte y las presenta en un mismo PLT 

        return 
    def to_pythorch(self):
        #definir que informacion será la relevante para el análisis multimodal, imagenes science ref, dif y multires? o queremos solo 
        #science y multires



# paths a ambos datasets
ZTF_path = 'dataset_ZTF.pkl'
multires_path = 'multiresolution_fits_files'


# abrimos el dataset de ZTF
with open(ZTF_path, "rb") as f:
    data_ZTF = pickle.load(f)




dict_ZTF_multires = {}

i = 0
while  i < len(data_ZTF): # para cada elemento i de data_ZTF
    
    for j in Path(multires_path).iterdir(): # comparar cada i con cada j elemento de multires

        if j.stem == data_ZTF['oid'].iloc[i]: # si coinciden los oid, creamos el objeto (al principio probe j.name pero es j.stem)

            resoluciones_multires = {} # aqui se guardan las imagenes multiresolucion de data panSTARRS

            specific_multires = os.path.join(multires_path, j.name) # ruta especifica de imagen multires

            oid = j.name 
            ra = data_ZTF['ra'].iloc[i]
            dec = data_ZTF['dec'].iloc[i]
            class_label = data_ZTF['class'].iloc[i]
            science_image = data_ZTF['science'].iloc[i]


            with fits.open(specific_multires) as hdul: #abrir imagen multires como hdul
            # Leer datos y resolución (CDELT1 o CDELT2)
                header = hdul[0].header
                data = hdul[0].data
                cdelt1 = header.get('CDELT1', None)  # Tamaño del píxel en grados
        
            if data is not None and cdelt1 is not None:
            # Guardar la resolución como clave y la imagen como valor en el diccionario
                resoluciones_multires[cdelt1] = data

            # Ordenar el diccionario por resolución (CDELT1, de mayor a menor nivel de detalle)
            resoluciones_multires = dict(sorted(resoluciones_multires.items(), key=lambda x: x[0]))

            observation = ZTFObservation(oid, ra, dec, science_image, class_label, resoluciones_multires)
            dict_ZTF_multires[oid] = observation

    i = i+1





