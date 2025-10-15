"""
Modelo de dominio: Préstamo
"""
from datetime import date, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .socio import Socio
    from .libro import Libro


class Prestamo:
    """Clase que representa un préstamo de libro"""
    
    DIAS_PRESTAMO = 14
    MULTA_POR_DIA = 10.0  # Multa en pesos por día de retraso
    
    def __init__(self, id_prestamo: int, socio: 'Socio', libro: 'Libro',
                 fecha_prestamo: date = None,
                 fecha_devolucion_esperada: date = None,
                 fecha_devolucion_real: date = None,
                 estado: str = "activo"):
        self.id_prestamo = id_prestamo
        self.socio = socio
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo or date.today()
        self.fecha_devolucion_esperada = (
            fecha_devolucion_esperada or 
            self.fecha_prestamo + timedelta(days=self.DIAS_PRESTAMO)
        )
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado = estado
    
    def esta_vencido(self) -> bool:
        """Verifica si el préstamo está vencido"""
        if self.estado == "devuelto":
            return False
        return date.today() > self.fecha_devolucion_esperada
    
    def calcular_multa(self) -> float:
        """Calcula la multa por retraso"""
        if not self.fecha_devolucion_real:
            fecha_referencia = date.today()
        else:
            fecha_referencia = self.fecha_devolucion_real
        
        if fecha_referencia <= self.fecha_devolucion_esperada:
            return 0.0
        
        dias_retraso = (fecha_referencia - 
                       self.fecha_devolucion_esperada).days
        return dias_retraso * self.MULTA_POR_DIA
    
    def registrar_devolucion(self):
        """Registra la devolución del libro"""
        self.fecha_devolucion_real = date.today()
        self.estado = "devuelto"
    
    def __repr__(self):
        return f"Prestamo(id={self.id_prestamo}, libro='{self.libro.titulo}', " \
               f"socio='{self.socio.nombre}', estado='{self.estado}')"
    
    def __str__(self):
        multa = self.calcular_multa()
        multa_str = f" - Multa: ${multa:.2f}" if multa > 0 else ""
        return f"[{self.id_prestamo}] {self.libro.titulo} -> {self.socio.nombre} " \
               f"(Vence: {self.fecha_devolucion_esperada}){multa_str}"

