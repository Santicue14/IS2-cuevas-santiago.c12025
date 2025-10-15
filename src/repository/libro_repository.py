"""
Repositorio para gestionar libros en la base de datos
"""
from typing import List, Optional
from model.libro import Libro
from dal.database_manager import DatabaseManager


class LibroRepository:
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
    
    def listar_todos(self) -> List[Libro]:
        """Listar todos los libros"""
        query = "SELECT * FROM libros ORDER BY titulo"
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
    
    def listar_disponibles(self) -> List[Libro]:
        """Listar libros disponibles"""
        query = "SELECT * FROM libros WHERE ejemplares_disponibles > 0 ORDER BY titulo"
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
    
    def eliminar(self, isbn: str) -> bool:
        """Eliminar un libro"""
        try:
            query = "DELETE FROM libros WHERE isbn = ?"
            self.db_manager.execute_query(query, (isbn,))
            self.db_manager.commit()
            return True
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al eliminar libro: {e}")
            return False

