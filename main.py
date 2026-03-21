import sys
from dataclasses import dataclass
from typing import List

@dataclass
class Tarea:
    id_tarea: str
    duracion: int
    categoria: str

@dataclass
class Recurso:
    id_recurso: str
    categorias_soportadas: List[str]

with open("tareas.txt", "r") as i:
    tareas = []
    for line in i:
        id_tarea, duracion, categoria = line.strip().split(",")
        tareas.append(Tarea(id_tarea, int(duracion), categoria))

#with open(recursos.txt, "r") as j:
#    recursos = []
#    for line in j:
#        id_recursos, categoria= line.strip().splir(",")
#        recursos.append(Recursos(id_recursos,categoria))
#print(recursos)
print(tareas)





# Pon esto al final de tu archivo main.py
print("¡Lectura terminada!")
print(f"La primera tarea es: {tareas[0].id_tarea}")
print(f"Esa tarea dura: {tareas[0].duracion} horas")