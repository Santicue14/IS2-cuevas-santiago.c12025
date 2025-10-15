"""
Servicio de lógica de negocio para Préstamos
"""
from typing import Optional, List
from model.prestamo import Prestamo
from repository.prestamo_repository import PrestamoRepository
from repository.libro_repository import LibroRepository
from repository.socio_repository import SocioRepository


class PrestamoService:
    """Servicio que gestiona la lógica de negocio de préstamos"""
    
    def __init__(self):
        self.repo_prestamo = PrestamoRepository()
        self.repo_libro = LibroRepository()
        self.repo_socio = SocioRepository()
    
    def realizar_prestamo(self, id_socio: int, isbn: str) -> Optional[Prestamo]:
        """Realiza un préstamo de libro"""
        # 1. Buscar socio
        socio = self.repo_socio.buscar_por_id(id_socio)
        if not socio:
            print("Error: Socio no encontrado")
            return None
        
        # 2. Verificar si el socio puede realizar préstamo
        if not socio.puede_realizar_prestamo():
            if not socio.activo:
                print("Error: El socio no está activo")
            else:
                print(f"Error: El socio ha alcanzado el límite de {socio.MAX_LIBROS_PERMITIDOS} libros")
            return None
        
        # 3. Buscar libro
        libro = self.repo_libro.buscar_por_isbn(isbn)
        if not libro:
            print("Error: Libro no encontrado")
            return None
        
        # 4. Verificar disponibilidad
        if not libro.esta_disponible():
            print("Error: No hay ejemplares disponibles de este libro")
            return None
        
        # 5. Crear préstamo
        prestamo = Prestamo(
            id_prestamo=0,  # Se asignará al insertar
            socio=socio,
            libro=libro
        )
        
        id_prestamo = self.repo_prestamo.crear(prestamo)
        if not id_prestamo:
            print("Error: No se pudo registrar el préstamo")
            return None
        
        prestamo.id_prestamo = id_prestamo
        
        # 6. Actualizar disponibilidad del libro
        libro.ejemplares_disponibles -= 1
        self.repo_libro.actualizar_disponibilidad(libro)
        
        # 7. Actualizar contador de libros del socio
        socio.libros_prestados += 1
        self.repo_socio.actualizar_libros_prestados(socio)
        
        print(f"✓ Préstamo realizado exitosamente")
        print(f"  ID Préstamo: {prestamo.id_prestamo}")
        print(f"  Fecha devolución: {prestamo.fecha_devolucion_esperada}")
        
        return prestamo
    
    def registrar_devolucion(self, id_prestamo: int) -> bool:
        """Registra la devolución de un libro"""
        # Buscar datos del préstamo
        query = "SELECT id_socio, isbn FROM prestamos WHERE id_prestamo = ? AND estado = 'activo'"
        cursor = self.repo_prestamo.db_manager.execute_query(query, (id_prestamo,))
        row = cursor.fetchone()
        
        if not row:
            print("Error: Préstamo no encontrado o ya fue devuelto")
            return False
        
        # Buscar socio y libro
        socio = self.repo_socio.buscar_por_id(row['id_socio'])
        libro = self.repo_libro.buscar_por_isbn(row['isbn'])
        
        if not socio or not libro:
            print("Error: Datos inconsistentes")
            return False
        
        # Buscar préstamo completo
        prestamo = self.repo_prestamo.buscar_por_id(id_prestamo, socio, libro)
        if not prestamo:
            print("Error: No se pudo recuperar el préstamo")
            return False
        
        # Registrar devolución
        prestamo.registrar_devolucion()
        
        # Actualizar en BD
        if not self.repo_prestamo.actualizar_devolucion(prestamo):
            return False
        
        # Actualizar disponibilidad del libro
        libro.ejemplares_disponibles += 1
        self.repo_libro.actualizar_disponibilidad(libro)
        
        # Actualizar contador de libros del socio
        socio.libros_prestados -= 1
        self.repo_socio.actualizar_libros_prestados(socio)
        
        # Mostrar información de multa si corresponde
        multa = prestamo.calcular_multa()
        print(f"✓ Devolución registrada exitosamente")
        if multa > 0:
            print(f"  ⚠ Multa por retraso: ${multa:.2f}")
        else:
            print(f"  Sin multas")
        
        return True
    
    def listar_prestamos_activos(self) -> List[dict]:
        """Listar todos los préstamos activos"""
        return self.repo_prestamo.listar_activos()
    
    def verificar_disponibilidad(self, isbn: str) -> bool:
        """Verifica si un libro está disponible"""
        libro = self.repo_libro.buscar_por_isbn(isbn)
        return libro is not None and libro.esta_disponible()

