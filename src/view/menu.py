"""
Vista - Menú principal del sistema de biblioteca
"""
import os
from datetime import date
from controller.libro_controller import LibroController
from controller.socio_controller import SocioController
from controller.prestamo_controller import PrestamoController


class Menu:
    """Clase que gestiona el menú de usuario"""
    
    def __init__(self):
        self.libro_controller = LibroController()
        self.socio_controller = SocioController()
        self.prestamo_controller = PrestamoController()
    
    def limpiar_pantalla(self):
        """Limpiar la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausar(self):
        """Pausar y esperar Enter"""
        input("\nPresione Enter para continuar...")
    
    def mostrar_titulo(self, titulo: str):
        """Mostrar título de sección"""
        print("\n" + "="*60)
        print(f"  {titulo}")
        print("="*60)
    
    # ==================== MENÚ PRINCIPAL ====================
    
    def mostrar_menu_principal(self):
        """Mostrar menú principal"""
        self.limpiar_pantalla()
        print("\n" + "╔"+"═"*58+"╗")
        print("║" + " "*10 + "SISTEMA DE GESTIÓN DE BIBLIOTECA" + " "*16 + "║")
        print("╚"+"═"*58+"╝")
        print("\n┌─ MENÚ PRINCIPAL ─────────────────────────────────────────┐")
        print("│                                                          │")
        print("│  1. Gestión de Libros                                    │")
        print("│  2. Gestión de Socios                                    │")
        print("│  3. Gestión de Préstamos                                 │")
        print("│  4. Reportes                                             │")
        print("│  0. Salir                                                │")
        print("│                                                          │")
        print("└──────────────────────────────────────────────────────────┘")
    
    # ==================== GESTIÓN DE LIBROS ====================
    
    def menu_libros(self):
        """Menú de gestión de libros"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo("GESTIÓN DE LIBROS")
            print("\n1. Registrar nuevo libro")
            print("2. Listar todos los libros")
            print("3. Listar libros disponibles")
            print("4. Buscar libro por ISBN")
            print("5. Eliminar libro")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_libro()
            elif opcion == "2":
                self.listar_todos_libros()
            elif opcion == "3":
                self.listar_libros_disponibles()
            elif opcion == "4":
                self.buscar_libro()
            elif opcion == "5":
                self.eliminar_libro()
            elif opcion == "0":
                break
            else:
                print("Opción inválida")
                self.pausar()
    
    def registrar_libro(self):
        """Registrar un nuevo libro"""
        self.mostrar_titulo("REGISTRAR NUEVO LIBRO")
        
        isbn = input("\nISBN: ").strip()
        if not isbn:
            print("Error: ISBN es obligatorio")
            self.pausar()
            return
        
        titulo = input("Título: ").strip()
        if not titulo:
            print("Error: Título es obligatorio")
            self.pausar()
            return
        
        autor = input("Autor: ").strip()
        if not autor:
            print("Error: Autor es obligatorio")
            self.pausar()
            return
        
        categoria = input("Categoría (opcional): ").strip()
        
        try:
            total_ejemplares = int(input("Número de ejemplares (default 1): ").strip() or "1")
            if total_ejemplares < 1:
                print("Error: Debe haber al menos un ejemplar")
                self.pausar()
                return
        except ValueError:
            print("Error: Número inválido")
            self.pausar()
            return
        
        if self.libro_controller.crear_libro(isbn, titulo, autor, categoria, total_ejemplares):
            print("\n✓ Libro registrado exitosamente")
        else:
            print("\n✗ No se pudo registrar el libro")
        
        self.pausar()
    
    def listar_todos_libros(self):
        """Listar todos los libros"""
        self.mostrar_titulo("LISTADO DE TODOS LOS LIBROS")
        
        libros = self.libro_controller.listar_todos()
        
        if not libros:
            print("\nNo hay libros registrados")
        else:
            print(f"\nTotal de libros: {len(libros)}\n")
            print(f"{'ISBN':<20} {'Título':<30} {'Autor':<25} {'Disp/Total':<10}")
            print("-"*90)
            for libro in libros:
                print(f"{libro.isbn:<20} {libro.titulo[:29]:<30} {libro.autor[:24]:<25} "
                      f"{libro.ejemplares_disponibles}/{libro.total_ejemplares:<10}")
        
        self.pausar()
    
    def listar_libros_disponibles(self):
        """Listar libros disponibles"""
        self.mostrar_titulo("LIBROS DISPONIBLES")
        
        libros = self.libro_controller.listar_disponibles()
        
        if not libros:
            print("\nNo hay libros disponibles en este momento")
        else:
            print(f"\nLibros disponibles: {len(libros)}\n")
            print(f"{'ISBN':<20} {'Título':<30} {'Autor':<25} {'Disponibles':<12}")
            print("-"*90)
            for libro in libros:
                print(f"{libro.isbn:<20} {libro.titulo[:29]:<30} {libro.autor[:24]:<25} "
                      f"{libro.ejemplares_disponibles:<12}")
        
        self.pausar()
    
    def buscar_libro(self):
        """Buscar libro por ISBN"""
        self.mostrar_titulo("BUSCAR LIBRO")
        
        isbn = input("\nIngrese ISBN: ").strip()
        libro = self.libro_controller.buscar_libro(isbn)
        
        if libro:
            print("\n✓ Libro encontrado:")
            print(f"\n  ISBN:              {libro.isbn}")
            print(f"  Título:            {libro.titulo}")
            print(f"  Autor:             {libro.autor}")
            print(f"  Categoría:         {libro.categoria or 'N/A'}")
            print(f"  Total ejemplares:  {libro.total_ejemplares}")
            print(f"  Disponibles:       {libro.ejemplares_disponibles}")
            print(f"  Estado:            {'✓ Disponible' if libro.esta_disponible() else '✗ No disponible'}")
        else:
            print(f"\n✗ No se encontró libro con ISBN: {isbn}")
        
        self.pausar()
    
    def eliminar_libro(self):
        """Eliminar un libro"""
        self.mostrar_titulo("ELIMINAR LIBRO")
        
        isbn = input("\nIngrese ISBN del libro a eliminar: ").strip()
        
        # Mostrar libro primero
        libro = self.libro_controller.buscar_libro(isbn)
        if not libro:
            print(f"\n✗ No se encontró libro con ISBN: {isbn}")
            self.pausar()
            return
        
        print(f"\nLibro: {libro.titulo} - {libro.autor}")
        confirmacion = input("¿Está seguro de eliminar este libro? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            if self.libro_controller.eliminar_libro(isbn):
                print("\n✓ Libro eliminado exitosamente")
            else:
                print("\n✗ No se pudo eliminar el libro")
        else:
            print("\nOperación cancelada")
        
        self.pausar()
    
    # ==================== GESTIÓN DE SOCIOS ====================
    
    def menu_socios(self):
        """Menú de gestión de socios"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo("GESTIÓN DE SOCIOS")
            print("\n1. Registrar nuevo socio")
            print("2. Listar todos los socios")
            print("3. Listar socios activos")
            print("4. Buscar socio por ID")
            print("5. Desactivar socio")
            print("6. Activar socio")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_socio()
            elif opcion == "2":
                self.listar_todos_socios()
            elif opcion == "3":
                self.listar_socios_activos()
            elif opcion == "4":
                self.buscar_socio()
            elif opcion == "5":
                self.desactivar_socio()
            elif opcion == "6":
                self.activar_socio()
            elif opcion == "0":
                break
            else:
                print("Opción inválida")
                self.pausar()
    
    def registrar_socio(self):
        """Registrar un nuevo socio"""
        self.mostrar_titulo("REGISTRAR NUEVO SOCIO")
        
        nombre = input("\nNombre completo: ").strip()
        if not nombre:
            print("Error: Nombre es obligatorio")
            self.pausar()
            return
        
        email = input("Email: ").strip()
        if not email:
            print("Error: Email es obligatorio")
            self.pausar()
            return
        
        telefono = input("Teléfono (opcional): ").strip()
        
        id_socio = self.socio_controller.registrar_socio(nombre, email, telefono)
        
        if id_socio:
            print(f"\n✓ Socio registrado exitosamente con ID: {id_socio}")
        else:
            print("\n✗ No se pudo registrar el socio")
        
        self.pausar()
    
    def listar_todos_socios(self):
        """Listar todos los socios"""
        self.mostrar_titulo("LISTADO DE TODOS LOS SOCIOS")
        
        socios = self.socio_controller.listar_todos()
        
        if not socios:
            print("\nNo hay socios registrados")
        else:
            print(f"\nTotal de socios: {len(socios)}\n")
            print(f"{'ID':<5} {'Nombre':<30} {'Email':<30} {'Estado':<10} {'Préstamos':<10}")
            print("-"*90)
            for socio in socios:
                estado = "Activo" if socio.activo else "Inactivo"
                print(f"{socio.id_socio:<5} {socio.nombre[:29]:<30} {socio.email[:29]:<30} "
                      f"{estado:<10} {socio.libros_prestados:<10}")
        
        self.pausar()
    
    def listar_socios_activos(self):
        """Listar socios activos"""
        self.mostrar_titulo("SOCIOS ACTIVOS")
        
        socios = self.socio_controller.listar_activos()
        
        if not socios:
            print("\nNo hay socios activos")
        else:
            print(f"\nSocios activos: {len(socios)}\n")
            print(f"{'ID':<5} {'Nombre':<30} {'Email':<30} {'Préstamos':<10}")
            print("-"*80)
            for socio in socios:
                print(f"{socio.id_socio:<5} {socio.nombre[:29]:<30} {socio.email[:29]:<30} "
                      f"{socio.libros_prestados:<10}")
        
        self.pausar()
    
    def buscar_socio(self):
        """Buscar socio por ID"""
        self.mostrar_titulo("BUSCAR SOCIO")
        
        try:
            id_socio = int(input("\nIngrese ID del socio: ").strip())
        except ValueError:
            print("Error: ID inválido")
            self.pausar()
            return
        
        socio = self.socio_controller.buscar_socio(id_socio)
        
        if socio:
            print("\n✓ Socio encontrado:")
            print(f"\n  ID:                {socio.id_socio}")
            print(f"  Nombre:            {socio.nombre}")
            print(f"  Email:             {socio.email}")
            print(f"  Teléfono:          {socio.telefono or 'N/A'}")
            print(f"  Estado:            {'Activo' if socio.activo else 'Inactivo'}")
            print(f"  Libros prestados:  {socio.libros_prestados}")
            print(f"  Puede prestar:     {'✓ Sí' if socio.puede_realizar_prestamo() else '✗ No'}")
        else:
            print(f"\n✗ No se encontró socio con ID: {id_socio}")
        
        self.pausar()
    
    def desactivar_socio(self):
        """Desactivar un socio"""
        self.mostrar_titulo("DESACTIVAR SOCIO")
        
        try:
            id_socio = int(input("\nIngrese ID del socio a desactivar: ").strip())
        except ValueError:
            print("Error: ID inválido")
            self.pausar()
            return
        
        if self.socio_controller.desactivar_socio(id_socio):
            print("\n✓ Socio desactivado exitosamente")
        else:
            print("\n✗ No se pudo desactivar el socio")
        
        self.pausar()
    
    def activar_socio(self):
        """Activar un socio"""
        self.mostrar_titulo("ACTIVAR SOCIO")
        
        try:
            id_socio = int(input("\nIngrese ID del socio a activar: ").strip())
        except ValueError:
            print("Error: ID inválido")
            self.pausar()
            return
        
        if self.socio_controller.activar_socio(id_socio):
            print("\n✓ Socio activado exitosamente")
        else:
            print("\n✗ No se pudo activar el socio")
        
        self.pausar()
    
    # ==================== GESTIÓN DE PRÉSTAMOS ====================
    
    def menu_prestamos(self):
        """Menú de gestión de préstamos"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo("GESTIÓN DE PRÉSTAMOS")
            print("\n1. Realizar préstamo")
            print("2. Registrar devolución")
            print("3. Listar préstamos activos")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.realizar_prestamo()
            elif opcion == "2":
                self.registrar_devolucion()
            elif opcion == "3":
                self.listar_prestamos_activos()
            elif opcion == "0":
                break
            else:
                print("Opción inválida")
                self.pausar()
    
    def realizar_prestamo(self):
        """Realizar un préstamo"""
        self.mostrar_titulo("REALIZAR PRÉSTAMO")
        
        try:
            id_socio = int(input("\nID del socio: ").strip())
        except ValueError:
            print("Error: ID inválido")
            self.pausar()
            return
        
        isbn = input("ISBN del libro: ").strip()
        
        prestamo = self.prestamo_controller.realizar_prestamo(id_socio, isbn)
        
        if not prestamo:
            print("\n✗ No se pudo realizar el préstamo")
        
        self.pausar()
    
    def registrar_devolucion(self):
        """Registrar devolución"""
        self.mostrar_titulo("REGISTRAR DEVOLUCIÓN")
        
        try:
            id_prestamo = int(input("\nID del préstamo: ").strip())
        except ValueError:
            print("Error: ID inválido")
            self.pausar()
            return
        
        if not self.prestamo_controller.registrar_devolucion(id_prestamo):
            print("\n✗ No se pudo registrar la devolución")
        
        self.pausar()
    
    def listar_prestamos_activos(self):
        """Listar préstamos activos"""
        self.mostrar_titulo("PRÉSTAMOS ACTIVOS")
        
        prestamos = self.prestamo_controller.listar_prestamos_activos()
        
        if not prestamos:
            print("\nNo hay préstamos activos")
        else:
            print(f"\nPréstamos activos: {len(prestamos)}\n")
            print(f"{'ID':<5} {'Socio':<25} {'Libro':<30} {'Vence':<12} {'Estado':<10}")
            print("-"*90)
            
            hoy = date.today()
            for p in prestamos:
                vencido = "⚠ VENCIDO" if p['fecha_devolucion_esperada'] < hoy else "Activo"
                print(f"{p['id_prestamo']:<5} {p['socio_nombre'][:24]:<25} "
                      f"{p['libro_titulo'][:29]:<30} {p['fecha_devolucion_esperada']:<12} "
                      f"{vencido:<10}")
        
        self.pausar()
    
    # ==================== REPORTES ====================
    
    def menu_reportes(self):
        """Menú de reportes"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo("REPORTES")
            print("\n1. Resumen general")
            print("2. Libros más prestados")
            print("3. Socios con más préstamos")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.mostrar_resumen_general()
            elif opcion == "2":
                print("\nFuncionalidad en desarrollo...")
                self.pausar()
            elif opcion == "3":
                print("\nFuncionalidad en desarrollo...")
                self.pausar()
            elif opcion == "0":
                break
            else:
                print("Opción inválida")
                self.pausar()
    
    def mostrar_resumen_general(self):
        """Mostrar resumen general del sistema"""
        self.mostrar_titulo("RESUMEN GENERAL")
        
        total_libros = len(self.libro_controller.listar_todos())
        libros_disponibles = len(self.libro_controller.listar_disponibles())
        total_socios = len(self.socio_controller.listar_todos())
        socios_activos = len(self.socio_controller.listar_activos())
        prestamos_activos = len(self.prestamo_controller.listar_prestamos_activos())
        
        print(f"\n📚 LIBROS")
        print(f"   Total de títulos:      {total_libros}")
        print(f"   Títulos disponibles:   {libros_disponibles}")
        
        print(f"\n👥 SOCIOS")
        print(f"   Total de socios:       {total_socios}")
        print(f"   Socios activos:        {socios_activos}")
        
        print(f"\n📖 PRÉSTAMOS")
        print(f"   Préstamos activos:     {prestamos_activos}")
        
        self.pausar()
    
    # ==================== EJECUTAR ====================
    
    def ejecutar(self):
        """Ejecutar el menú principal"""
        while True:
            self.mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.menu_libros()
            elif opcion == "2":
                self.menu_socios()
            elif opcion == "3":
                self.menu_prestamos()
            elif opcion == "4":
                self.menu_reportes()
            elif opcion == "0":
                self.limpiar_pantalla()
                print("\n¡Gracias por usar el Sistema de Gestión de Biblioteca!")
                print("Hasta luego.\n")
                break
            else:
                print("\n✗ Opción inválida. Por favor, seleccione una opción válida.")
                self.pausar()

