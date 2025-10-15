"""
Servicio de lógica de negocio para Libros
"""
from typing import List, Optional
from model.libro import Libro
from repository.libro_repository import LibroRepository


class LibroService:
    """Servicio que gestiona la lógica de negocio de libros"""
    
    def __init__(self):
        self.repo = LibroRepository()
    
    def crear_libro(self, isbn: str, titulo: str, autor: str, 
                   categoria: str = "", total_ejemplares: int = 1) -> bool:
        """Crear un nuevo libro"""
        # Validaciones de negocio
        if not isbn or not titulo or not autor:
            print("Error: ISBN, título y autor son obligatorios")
            return False
        
        if total_ejemplares < 1:
            print("Error: Debe haber al menos un ejemplar")
            return False
        
        # Verificar que no exista
        libro_existente = self.repo.buscar_por_isbn(isbn)
        if libro_existente:
            print(f"Error: Ya existe un libro con ISBN {isbn}")
            return False
        
        # Crear libro
        libro = Libro(
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            categoria=categoria,
            total_ejemplares=total_ejemplares,
            ejemplares_disponibles=total_ejemplares
        )
        
        return self.repo.crear(libro)
    
    def buscar_libro(self, isbn: str) -> Optional[Libro]:
        """Buscar libro por ISBN"""
        return self.repo.buscar_por_isbn(isbn)
    
    def listar_todos_los_libros(self) -> List[Libro]:
        """Listar todos los libros"""
        return self.repo.listar_todos()
    
    def listar_libros_disponibles(self) -> List[Libro]:
        """Listar libros con ejemplares disponibles"""
        return self.repo.listar_disponibles()
    
    def eliminar_libro(self, isbn: str) -> bool:
        """Eliminar un libro"""
        libro = self.repo.buscar_por_isbn(isbn)
        if not libro:
            print(f"Error: No existe libro con ISBN {isbn}")
            return False
        
        # Verificar que no tenga ejemplares prestados
        if libro.ejemplares_disponibles < libro.total_ejemplares:
            print("Error: No se puede eliminar un libro con ejemplares prestados")
            return False
        
        return self.repo.eliminar(isbn)

