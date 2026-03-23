import sys
import random
from dataclasses import dataclass
from typing import List, Tuple

# ==========================================
# 1. DEFINICIÓN DE ESTRUCTURAS DE DATOS
# ==========================================
@dataclass
class Tarea:
    id_tarea: str
    duracion: int
    categoria: str

@dataclass
class Recurso:
    id_recurso: str
    categorias_soportadas: List[str]

# ==========================================
# 2. FUNCIONES DE LECTURA DE ARCHIVOS
# ==========================================
def cargar_tareas(ruta: str) -> List[Tarea]:
    """Lee el archivo de tareas y crea una lista de objetos Tarea."""
    tareas = []
    try:
        with open(ruta, "r") as archivo:
            for linea in archivo:
                if linea.strip(): # Ignora líneas en blanco
                    id_tarea, duracion, categoria = linea.strip().split(",")
                    tareas.append(Tarea(id_tarea, int(duracion), categoria))
        return tareas
    except FileNotFoundError:
        print(f"Error: No se encontró '{ruta}'.")
        sys.exit(1)

def cargar_recursos(ruta: str) -> List[Recurso]:
    """Lee el archivo de recursos y crea una lista de objetos Recurso."""
    recursos = []
    try:
        with open(ruta, "r") as archivo:
            for linea in archivo:
                if linea.strip():
                    partes = linea.strip().split(",")
                    recursos.append(Recurso(partes[0], partes[1:]))
        return recursos
    except FileNotFoundError:
        print(f"Error: No se encontró '{ruta}'.")
        sys.exit(1)

# ==========================================
# 3. LÓGICA DEL ALGORITMO (EL CORAZÓN DEL CÓDIGO)
# ==========================================
def contar_compatibles(tarea: Tarea, recursos: List[Recurso]) -> int:
    """Cuenta cuántos recursos pueden hacer una tarea (para saber qué tan restrictiva es)."""
    return sum(1 for r in recursos if tarea.categoria in r.categorias_soportadas)

def buscar_mejor_cronograma(tareas: List[Tarea], recursos: List[Recurso], makespan_objetivo: int, iteraciones: int = 2000) -> Tuple[int, List[str]]:
    """
    Busca la mejor asignación posible probando miles de combinaciones.
    Como el problema es NP-Hard, usamos aleatoriedad para explorar opciones rápidamente.
    """
    mejor_makespan = float('inf')
    mejor_cronograma = []

    for _ in range(iteraciones):
        # Diccionario para llevar el tiempo en que se desocupa cada recurso
        cargas = {r.id_recurso: 0 for r in recursos}
        cronograma_actual = []
        
        # ESTRATEGIA: Ordenar tareas. 
        # 1. Primero las que tienen menos recursos compatibles (son más difíciles de ubicar).
        # 2. Segundo por duración (las más largas primero), pero con un factor aleatorio 
        #    para generar combinaciones distintas en cada iteración.
        tareas_ordenadas = sorted(
            tareas,
            key=lambda t: (contar_compatibles(t, recursos), -t.duracion + random.uniform(-3, 3))
        )

        exito = True
        for tarea in tareas_ordenadas:
            # Filtrar solo los recursos que saben hacer esta tarea
            recursos_utiles = [r for r in recursos if tarea.categoria in r.categorias_soportadas]

            if not recursos_utiles:
                exito = False
                break # Si una tarea no tiene recurso, este intento fracasa

            # Asignar la tarea al recurso que termine más temprano (Greedy)
            mejor_recurso = min(recursos_utiles, key=lambda r: cargas[r.id_recurso])
            
            # Calcular tiempos
            tiempo_inicio = cargas[mejor_recurso.id_recurso]
            tiempo_fin = tiempo_inicio + tarea.duracion
            
            # Actualizar la carga del recurso elegido
            cargas[mejor_recurso.id_recurso] = tiempo_fin
            
            # Formato estricto para output.txt: ID_TAREA, ID_RECURSO, TIEMPO_INICIO, TIEMPO_TERMINO
            cronograma_actual.append(f"{tarea.id_tarea},{mejor_recurso.id_recurso},{tiempo_inicio},{tiempo_fin}")

        # Evaluar si esta iteración es la mejor que hemos visto hasta ahora
        if exito:
            makespan_actual = max(cargas.values())
            if makespan_actual < mejor_makespan:
                mejor_makespan = makespan_actual
                mejor_cronograma = cronograma_actual
                
                # Si logramos llegar o mejorar el objetivo pedido por el usuario, cortamos para ahorrar tiempo
                if mejor_makespan <= makespan_objetivo:
                    break 

    return mejor_makespan, mejor_cronograma

# ==========================================
# 4. EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    # 1. Atrapar el objetivo desde el comando de consola (REGLA ESTRICTA)
    if len(sys.argv) < 2:
        print("Error. Uso correcto: python main.py <makespan_objetivo>")
        sys.exit(1)
        
    try:
        makespan_objetivo = int(sys.argv[1])
    except ValueError:
        print("Error: El makespan objetivo debe ser un número entero.")
        sys.exit(1)

    # 2. Cargar datos
    tareas = cargar_tareas("tareas.txt")
    recursos = cargar_recursos("recursos.txt")

    if not tareas or not recursos:
        sys.exit(1)

    # 3. Diagnóstico rápido (Opcional, pero no afecta la evaluación)
    print(f"\n--- DIAGNÓSTICO ---")
    print(f"Makespan Objetivo Solicitado: {makespan_objetivo}")
    print(f"Cota inferior teórica: {sum(t.duracion for t in tareas) / len(recursos):.2f}")
    print("-------------------\n")

    # 4. Correr el algoritmo
    makespan_final, cronograma_final = buscar_mejor_cronograma(tareas, recursos, makespan_objetivo)

    # 5. Guardar resultado en output.txt
    if cronograma_final:
        with open("output.txt", "w") as archivo:
            for linea in cronograma_final:
                archivo.write(f"{linea}\n")
        print(f"✅ Archivo output.txt generado. Makespan final: {makespan_final}")
    else:
        print("❌ Error: No se pudo generar un cronograma válido.")