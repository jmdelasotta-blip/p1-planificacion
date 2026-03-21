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
    categorias_soportadas: StopIteration

with open("tareas.txt", "r") as i:
    tareas = []
    for line in i:
        id_tarea, duracion, categoria = line.strip().split(",")
        tareas.append(Tarea(id_tarea, int(duracion), categoria))

with open("recursos.txt", "r") as j:
    recursos = []
    for line in j:
        id_recursos, categoria= line.strip().split(",")
        recursos.append(Recurso(id_recursos, categoria))
print(f"Estas son las tareas a asignar: {tareas}")
print(f"Estas son las tareas a asignar: {recursos}")
for m in recursos:
    print(m)
print(recursos[0])
# Pon esto al final de tu archivo main.py
print("¡Lectura terminada!")