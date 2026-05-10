"""
=============================================================
  Vista Inicio - Sistema CSR
  Dashboard principal con estadísticas y bienvenida
=============================================================
"""

import tkinter as tk

# Colores del sistema
COLORES = {
    "fondo":        "#FFFFFF",
    "texto":        "#1A1A1A",
    "acento":       "#6B4C3B",
    "acento_claro": "#C4956A",
    "separador":    "#E0D5CC",
    "sidebar":      "#F8F5F2",
    "titulo_bg":    "#1A1A1A",
    "fila_alt":     "#F5F0EB",
}


class VistaInicio:
    """
    Vista del dashboard de inicio.
    Muestra métricas del sistema y accesos rápidos.
    """

    def __init__(self, padre, app):
        """
        Inicializa la vista de inicio.
        
        Args:
            padre: Frame padre donde se renderizará la vista.
            app: Instancia de la aplicación principal CSRApp.
        """
        # Referencia al frame padre
        self.padre = padre
        # Referencia a la app principal
        self.app = app

        # Construir la vista
        self._construir()

    def _construir(self):
        """Construye todos los elementos de la vista de inicio."""
        # Marco scrollable principal
        canvas = tk.Canvas(self.padre, bg=COLORES["fondo"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.padre, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame interno del canvas
        self.marco = tk.Frame(canvas, bg=COLORES["fondo"])
        ventana_id = canvas.create_window((0, 0), window=self.marco, anchor="nw")

        # Ajustar el canvas cuando cambie el tamaño del frame interno
        def ajustar_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(ventana_id, width=canvas.winfo_width())

        self.marco.bind("<Configure>", ajustar_canvas)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(ventana_id, width=e.width))

        # Scroll con mouse
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # Construir secciones de la vista
        self._seccion_bienvenida()
        self._seccion_estadisticas()
        self._seccion_accesos_rapidos()

    def _seccion_bienvenida(self):
        """Crea la sección de bienvenida con el encabezado principal."""
        # Marco de bienvenida con fondo suave
        marco_bienvenida = tk.Frame(self.marco, bg=COLORES["fila_alt"])
        marco_bienvenida.pack(fill="x", padx=30, pady=(25, 0))

        # Contenido interno con padding
        contenido = tk.Frame(marco_bienvenida, bg=COLORES["fila_alt"], bd=1, relief="flat")
        contenido.pack(fill="x", padx=0, pady=0)

        # Decoración - línea de acento
        linea = tk.Frame(contenido, bg=COLORES["acento"], height=3)
        linea.pack(fill="x")

        # Texto de bienvenida
        info_frame = tk.Frame(contenido, bg=COLORES["fila_alt"])
        info_frame.pack(fill="x", padx=25, pady=20)

        tk.Label(
            info_frame,
            text="Bienvenido al Sistema CSR",
            font=("Verdana", 22, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fila_alt"]
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text="Software FJ  ·  Gestión de Clientes, Servicios y Reservas",
            font=("Verdana", 11),
            fg=COLORES["acento_claro"],
            bg=COLORES["fila_alt"]
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            info_frame,
            text=(
                "Sistema orientado a objetos con manejo avanzado de excepciones. "
                "Gestione clientes, configure servicios y administre reservas de forma integral."
            ),
            font=("Verdana", 10),
            fg="#555555",
            bg=COLORES["fila_alt"],
            wraplength=800,
            justify="left"
        ).pack(anchor="w", pady=(10, 0))

    def _seccion_estadisticas(self):
        """Crea las tarjetas de estadísticas del sistema."""
        # Separador
        tk.Frame(self.marco, bg=COLORES["separador"], height=1).pack(fill="x", padx=30, pady=20)

        # Título de sección
        tk.Label(
            self.marco,
            text="Resumen del Sistema",
            font=("Verdana", 13, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).pack(anchor="w", padx=30)

        # Obtener estadísticas del controlador
        stats = self.app.controlador.obtener_estadisticas()

        # Marco de las tarjetas con diseño de cuadrícula
        marco_cards = tk.Frame(self.marco, bg=COLORES["fondo"])
        marco_cards.pack(fill="x", padx=30, pady=15)

        # Definición de las tarjetas de métricas
        metricas = [
            ("Clientes", str(stats.get("total_clientes", 0)),
             f"Activos: {stats.get('clientes_activos', 0)}", COLORES["texto"]),
            ("Servicios", str(stats.get("total_servicios", 0)),
             f"Disponibles: {stats.get('servicios_disponibles', 0)}", COLORES["acento"]),
            ("Reservas", str(stats.get("total_reservas", 0)),
             f"Confirmadas: {stats.get('confirmadas', 0)}", COLORES["texto"]),
            ("Ingresos", f"${stats.get('ingresos_totales', 0):,.0f}",
             "Reservas activas", COLORES["acento"]),
        ]

        # Crear cada tarjeta de métrica
        for i, (etiqueta, valor, subtexto, color_acento) in enumerate(metricas):
            self._crear_tarjeta_metrica(marco_cards, etiqueta, valor, subtexto, color_acento)

    def _crear_tarjeta_metrica(self, padre, etiqueta: str, valor: str,
                                subtexto: str, color_acento: str):
        """
        Crea una tarjeta individual de métrica.
        
        Args:
            padre: Frame padre de la tarjeta.
            etiqueta: Nombre de la métrica.
            valor: Valor numérico a mostrar.
            subtexto: Información adicional.
            color_acento: Color decorativo de la tarjeta.
        """
        # Marco de la tarjeta con borde negro
        card = tk.Frame(
            padre,
            bg=COLORES["fondo"],
            bd=1,
            relief="solid",
            highlightbackground=COLORES["texto"],
            highlightthickness=1
        )
        card.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=5)

        # Línea superior de color como acento
        linea_top = tk.Frame(card, bg=color_acento, height=4)
        linea_top.pack(fill="x")

        # Contenido interno
        contenido = tk.Frame(card, bg=COLORES["fondo"])
        contenido.pack(fill="both", expand=True, padx=20, pady=15)

        # Valor grande (número/dato principal)
        tk.Label(
            contenido,
            text=valor,
            font=("Verdana", 26, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).pack(anchor="w")

        # Etiqueta de la métrica
        tk.Label(
            contenido,
            text=etiqueta,
            font=("Verdana", 11, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).pack(anchor="w")

        # Subtexto informativo
        tk.Label(
            contenido,
            text=subtexto,
            font=("Verdana", 9),
            fg=COLORES["acento_claro"],
            bg=COLORES["fondo"]
        ).pack(anchor="w", pady=(2, 0))

    def _seccion_accesos_rapidos(self):
        """Crea los botones de acceso rápido a las secciones principales."""
        # Separador
        tk.Frame(self.marco, bg=COLORES["separador"], height=1).pack(fill="x", padx=30, pady=(10, 20))

        # Título
        tk.Label(
            self.marco,
            text="Accesos Rápidos",
            font=("Verdana", 13, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).pack(anchor="w", padx=30)

        # Marco de botones
        marco_botones = tk.Frame(self.marco, bg=COLORES["fondo"])
        marco_botones.pack(fill="x", padx=30, pady=15)

        # Definición de accesos rápidos
        accesos = [
            ("Registrar Cliente",   "clientes"),
            ("Agregar Servicio",    "servicios"),
            ("Nueva Reserva",       "reservas"),
            ("Ver Logs",            "logs"),
        ]

        # Crear cada botón de acceso rápido
        for texto, vista in accesos:
            btn = self.app.crear_boton(
                marco_botones, texto,
                lambda v=vista: self.app.mostrar_vista(v),
                ancho=20
            )
            btn.pack(side="left", padx=(0, 10))

        # Padding inferior
        tk.Frame(self.marco, bg=COLORES["fondo"], height=40).pack()
