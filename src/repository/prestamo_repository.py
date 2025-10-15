"""
Repositorio para gestionar préstamos en la base de datos
"""
from typing import List, Optional
from datetime import datetime
from model.prestamo import Prestamo
from model.socio import Socio
from model.libro import Libro
from dal.database_manager import DatabaseManager


class PrestamoRepository:
    """Repositorio para gestionar préstamos"""
    
    def __init__(self):
        self.db_manager = DatabaseManager.get_instance()
        self.db_manager.connect()
    
    def crear(self, prestamo: Prestamo) -> Optional[int]:
        """Crear un nuevo préstamo"""
        try:
            query = '''
                INSERT INTO prestamos 
                (id_socio, isbn, fecha_prestamo, fecha_devolucion_esperada, estado)
                VALUES (?, ?, ?, ?, ?)
            '''
            cursor = self.db_manager.execute_query(query, (
                prestamo.socio.id_socio,
                prestamo.libro.isbn,
                prestamo.fecha_prestamo.isoformat(),
                prestamo.fecha_devolucion_esperada.isoformat(),
                prestamo.estado
            ))
            self.db_manager.commit()
            return cursor.lastrowid
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al crear préstamo: {e}")
            return None
    
    def buscar_por_id(self, id_prestamo: int, socio: Socio, libro: Libro) -> Optional[Prestamo]:
        """Buscar préstamo por ID"""
        query = "SELECT * FROM prestamos WHERE id_prestamo = ?"
        cursor = self.db_manager.execute_query(query, (id_prestamo,))
        row = cursor.fetchone()
        
        if row:
            fecha_devolucion_real = None
            if row['fecha_devolucion_real']:
                fecha_devolucion_real = datetime.fromisoformat(row['fecha_devolucion_real']).date()
            
            return Prestamo(
                id_prestamo=row['id_prestamo'],
                socio=socio,
                libro=libro,
                fecha_prestamo=datetime.fromisoformat(row['fecha_prestamo']).date(),
                fecha_devolucion_esperada=datetime.fromisoformat(row['fecha_devolucion_esperada']).date(),
                fecha_devolucion_real=fecha_devolucion_real,
                estado=row['estado']
            )
        return None
    
    def listar_activos(self) -> List[tuple]:
        """Listar préstamos activos (devuelve tuplas de datos básicos)"""
        query = '''
            SELECT p.id_prestamo, p.id_socio, p.isbn, p.fecha_prestamo,
                   p.fecha_devolucion_esperada, p.estado,
                   s.nombre as socio_nombre, l.titulo as libro_titulo
            FROM prestamos p
            JOIN socios s ON p.id_socio = s.id_socio
            JOIN libros l ON p.isbn = l.isbn
            WHERE p.estado = 'activo'
            ORDER BY p.fecha_devolucion_esperada
        '''
        cursor = self.db_manager.execute_query(query)
        
        prestamos = []
        for row in cursor.fetchall():
            prestamos.append({
                'id_prestamo': row['id_prestamo'],
                'id_socio': row['id_socio'],
                'isbn': row['isbn'],
                'socio_nombre': row['socio_nombre'],
                'libro_titulo': row['libro_titulo'],
                'fecha_prestamo': datetime.fromisoformat(row['fecha_prestamo']).date(),
                'fecha_devolucion_esperada': datetime.fromisoformat(row['fecha_devolucion_esperada']).date(),
                'estado': row['estado']
            })
        return prestamos
    
    def actualizar_devolucion(self, prestamo: Prestamo) -> bool:
        """Actualizar préstamo con devolución"""
        try:
            multa = prestamo.calcular_multa()
            query = '''
                UPDATE prestamos
                SET fecha_devolucion_real = ?,
                    estado = ?,
                    multa = ?
                WHERE id_prestamo = ?
            '''
            self.db_manager.execute_query(query, (
                prestamo.fecha_devolucion_real.isoformat(),
                prestamo.estado,
                multa,
                prestamo.id_prestamo
            ))
            self.db_manager.commit()
            return True
        except Exception as e:
            self.db_manager.rollback()
            print(f"Error al actualizar devolución: {e}")
            return False
    
    def contar_prestamos_activos_por_socio(self, id_socio: int) -> int:
        """Contar préstamos activos de un socio"""
        query = "SELECT COUNT(*) as total FROM prestamos WHERE id_socio = ? AND estado = 'activo'"
        cursor = self.db_manager.execute_query(query, (id_socio,))
        row = cursor.fetchone()
        return row['total'] if row else 0

