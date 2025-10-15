"""
Modelo de dominio: Libro
"""


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
               f"disponibles={self.ejemplares_disponibles}/{self.total_ejemplares})"
    
    def __str__(self):
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn})"

