import pandas as pd

# Cargar el archivo pickle generado
def load_data(pkl_file="MMobjects.pkl"):
    print(f"Cargando datos desde {pkl_file}...")
    try:
        df = pd.read_pickle(pkl_file)
        print(f"Datos cargados correctamente: {len(df)} objetos disponibles.")
        print("\nVista previa de los datos:")
        print(df.head())  # Mostrar primeras filas para verificar
        print("\nClases únicas disponibles:")
        print(df['class_label'].unique())  # Mostrar todas las clases presentes
        return df
    except FileNotFoundError:
        print("Error: Archivo no encontrado.")
        return None

# Identificar las clases y su proporción
def class_distribution(df):
    print("\nConteo de clases:")
    print(df['class_label'].value_counts())  # Verificar conteo absoluto
    
    class_counts = df['class_label'].value_counts(normalize=True) * 100
    print("\nDistribución de clases en el conjunto de datos (%):")
    print(class_counts)
    return class_counts

# Identificar la cantidad de objetos almacenados
def count_objects(df):
    count = len(df)
    print(f"\nCantidad total de objetos almacenados: {count}")
    return count

# Ejemplo de uso
if __name__ == "__main__":
    df_objects = load_data()
    
    if df_objects is not None:
        print("\nCantidad de objetos en el archivo:")
        count_objects(df_objects)
        
        print("\nDistribución de clases:")
        class_distribution(df_objects)
