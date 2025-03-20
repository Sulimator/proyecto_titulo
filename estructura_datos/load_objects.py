import pickle
import matplotlib.pyplot as plt
import numpy as np
from clases import MMobjects

# Cargar los datos
with open("MMobjects.pkl", "rb") as f:
    mmobjects_container = pickle.load(f)

print(f"Se han cargado {len(mmobjects_container.objs)} objetos MMObject.")

# Obtener el conteo de clases
clases_contadas = {}
for obj in mmobjects_container.objs:
    label = obj.class_label
    clases_contadas[label] = clases_contadas.get(label, 0) + 1

print("\nDistribución de clases en los objetos guardados:")
for clase, cantidad in clases_contadas.items():
    print(f"{clase}: {cantidad}")

# Seleccionar algunos objetos para visualizar
objetos_a_visualizar = mmobjects_container.objs[:5]  # Cambia el número si quieres más o menos

# Función para asegurarse de que la imagen es 2D
def procesar_imagen(imagen):
    if imagen is None:
        return None
    if isinstance(imagen, np.ndarray):
        if imagen.ndim == 1:
            print("⚠️ Imagen en formato 1D. Intentando reformatear...")
            size = int(np.sqrt(imagen.size))  # Suponiendo una imagen cuadrada
            if size * size == imagen.size:
                return imagen.reshape((size, size))
            else:
                print("❌ No se pudo reformatear la imagen 1D a 2D.")
                return None
        return imagen  # Si ya es 2D o más, devolver directamente
    return None

for obj in objetos_a_visualizar:
    print(f"\n📌 Mostrando imágenes para el objeto {obj.oid}")

    # Definir imágenes base y multiresolución
    imagenes_base = {
        "Science": obj.science_image,
        "Reference": obj.ref_image if obj.ref_image is not None else obj.science_image,
        "Difference": obj.diff_image
    }
    resoluciones = sorted(obj.multires_images.items(), key=lambda x: x[0])
    num_resoluciones = len(resoluciones)

    # Crear una figura con filas para cada tipo de imagen
    total_columnas = num_resoluciones + 3  # Science, Ref, Diff + Multiresoluciones
    fig, axs = plt.subplots(1, total_columnas, figsize=(4 * total_columnas, 6))
    axs = np.array(axs, dtype=object).reshape(1, -1)  # Asegurar estructura bidimensional

    # Mostrar imágenes base en las primeras columnas
    for i, (titulo, imagen) in enumerate(imagenes_base.items()):
        imagen = procesar_imagen(imagen)
        if imagen is not None:
            axs[0, i].imshow(imagen, cmap="gray", origin="lower")
        axs[0, i].set_title(titulo, fontsize=10)
        axs[0, i].axis("off")

    # Mostrar imágenes de multiresolución en sus respectivas columnas
    for j, (resolucion, imagen) in enumerate(resoluciones):
        imagen = procesar_imagen(imagen)
        if imagen is not None:
            axs[0, j + 3].imshow(imagen, cmap="gray", origin="lower")
        axs[0, j + 3].set_title(f"Res: {resolucion:.6f}°", fontsize=10)
        axs[0, j + 3].axis("off")

    plt.tight_layout()
    plt.show()
