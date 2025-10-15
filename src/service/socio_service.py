"""
Servicio de lógica de negocio para Socios
"""
from typing import List, Optional
from model.socio import Socio
from repository.socio_repository import SocioRepository
import re


class SocioService:
    """Servicio que gestiona la lógica de negocio de socios"""
    
    def __init__(self):
        self.repo = SocioRepository()
    
    def _validar_email(self, email: str) -> bool:
        """Validar formato de email"""
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email) is not None
    
    def registrar_socio(self, nombre: str, email: str, telefono: str = "") -> Optional[int]:
        """Registrar un nuevo socio"""
        # Validaciones de negocio
        if not nombre or not email:
            print("Error: Nombre y email son obligatorios")
            return None
        
        if not self._validar_email(email):
            print("Error: Email inválido")
            return None
        
        # Crear socio
        socio = Socio(
            id_socio=0,  # Se asignará automáticamente
            nombre=nombre,
            email=email,
            telefono=telefono,
            activo=True,
            libros_prestados=0
        )
        
        id_socio = self.repo.crear(socio)
        if id_socio:
            print(f"Socio registrado exitosamente con ID: {id_socio}")
        
        return id_socio
    
    def buscar_socio(self, id_socio: int) -> Optional[Socio]:
        """Buscar socio por ID"""
        return self.repo.buscar_por_id(id_socio)
    
    def listar_todos_los_socios(self) -> List[Socio]:
        """Listar todos los socios"""
        return self.repo.listar_todos()
    
    def listar_socios_activos(self) -> List[Socio]:
        """Listar socios activos"""
        return self.repo.listar_activos()
    
    def desactivar_socio(self, id_socio: int) -> bool:
        """Desactivar un socio"""
        socio = self.repo.buscar_por_id(id_socio)
        if not socio:
            print(f"Error: No existe socio con ID {id_socio}")
            return False
        
        # Verificar que no tenga préstamos activos
        if socio.libros_prestados > 0:
            print("Error: No se puede desactivar un socio con préstamos activos")
            return False
        
        return self.repo.actualizar_estado(id_socio, False)
    
    def activar_socio(self, id_socio: int) -> bool:
        """Activar un socio"""
        socio = self.repo.buscar_por_id(id_socio)
        if not socio:
            print(f"Error: No existe socio con ID {id_socio}")
            return False
        
        return self.repo.actualizar_estado(id_socio, True)

