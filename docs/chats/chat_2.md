User: en el proyecto que significan y donde encuentro:
- solo-mode
- num-trials
- num-tasks

GitHub Copilot: Voy a buscar estos términos en el proyecto para explicarte qué significan y dónde se encuentran. 

Searched for regex `solo-mode|solo_mode`, 20 results

Searched for regex `num-trials|num_trials`, 20 results

Searched for regex `num-tasks|num_tasks`, 20 results

Ahora voy a revisar los archivos principales para entender mejor estos conceptos: 

Read [](file:///workspaces/tau2-bench/src/tau2/config.py)

Read [](file:///workspaces/tau2-bench/src/tau2/cli.py#30-30), lines 30 to 110

Read [](file:///workspaces/tau2-bench/src/tau2/data_model/simulation.py#50-50), lines 50 to 130

Ahora busco más información sobre `solo-mode`: 

Read [](file:///workspaces/tau2-bench/src/tau2/scripts/manual_mode.py#265-265), lines 265 to 285

Read [](file:///workspaces/tau2-bench/src/tau2/scripts/manual_mode.py#560-560), lines 560 to 580

Read [](file:///workspaces/tau2-bench/README.md#120-120), lines 120 to 145

Perfecto, ahora voy a leer un poco más sobre el manual mode para entender mejor solo-mode: 

Read [](file:///workspaces/tau2-bench/src/tau2/scripts/manual_mode.py#1-1), lines 1 to 100

Searched for text `display_mode_selection`, 2 results

Read [](file:///workspaces/tau2-bench/src/tau2/scripts/manual_mode.py#398-398), lines 398 to 440

Perfecto. Ahora tengo suficiente información. Voy a proporcionar una respuesta clara al usuario.

## Resumen de los 3 términos:

### 1. **`num-trials`** (Número de pruebas)
- **Qué es**: El número de veces que cada tarea se ejecuta
- **Valor por defecto**: 1
- **Dónde encontrarlo**:
  - Definido en: config.py (`DEFAULT_NUM_TRIALS = 1`)
  - Argumento CLI: cli.py (`--num-trials`)
  - Modelo de datos: simulation.py
  
**Ejemplo de uso**:
```bash
tau2 run --domain airline --num-trials 3
```
Esto ejecutará cada tarea 3 veces para obtener resultados más robustos.

---

### 2. **`num-tasks`** (Número de tareas)
- **Qué es**: Limita el número de tareas a ejecutar (útil para pruebas rápidas)
- **Valor por defecto**: `None` (ejecuta todas las tareas)
- **Dónde encontrarlo**:
  - Argumento CLI: cli.py (`--num-tasks`)
  - Modelo de datos: simulation.py
  - Procesamiento: run.py

**Ejemplo de uso**:
```bash
tau2 run --domain airline --num-tasks 5
```
Esto ejecutará solo las primeras 5 tareas en lugar de todas.

---

### 3. **`solo-mode`** (Modo solo)
- **Qué es**: Un modo de interacción manual donde trabajas directamente en un ticket sin interactuar con un usuario simulado
- **Contexto**: Solo disponible en modo manual (`tau2 manual`) cuando juegas como el agente
- **Dónde encontrarlo**:
  - Modo manual: manual_mode.py
  - Evaluador: evaluator_env.py

**Dos modos**:
- **Normal Mode**: Interactúas con un usuario simulado (conversación de ida y vuelta)
- **Solo Mode**: Trabajas independientemente en un ticket sin interacción con el usuario

Este modo se selecciona interactivamente cuando ejecutas:
```bash
tau2 manual


User: como se puede ejecutar una tarea especifica?

GitHub Copilot: Voy a buscar cómo ejecutar tareas específicas en el proyecto: 

Searched for regex `task-ids|task_ids`, 20 results

Read [](file:///workspaces/tau2-bench/src/tau2/cli.py#85-85), lines 85 to 105

Read [](file:///workspaces/tau2-bench/src/tau2/run.py#70-70), lines 70 to 95

Read [](file:///workspaces/tau2-bench/README.md#200-200), lines 200 to 220

Ahora voy a buscar ejemplos de IDs de tareas para mostrar cómo se ven: 

Ran terminal command:  find /workspaces/tau2-bench/data/tau2/domains -name "*.yaml" | head -5

Ran terminal command:  ls -la /workspaces/tau2-bench/data/tau2/domains/airline/

Ran terminal command:  head -50 /workspaces/tau2-bench/data/tau2/domains/airline/tasks.json | grep -A 2 '"id"' | head -15

Ran terminal command:  python3 -c "import json; data = json.load(open('/workspaces/tau2-bench/data/tau2/domains/airline/tasks.json')); print(f'Total tareas: {len(data)}'); print('Primeros 5 IDs:', [t['id'] for t in data[:5]])"

Perfecto! Ahora tengo toda la información. Voy a dar una respuesta completa:

## Cómo ejecutar una tarea específica

Para ejecutar tareas específicas, usa el argumento **`--task-ids`** seguido de uno o más IDs de tareas:

### Ejecutar una sola tarea:
```bash
tau2 run \
  --domain airline \
  --agent-llm gpt-4.1 \
  --user-llm gpt-4.1 \
  --task-ids 0
```

### Ejecutar múltiples tareas específicas:
```bash
tau2 run \
  --domain airline \
  --agent-llm gpt-4.1 \
  --user-llm gpt-4.1 \
  --task-ids 0 5 10 15
```

### Ver las tareas disponibles

Para ver qué tareas están disponibles en un dominio, puedes explorar los archivos de tareas:

```bash
# Ver todas las tareas del dominio airline
cat /workspaces/tau2-bench/data/tau2/domains/airline/tasks.json | python3 -m json.tool | less

# Ver solo los IDs disponibles
python3 -c "import json; data = json.load(open('/workspaces/tau2-bench/data/tau2/domains/airline/tasks.json')); print([t['id'] for t in data])"
```

### Información importante

- **IDs de tareas**: Son cadenas de texto (por ejemplo: `"0"`, `"1"`, `"2"`, etc.)
- **Ubicación**: cli.py define el argumento `--task-ids`
- **Procesamiento**: run.py filtra las tareas según los IDs proporcionados
- El dominio **airline** tiene **50 tareas** en total (IDs del `"0"` al `"49"`)

### Alternativas

Si solo quieres probar rápido sin especificar IDs exactos, también puedes usar:
```bash
# Ejecutar las primeras N tareas
tau2 run --domain airline --agent-llm gpt-4.1 --num-tasks 3
```

Esto ejecutará las primeras 3 tareas sin necesidad de conocer sus IDs específicos.