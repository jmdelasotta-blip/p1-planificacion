import sys
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
cargas: Dict[str, int] = {}        # tiempo acumulado por recurso
cronograma_final: List[str] = []   # 🔥 NUEVO: Aquí guardaremos las líneas exactas para el txt

for r in recursos:
    cargas[r.id_recurso] = 0

# -------------------------
# Función de asignación
# -------------------------
def asignar_tareas(tareas: List[Tarea], recursos: List[Recurso]) -> None:

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

        # 🔥 CALCULAR TIEMPOS PARA EL ARCHIVO DE SALIDA
        tiempo_inicio = cargas[mejor_recurso.id_recurso]
        tiempo_fin = tiempo_inicio + tarea.duracion

        # Asignar tarea al recurso elegido (actualizar el reloj de ese recurso)
        cargas[mejor_recurso.id_recurso] = tiempo_fin
        
        # Guardar la línea con el formato exacto que pide el profesor
        linea_csv = f"{tarea.id_tarea},{mejor_recurso.id_recurso},{tiempo_inicio},{tiempo_fin}"
        cronograma_final.append(linea_csv)

# -------------------------
# Ejecución del programa
# -------------------------
# 🔥 REGLA: El programa debe recibir un argumento en consola (ej: python prueba.py 12)
if len(sys.argv) < 2:
    print("Uso: python prueba.py <makespan_objetivo>")
    sys.exit(1) # Detenemos el programa si no lo ejecutan correctamente

makespan_objetivo = sys.argv[1] # Capturamos el número, aunque no lo usemos para calcular, debe estar ahí.

# Corremos el algoritmo
asignar_tareas(tareas, recursos)
makespan_logrado = max(cargas.values())

# -------------------------
# Guardar resultados en archivo
# -------------------------
# 🔥 REGLA: El archivo DEBE llamarse output.txt y no tener ningún encabezado
with open("output.txt", "w") as archivo:
    for linea in cronograma_final:
        archivo.write(f"{linea}\n")

print(f"\n¡Archivo output.txt generado correctamente! ✅")
print(f"Makespan logrado: {makespan_logrado}")
print(f"Makespan objetivo solicitado en consola: {makespan_objetivo}")