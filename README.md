## Diagrama de funcionamiento

```mermaid
flowchart TD
    A[Inicio] --> B[Definir clases Tarea y Recurso]
    B --> C[Leer tareas.txt]
    C --> D[Crear objetos Tarea]
    D --> E[Leer recursos.txt]
    E --> F[Crear objetos Recurso]

    F --> G{Se entregó argumento por línea de comandos?}
    G -- No --> H[Mostrar mensaje de uso]
    H --> I[Terminar programa]
    G -- Sí --> J[Guardar makespan_objetivo]

    J --> K[Ordenar tareas por duración descendente LPT]
    K --> L[Entrar a tksallocator]

    L --> M[Inicializar contadores de tiempo por recurso en 0]
    M --> N[Inicializar cronograma_final vacío]
    N --> O[Recorrer cada tarea]

    O --> P[Inicializar recurso_elegido vacío]
    P --> Q[Inicializar tiempo_mas_bajo alto]
    Q --> R[Recorrer cada recurso]

    R --> S{El recurso soporta la categoría de la tarea?}
    S -- No --> T[Revisar siguiente recurso]
    T --> U{Quedan recursos?}
    U -- Sí --> R
    U -- No --> V[Usar recurso_elegido encontrado]

    S -- Sí --> W{Su tiempo acumulado es menor al mínimo actual?}
    W -- No --> T
    W -- Sí --> X[Actualizar tiempo_mas_bajo]
    X --> Y[Actualizar recurso_elegido]
    Y --> T

    V --> Z[Calcular tiempo_inicio]
    Z --> AA[Calcular tiempo_fin = inicio + duración]
    AA --> AB[Actualizar contador del recurso]
    AB --> AC[Guardar línea en cronograma_final]

    AC --> AD{Quedan tareas?}
    AD -- Sí --> O
    AD -- No --> AE[Calcular makespan_final]

    AE --> AF[Mostrar makespan objetivo y makespan logrado]
    AF --> AG[Retornar cronograma_final]
    AG --> AH[Escribir output.txt]
    AH --> AI[Fin]
    Y --> Z[Fin]
