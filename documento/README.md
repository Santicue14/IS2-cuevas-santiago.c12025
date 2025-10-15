# SISTEMA DE GESTIÓN DE BIBLIOTECA

## Índice
1. [Introducción](#introducción)
2. [Identificación de Capas](#identificación-de-capas)
3. [Problema y Patrón de Diseño](#problema-y-patrón-de-diseño)
4. [Arquitectura del Sistema](#arquitectura-del-sistema)
5. [Diagrama de Clases UML](#diagrama-de-clases-uml)
6. [Validación del Modelo](#validación-del-modelo)

---

## Introducción

El sistema de gestión de biblioteca permite:
- Registrar socios de la biblioteca
- Gestionar préstamos de libros
- Controlar devoluciones
- Administrar catálogo de libros
- Generar reportes de préstamos

El objetivo es desarrollar una solución arquitectónica robusta que separe responsabilidades y facilite el mantenimiento y escalabilidad del sistema.

---

## Identificación de Capas

### 1. Capa de Presentación (User Interface)
**Responsabilidad**: Interactuar con el usuario final (bibliotecarios, socios, administradores)

**Funciones principales**:
- Mostrar formularios de registro de socios
- Visualizar catálogo de libros disponibles
- Interfaz para registrar préstamos y devoluciones
- Mostrar reportes y estadísticas
- Gestionar autenticación de usuarios
- Validar datos de entrada del usuario

### 2. Capa de Lógica de Negocio (Business Logic)
**Responsabilidad**: Implementar las reglas del negocio y coordinar las operaciones

**Funciones principales**:
- Validar si un socio puede realizar un préstamo (límite de libros, multas pendientes)
- Calcular fechas de devolución según el tipo de libro
- Aplicar multas por retraso en devoluciones
- Gestionar disponibilidad de ejemplares
- Verificar estado de membresía de socios
- Procesar búsquedas y filtros de libros
- Generar notificaciones de vencimiento

### 3. Capa de Datos (Data Access Layer)
**Responsabilidad**: Gestionar el acceso y persistencia de datos

**Funciones principales**:
- CRUD (Crear, Leer, Actualizar, Eliminar) de Socios
- CRUD de Libros y Ejemplares
- CRUD de Préstamos
- Gestionar transacciones de base de datos
- Consultas complejas (libros más prestados, socios morosos)
- Mantener integridad referencial
- Gestionar conexiones a la base de datos

---

## Problema y Patrón de Diseño

### Problema Identificado: Acceso Centralizado a la Base de Datos

**Descripción del problema**:
En un sistema de biblioteca, múltiples componentes necesitan acceder a la base de datos (para consultar libros, registrar préstamos, actualizar socios, etc.). Si cada componente crea su propia conexión a la base de datos, podemos enfrentar:
- Múltiples conexiones innecesarias que consumen recursos
- Inconsistencias en la configuración de conexión
- Dificultad para gestionar el pool de conexiones
- Problemas de concurrencia y bloqueos

### Patrón de Diseño Propuesto: **Singleton**

**¿Qué es Singleton?**
Es un patrón de diseño creacional que garantiza que una clase tenga una única instancia y proporciona un punto de acceso global a ella.

**¿Por qué Singleton para este problema?**
1. **Única instancia**: Asegura que solo exista una conexión/gestor de base de datos en todo el sistema
2. **Acceso global**: Todos los componentes pueden acceder a la misma instancia sin crear nuevas conexiones
3. **Control centralizado**: Facilita la gestión de la conexión, transacciones y cierre de recursos
4. **Eficiencia**: Reduce el overhead de crear múltiples conexiones
5. **Configuración única**: La configuración de la base de datos se define en un solo lugar

**Aplicación en nuestro sistema**:
- Crear una clase `DatabaseManager` como Singleton
- Esta clase gestiona la conexión a la base de datos
- Todas las operaciones de datos pasan por esta única instancia
- Garantiza thread-safety para operaciones concurrentes

### Patrón Arquitectónico: **MVC (Modelo-Vista-Controlador)**

Adicionalmente, la arquitectura general sigue el patrón **MVC**:
- **Modelo**: Clases de dominio (Libro, Socio, Préstamo) y acceso a datos
- **Vista**: Interfaz de usuario (formularios, listas, reportes)
- **Controlador**: Lógica de negocio que coordina entre vista y modelo

---

## Arquitectura del Sistema

![Diagrama de Arquitectura](https://img.plantuml.biz/plantuml/svg/ZLJRRjim47pVhnZ8RQ8kxk8QI8CW2G2Xb0e3OhCaJBsaKcPDWv8RO9D_lsnTiw96OKj78QpxxttrtCxOxHYSf42YX4Y3K4L2xm6DkBm0H5HboYIbDwtCzXBQIGzRS0YBBl_cEBQcn5OByYn3tU_r2qakenBtdDs2K-FVI_OCHakWpn9aTS7P9qIZe2kBVmSwMwELXmzqBXaqf1gWZTa2aNPOzOHo40uvsyNJUoQWSxxlWVb5A2RbyNu3xPJK4aV4S5e0RcIhEsqTWKGwWaqG9r0ZH8jIFse1TEzG_AoqtEMRaSjfUZC2gU9D3lIaXCQ7JhlHFCw-60GNKdPaicZXzGWtX5a4dgzGkbLM3Dw6p4bucGqUKK0I_WxyK3FuxF5sgl3QMgoMrUUC3mQVdKAom7BsrTkrJcExZWoZ8kNptw1V7rv7x1BlsM7lq85PZ4mclPlUU3Ebvvf745G9C68mVdonV7nCCz4mrL4kgdB7MQT3oTpzwKMULJs4xUHfJPFOQLOy3Ir4N-fwLE89vWkOP7m_qZ0HIb-2zT-wJdju55qiIrcaPLrzNB6wlfv-CwMex6GkcPsJxrPv3qvaFrnT-UFCaXV0OttSxRAuKPsSld7_0G00)

### Tabla de Capas

| Capa | Elementos | Responsabilidad | Componentes Principales |
|------|-----------|-----------------|-------------------------|
| **User Interface** | Vista al usuario | Presentar interfaz para bibliotecarios y socios | Formularios de préstamo, registro de socios, búsqueda de libros |
| **Business Logic (Server)** | Lógica del negocio | Procesar reglas de negocio, validaciones y coordinación | Servicios de préstamo, validación de disponibilidad, cálculo de multas |
| **Data Access Layer (Repository)** | Acceso a datos | Intermediario entre la lógica y la base de datos | Repositorios de Libro, Socio, Préstamo |
| **Database** | Base de datos SQLite/PostgreSQL | Persistir datos del sistema | Tablas: libros, socios, prestamos, ejemplares, multas |
| **Common/Domain** | Clases de dominio | Modelos compartidos entre capas | Libro, Socio, Préstamo, Ejemplar, Multa |
| **Database Manager** | Singleton de conexión | Gestionar conexión única a la BD | DatabaseManager (patrón Singleton) |

---

## Diagrama de Clases UML

![Diagrama de Clases](https://img.plantuml.biz/plantuml/svg/hLRTRjim47ttLwnXx5S0qAqgAgbHs0H8OGHmC55C6sQSiinJ1wxKt_Tzau1jP7aWkAPpxjxvVD-RvqJTIDr52HIGBe50jY4uJ6Pq7N93iIIXk5lVkr_kpPBIJwbFW0kFpMvW7c6gvb8VWLbw_mIB-6fJiQ7HVm3MVj-W4lOYL6yXHZs0YdOcYr3kAXMxkjZAOgXOtGHXx8eIX3SXZA5Pm9QNQCeNSbDcNXu9hOXa11uJK1VHBj3jRvYyRZZGRf-GGRjTZJKUzYoZdZIZvCWZxZgTjhYyy8jEOvGOv8h0KQvOTWZ98iZNbmGl0lBqC6EqWl0ckGb0l0cmG_02k6W_01l0G_0_g1k_1JsFpSBdTyPvLw2MuPvMuOvBKvCNvCOw1Nw1MxrPwDbExbJypctAQhDFzqMhqpNkHoJppJjpNrsrtvNkrJtFw_qxysRcxhstshFcxcyhSxxslzvtzlCytsxsxVxxzzpwvPxtrwxSBcxbVVxxpRxVtzxojtMTjYHkpJyFdNqRABhMNOJ28XN1aHN0_n0W4rL40MML2INKb2LG4JMKb2LGW5M0YIK0JOK1POK2LOb0ZOb1ROb2VOc08e21e12e30e34e3W00)

### Descripción de Clases Principales:

**1. DatabaseManager (Singleton)**
- `instance: DatabaseManager` (atributo de clase estático)
- `connection: Connection`
- `get_instance(): DatabaseManager` (método estático)
- `execute_query(query: str, params: tuple): ResultSet`
- `commit(): void`
- `rollback(): void`

**2. Libro**
- `isbn: str`
- `titulo: str`
- `autor: str`
- `categoria: str`
- `total_ejemplares: int`
- `ejemplares_disponibles: int`
- `esta_disponible(): bool`

**3. Socio**
- `id_socio: int`
- `nombre: str`
- `email: str`
- `telefono: str`
- `fecha_registro: date`
- `activo: bool`
- `libros_prestados: int`
- `tiene_multas_pendientes(): bool`
- `puede_realizar_prestamo(): bool`

**4. Prestamo**
- `id_prestamo: int`
- `socio: Socio`
- `libro: Libro`
- `fecha_prestamo: date`
- `fecha_devolucion_esperada: date`
- `fecha_devolucion_real: date`
- `estado: str` (activo, devuelto, vencido)
- `calcular_multa(): float`
- `registrar_devolucion(): void`
- `esta_vencido(): bool`

**5. ServicioPrestamo (Business Logic)**
- `db_manager: DatabaseManager`
- `repositorio_libro: RepositorioLibro`
- `repositorio_socio: RepositorioSocio`
- `repositorio_prestamo: RepositorioPrestamo`
- `realizar_prestamo(socio: Socio, libro: Libro): Prestamo`
- `registrar_devolucion(prestamo: Prestamo): void`
- `verificar_disponibilidad(libro: Libro): bool`

**6. RepositorioLibro (Data Access Layer)**
- `db_manager: DatabaseManager`
- `buscar_por_isbn(isbn: str): Libro`
- `listar_disponibles(): List[Libro]`
- `actualizar_disponibilidad(libro: Libro): void`

---

## Validación del Modelo

### Implementación en Python

A continuación se presenta la implementación del modelo con enfoque en el patrón **Singleton** para el gestor de base de datos:

```python
# database_manager.py - Patrón Singleton
import sqlite3
import threading
from typing import Any, List, Tuple


class DatabaseManager:
    """
    Implementación del patrón Singleton para gestionar
    la conexión a la base de datos de forma centralizada.
    Thread-safe.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.connection = None
        self.database_path = "biblioteca.db"
        self._initialized = True
    
    @classmethod
    def get_instance(cls):
        """Método para obtener la única instancia"""
        return cls()
    
    def connect(self):
        """Establecer conexión a la base de datos"""
        if self.connection is None:
            self.connection = sqlite3.connect(
                self.database_path,
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row
            self._crear_tablas()
    
    def _crear_tablas(self):
        """Crear tablas si no existen"""
        cursor = self.connection.cursor()
        
        # Tabla de libros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                isbn TEXT PRIMARY KEY,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                categoria TEXT,
                total_ejemplares INTEGER DEFAULT 1,
                ejemplares_disponibles INTEGER DEFAULT 1
            )
        ''')
        
        # Tabla de socios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS socios (
                id_socio INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono TEXT,
                fecha_registro DATE DEFAULT CURRENT_DATE,
                activo BOOLEAN DEFAULT 1,
                libros_prestados INTEGER DEFAULT 0
            )
        ''')
        
        # Tabla de préstamos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prestamos (
                id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
                id_socio INTEGER NOT NULL,
                isbn TEXT NOT NULL,
                fecha_prestamo DATE DEFAULT CURRENT_DATE,
                fecha_devolucion_esperada DATE NOT NULL,
                fecha_devolucion_real DATE,
                estado TEXT DEFAULT 'activo',
                multa REAL DEFAULT 0.0,
                FOREIGN KEY (id_socio) REFERENCES socios(id_socio),
                FOREIGN KEY (isbn) REFERENCES libros(isbn)
            )
        ''')
        
        self.connection.commit()
    
    def execute_query(self, query: str, params: Tuple = ()) -> Any:
        """Ejecutar una consulta SQL"""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor
    
    def commit(self):
        """Confirmar transacción"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """Revertir transacción"""
        if self.connection:
            self.connection.rollback()
    
    def close(self):
        """Cerrar conexión"""
        if self.connection:
            self.connection.close()
            self.connection = None


# modelos.py - Clases de Dominio
from datetime import date, timedelta
from typing import Optional


class Libro:
    """Clase que representa un libro en el catálogo"""
    
    def __init__(self, isbn: str, titulo: str, autor: str, 
                 categoria: str = "", total_ejemplares: int = 1,
                 ejemplares_disponibles: int = 1):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.total_ejemplares = total_ejemplares
        self.ejemplares_disponibles = ejemplares_disponibles
    
    def esta_disponible(self) -> bool:
        """Verifica si hay ejemplares disponibles"""
        return self.ejemplares_disponibles > 0
    
    def __repr__(self):
        return f"Libro(isbn='{self.isbn}', titulo='{self.titulo}', " \
               f"disponibles={self.ejemplares_disponibles})"


class Socio:
    """Clase que representa un socio de la biblioteca"""
    
    MAX_LIBROS_PERMITIDOS = 3
    
    def __init__(self, id_socio: int, nombre: str, email: str,
                 telefono: str = "", fecha_registro: date = None,
                 activo: bool = True, libros_prestados: int = 0):
        self.id_socio = id_socio
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.fecha_registro = fecha_registro or date.today()
        self.activo = activo
        self.libros_prestados = libros_prestados
    
    def puede_realizar_prestamo(self) -> bool:
        """Verifica si el socio puede realizar un préstamo"""
        return (self.activo and 
                self.libros_prestados < self.MAX_LIBROS_PERMITIDOS)
    
    def tiene_multas_pendientes(self) -> bool:
        """Verifica si tiene multas pendientes (implementar con BD)"""
        # Esta lógica se implementaría consultando la BD
        return False
    
    def __repr__(self):
        return f"Socio(id={self.id_socio}, nombre='{self.nombre}', " \
               f"prestados={self.libros_prestados})"


class Prestamo:
    """Clase que representa un préstamo de libro"""
    
    DIAS_PRESTAMO = 14
    MULTA_POR_DIA = 10.0  # Multa en pesos por día de retraso
    
    def __init__(self, id_prestamo: int, socio: Socio, libro: Libro,
                 fecha_prestamo: date = None,
                 fecha_devolucion_esperada: date = None,
                 fecha_devolucion_real: date = None,
                 estado: str = "activo"):
        self.id_prestamo = id_prestamo
        self.socio = socio
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo or date.today()
        self.fecha_devolucion_esperada = (
            fecha_devolucion_esperada or 
            self.fecha_prestamo + timedelta(days=self.DIAS_PRESTAMO)
        )
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado
    
    def esta_vencido(self) -> bool:
        """Verifica si el préstamo está vencido"""
        if self.estado == "devuelto":
            return False
        return date.today() > self.fecha_devolucion_esperada
    
    def calcular_multa(self) -> float:
        """Calcula la multa por retraso"""
        if not self.fecha_devolucion_real:
            fecha_referencia = date.today()
        else:
            fecha_referencia = self.fecha_devolucion_real
        
        if fecha_referencia <= self.fecha_devolucion_esperada:
            return 0.0
        
        dias_retraso = (fecha_referencia - 
                       self.fecha_devolucion_esperada).days
        return dias_retraso * self.MULTA_POR_DIA
    
    def registrar_devolucion(self):
        """Registra la devolución del libro"""
        self.fecha_devolucion_real = date.today()
        self.estado = "devuelto"
    
    def __repr__(self):
        return f"Prestamo(id={self.id_prestamo}, libro='{self.libro.titulo}', " \
               f"socio='{self.socio.nombre}', estado='{self.estado}')"


# repositorios.py - Capa de Acceso a Datos
from typing import List, Optional


class RepositorioLibro:
    """Repositorio para gestionar libros en la base de datos"""
    
    def __init__(self):
        self.db_manager = DatabaseManager.get_instance()
        self.db_manager.connect()
    
    def crear(self, libro: Libro) -> bool:
        """Crear un nuevo libro"""
        try:
            query = '''
                INSERT INTO libros (isbn, titulo, autor, categoria, 
                                   total_ejemplares, ejemplares_disponibles)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            self.db_manager.execute_query(query, (
                libro.isbn, libro.titulo, libro.autor, libro.categoria,
                libro.total_ejemplares, libro.ejemplares_disponibles
            ))
            self.db_manager.commit()
            return True
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al crear libro: {e}")
            return False
    
    def buscar_por_isbn(self, isbn: str) -> Optional[Libro]:
        """Buscar un libro por ISBN"""
        query = "SELECT * FROM libros WHERE isbn = ?"
        cursor = self.db_manager.execute_query(query, (isbn,))
        row = cursor.fetchone()
        
        if row:
            return Libro(
                isbn=row['isbn'],
                titulo=row['titulo'],
                autor=row['autor'],
                categoria=row['categoria'],
                total_ejemplares=row['total_ejemplares'],
                ejemplares_disponibles=row['ejemplares_disponibles']
            )
        return None
    
    def listar_disponibles(self) -> List[Libro]:
        """Listar libros disponibles"""
        query = "SELECT * FROM libros WHERE ejemplares_disponibles > 0"
        cursor = self.db_manager.execute_query(query)
        
        libros = []
        for row in cursor.fetchall():
            libros.append(Libro(
                isbn=row['isbn'],
                titulo=row['titulo'],
                autor=row['autor'],
                categoria=row['categoria'],
                total_ejemplares=row['total_ejemplares'],
                ejemplares_disponibles=row['ejemplares_disponibles']
            ))
        return libros
    
    def actualizar_disponibilidad(self, libro: Libro) -> bool:
        """Actualizar disponibilidad de ejemplares"""
        try:
            query = '''
                UPDATE libros 
                SET ejemplares_disponibles = ?
                WHERE isbn = ?
            '''
            self.db_manager.execute_query(
                query, 
                (libro.ejemplares_disponibles, libro.isbn)
            )
            self.db_manager.commit()
            return True
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al actualizar disponibilidad: {e}")
            return False


class RepositorioSocio:
    """Repositorio para gestionar socios"""
    
    def __init__(self):
        self.db_manager = DatabaseManager.get_instance()
        self.db_manager.connect()
    
    def crear(self, socio: Socio) -> Optional[int]:
        """Crear un nuevo socio"""
        try:
            query = '''
                INSERT INTO socios (nombre, email, telefono, activo)
                VALUES (?, ?, ?, ?)
            '''
            cursor = self.db_manager.execute_query(query, (
                socio.nombre, socio.email, socio.telefono, socio.activo
            ))
            self.db_manager.commit()
            return cursor.lastrowid
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al crear socio: {e}")
            return None
    
    def buscar_por_id(self, id_socio: int) -> Optional[Socio]:
        """Buscar socio por ID"""
        query = "SELECT * FROM socios WHERE id_socio = ?"
        cursor = self.db_manager.execute_query(query, (id_socio,))
        row = cursor.fetchone()
        
        if row:
            return Socio(
                id_socio=row['id_socio'],
                nombre=row['nombre'],
                email=row['email'],
                telefono=row['telefono'],
                activo=bool(row['activo']),
                libros_prestados=row['libros_prestados']
            )
        return None
    
    def actualizar_libros_prestados(self, socio: Socio) -> bool:
        """Actualizar contador de libros prestados"""
        try:
            query = '''
                UPDATE socios 
                SET libros_prestados = ?
                WHERE id_socio = ?
            '''
            self.db_manager.execute_query(
                query,
                (socio.libros_prestados, socio.id_socio)
            )
            self.db_manager.commit()
            return True
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al actualizar libros prestados: {e}")
            return False


class RepositorioPrestamo:
    """Repositorio para gestionar préstamos"""
    
    def __init__(self):
        self.db_manager = DatabaseManager.get_instance()
        self.db_manager.connect()
    
    def crear(self, prestamo: Prestamo) -> Optional[int]:
        """Crear un nuevo préstamo"""
        try:
            query = '''
                INSERT INTO prestamos 
                (id_socio, isbn, fecha_devolucion_esperada, estado)
                VALUES (?, ?, ?, ?)
            '''
            cursor = self.db_manager.execute_query(query, (
                prestamo.socio.id_socio,
                prestamo.libro.isbn,
                prestamo.fecha_devolucion_esperada,
                prestamo.estado
            ))
            self.db_manager.commit()
            return cursor.lastrowid
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al crear préstamo: {e}")
            return None
    
    def actualizar_devolucion(self, prestamo: Prestamo) -> bool:
        """Actualizar préstamo con devolución"""
        try:
            multa = prestamo.calcular_multa()
            query = '''
                UPDATE prestamos
                SET fecha_devolucion_real = ?,
                    estado = ?,
                    multa = ?
                WHERE id_prestamo = ?
            '''
            self.db_manager.execute_query(query, (
                prestamo.fecha_devolucion_real,
                prestamo.estado,
                multa,
                prestamo.id_prestamo
            ))
            self.db_manager.commit()
            return True
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al actualizar devolución: {e}")
            return False


# servicios.py - Capa de Lógica de Negocio
class ServicioPrestamo:
    """Servicio que gestiona la lógica de negocio de préstamos"""
    
    def __init__(self):
        self.repo_libro = RepositorioLibro()
        self.repo_socio = RepositorioSocio()
        self.repo_prestamo = RepositorioPrestamo()
    
    def verificar_disponibilidad(self, isbn: str) -> bool:
        """Verifica si un libro está disponible"""
        libro = self.repo_libro.buscar_por_isbn(isbn)
        return libro is not None and libro.esta_disponible()
    
    def realizar_prestamo(self, id_socio: int, isbn: str) -> Optional[Prestamo]:
        """Realiza un préstamo de libro"""
        # 1. Buscar socio
        socio = self.repo_socio.buscar_por_id(id_socio)
        if not socio:
            print("Error: Socio no encontrado")
            return None
        
        # 2. Verificar si el socio puede realizar préstamo
        if not socio.puede_realizar_prestamo():
            print("Error: El socio no puede realizar más préstamos")
            return None
        
        # 3. Buscar libro
        libro = self.repo_libro.buscar_por_isbn(isbn)
        if not libro:
            print("Error: Libro no encontrado")
            return None
        
        # 4. Verificar disponibilidad
        if not libro.esta_disponible():
            print("Error: No hay ejemplares disponibles")
            return None
        
        # 5. Crear préstamo
        prestamo = Prestamo(
            id_prestamo=0,  # Se asignará al insertar
            socio=socio,
            libro=libro
        )
        
        id_prestamo = self.repo_prestamo.crear(prestamo)
        if not id_prestamo:
            print("Error: No se pudo registrar el préstamo")
            return None
        
        prestamo.id_prestamo = id_prestamo
        
        # 6. Actualizar disponibilidad del libro
        libro.ejemplares_disponibles -= 1
        self.repo_libro.actualizar_disponibilidad(libro)
        
        # 7. Actualizar contador de libros del socio
        socio.libros_prestados += 1
        self.repo_socio.actualizar_libros_prestados(socio)
        
        print(f"Préstamo realizado exitosamente: {prestamo}")
        return prestamo
    
    def registrar_devolucion(self, id_prestamo: int) -> bool:
        """Registra la devolución de un libro"""
        # En una implementación completa, buscaríamos el préstamo
        # Por simplicidad, asumimos que tenemos el objeto
        print(f"Devolución registrada para préstamo ID: {id_prestamo}")
        return True


# main.py - Ejemplo de uso
def main():
    print("=== SISTEMA DE GESTIÓN DE BIBLIOTECA ===\n")
    
    # Demostración del patrón Singleton
    print("1. Verificando patrón Singleton:")
    db1 = DatabaseManager.get_instance()
    db2 = DatabaseManager.get_instance()
    print(f"   db1 es db2: {db1 is db2}")  # Debe ser True
    print(f"   ID de db1: {id(db1)}")
    print(f"   ID de db2: {id(db2)}\n")
    
    # Crear repositorios
    repo_libro = RepositorioLibro()
    repo_socio = RepositorioSocio()
    servicio = ServicioPrestamo()
    
    # 2. Crear libros
    print("2. Creando libros en el catálogo:")
    libro1 = Libro(
        isbn="978-3-16-148410-0",
        titulo="Cien Años de Soledad",
        autor="Gabriel García Márquez",
        categoria="Literatura",
        total_ejemplares=3,
        ejemplares_disponibles=3
    )
    libro2 = Libro(
        isbn="978-0-7475-3269-9",
        titulo="Harry Potter y la Piedra Filosofal",
        autor="J.K. Rowling",
        categoria="Fantasía",
        total_ejemplares=5,
        ejemplares_disponibles=5
    )
    
    repo_libro.crear(libro1)
    repo_libro.crear(libro2)
    print(f"   Creado: {libro1}")
    print(f"   Creado: {libro2}\n")
    
    # 3. Crear socios
    print("3. Registrando socios:")
    socio1 = Socio(
        id_socio=0,
        nombre="Juan Pérez",
        email="juan.perez@email.com",
        telefono="123456789"
    )
    socio2 = Socio(
        id_socio=0,
        nombre="María González",
        email="maria.gonzalez@email.com",
        telefono="987654321"
    )
    
    id_socio1 = repo_socio.crear(socio1)
    id_socio2 = repo_socio.crear(socio2)
    socio1.id_socio = id_socio1
    socio2.id_socio = id_socio2
    print(f"   Registrado: {socio1}")
    print(f"   Registrado: {socio2}\n")
    
    # 4. Realizar préstamos
    print("4. Realizando préstamos:")
    prestamo1 = servicio.realizar_prestamo(
        id_socio=id_socio1,
        isbn="978-3-16-148410-0"
    )
    prestamo2 = servicio.realizar_prestamo(
        id_socio=id_socio2,
        isbn="978-0-7475-3269-9"
    )
    print()
    
    # 5. Verificar disponibilidad
    print("5. Verificando disponibilidad:")
    libro_actualizado = repo_libro.buscar_por_isbn("978-3-16-148410-0")
    print(f"   {libro_actualizado}\n")
    
    # 6. Listar libros disponibles
    print("6. Libros disponibles en el catálogo:")
    disponibles = repo_libro.listar_disponibles()
    for libro in disponibles:
        print(f"   - {libro}")
    print()
    
    # 7. Calcular multa (simulando retraso)
    print("7. Cálculo de multas:")
    print(f"   Préstamo sin retraso: Multa = ${prestamo1.calcular_multa()}")
    
    # Simular préstamo vencido
    from datetime import timedelta
    prestamo1.fecha_devolucion_esperada = date.today() - timedelta(days=5)
    multa = prestamo1.calcular_multa()
    print(f"   Préstamo con 5 días de retraso: Multa = ${multa}\n")
    
    print("=== FIN DE LA DEMOSTRACIÓN ===")


if __name__ == "__main__":
    main()
```

### Ejecución del Código

Para ejecutar la validación:

```bash
python src/main.py
```

### Salida Esperada

```
=== SISTEMA DE GESTIÓN DE BIBLIOTECA ===

1. Verificando patrón Singleton:
   db1 es db2: True
   ID de db1: 140234567890123
   ID de db2: 140234567890123

2. Creando libros en el catálogo:
   Creado: Libro(isbn='978-3-16-148410-0', titulo='Cien Años de Soledad', disponibles=3)
   Creado: Libro(isbn='978-0-7475-3269-9', titulo='Harry Potter y la Piedra Filosofal', disponibles=5)

3. Registrando socios:
   Registrado: Socio(id=1, nombre='Juan Pérez', prestados=0)
   Registrado: Socio(id=2, nombre='María González', prestados=0)

4. Realizando préstamos:
   Préstamo realizado exitosamente: Prestamo(id=1, libro='Cien Años de Soledad', socio='Juan Pérez', estado='activo')
   Préstamo realizado exitosamente: Prestamo(id=2, libro='Harry Potter y la Piedra Filosofal', socio='María González', estado='activo')

5. Verificando disponibilidad:
   Libro(isbn='978-3-16-148410-0', titulo='Cien Años de Soledad', disponibles=2)

6. Libros disponibles en el catálogo:
   - Libro(isbn='978-3-16-148410-0', titulo='Cien Años de Soledad', disponibles=2)
   - Libro(isbn='978-0-7475-3269-9', titulo='Harry Potter y la Piedra Filosofal', disponibles=4)

7. Cálculo de multas:
   Préstamo sin retraso: Multa = $0.0
   Préstamo con 5 días de retraso: Multa = $50.0

=== FIN DE LA DEMOSTRACIÓN ===
```

---

## Conclusión

Este diseño arquitectónico del sistema de gestión de biblioteca demuestra:

1. **Separación clara de responsabilidades** en tres capas (Presentación, Lógica de Negocio, Datos)
2. **Aplicación del patrón Singleton** para gestionar la conexión a la base de datos de forma centralizada y eficiente
3. **Implementación del patrón MVC** como arquitectura general del sistema
4. **Código funcional** que valida el diseño propuesto

El uso del patrón Singleton para `DatabaseManager` resuelve efectivamente el problema de acceso centralizado a la base de datos, garantizando:
- Una única instancia de conexión
- Thread-safety mediante locks
- Gestión eficiente de recursos
- Punto de acceso global y consistente

La arquitectura en capas facilita el mantenimiento, testing y escalabilidad del sistema.

---

## Implementación Práctica - Estructura de Carpetas

El código fuente implementa la arquitectura propuesta utilizando una estructura de carpetas bien organizada:

```
src/
├── model/                      # Modelos de Dominio
│   ├── __init__.py
│   ├── libro.py               # Clase Libro
│   ├── socio.py               # Clase Socio
│   └── prestamo.py            # Clase Prestamo
│
├── dal/                       # Data Access Layer (Singleton)
│   ├── __init__.py
│   └── database_manager.py   # Patrón Singleton para BD
│
├── repository/                # Capa de Repositorios
│   ├── __init__.py
│   ├── libro_repository.py   # CRUD de Libros
│   ├── socio_repository.py   # CRUD de Socios
│   └── prestamo_repository.py # CRUD de Préstamos
│
├── service/                   # Lógica de Negocio
│   ├── __init__.py
│   ├── libro_service.py      # Validaciones y reglas de Libros
│   ├── socio_service.py      # Validaciones y reglas de Socios
│   └── prestamo_service.py   # Validaciones y reglas de Préstamos
│
├── controller/                # Controladores
│   ├── __init__.py
│   ├── libro_controller.py   # Coordina operaciones de Libros
│   ├── socio_controller.py   # Coordina operaciones de Socios
│   └── prestamo_controller.py # Coordina operaciones de Préstamos
│
├── view/                      # Vista (Interfaz de Usuario)
│   ├── __init__.py
│   └── menu.py               # Menú interactivo completo
│
├── main.py                    # Punto de entrada del sistema
├── demo.py                    # Script de demostración
└── README.md                  # Documentación técnica
```

### Flujo de Ejecución (View → Controller → Service → Repository → DAL)

**Ejemplo: Realizar un Préstamo**

```
1. Usuario selecciona "Realizar préstamo" en el menú
   ↓
2. view/menu.py → Menu.realizar_prestamo()
   - Captura ID de socio e ISBN del libro
   ↓
3. controller/prestamo_controller.py → PrestamoController.realizar_prestamo()
   - Recibe la petición y coordina
   ↓
4. service/prestamo_service.py → PrestamoService.realizar_prestamo()
   - Valida que el socio esté activo
   - Valida que no exceda el límite de préstamos
   - Valida que el libro esté disponible
   - Aplica reglas de negocio
   ↓
5. repository/prestamo_repository.py → PrestamoRepository.crear()
   - Crea el registro del préstamo en BD
   ↓
6. dal/database_manager.py → DatabaseManager.execute_query()
   - Ejecuta la query SQL (única instancia - Singleton)
   ↓
7. Base de datos SQLite (biblioteca.db)
   - Persiste los datos
```

### Ejecución del Sistema

**Opción 1: Menú Interactivo**
```bash
cd src
python main.py
```

**Opción 2: Script de Demostración**
```bash
cd src
python demo.py
```

### Características Implementadas

✅ **Gestión de Libros**
- Registrar nuevos libros con ISBN, título, autor, categoría y ejemplares
- Listar todos los libros del catálogo
- Listar libros disponibles
- Buscar libros por ISBN
- Eliminar libros (con validación de ejemplares prestados)

✅ **Gestión de Socios**
- Registrar nuevos socios con validación de email
- Listar todos los socios
- Listar socios activos
- Buscar socios por ID
- Activar/Desactivar socios (con validación de préstamos)

✅ **Gestión de Préstamos**
- Realizar préstamos con validaciones completas
- Registrar devoluciones con cálculo de multas
- Listar préstamos activos con detección de vencidos

✅ **Reportes**
- Resumen general del sistema
- Estadísticas de libros, socios y préstamos

### Validaciones y Reglas de Negocio

**Libros:**
- ISBN único y obligatorio
- Al menos 1 ejemplar
- No se puede eliminar si tiene ejemplares prestados

**Socios:**
- Email único y con formato válido
- Máximo 3 libros prestados simultáneamente
- No se puede desactivar si tiene préstamos activos

**Préstamos:**
- Duración estándar: 14 días
- Multa: $10 por día de retraso
- Solo socios activos pueden realizar préstamos
- Solo libros con ejemplares disponibles

### Tecnologías Utilizadas

- **Lenguaje:** Python 3.7+
- **Base de Datos:** SQLite 3
- **Patrones de Diseño:**
  - Singleton (DatabaseManager)
  - Repository Pattern
  - MVC (Model-View-Controller)
- **Arquitectura:** Capas separadas (View, Controller, Service, Repository, DAL)

### Salida de la Demostración

```
╔══════════════════════════════════════════════════════════╗
║     DEMOSTRACIÓN: SISTEMA DE GESTIÓN DE BIBLIOTECA      ║
╚══════════════════════════════════════════════════════════╝

1. VERIFICANDO PATRÓN SINGLETON
   DatabaseManager 1: ID 1907452880144
   DatabaseManager 2: ID 1907452880144
   ¿Son la misma instancia? True
   ✓ Patrón Singleton funcionando correctamente

2. REGISTRANDO LIBROS EN EL CATÁLOGO
   ✓ 'Cien Años de Soledad' - Gabriel García Márquez (3 ejemplares)
   ✓ 'Harry Potter y la Piedra Filosofal' - J.K. Rowling (5 ejemplares)
   ✓ '1984' - George Orwell (2 ejemplares)
   ✓ 'El Señor de los Anillos' - J.R.R. Tolkien (4 ejemplares)

3. REGISTRANDO SOCIOS
   ✓ Juan Pérez - ID: 1
   ✓ María González - ID: 2
   ✓ Pedro Ramírez - ID: 3
   ✓ Ana López - ID: 4

... [más output] ...

✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE
```

