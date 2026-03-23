
Y una versión todavía más técnica, por si quieres que el README suene más “algorítmico”:

```md
## Heurística de planificación

```mermaid
flowchart TD
    A[Entrada: tareas y recursos] --> B[Definir meta de makespan]
    B --> C[Inicializar mejor solución conocida]
    C --> D[Para cada iteración]
    D --> E[Ordenar tareas por menor compatibilidad y mayor duración]
    E --> F[Para cada tarea]
    F --> G[Construir conjunto de recursos compatibles]
    G --> H{Conjunto vacío?}
    H -- Sí --> I[Invalidar iteración]
    H -- No --> J[Seleccionar recurso con carga mínima]
    J --> K[Asignar tarea al final de la cola del recurso]
    K --> L[Actualizar carga]
    L --> M{Quedan tareas?}
    M -- Sí --> F
    M -- No --> N[Evaluar makespan]

    N --> O{Mejora incumbente?}
    O -- Sí --> P[Actualizar mejor solución]
    O -- No --> D
    P --> Q{Cumple meta?}
    Q -- Sí --> R[Finalizar anticipadamente]
    Q -- No --> D
    R --> S[Salida: output.txt]
    D -->|última iteración| S
    Y --> Z[Fin]
