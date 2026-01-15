Searched for regex `tasks\.json` (`**/*.py`), 9 results

Searched for files matching `**/tasks.py`, 1 match

Searched codebase for "Pydantic model Task evaluation_criteria user_scenario", 16 results

Perfecto, encontré el archivo principal. Ahora déjame leer el modelo Pydantic completo: 

Read [](file:///workspaces/tau2-bench/src/tau2/data_model/tasks.py)

Perfecto! Ahora tengo toda la información. Déjame presentar la documentación completa basada en los modelos Pydantic:

---

## Archivo `tasks.json` - Documentación Completa

El archivo `tasks.json` es utilizado por tasks.py y se carga mediante funciones como las definidas en utils.py.

### Modelo Pydantic: `Task`

Representa una tarea para un dominio particular. Esta información se envía al simulador de usuario, al entorno y al evaluador.

---

### **Campos Principales**

#### **`id`** (string, requerido)
- **Descripción**: Identificador único de la tarea
- **Uso**: Para identificar y rastrear tareas específicas en evaluaciones

#### **`description`** (objeto opcional)
**Modelo**: `Description`  
Descripción de la tarea que puede enviarse al evaluador.

- **`purpose`** (string, opcional): Explica qué está probando el escenario (ej: "Test the get_current_available_credit functionality")
- **`relevant_policies`** (string, opcional): La parte de la política que es relevante para el escenario
- **`notes`** (string, opcional): Información adicional sobre el escenario no cubierta por otros campos

---

#### **`user_scenario`** (objeto, requerido)
**Modelo**: `UserScenario`  
Toda la información que se enviará al simulador de usuario.

- **`persona`** (string, opcional): Persona del usuario. Define al usuario en general, no la situación específica (ej: "A responsible cardholder who regularly monitors their credit usage")

- **`instructions`** (objeto o string, requerido): **Modelo**: `StructuredUserInstructions`  
  Define la situación específica del usuario y las tareas que está intentando completar:
  
  - **`domain`** (string, requerido): El dominio de la tarea (ej: "retail_banking_consumers")
  - **`reason_for_call`** (string, requerido): La razón por la que el usuario llama al agente (ej: "You want to check the available credit on your credit card ending in 6417.")
  - **`known_info`** (string, opcional): Información conocida sobre el usuario (ej: "You are Dylan Parker.\nYour customer login ID is 45682409.")
  - **`unknown_info`** (string, opcional): Información que el usuario no conoce
  - **`task_instructions`** (string, requerido): Instrucciones específicas para el usuario (ej: "Ask the agent to check your available credit on your credit card.")

---

#### **`ticket`** (string, opcional)
- **Descripción**: Tarea en formato de ticket para resolución de agente en modo solo
- **Uso**: Describe brevemente la solicitud del cliente desde la perspectiva del agente

---

#### **`initial_state`** (objeto, opcional)
**Modelo**: `InitialState`  
Estado inicial de la tarea. Se usa para configurar el estado inicial del entorno y del orquestador.

- **`initialization_data`** (objeto, opcional): Datos de actualización del entorno inicial
  - **`agent_data`** (dict, opcional): Datos de actualización del entorno del agente
  - **`user_data`** (dict, opcional): Datos de actualización del entorno del usuario

- **`initialization_actions`** (array, opcional): Acciones iniciales a tomar en el entorno
  - Cada acción tiene: `env_type`, `func_name`, `arguments`

- **`message_history`** (array, opcional): Mensajes ya intercambiados entre usuario, agente y entorno. Los últimos mensajes deben ser del usuario o agente.

---

#### **`evaluation_criteria`** (objeto, opcional)
**Modelo**: `EvaluationCriteria`  
Criterios de evaluación para la tarea. Se envía al evaluador.

- **`actions`** (array, opcional): Acciones que el agente debe tomar para completar la tarea  
  **Modelo**: `Action`
  - **`action_id`** (string, requerido): Identificador único de la acción dentro del escenario
  - **`requestor`** (string, default: "assistant"): Quién solicita la acción ("assistant" o "user")
  - **`name`** (string, requerido): Nombre de la acción/herramienta a ejecutar
  - **`arguments`** (dict, requerido): Argumentos para la acción
  - **`info`** (string, opcional): Información sobre la acción
  - **`compare_args`** (array[string], opcional): Argumentos a verificar en la llamada de herramienta. Si es `null`, se verifican todos los argumentos

- **`env_assertions`** (array, opcional): Lista de aserciones sobre el entorno del agente o usuario  
  **Modelo**: `EnvAssertion`
  - **`env_type`**: Tipo de entorno ("assistant" o "user")
  - **`func_name`**: Nombre de la función a llamar
  - **`arguments`**: Argumentos para la función
  - **`assert_value`** (bool, default: true): Valor esperado de la aserción
  - **`message`** (string, opcional): Mensaje a mostrar si falla la aserción

- **`communicate_info`** (array[string], opcional): Lista de información que el agente debe comunicar al usuario (deprecado)

- **`nl_assertions`** (array[string], opcional): Lista de aserciones para la tarea en lenguaje natural (ej: "The agent provided the available credit amount")

- **`reward_basis`** (array[string], opcional): Base de la recompensa. Valores posibles: "DB", "ENV_ASSERTION", "NL_ASSERTION", "ACTION", "COMMUNICATE". Default: ["DB", "COMMUNICATE"]

---

### **Flujo de Uso**

1. **Carga**: Las tareas se cargan desde `tasks.json` mediante funciones de utilidad específicas del dominio
2. **Simulación**: La información del `user_scenario` se pasa al simulador de usuario
3. **Inicialización**: El `initial_state` configura el entorno y el historial de mensajes
4. **Ejecución**: El agente interactúa con el usuario simulado
5. **Evaluación**: Los `evaluation_criteria` determinan si la tarea se completó exitosamente mediante:
   - Verificación de acciones ejecutadas (`actions`)
   - Aserciones de entorno (`env_assertions`)
   - Aserciones en lenguaje natural (`nl_assertions`)
   - Información comunicada (`communicate_info`)