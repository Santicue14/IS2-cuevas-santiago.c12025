"""
Data Access Layer - Patrón Singleton para gestión de base de datos
"""
import sqlite3
import threading
from typing import Any, Tuple


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

