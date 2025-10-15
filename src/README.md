# Sistema de Gestión de Biblioteca - Código Fuente

## Arquitectura en Capas

El sistema sigue una arquitectura en capas bien definida:

```
┌─────────────────────────────────────────┐
│            VIEW (Vista)                 │  ← Interfaz de usuario (menú)
│         view/menu.py                    │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│        CONTROLLER (Controlador)         │  ← Coordina operaciones
│   libro_controller.py                   │
│   socio_controller.py                   │
│   prestamo_controller.py                │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│        SERVICE (Lógica de Negocio)      │  ← Reglas de negocio
│   libro_service.py                      │
│   socio_service.py                      │
│   prestamo_service.py                   │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│       REPOSITORY (Repositorio)          │  ← Acceso a datos
│   libro_repository.py                   │
│   socio_repository.py                   │
│   prestamo_repository.py                │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      DAL (Data Access Layer)            │  ← Gestión de BD (Singleton)
│   database_manager.py                   │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         BASE DE DATOS                   │
│         biblioteca.db                   │
└─────────────────────────────────────────┘
```

## Estructura de Carpetas

```
src/
├── model/                  # Modelos de dominio
│   ├── __init__.py
│   ├── libro.py           # Clase Libro
│   ├── socio.py           # Clase Socio
│   └── prestamo.py        # Clase Prestamo
│
├── dal/                   # Data Access Layer
│   ├── __init__.py
│   └── database_manager.py # Singleton para BD
│
├── repository/            # Capa de repositorios
│   ├── __init__.py
│   ├── libro_repository.py
│   ├── socio_repository.py
│   └── prestamo_repository.py
│
├── service/               # Lógica de negocio
│   ├── __init__.py
│   ├── libro_service.py
│   ├── socio_service.py
│   └── prestamo_service.py
│
├── controller/            # Controladores
│   ├── __init__.py
│   ├── libro_controller.py
│   ├── socio_controller.py
│   └── prestamo_controller.py
│
├── view/                  # Vista (UI)
│   ├── __init__.py
│   └── menu.py           # Menú interactivo
│
└── main.py               # Punto de entrada

```

## Responsabilidades por Capa

### 1. VIEW (Vista)
- Interactuar con el usuario
- Mostrar menús y opciones
- Capturar entrada del usuario
- Mostrar resultados y mensajes
- **No contiene lógica de negocio**

### 2. CONTROLLER (Controlador)
- Recibir peticiones de la vista
- Coordinar llamadas a servicios
- Retornar resultados a la vista
- **No contiene lógica de negocio ni acceso a datos**

### 3. SERVICE (Servicio - Lógica de Negocio)
- Implementar reglas de negocio
- Validaciones complejas
- Coordinar múltiples repositorios
- Transacciones de negocio
- **No accede directamente a la BD**

### 4. REPOSITORY (Repositorio)
- CRUD básico (Create, Read, Update, Delete)
- Consultas a la base de datos
- Mapeo entre BD y modelos
- **No contiene lógica de negocio**

### 5. DAL (Data Access Layer)
- Gestión de conexión a BD (Singleton)
- Ejecución de queries
- Manejo de transacciones (commit/rollback)
- Creación de tablas

### 6. MODEL (Modelo de Dominio)
- Clases de entidades del negocio
- Propiedades y métodos básicos
- Independiente de la persistencia

## Patrones de Diseño Utilizados

### Singleton (DAL)
El `DatabaseManager` implementa el patrón Singleton para garantizar una única instancia de conexión a la BD.

```python
db1 = DatabaseManager.get_instance()
db2 = DatabaseManager.get_instance()
# db1 is db2 → True
```

### Repository Pattern
Separa la lógica de acceso a datos de la lógica de negocio.

### MVC (Model-View-Controller)
Arquitectura general del sistema:
- **Model**: Clases de dominio (Libro, Socio, Préstamo)
- **View**: Menú interactivo
- **Controller**: Controladores que coordinan

## Flujo de Datos

### Ejemplo: Realizar un Préstamo

```
1. Usuario selecciona opción en MENU
   ↓
2. Menu.realizar_prestamo() llama a
   ↓
3. PrestamoController.realizar_prestamo()
   ↓
4. PrestamoService.realizar_prestamo()
   - Valida reglas de negocio
   - Verifica disponibilidad
   ↓
5. PrestamoRepository.crear()
   ↓
6. DatabaseManager.execute_query()
   ↓
7. Base de datos SQLite
```

## Ejecución

Para ejecutar el sistema:

```bash
cd src
python main.py
```

## Características del Sistema

- ✅ Gestión completa de libros (CRUD)
- ✅ Gestión de socios (registro, activación/desactivación)
- ✅ Préstamos y devoluciones
- ✅ Cálculo automático de multas por retraso
- ✅ Validaciones de reglas de negocio
- ✅ Menú interactivo completo
- ✅ Reportes básicos

## Reglas de Negocio Implementadas

1. **Libros**:
   - ISBN único
   - Al menos 1 ejemplar
   - No se puede eliminar si hay ejemplares prestados

2. **Socios**:
   - Email único y válido
   - Máximo 3 libros prestados simultáneamente
   - No se puede desactivar si tiene préstamos activos

3. **Préstamos**:
   - Duración: 14 días
   - Multa: $10 por día de retraso
   - Solo socios activos pueden prestar
   - Solo libros con ejemplares disponibles

## Tecnologías

- Python 3.7+
- SQLite 3
- Arquitectura en capas
- Patrón Singleton
- Repository Pattern

