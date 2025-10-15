"""
Controlador para gestionar operaciones de libros
"""
from service.libro_service import LibroService


class LibroController:
    """Controlador para coordinar operaciones de libros"""
    
    def __init__(self):
        self.service = LibroService()
    
    def crear_libro(self, isbn: str, titulo: str, autor: str, 
                   categoria: str = "", total_ejemplares: int = 1) -> bool:
        """Crear un nuevo libro"""
        return self.service.crear_libro(isbn, titulo, autor, categoria, total_ejemplares)
    
    def listar_todos(self):
        """Listar todos los libros"""
        return self.service.listar_todos_los_libros()
    
    def listar_disponibles(self):
        """Listar libros disponibles"""
        return self.service.listar_libros_disponibles()
    
    def buscar_libro(self, isbn: str):
        """Buscar libro por ISBN"""
        return self.service.buscar_libro(isbn)
    
    def eliminar_libro(self, isbn: str) -> bool:
        """Eliminar un libro"""
        return self.service.eliminar_libro(isbn)

