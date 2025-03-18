import pickle
from clases import MMobjects

with open("MMobjects.pkl", "rb") as f:
    mmobjects_container = pickle.load(f)

print(f"Se han cargado {len(mmobjects_container.objs)} objetos MMObject.")
mmobjects_container.show_all()
