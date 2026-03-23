import sys
import random

# Clases simples para guardar la info
class Tarea:
    def __init__(self, id_tarea, duracion, categoria):
        self.id_tarea = id_tarea
        self.duracion = int(duracion)
        self.categoria = categoria

class Recurso:
    def __init__(self, id_recurso, categorias_soportadas):
        self.id_recurso = id_recurso
        self.categorias_soportadas = categorias_soportadas

def leer_tareas(archivo):
    lista = []
    try:
        with open(archivo, "r") as f:
            for linea in f:
                if linea.strip():
                    datos = linea.strip().split(",")
                    # datos[0] es id, datos[1] es duracion, datos[2] es categoria
                    lista.append(Tarea(datos[0], datos[1], datos[2]))
        return lista
    except:
        print("No se encontro el archivo de tareas")
        sys.exit(1)

def leer_recursos(archivo):
    lista = []
    try:
        with open(archivo, "r") as f:
            for linea in f:
                if linea.strip():
                    datos = linea.strip().split(",")
                    lista.append(Recurso(datos[0], datos[1:]))
        return lista
    except:
        print("No se encontro el archivo de recursos")
        sys.exit(1)

def cant_compatibles(tarea, recursos):
    # cuenta cuantos recursos le sirven a la tarea para saber si es dificil de asignar
    return sum(1 for r in recursos if tarea.categoria in r.categorias_soportadas)

def resolver(tareas, recursos, meta, iteraciones=2000):
    mejor_tiempo = float('inf')
    mejor_plan = []

    for i in range(iteraciones):
        # diccionario con la carga actual de cada recurso
        cargas = {r.id_recurso: 0 for r in recursos}
        plan_actual = []
        
        # ordenamos las tareas. le sumamos algo de random a la duracion 
        # para que el orden cambie un poco en cada iteracion y probar opciones
        tareas_ord = sorted(
            tareas,
            key=lambda t: (cant_compatibles(t, recursos), -t.duracion + random.uniform(-3, 3))
        )

        se_pudo = True
        for t in tareas_ord:
            # filtramos los recursos que saben hacer esta tarea
            sirven = [r for r in recursos if t.categoria in r.categorias_soportadas]

            if not sirven:
                se_pudo = False
                break 

            # elegimos el recurso que se desocupe mas temprano (algoritmo goloso)
            mejor_r = min(sirven, key=lambda r: cargas[r.id_recurso])
            
            inicio = cargas[mejor_r.id_recurso]
            fin = inicio + t.duracion
            
            cargas[mejor_r.id_recurso] = fin
            
            # guardamos el formato pedido
            plan_actual.append(f"{t.id_tarea},{mejor_r.id_recurso},{inicio},{fin}")

        if se_pudo:
            tiempo_max = max(cargas.values())
            # si encontramos algo mejor, lo guardamos
            if tiempo_max < mejor_tiempo:
                mejor_tiempo = tiempo_max
                mejor_plan = plan_actual
                
                # cortamos si ya llegamos a la meta del usuario
                if mejor_tiempo <= meta:
                    break 

    return mejor_tiempo, mejor_plan

if __name__ == "__main__":
    # 1. Pedir interactivamente el objetivo al usuario
    while True:
        try:
            entrada = input("\n🎯 Ingresa el makespan objetivo que deseas alcanzar (ej. 13): ")
            makespan_objetivo = int(entrada)
            break # Si ingresó un número válido, salimos del bucle
        except ValueError:
            print("⚠️ Por favor, ingresa un número entero válido.")

    # 2. Cargar datos
    tareas = leer_tareas("tareas.txt")
    recursos = leer_recursos("recursos.txt")

    if len(tareas) == 0 or len(recursos) == 0:
        print("Faltan datos")
        sys.exit(1)

    # 3. Diagnóstico rápido
    print(f"\n--- DIAGNÓSTICO ---")
    print(f"Makespan Objetivo Solicitado: {makespan_objetivo}")
    print(f"Cota inferior teórica (límite matemático): {sum(t.duracion for t in tareas) / len(recursos):.2f}")
    print(f"Duración máxima de una tarea: {max(t.duracion for t in tareas)}")
    print("-------------------\n")

    # 4. Correr el algoritmo (ahora le pasamos el makespan_objetivo)
    print("Calculando mejor cronograma (probando miles de combinaciones)...")
    makespan_final, cronograma_final = buscar_mejor_cronograma(tareas, recursos, makespan_objetivo)

    # 5. Guardar resultado
    if cronograma_final:
        with open("output.txt", "w") as archivo:
            # Documentación del formato para quien lea el código:
            # 1: ID de la tarea, 2: ID del recurso, 3: Inicio, 4: Fin
            for linea in cronograma_final:
                archivo.write(f"{linea}\n")
        print(f"✅ ¡Éxito! Archivo output.txt generado correctamente.")
    else:
        print("❌ Error: No se pudo generar un cronograma válido.")

    # 6. Evaluación final (Logrado o No Logrado)
    print("\n==================================")
    print(f"📊 RESULTADO FINAL: {makespan_final}")
    print("==================================")
    
    if makespan_final <= makespan_objetivo:
        print(f"🏆 ¡LOGRADO! El algoritmo alcanzó un makespan de {makespan_final}, cumpliendo tu objetivo de {makespan_objetivo}.")
    else:
        print(f"🛑 NO LOGRADO. El mejor makespan posible fue {makespan_final}. No se pudo alcanzar tu objetivo de {makespan_objetivo}.")
        print("💡 Recuerda: Revisa la cota teórica en el diagnóstico. A veces es físicamente imposible bajar más.")