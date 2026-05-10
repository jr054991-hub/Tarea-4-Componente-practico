#Sistema Integral de Gestión CSR - Software FJ

# Importaciones estándar del sistema _ Yenifer Gonzalez
import tkinter as tk
from tkinter import ttk, messagebox, font
import sys
import os

# Asegurar que el directorio raíz esté en el path _ Yenifer Gonzalez
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos del sistema _ Yenifer Gonzalez
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriEspecializada
from reserva import Reserva
from logger import Logger
from exceptions import (
    ClienteInvalidoError, ServicioNoDisponibleError,
    ReservaInvalidaError, ParametroFaltanteError
)
from app import CSRApp


def main():
    """Función principal que inicializa y ejecuta la aplicación."""
    try:
        # Crear la ventana raíz de tkinter _ Yenifer Gonzalez
        root = tk.Tk()

        # Inicializar el logger del sistema _ Yenifer Gonzalez
        logger = Logger()
        logger.registrar_evento("Sistema CSR iniciado correctamente.")

        # Crear e inicializar la aplicación principal _ Yenifer Gonzalez
        app = CSRApp(root, logger)

        # Iniciar el loop principal de la interfaz gráfica _ Yenifer Gonzalez
        root.mainloop()

    except Exception as e:
        # Capturar cualquier error crítico al inicio _ Yenifer Gonzalez
        print(f"Error crítico al iniciar la aplicación: {e}")
        sys.exit(1)


# Punto de entrada del programa _Yenifer Gonzalez
if __name__ == "__main__":
    main()