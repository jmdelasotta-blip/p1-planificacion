## Diagrama de funcionamiento

```mermaid
flowchart TD
    A[Inicio] --> B[Leer tareas.txt]
    B --> C[Leer recursos.txt]
    C --> D[Crear lista de tareas y recursos]

    D --> E[Inicializar mejor_makespan = infinito]
    E --> F[Repetir varias iteraciones]

    F --> G[Inicializar carga de cada recurso en 0]
    G --> H[Ordenar tareas]

    H --> H1[Priorizar tareas con menos recursos compatibles]
    H1 --> H2[Luego priorizar tareas de mayor duración]
    H2 --> H3[Agregar pequeña aleatoriedad]

    H3 --> I[Recorrer tareas ordenadas]
    I --> J[Buscar recursos compatibles con la categoría]

    J --> K{Hay recursos compatibles?}
    K -- No --> L[Descartar iteración]
    L --> F

    K -- Sí --> M[Elegir recurso con menor carga]
    M --> N[Asignar tiempo inicio = carga actual]
    N --> O[Asignar tiempo fin = inicio + duración]
    O --> P[Actualizar carga del recurso]
    P --> Q[Guardar asignación en cronograma]

    Q --> R{Quedan tareas?}
    R -- Sí --> I
    R -- No --> S[Calcular makespan actual]

    S --> T{Es mejor que el mejor_makespan?}
    T -- Sí --> U[Guardar mejor cronograma]
    T -- No --> V[Continuar]

    U --> W{Makespan menor a 10?}
    W -- Sí --> X[Terminar búsqueda anticipadamente]
    W -- No --> V

    V --> F
    X --> Y[Escribir output.txt]
    F -->|Fin de iteraciones| Y
    Y --> Z[Fin]
