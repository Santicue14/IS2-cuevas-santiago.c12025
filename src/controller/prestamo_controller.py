"""
Controlador para gestionar operaciones de préstamos
"""
from service.prestamo_service import PrestamoService


class PrestamoController:
    """Controlador para coordinar operaciones de préstamos"""
    
    def __init__(self):
        self.service = PrestamoService()
    
    def realizar_prestamo(self, id_socio: int, isbn: str):
        """Realizar un préstamo"""
        return self.service.realizar_prestamo(id_socio, isbn)
    
    def registrar_devolucion(self, id_prestamo: int) -> bool:
        """Registrar devolución de un libro"""
        return self.service.registrar_devolucion(id_prestamo)
    
    def listar_prestamos_activos(self):
        """Listar préstamos activos"""
        return self.service.listar_prestamos_activos()
    
    def verificar_disponibilidad(self, isbn: str) -> bool:
        """Verificar disponibilidad de un libro"""
        return self.service.verificar_disponibilidad(isbn)

