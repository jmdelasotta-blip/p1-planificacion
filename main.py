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
        tareas.append((id_tarea, int(duracion), categoria))

with open("recursos.txt", "r") as j:
    recursos = []
    for line in j:
        id_recursos, categoria= line.strip().split(",")
        recursos.append((id_recursos, categoria))

for i in range(len(recursos)):
    print(recursos[i])
print(" ")
for i in range(len(tareas)):
    print(tareas[i])
tkstime=0
for i in range(len(tareas)):
    tkstime=tkstime+tareas[i][1]
print(tkstime)

r1queue=[]
r2queue=[]
r3queue=[]
def r1process():
    r1counter=0
    #Recurso 1 admite tareas 'CAT_A'
    for i in range(len(tareas)):
        if tareas[i][2]=='CAT_A':
            r1counter=r1counter+tareas[i][1]
            r1queue.append(tareas[i][0])
            tareas.remove(tareas[i])
            print(r1counter)
        break

r1process()
print(tareas)
def r2process():
    pass
def r3process():
    pass




with open("mis_resultados.txt", "w") as archivo_nuevo:
    archivo_nuevo.write("Hola, este es mi primer texto guardado.\n")
    archivo_nuevo.write("Esta es la segunda línea.")