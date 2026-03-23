## Diagrama de funcionamiento

```mermaid
flowchart TD
    A[Inicio] --> B[Solicitar makespan objetivo al usuario]
    B --> C{Es un entero válido?}
    C -- No --> D[Mostrar error y volver a pedir]
    D --> B
    C -- Sí --> E[Guardar objetivo]

    E --> F[Leer tareas_EP.txt]
    F --> G{Archivo válido?}
    G -- No --> H[Mostrar error y terminar]
    G -- Sí --> I[Crear lista de tareas]

    I --> J[Leer recursos_EP.txt]
    J --> K{Archivo válido?}
    K -- No --> H
    K -- Sí --> L[Crear lista de recursos]

    L --> M{Hay tareas y recursos?}
    M -- No --> N[Mostrar Faltan datos y terminar]
    M -- Sí --> O[Calcular duración máxima]
    O --> P[Calcular límite teórico]
    P --> Q[Mostrar resumen de datos]

    Q --> R[Entrar a resolver]
    R --> S[Inicializar mejor_tiempo = infinito]
    S --> T[Inicializar mejor_plan vacío]
    T --> U[Repetir hasta iteraciones]

    U --> V[Inicializar cargas por recurso en 0]
    V --> W[Inicializar plan_actual vacío]
    W --> X[Ordenar tareas por compatibilidad y duración con aleatoriedad]

    X --> Y[Recorrer tareas ordenadas]
    Y --> Z[Filtrar recursos compatibles]

    Z --> AA{Hay recursos compatibles?}
    AA -- No --> AB[Marcar se_pudo = False]
    AB --> AC[Descartar iteración actual]
    AC --> U

    AA -- Sí --> AD[Elegir recurso con menor carga]
    AD --> AE[Calcular inicio]
    AE --> AF[Calcular fin]
    AF --> AG[Actualizar carga del recurso]
    AG --> AH[Guardar asignación en plan_actual]

    AH --> AI{Quedan tareas?}
    AI -- Sí --> Y
    AI -- No --> AJ[Calcular tiempo_max]

    AJ --> AK{tiempo_max mejora mejor_tiempo?}
    AK -- No --> U
    AK -- Sí --> AL[Guardar mejor_tiempo y mejor_plan]

    AL --> AM{mejor_tiempo menor o igual a meta?}
    AM -- Sí --> AN[Salir antes del ciclo]
    AM -- No --> U

    AN --> AO[Retornar mejor_tiempo y mejor_plan]
    U -->|fin de iteraciones| AO

    AO --> AP{Existe plan_final?}
    AP -- Sí --> AQ[Escribir output.txt]
    AP -- No --> AR[Mostrar error de cronograma inválido]

    AQ --> AS[Mostrar resultado final]
    AR --> AS
    AS --> AT{resultado menor o igual a objetivo?}
    AT -- Sí --> AU[Mostrar LOGRADO]
    AT -- No --> AV[Mostrar NO LOGRADO]
    AU --> AW[Fin]
    AV --> AW
    Y --> Z[Fin]
