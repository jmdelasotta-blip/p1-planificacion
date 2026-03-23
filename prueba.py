import sys
from dataclasses import dataclass
from typing import List

# ==========================================
# 1. TUS CLASES (Corregidas para mypy)
# ==========================================
@dataclass
class Tarea:
    id_tarea: str
    duracion: int
    categoria: str

@dataclass
class Recurso:
    id_recurso: str
    # Cambiamos "StopIteration" por "List[str]" para que mypy no tire error
    categorias_soportadas: List[str] 

# ==========================================
# 2. LECTURA DE ARCHIVOS
# ==========================================
# Leemos tareas tal como lo hacías tú
tareas = []
with open("tareas.txt", "r") as i:
    for line in i:
        if line.strip():
            id_tarea, duracion, categoria = line.strip().split(",")
            tareas.append(Tarea(id_tarea, int(duracion), categoria))

# Leemos recursos tal como lo hacías tú
recursos = []
with open("recursos.txt", "r") as j:
    for line in j:
        if line.strip():
            partes = line.strip().split(",")
            id_recursos = partes[0]
            categorias = partes[1:] # Atrapa todas las categorías que tenga
            recursos.append(Recurso(id_recursos, categorias))

# ==========================================
# 3. REGLA OBLIGATORIA DEL ENUNCIADO
# ==========================================
# El profe ejecutará: python main.py <makespan_objetivo>
if len(sys.argv) > 1:
    makespan_objetivo = sys.argv[1]
else:
    print("Por favor, ejecuta así: python main.py <numero>")
    sys.exit(1)

# ==========================================
# 4. OPTIMIZACIÓN LPT (Para sacar buena nota)
# ==========================================
# Ordenamos las tareas de la más larga a la más corta.
tareas.sort(key=lambda t: t.duracion, reverse=True)

# ==========================================
# 5. TU FUNCIÓN ASIGNADORA (Sin hardcoding)
# ==========================================
def tksallocator():
    # En vez de crear r1counter=0, r2counter=0 a mano, creamos un diccionario.
    # Si hay 3 recursos, esto crea los 3 contadores. Si hay 20, crea 20.
    contadores_tiempo = {}
    for r in recursos:
        contadores_tiempo[r.id_recurso] = 0
        
    cronograma_final = []

    # En vez de tu "while True" con el "if i==8: break", usamos un "for".
    # Así recorre TODAS las tareas sin importar si son 8 o 1000.
    for tarea in tareas:
        
        # Variables para buscar a la máquina más desocupada
        recurso_elegido = ""
        tiempo_mas_bajo = 999999 # Partimos con un número alto
        
        # Este ciclo reemplaza a tus "if r1 <= r2 and r1 <= r3"
        for recurso in recursos:
            # Primero: ¿Soporta la categoría?
            if tarea.categoria in recurso.categorias_soportadas:
                
                # Segundo: ¿Es el que tiene menos tiempo acumulado?
                if contadores_tiempo[recurso.id_recurso] < tiempo_mas_bajo:
                    tiempo_mas_bajo = contadores_tiempo[recurso.id_recurso]
                    recurso_elegido = recurso.id_recurso
                    
        # Aquí ya encontramos cuál es el recurso más desocupado
        # Calculamos a qué hora empieza y a qué hora termina esta tarea
        tiempo_inicio = contadores_tiempo[recurso_elegido]
        tiempo_fin = tiempo_inicio + tarea.duracion
        
        # Actualizamos el contador de ese recurso (igual que tu r1counter = r1counter + duracion)
        contadores_tiempo[recurso_elegido] = tiempo_fin
        
        # Guardamos la línea en formato perfecto para el txt
        linea = f"{tarea.id_tarea},{recurso_elegido},{tiempo_inicio},{tiempo_fin}"
        cronograma_final.append(linea)

    return cronograma_final

# Ejecutamos tu función
resultados_para_imprimir = tksallocator()

# ==========================================
# 6. ESCRITURA ESTRICTA DEL OUTPUT.TXT
# ==========================================
# Ya no ponemos texto extra, solo el formato CSV que pide el verificador
with open("output.txt", "w") as archivo_nuevo:
    for linea in resultados_para_imprimir:
        archivo_nuevo.write(linea + "\n")