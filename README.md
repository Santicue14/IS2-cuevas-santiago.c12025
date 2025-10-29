# Sistema de Gestión de Biblioteca

## Resumen del Proyecto

Este proyecto implementa un **Sistema de Gestión de Biblioteca** completo utilizando una arquitectura en capas bien definida, demostrando los conceptos de diseño de software y patrones arquitectónicos.

## Cómo Ejecutar el Sistema

### Opción 1: Menú Interactivo (Recomendado)

```bash
cd src
python main.py
```

Esto abrirá un menú interactivo completo con las siguientes opciones:
- Gestión de Libros (registrar, listar, buscar, eliminar)
- Gestión de Socios (registrar, listar, activar/desactivar)
- Gestión de Préstamos (prestar, devolver, listar)
- Reportes (resumen general)

### Opción 2: Demostración Automática

```bash
cd src
python demo.py
```

Este script ejecuta una demostración completa que muestra:
-  Patrón Singleton en acción
-  Registro de libros y socios
-  Realización de préstamos
-  Devoluciones con cálculo de multas
-  Validaciones de reglas de negocio
-  Arquitectura en capas funcionando

## Consigna Resuelta

La consigna académica está completamente resuelta en `documento/README.md`:

**Identificación de las 3 capas principales**:
- Capa de Presentación (View)
- Capa de Lógica de Negocio (Service)
- Capa de Datos (Repository + DAL)

**Problema y Patrón de Diseño**:
- Problema: Acceso centralizado a la base de datos
- Solución: Patrón **Singleton** en DatabaseManager
- Arquitectura: Patrón **MVC** (Model-View-Controller)

**Esquema gráfico (UML)**:
- Diagrama de arquitectura en capas (PlantUML)
- Diagrama de clases completo

**Validación del modelo**:
- Implementación completa en Python
- Sistema funcional con menú interactivo
- Script de demostración

## Características Implementadas

### Gestión de Libros
-  Registrar libros con ISBN, título, autor, categoría y ejemplares
-  Listar todos los libros del catálogo
-  Listar solo libros disponibles
-  Buscar libros por ISBN
-  Eliminar libros (con validación)

### Gestión de Socios
-  Registrar socios con validación de email
-  Listar todos los socios
-  Listar socios activos
-  Buscar socios por ID
-  Activar/Desactivar socios

### Gestión de Préstamos
-  Realizar préstamos con validaciones completas
-  Registrar devoluciones
-  Cálculo automático de multas por retraso
-  Listar préstamos activos con detección de vencidos

### Reportes
-  Resumen general del sistema
-  Estadísticas en tiempo real

## Reglas de Negocio

**Libros:**
- ISBN único y obligatorio
- Al menos 1 ejemplar
- No se puede eliminar si tiene ejemplares prestados

**Socios:**
- Email único y válido (validación con regex)
- Máximo 3 libros prestados simultáneamente
- No se puede desactivar si tiene préstamos activos

**Préstamos:**
- Duración: 14 días
- Multa: $10 por día de retraso
- Solo socios activos pueden prestar
- Solo libros disponibles

## Patrones de Diseño Utilizados

### 1. Singleton (DAL)
El `DatabaseManager` garantiza una única instancia de conexión a BD.

```python
db1 = DatabaseManager.get_instance()
db2 = DatabaseManager.get_instance()
# db1 is db2 → True (misma instancia)
```

### 2. Repository Pattern
Separa la lógica de acceso a datos de la lógica de negocio.

### 3. MVC (Model-View-Controller)
- **Model**: Libro, Socio, Préstamo
- **View**: Menu (interfaz de usuario)
- **Controller**: LibroController, SocioController, PrestamoController

## Tecnologías

- **Lenguaje**: Python 3.7+
- **Base de Datos**: SQLite 3
- **Arquitectura**: Capas separadas
- **Patrones**: Singleton, Repository, MVC


## Documentación

- **Documento académico**: `documento/README.md` (consigna completa resuelta)
- **Documentación técnica**: `src/README.md` (detalles de implementación)
- **Este archivo**: Instrucciones de uso rápido

## Verificación de Funcionamiento

Para verificar que todo funciona correctamente:

1. Ejecutar la demostración:
   ```bash
   cd src
   python demo.py
   ```

2. Verificar que muestre:
   - Patrón Singleton funcionando
   - Libros registrados
   - Socios registrados
   - Préstamos realizados
   - Devoluciones con cálculo de multas
   - Validaciones de reglas de negocio

3. Luego probar el menú interactivo:
   ```bash
   python main.py
   ```

## Autor

**Alumno**: Santiago Cuevas  
**Materia**: Ingeniería de Software 2  
**Año**: 2025  
**Universidad**: Universidad Nacional de José Clemente Paz

