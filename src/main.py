"""
Sistema de Gestión de Biblioteca
Arquitectura en capas: View -> Controller -> Service -> Repository -> DAL
"""
import sys
from pathlib import Path

# Agregar el directorio src al path para permitir imports absolutos
sys.path.insert(0, str(Path(__file__).parent))

from view.menu import Menu


def main():
    """Función principal del sistema"""
    menu = Menu()
    menu.ejecutar()


if __name__ == "__main__":
    main()
