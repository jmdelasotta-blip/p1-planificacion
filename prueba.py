from dataclasses import dataclass
from typing import List, Dict

# -------------------------
# Definición de clases
# -------------------------
@dataclass
class Tarea:
    id_tarea: str
    duracion: int
    categoria: str

@dataclass
class Recurso:
    id_recurso: str
    categorias_soportadas: List[str]


# -------------------------
# Lectura de tareas
# -------------------------
tareas: List[Tarea] = []

with open("tareas.txt", "r") as archivo:
    for linea in archivo:
        id_tarea, duracion, categoria = linea.strip().split(",")
        tarea = Tarea(id_tarea, int(duracion), categoria)
        tareas.append(tarea)


# -------------------------
# Lectura de recursos
# -------------------------
recursos: List[Recurso] = []

with open("recursos.txt", "r") as archivo:
    for linea in archivo:
        partes = linea.strip().split(",")
        id_recurso = partes[0]
        categorias = partes[1:]  # puede tener una o más categorías
        recurso = Recurso(id_recurso, categorias)
        recursos.append(recurso)


# -------------------------
# Inicialización de estructuras
# -------------------------
colas: Dict[str, List[str]] = {}   # tareas asignadas a cada recurso
cargas: Dict[str, int] = {}        # tiempo acumulado por recurso

for r in recursos:
    colas[r.id_recurso] = []
    cargas[r.id_recurso] = 0


# -------------------------
# Función de asignación
# -------------------------
def asignar_tareas(tareas: List[Tarea], recursos: List[Recurso]):

    # 🔥 PASO CLAVE: ordenar tareas de mayor a menor duración
    tareas_ordenadas = sorted(tareas, key=lambda t: t.duracion, reverse=True)

    for tarea in tareas_ordenadas:

        # Buscar recursos que puedan ejecutar la tarea
        recursos_compatibles = []
        for r in recursos:
            if tarea.categoria in r.categorias_soportadas:
                recursos_compatibles.append(r)

        # Si no hay recurso compatible
        if len(recursos_compatibles) == 0:
            print(f"No hay recurso disponible para la tarea {tarea.id_tarea}")
            continue

        # Elegir el recurso con menor carga acumulada
        mejor_recurso = recursos_compatibles[0]
        for r in recursos_compatibles:
            if cargas[r.id_recurso] < cargas[mejor_recurso.id_recurso]:
                mejor_recurso = r

        # Asignar tarea al recurso elegido
        colas[mejor_recurso.id_recurso].append(tarea.id_tarea)
        cargas[mejor_recurso.id_recurso] += tarea.duracion


# -------------------------
# Ejecución del algoritmo
# -------------------------
asignar_tareas(tareas, recursos)


# -------------------------
# Cálculo del makespan
# -------------------------
makespan = max(cargas.values())


# -------------------------
# Mostrar resultados
# -------------------------
print("\nRESULTADOS:\n")

for r in recursos:
    rid = r.id_recurso
    print(f"Recurso {rid}:")
    print(f"  Tiempo total: {cargas[rid]}")
    print(f"  Tareas: {colas[rid]}\n")

print(f"Makespan: {makespan}")


# -------------------------
# Guardar resultados en archivo
# -------------------------
with open("mis_resultados.txt", "w") as archivo:
    archivo.write("Resultados del algoritmo de asignación\n\n")

    for r in recursos:
        rid = r.id_recurso
        archivo.write(f"Recurso {rid}:\n")
        archivo.write(f"  Tiempo total: {cargas[rid]}\n")
        archivo.write(f"  Tareas: {colas[rid]}\n\n")

    archivo.write(f"Makespan: {makespan}\n")


print("\nArchivo generado correctamente ✅")
print("¡Fin del programa!")