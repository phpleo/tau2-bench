# Checklist para Crear un Nuevo Dominio

Este documento proporciona una guía paso a paso para crear un nuevo dominio en Tau2. Usaremos "Banking" como ejemplo.

## Checklist: Creación del Dominio Banking

### 1. Estructura de Archivos del Código Fuente

#### 1.1 Crear la carpeta del dominio
- [ ] Crear directorio `/src/tau2/domains/banking/`
- [ ] Crear archivo `__init__.py` vacío en el directorio

#### 1.2 Implementar el modelo de datos
- [ ] Crear archivo `data_model.py`
  - [ ] Implementar la clase `DB` que extiende de la clase base
  - [ ] Definir las tablas y esquemas de datos para Banking
  - [ ] Implementar métodos para cargar/guardar datos desde archivos

#### 1.3 Implementar el modelo de datos del usuario (Opcional)
- [ ] Crear archivo `user_data_model.py` (si es necesario)
  - [ ] Implementar la clase `DB` para datos específicos del usuario
  - [ ] Definir las tablas y esquemas de datos de usuario para Banking

#### 1.4 Implementar las herramientas del dominio
- [ ] Crear archivo `tools.py`
  - [ ] Implementar clase que extiende `ToolKitBase`
  - [ ] Definir herramientas específicas del dominio (ej: check_balance, transfer_money, pay_bill, etc.)
  - [ ] Agregar descripciones y esquemas para cada herramienta
  - [ ] Implementar la lógica de cada herramienta

#### 1.5 Implementar las herramientas del usuario (Opcional)
- [ ] Crear archivo `user_tools.py` (si es necesario)
  - [ ] Implementar clase que extiende `ToolKitBase`
  - [ ] Definir herramientas específicas del usuario para simulación

#### 1.6 Implementar el entorno del dominio
- [ ] Crear archivo `environment.py`
  - [ ] Implementar función `get_environment()` que retorna una instancia de `Environment`
  - [ ] Implementar función `get_tasks()` que retorna la lista de tareas del dominio
  - [ ] Configurar el entorno con las herramientas y base de datos correspondientes

#### 1.7 Implementar utilidades (Opcional)
- [ ] Crear archivo `utils.py`
  - [ ] Agregar funciones auxiliares específicas del dominio

### 2. Estructura de Archivos de Datos

#### 2.1 Crear la carpeta de datos
- [ ] Crear directorio `/data/tau2/domains/banking/`

#### 2.2 Crear la base de datos del dominio
- [ ] Crear archivo `db.json` o `db.toml`
  - [ ] Definir la estructura inicial de datos (cuentas, transacciones, etc.)
  - [ ] Poblar con datos de ejemplo realistas

#### 2.3 Crear la base de datos del usuario (Opcional)
- [ ] Crear archivo `user_db.json` o `user_db.toml` (si es necesario)
  - [ ] Definir la estructura de datos del usuario
  - [ ] Poblar con datos de ejemplo

#### 2.4 Crear el archivo de políticas
- [ ] Crear archivo `policy.md`
  - [ ] Documentar las políticas y reglas del dominio Banking
  - [ ] Incluir límites de transacciones, requisitos de seguridad, etc.
  - [ ] Definir comportamientos esperados y restricciones

#### 2.5 Crear las tareas
- [ ] Crear archivo `tasks.json`
  - [ ] Definir tareas específicas del dominio (ej: "Transfer money to another account", "Check recent transactions", etc.)
  - [ ] Incluir para cada tarea:
    - [ ] ID único
    - [ ] Descripción
    - [ ] Criterios de evaluación
    - [ ] Datos de contexto necesarios

#### 2.6 Crear los splits de tareas
- [ ] Crear archivo `split_tasks.json`
  - [ ] Implementar al menos el split `base` (obligatorio)
  - [ ] Definir splits adicionales si es necesario (ej: `train`, `test`, `val`)
  - [ ] Incluir los IDs de las tareas correspondientes a cada split

### 3. Pruebas

#### 3.1 Crear la estructura de tests
- [ ] Crear directorio `/tests/test_domains/test_banking/`
- [ ] Crear archivo `__init__.py` vacío

#### 3.2 Implementar tests para herramientas
- [ ] Crear archivo `test_tools_banking.py`
  - [ ] Escribir tests para cada herramienta del dominio
  - [ ] Verificar inputs válidos e inválidos
  - [ ] Verificar la lógica de negocio

#### 3.3 Implementar tests para herramientas de usuario (Opcional)
- [ ] Crear archivo `test_user_tools_banking.py` (si aplica)
  - [ ] Escribir tests para las herramientas de usuario

#### 3.4 Ejecutar las pruebas
- [ ] Ejecutar `pytest tests/test_domains/test_banking/`
- [ ] Verificar que todos los tests pasen
- [ ] Alcanzar cobertura de código adecuada

### 4. Registro del Dominio

#### 4.1 Registrar en el sistema
- [ ] Abrir archivo `/src/tau2/registry.py`
- [ ] Importar las funciones del dominio:
  ```python
  from tau2.domains.banking.environment import get_environment as banking_get_environment
  from tau2.domains.banking.environment import get_tasks as banking_get_tasks
  ```
- [ ] Registrar el dominio:
  ```python
  registry.register_domain(banking_get_environment, "banking")
  registry.register_tasks(banking_get_tasks, "banking")
  ```

### 5. Documentación

- [ ] Actualizar el README principal si es necesario
- [ ] Documentar características específicas del dominio Banking
- [ ] Agregar ejemplos de uso
- [ ] Documentar las herramientas disponibles y sus casos de uso

### 6. Validación Final

- [ ] Ejecutar todos los tests del proyecto: `pytest`
- [ ] Verificar que el dominio se carga correctamente
- [ ] Ejecutar una tarea de ejemplo end-to-end
- [ ] Revisar que no hay conflictos con otros dominios
- [ ] Validar el formato de todos los archivos JSON/TOML

---

## Ejemplo de Herramientas para el Dominio Banking

Algunas herramientas que podrían implementarse:

- `check_balance`: Consultar el balance de una cuenta
- `transfer_money`: Transferir dinero entre cuentas
- `pay_bill`: Pagar una factura
- `view_transactions`: Ver historial de transacciones
- `block_card`: Bloquear una tarjeta
- `request_loan`: Solicitar un préstamo
- `set_spending_limit`: Establecer límite de gasto
- `add_beneficiary`: Agregar un beneficiario

## Ejemplo de Tareas para el Dominio Banking

Algunas tareas que podrían definirse:

- "Transfer $500 to John's account"
- "Check my account balance and report if it's below $1000"
- "Pay my electricity bill due on the 15th"
- "Block my credit card ending in 1234"
- "Show me all transactions from last month over $100"
- "Set up automatic payment for my rent"