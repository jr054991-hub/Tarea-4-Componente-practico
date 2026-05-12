
import tkinter as tk
from tkinter import ttk

COLORES = {
    "fondo":        "#FFFFFF",
    "texto":        "#1A1A1A",
    "acento":       "#6B4C3B",
    "acento_claro": "#C4956A",
    "separador":    "#E0D5CC",
    "borde":        "#1A1A1A",
    "error":        "#C62828",
    "exito":        "#2E7D32",
    "fila_alt":     "#F5F0EB",
    "sidebar":      "#F8F5F2",
}


class VistaLogs:
    """
    Vista para visualización de logs del sistema.
    Muestra eventos y errores registrados por el Logger.
    """

    def __init__(self, padre, app):
        """
        Inicializa la vista de logs.
        
        Args:
            padre: Frame padre donde se renderizará.
            app: Instancia principal de CSRApp.
        """
        # Referencia al frame padre y a la app
        self.padre = padre
        self.app = app
        # Tabla de logs
        self.tabla = None
        # Construir la vista
        self._construir()

    def _construir(self):
        """Construye la vista completa de logs."""
        # Marco scrollable
        canvas = tk.Canvas(self.padre, bg=COLORES["fondo"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.padre, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.marco = tk.Frame(canvas, bg=COLORES["fondo"])
        vid = canvas.create_window((0, 0), window=self.marco, anchor="nw")

        def ajustar(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(vid, width=canvas.winfo_width())

        self.marco.bind("<Configure>", ajustar)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(vid, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # Título de la sección
        self.app.crear_titulo_seccion(
            self.marco,
            "Registro de Logs",
            "Historial de eventos y errores del sistema CSR"
        )

        # Botón para actualizar logs
        marco_botones = tk.Frame(self.marco, bg=COLORES["fondo"])
        marco_botones.pack(fill="x", padx=30, pady=(0, 15))

        self.app.crear_boton(
            marco_botones,
            "Actualizar",
            self._actualizar_tabla,
            ancho=15
        ).pack(side="left")

        # Tabla de logs
        self._crear_tabla_logs()

        # Cargar datos iniciales
        self._actualizar_tabla()

    def _crear_tabla_logs(self):
        """Crea la tabla para mostrar los logs."""
        # Columnas de la tabla
        columnas = ["Tipo", "Timestamp", "Mensaje"]

        # Crear tabla usando el método de la app
        self.tabla = self.app.crear_tabla(self.marco, columnas, alto=20)

    def _actualizar_tabla(self):
        """Actualiza la tabla con los logs actuales."""
        # Obtener registros del logger
        registros = self.app.logger.obtener_registros()

        # Convertir a formato de tabla
        datos_tabla = []
        for tipo, timestamp, mensaje in registros:
            # Determinar color según tipo
            color_tag = "fila_error" if tipo == "error" else "fila_normal"
            datos_tabla.append({
                "Tipo": "ERROR" if tipo == "error" else "EVENTO",
                "Timestamp": timestamp,
                "Mensaje": mensaje
            })

        # Llenar tabla
        self.app.llenar_tabla(self.tabla, datos_tabla)
