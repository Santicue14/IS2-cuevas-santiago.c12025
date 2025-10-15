"""
Controlador para gestionar operaciones de socios
"""
from service.socio_service import SocioService


class SocioController:
    """Controlador para coordinar operaciones de socios"""
    
    def __init__(self):
        self.service = SocioService()
    
    def registrar_socio(self, nombre: str, email: str, telefono: str = ""):
        """Registrar un nuevo socio"""
        return self.service.registrar_socio(nombre, email, telefono)
    
    def listar_todos(self):
        """Listar todos los socios"""
        return self.service.listar_todos_los_socios()
    
    def listar_activos(self):
        """Listar socios activos"""
        return self.service.listar_socios_activos()
    
    def buscar_socio(self, id_socio: int):
        """Buscar socio por ID"""
        return self.service.buscar_socio(id_socio)
    
    def desactivar_socio(self, id_socio: int) -> bool:
        """Desactivar un socio"""
        return self.service.desactivar_socio(id_socio)
    
    def activar_socio(self, id_socio: int) -> bool:
        """Activar un socio"""
        return self.service.activar_socio(id_socio)

