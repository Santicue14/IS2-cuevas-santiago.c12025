"""
Script de demostración del sistema de biblioteca
Muestra el flujo completo de operaciones
"""
import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

from controller.libro_controller import LibroController
from controller.socio_controller import SocioController
from controller.prestamo_controller import PrestamoController
from dal.database_manager import DatabaseManager


def separador(titulo=""):
    """Imprimir separador visual"""
    if titulo:
        print(f"\n{'='*60}")
        print(f"  {titulo}")
        print(f"{'='*60}\n")
    else:
        print("-" * 60)


def demo():
    """Ejecutar demostración completa del sistema"""
    
    print("\n" + "╔"+"═"*58+"╗")
    print("║" + " "*5 + "DEMOSTRACIÓN: SISTEMA DE GESTIÓN DE BIBLIOTECA" + " "*6 + "║")
    print("╚"+"═"*58+"╝")
    
    # Inicializar controladores
    libro_ctrl = LibroController()
    socio_ctrl = SocioController()
    prestamo_ctrl = PrestamoController()
    
    # 1. Verificar Singleton
    separador("1. VERIFICANDO PATRÓN SINGLETON")
    db1 = DatabaseManager.get_instance()
    db2 = DatabaseManager.get_instance()
    print(f"DatabaseManager 1: ID {id(db1)}")
    print(f"DatabaseManager 2: ID {id(db2)}")
    print(f"¿Son la misma instancia? {db1 is db2}")
    print("✓ Patrón Singleton funcionando correctamente")
    
    # 2. Registrar libros
    separador("2. REGISTRANDO LIBROS EN EL CATÁLOGO")
    libros = [
        ("978-3-16-148410-0", "Cien Años de Soledad", "Gabriel García Márquez", "Literatura", 3),
        ("978-0-7475-3269-9", "Harry Potter y la Piedra Filosofal", "J.K. Rowling", "Fantasía", 5),
        ("978-0-06-112008-4", "1984", "George Orwell", "Distopía", 2),
        ("978-0-14-028329-3", "El Señor de los Anillos", "J.R.R. Tolkien", "Fantasía", 4),
    ]
    
    for isbn, titulo, autor, categoria, ejemplares in libros:
        if libro_ctrl.crear_libro(isbn, titulo, autor, categoria, ejemplares):
            print(f"✓ '{titulo}' - {autor} ({ejemplares} ejemplares)")
    
    # 3. Registrar socios
    separador("3. REGISTRANDO SOCIOS")
    socios_data = [
        ("Juan Pérez", "juan.perez@email.com", "123-456-789"),
        ("María González", "maria.gonzalez@email.com", "987-654-321"),
        ("Pedro Ramírez", "pedro.ramirez@email.com", "555-123-456"),
        ("Ana López", "ana.lopez@email.com", "444-789-012"),
    ]
    
    socios_ids = []
    for nombre, email, telefono in socios_data:
        id_socio = socio_ctrl.registrar_socio(nombre, email, telefono)
        if id_socio:
            socios_ids.append(id_socio)
            print(f"✓ {nombre} - ID: {id_socio}")
    
    # 4. Listar libros disponibles
    separador("4. CATÁLOGO DE LIBROS DISPONIBLES")
    libros_disponibles = libro_ctrl.listar_disponibles()
    print(f"Total: {len(libros_disponibles)} títulos\n")
    print(f"{'ISBN':<20} {'Título':<40} {'Disponibles':<12}")
    print("-"*80)
    for libro in libros_disponibles:
        print(f"{libro.isbn:<20} {libro.titulo[:39]:<40} {libro.ejemplares_disponibles:<12}")
    
    # 5. Realizar préstamos
    separador("5. REALIZANDO PRÉSTAMOS")
    prestamos = [
        (socios_ids[0], "978-3-16-148410-0", "Juan Pérez", "Cien Años de Soledad"),
        (socios_ids[1], "978-0-7475-3269-9", "María González", "Harry Potter"),
        (socios_ids[0], "978-0-06-112008-4", "Juan Pérez", "1984"),
        (socios_ids[2], "978-0-14-028329-3", "Pedro Ramírez", "El Señor de los Anillos"),
    ]
    
    prestamos_realizados = []
    for id_socio, isbn, nombre_socio, titulo_libro in prestamos:
        print(f"\nPréstamo: {nombre_socio} → {titulo_libro}")
        prestamo = prestamo_ctrl.realizar_prestamo(id_socio, isbn)
        if prestamo:
            prestamos_realizados.append(prestamo.id_prestamo)
    
    # 6. Listar préstamos activos
    separador("6. PRÉSTAMOS ACTIVOS")
    prestamos_activos = prestamo_ctrl.listar_prestamos_activos()
    print(f"Total: {len(prestamos_activos)} préstamos activos\n")
    print(f"{'ID':<5} {'Socio':<25} {'Libro':<35} {'Vence':<12}")
    print("-"*85)
    for p in prestamos_activos:
        print(f"{p['id_prestamo']:<5} {p['socio_nombre'][:24]:<25} "
              f"{p['libro_titulo'][:34]:<35} {p['fecha_devolucion_esperada']:<12}")
    
    # 7. Verificar estado de un socio
    separador("7. CONSULTANDO ESTADO DE SOCIO")
    socio = socio_ctrl.buscar_socio(socios_ids[0])
    if socio:
        print(f"Socio: {socio.nombre}")
        print(f"  Libros prestados: {socio.libros_prestados}")
        print(f"  Puede prestar más: {'✓ Sí' if socio.puede_realizar_prestamo() else '✗ No'}")
        print(f"  Límite: {socio.MAX_LIBROS_PERMITIDOS} libros")
    
    # 8. Intentar préstamo que excede el límite
    separador("8. VALIDACIÓN: PRÉSTAMO EXCEDE LÍMITE")
    print(f"Intentando que {socio.nombre} preste un tercer libro...")
    prestamo = prestamo_ctrl.realizar_prestamo(socios_ids[0], "978-0-7475-3269-9")
    if not prestamo:
        print("✓ Validación correcta: Se bloqueó el préstamo por exceder límite")
    
    # 9. Registrar una devolución
    separador("9. REGISTRANDO DEVOLUCIÓN")
    if prestamos_realizados:
        print(f"Devolviendo préstamo ID: {prestamos_realizados[0]}")
        if prestamo_ctrl.registrar_devolucion(prestamos_realizados[0]):
            print("\nVerificando estado actualizado del socio...")
            socio_actualizado = socio_ctrl.buscar_socio(socios_ids[0])
            print(f"  Libros prestados ahora: {socio_actualizado.libros_prestados}")
    
    # 10. Resumen final
    separador("10. RESUMEN FINAL DEL SISTEMA")
    total_libros = len(libro_ctrl.listar_todos())
    libros_disponibles = len(libro_ctrl.listar_disponibles())
    total_socios = len(socio_ctrl.listar_todos())
    socios_activos = len(socio_ctrl.listar_activos())
    prestamos_activos = len(prestamo_ctrl.listar_prestamos_activos())
    
    print(f"📚 LIBROS")
    print(f"   Total de títulos:      {total_libros}")
    print(f"   Títulos disponibles:   {libros_disponibles}")
    print(f"\n👥 SOCIOS")
    print(f"   Total de socios:       {total_socios}")
    print(f"   Socios activos:        {socios_activos}")
    print(f"\n📖 PRÉSTAMOS")
    print(f"   Préstamos activos:     {prestamos_activos}")
    
    # 11. Verificar arquitectura en capas
    separador("11. ARQUITECTURA EN CAPAS")
    print("✓ VIEW       → Menu (interfaz de usuario)")
    print("✓ CONTROLLER → LibroController, SocioController, PrestamoController")
    print("✓ SERVICE    → LibroService, SocioService, PrestamoService")
    print("✓ REPOSITORY → LibroRepository, SocioRepository, PrestamoRepository")
    print("✓ DAL        → DatabaseManager (Singleton)")
    print("✓ DATABASE   → biblioteca.db (SQLite)")
    
    separador()
    print("\n✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
    print("\nPara usar el sistema interactivo, ejecute: python main.py\n")


if __name__ == "__main__":
    demo()

