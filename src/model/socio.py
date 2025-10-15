"""
Modelo de dominio: Socio
"""
from datetime import date


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
        """Verifica si tiene multas pendientes"""
        # Esta lógica se implementaría consultando la BD
        return False
    
    def __repr__(self):
        return f"Socio(id={self.id_socio}, nombre='{self.nombre}', " \
               f"prestados={self.libros_prestados})"
    
    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"[{self.id_socio}] {self.nombre} - {self.email} ({estado})"

