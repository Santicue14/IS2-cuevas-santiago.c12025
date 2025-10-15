"""
Repositorio para gestionar socios en la base de datos
"""
from typing import List, Optional
from model.socio import Socio
from dal.database_manager import DatabaseManager


class SocioRepository:
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
    
    def listar_todos(self) -> List[Socio]:
        """Listar todos los socios"""
        query = "SELECT * FROM socios ORDER BY nombre"
        cursor = self.db_manager.execute_query(query)
        
        socios = []
        for row in cursor.fetchall():
            socios.append(Socio(
                id_socio=row['id_socio'],
                nombre=row['nombre'],
                email=row['email'],
                telefono=row['telefono'],
                activo=bool(row['activo']),
                libros_prestados=row['libros_prestados']
            ))
        return socios
    
    def listar_activos(self) -> List[Socio]:
        """Listar socios activos"""
        query = "SELECT * FROM socios WHERE activo = 1 ORDER BY nombre"
        cursor = self.db_manager.execute_query(query)
        
        socios = []
        for row in cursor.fetchall():
            socios.append(Socio(
                id_socio=row['id_socio'],
                nombre=row['nombre'],
                email=row['email'],
                telefono=row['telefono'],
                activo=bool(row['activo']),
                libros_prestados=row['libros_prestados']
            ))
        return socios
    
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
    
    def actualizar_estado(self, id_socio: int, activo: bool) -> bool:
        """Actualizar estado de un socio"""
        try:
            query = "UPDATE socios SET activo = ? WHERE id_socio = ?"
            self.db_manager.execute_query(query, (activo, id_socio))
            self.db_manager.commit()
            return True
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al actualizar estado: {e}")
            return False

