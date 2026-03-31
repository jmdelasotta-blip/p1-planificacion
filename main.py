import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple


# =========================================================
# CLASES
# =========================================================

@dataclass
class Tarea:
    id_tarea: str
    duracion: int
    categoria: str


@dataclass
class Recurso:
    id_recurso: str
    categorias_soportadas: List[str]


# =========================================================
# CARGA DE DATOS
# =========================================================

def cargar_tareas(nombre_archivo: str) -> List[Tarea]:
    lista_tareas: List[Tarea] = []

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue

            partes = linea.split(",")
            id_tarea = partes[0]
            duracion = int(partes[1])
            categoria = partes[2]

            lista_tareas.append(Tarea(id_tarea, duracion, categoria))

    return lista_tareas


def cargar_recursos(nombre_archivo: str) -> List[Recurso]:
    lista_recursos: List[Recurso] = []

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue

            partes = linea.split(",")
            id_recurso = partes[0]
            categorias = partes[1:]

            lista_recursos.append(Recurso(id_recurso, categorias))

    return lista_recursos


# =========================================================
# MAPA CATEGORIAS -> RECURSOS
# =========================================================

def armar_mapa_categorias(recursos: List[Recurso]) -> Dict[str, List[str]]:
    mapa: Dict[str, List[str]] = {}

    for recurso in recursos:
        for categoria in recurso.categorias_soportadas:
            if categoria not in mapa:
                mapa[categoria] = []
            mapa[categoria].append(recurso.id_recurso)

    return mapa


# =========================================================
# ELECCION DE RECURSO
# =========================================================

def elegir_recurso_menos_cargado(
    recursos_compatibles: List[str],
    carga_actual_por_recurso: Dict[str, int]
) -> str:
    mejor_recurso = recursos_compatibles[0]
    menor_carga = carga_actual_por_recurso[mejor_recurso]

    for recurso_id in recursos_compatibles[1:]:
        if carga_actual_por_recurso[recurso_id] < menor_carga:
            mejor_recurso = recurso_id
            menor_carga = carga_actual_por_recurso[recurso_id]

    return mejor_recurso


# =========================================================
# GENERACION DEL CRONOGRAMA
# =========================================================

def generar_cronograma(
    tareas: List[Tarea],
    recursos: List[Recurso]
) -> Tuple[int, List[str]]:

    carga_por_recurso: Dict[str, int] = {}
    for recurso in recursos:
        carga_por_recurso[recurso.id_recurso] = 0

    mapa_categorias = armar_mapa_categorias(recursos)

    tareas_ordenadas = sorted(tareas, key=lambda t: t.duracion, reverse=True)

    salida: List[str] = []

    for tarea in tareas_ordenadas:
        recursos_compatibles = mapa_categorias.get(tarea.categoria, [])

        if len(recursos_compatibles) == 0:
            raise ValueError(
                f"No hay recurso compatible para la tarea {tarea.id_tarea}"
            )

        recurso_elegido = elegir_recurso_menos_cargado(
            recursos_compatibles,
            carga_por_recurso
        )

        inicio = carga_por_recurso[recurso_elegido]
        fin = inicio + tarea.duracion

        carga_por_recurso[recurso_elegido] = fin

        salida.append(f"{tarea.id_tarea},{recurso_elegido},{inicio},{fin}")

    makespan = max(carga_por_recurso.values()) if carga_por_recurso else 0

    return makespan, salida


# =========================================================
# OUTPUT
# =========================================================

def escribir_output(nombre_archivo: str, lineas: List[str]) -> None:
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for linea in lineas:
            archivo.write(linea + "\n")


# =========================================================
# MAIN
# =========================================================

def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(1)

    # Aunque no lo usemos, lo dejamos porque lo piden
    makespan_objetivo = int(sys.argv[1])

    tareas = cargar_tareas("tareas.txt")
    recursos = cargar_recursos("recursos.txt")

    _, cronograma = generar_cronograma(tareas, recursos)

    escribir_output("output.txt", cronograma)


if __name__ == "__main__":
    main()

print("¡Archivo generado exitosamente!")
print("Revisa el archivo 'output.txt' para ver el cronograma generado.")
