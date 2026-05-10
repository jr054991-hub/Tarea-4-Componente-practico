#Módulo Principal - Sistema CSR
import tkinter as tk
from tkinter import ttk, messagebox, font
from controlador import ControladorCSR


# ---- Paleta de colores del sistema ----
COLORES = {
    "fondo":        "#FFFFFF",    # Blanco - fondo principal
    "texto":        "#1A1A1A",    # Negro suave - texto principal
    "boton":        "#1A1A1A",    # Negro - botones principales
    "boton_texto":  "#FFFFFF",    # Blanco - texto sobre botones
    "acento":       "#6B4C3B",    # Café oscuro - acento principal
    "acento_claro": "#C4956A",    # Café claro - acento secundario
    "borde":        "#1A1A1A",    # Negro - bordes de cuadros
    "fondo_tabla":  "#FFFFFF",    # Blanco - fondo de tablas
    "fila_alt":     "#F5F0EB",    # Beige muy suave - filas alternas
    "encabezado":   "#1A1A1A",    # Negro - encabezados de tabla
    "enc_texto":    "#FFFFFF",    # Blanco - texto de encabezados
    "exito":        "#2E7D32",    # Verde oscuro - mensajes de éxito
    "error":        "#C62828",    # Rojo oscuro - mensajes de error
    "separador":    "#E0D5CC",    # Beige suave - líneas separadoras
    "hover":        "#333333",    # Gris oscuro - hover de botones
    "sidebar":      "#F8F5F2",    # Blanco roto - fondo sidebar
    "titulo_bg":    "#1A1A1A",    # Negro - barra de título
}


class CSRApp:
    """
    Clase principal de la aplicación CSR.
    Gestiona la ventana principal y todas las vistas de la UI.
    """

    def __init__(self, root: tk.Tk, logger):
        """
        Inicializa la aplicación con la ventana raíz y el logger.
        
        Args:
            root: Ventana principal de tkinter.
            logger: Instancia del Logger del sistema.
        """
        # Referencia a la ventana principal
        self.root = root
        # Referencia al logger
        self.logger = logger
        # Inicializar el controlador del sistema
        self.controlador = ControladorCSR(logger)
        # Vista activa actual
        self.vista_actual = None

        # Configurar la ventana principal
        self._configurar_ventana()
        # Configurar estilos globales de ttk
        self._configurar_estilos()
        # Construir la estructura principal de la UI
        self._construir_ui()
        # Mostrar la vista de inicio por defecto
        self.mostrar_vista("inicio")

    def _configurar_ventana(self):
        """Configura la ventana principal: título, tamaño y pantalla completa."""
        # Título de la aplicación
        self.root.title("Sistema Integral de Gestión CSR — Software FJ")
        # Color de fondo de la ventana raíz
        self.root.configure(bg=COLORES["fondo"])
        # Maximizar la ventana al tamaño de la pantalla del dispositivo
        self.root.state("zoomed")  # Pantalla completa en Windows/Linux
        # Permitir redimensionamiento
        self.root.resizable(True, True)
        # Asegurarse de que la ventana ocupe toda la pantalla al inicio
        self.root.update_idletasks()
        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        # Establecer geometría máxima
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        # Mínimo de la ventana para garantizar legibilidad
        self.root.minsize(900, 600)

    def _configurar_estilos(self):
        """Define los estilos globales de los widgets ttk."""
        # Crear objeto de estilo de ttk
        estilo = ttk.Style()
        # Usar el tema claro como base
        estilo.theme_use("clam")

        # ---- Estilo para Treeview (tablas) ----
        estilo.configure(
            "CSR.Treeview",
            background=COLORES["fondo_tabla"],    # Fondo blanco
            foreground=COLORES["texto"],           # Texto negro
            fieldbackground=COLORES["fondo_tabla"],
            rowheight=34,                          # Altura de filas
            font=("Verdana", 10),                  # Tipografía Verdana
            borderwidth=0
        )
        # Estilo del encabezado de las tablas
        estilo.configure(
            "CSR.Treeview.Heading",
            background=COLORES["encabezado"],      # Negro
            foreground=COLORES["enc_texto"],       # Blanco
            font=("Verdana", 10, "bold"),           # Negrita
            relief="flat"
        )
        # Selección en la tabla
        estilo.map(
            "CSR.Treeview",
            background=[("selected", COLORES["acento"])],
            foreground=[("selected", "#FFFFFF")]
        )

        # ---- Estilo para Scrollbar ----
        estilo.configure(
            "CSR.Vertical.TScrollbar",
            background=COLORES["separador"],
            troughcolor=COLORES["fondo"],
            arrowcolor=COLORES["texto"]
        )

        # ---- Estilo para Entry (campos de texto) ----
        estilo.configure(
            "CSR.TEntry",
            fieldbackground=COLORES["fondo"],
            foreground=COLORES["texto"],
            font=("Verdana", 11)
        )

    def _construir_ui(self):
        """Construye la estructura principal de la interfaz: barra superior, sidebar y contenido."""
        # Barra de título superior
        self._crear_barra_titulo()

        # Contenedor principal que divide sidebar y contenido
        contenedor_principal = tk.Frame(
            self.root,
            bg=COLORES["fondo"]
        )
        contenedor_principal.pack(fill="both", expand=True)

        # Sidebar de navegación (panel izquierdo)
        self._crear_sidebar(contenedor_principal)

        # Marco de contenido principal (panel derecho)
        self.marco_contenido = tk.Frame(
            contenedor_principal,
            bg=COLORES["fondo"]
        )
        self.marco_contenido.pack(side="left", fill="both", expand=True)

        # Barra de estado inferior
        self._crear_barra_estado()

    def _crear_barra_titulo(self):
        """Crea la barra de título superior de la aplicación."""
        # Marco de la barra de título
        barra = tk.Frame(self.root, bg=COLORES["titulo_bg"], height=70)
        barra.pack(fill="x", side="top")
        barra.pack_propagate(False)  # Mantener altura fija

        # Contenedor para centrar el texto
        contenedor = tk.Frame(barra, bg=COLORES["titulo_bg"])
        contenedor.pack(expand=True, fill="both")

        # Título principal "CSR"
        titulo_corto = tk.Label(
            contenedor,
            text="CSR",
            font=("Verdana", 22, "bold"),
            fg=COLORES["acento_claro"],
            bg=COLORES["titulo_bg"]
        )
        titulo_corto.pack(side="left", padx=(30, 8), pady=15)

        # Separador vertical decorativo
        sep = tk.Label(
            contenedor,
            text="│",
            font=("Verdana", 18),
            fg=COLORES["acento"],
            bg=COLORES["titulo_bg"]
        )
        sep.pack(side="left", pady=15)

        # Título completo del sistema
        titulo_largo = tk.Label(
            contenedor,
            text="Sistema Integral de Gestión",
            font=("Verdana", 14),
            fg="#CCCCCC",
            bg=COLORES["titulo_bg"]
        )
        titulo_largo.pack(side="left", padx=(8, 0), pady=15)

        # Nombre de la empresa (derecha)
        empresa = tk.Label(
            contenedor,
            text="Software FJ",
            font=("Verdana", 11, "italic"),
            fg=COLORES["acento_claro"],
            bg=COLORES["titulo_bg"]
        )
        empresa.pack(side="right", padx=30, pady=15)

    def _crear_sidebar(self, padre):
        """
        Crea el panel de navegación lateral (sidebar).
        
        Args:
            padre: Frame padre donde se colocará el sidebar.
        """
        # Marco del sidebar
        self.sidebar = tk.Frame(
            padre,
            bg=COLORES["sidebar"],
            width=220,
            relief="flat",
            bd=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # Mantener ancho fijo

        # Línea separadora vertical derecha del sidebar
        separador = tk.Frame(self.sidebar, bg=COLORES["separador"], width=1)
        separador.pack(side="right", fill="y")

        # Título de la sección de navegación
        tk.Label(
            self.sidebar,
            text="NAVEGACIÓN",
            font=("Verdana", 8, "bold"),
            fg=COLORES["acento"],
            bg=COLORES["sidebar"]
        ).pack(pady=(25, 10), padx=20, anchor="w")

        # Definición de los botones del sidebar
        opciones_nav = [
            ("Inicio",        "inicio"),
            ("Clientes",       "clientes"),
            ("Servicios",      "servicios"),
            ("Reservas",       "reservas"),
            ("Registro Logs",  "logs"),
        ]

        # Crear cada botón de navegación
        self.botones_nav = {}
        for texto, vista in opciones_nav:
            btn = self._crear_boton_nav(self.sidebar, texto, vista)
            self.botones_nav[vista] = btn

        # Espaciador flexible
        tk.Frame(self.sidebar, bg=COLORES["sidebar"]).pack(fill="y", expand=True)

        # Versión en la parte inferior del sidebar
        tk.Label(
            self.sidebar,
            text="v1.0.0 — 2025",
            font=("Verdana", 8),
            fg=COLORES["separador"],
            bg=COLORES["sidebar"]
        ).pack(pady=15, padx=20, anchor="w")

    def _crear_boton_nav(self, padre, texto: str, vista: str) -> tk.Button:
        """
        Crea un botón de navegación en el sidebar.
        
        Args:
            padre: Frame padre.
            texto: Texto del botón.
            vista: Nombre de la vista a mostrar.
            
        Returns:
            El botón tkinter creado.
        """
        # Crear el botón de navegación
        btn = tk.Button(
            padre,
            text=texto,
            font=("Verdana", 11),
            fg=COLORES["texto"],
            bg=COLORES["sidebar"],
            bd=0,
            relief="flat",
            cursor="hand2",
            anchor="w",
            padx=20,
            pady=10,
            activebackground=COLORES["separador"],
            activeforeground=COLORES["texto"],
            command=lambda v=vista: self.mostrar_vista(v)
        )
        btn.pack(fill="x", pady=1)
        return btn

    def _crear_barra_estado(self):
        """Crea la barra de estado inferior de la aplicación."""
        # Marco de la barra de estado
        self.barra_estado = tk.Frame(
            self.root,
            bg=COLORES["titulo_bg"],
            height=28
        )
        self.barra_estado.pack(fill="x", side="bottom")
        self.barra_estado.pack_propagate(False)

        # Etiqueta de estado
        self.lbl_estado = tk.Label(
            self.barra_estado,
            text="Sistema listo.",
            font=("Verdana", 9),
            fg="#AAAAAA",
            bg=COLORES["titulo_bg"]
        )
        self.lbl_estado.pack(side="left", padx=15, pady=4)

    def actualizar_estado(self, mensaje: str, tipo: str = "info"):
        """
        Actualiza el mensaje en la barra de estado inferior.
        
        Args:
            mensaje: Texto a mostrar.
            tipo: 'info', 'exito' o 'error' para el color.
        """
        # Seleccionar color según tipo de mensaje
        colores_tipo = {
            "info":  "#AAAAAA",
            "exito": "#6BCB77",
            "error": "#FF6B6B"
        }
        color = colores_tipo.get(tipo, "#AAAAAA")
        self.lbl_estado.configure(text=f"  {mensaje}", fg=color)

    def mostrar_vista(self, nombre_vista: str):
        """
        Muestra una vista en el área de contenido principal.
        
        Args:
            nombre_vista: Identificador de la vista a mostrar.
        """
        # Limpiar el contenido actual
        for widget in self.marco_contenido.winfo_children():
            widget.destroy()

        # Actualizar estado de botones del sidebar
        for vista, btn in self.botones_nav.items():
            if vista == nombre_vista:
                # Botón activo: resaltar con acento
                btn.configure(
                    fg=COLORES["acento"],
                    bg=COLORES["separador"],
                    font=("Verdana", 11, "bold")
                )
            else:
                # Botón inactivo: estilo normal
                btn.configure(
                    fg=COLORES["texto"],
                    bg=COLORES["sidebar"],
                    font=("Verdana", 11)
                )

        # Renderizar la vista correspondiente
        if nombre_vista == "inicio":
            from vista_inicio import VistaInicio
            VistaInicio(self.marco_contenido, self)
        elif nombre_vista == "clientes":
            from vista_clientes import VistaClientes
            VistaClientes(self.marco_contenido, self)
        elif nombre_vista == "servicios":
            from vista_servicios import VistaServicios
            VistaServicios(self.marco_contenido, self)
        elif nombre_vista == "reservas":
            from vista_reservas import VistaReservas
            VistaReservas(self.marco_contenido, self)
        elif nombre_vista == "logs":
            from vista_logs import VistaLogs
            VistaLogs(self.marco_contenido, self)

    def crear_boton(self, padre, texto: str, comando, ancho: int = 18,
                    estilo: str = "primario") -> tk.Button:
        """
        Crea un botón estilizado según el sistema de diseño CSR.
        
        Args:
            padre: Frame padre del botón.
            texto: Texto del botón.
            comando: Función a ejecutar al hacer clic.
            ancho: Ancho del botón en caracteres.
            estilo: 'primario' (negro), 'secundario' (café) o 'peligro' (rojo).
            
        Returns:
            Botón tkinter configurado.
        """
        # Colores según el estilo del botón
        estilos_colores = {
            "primario":   (COLORES["boton"],   COLORES["boton_texto"],  COLORES["hover"]),
            "secundario": (COLORES["acento"],  "#FFFFFF",               COLORES["acento_claro"]),
            "peligro":    ("#C62828",           "#FFFFFF",               "#B71C1C"),
            "exitoso":    ("#2E7D32",           "#FFFFFF",               "#1B5E20"),
        }
        bg, fg, hover = estilos_colores.get(estilo, estilos_colores["primario"])

        # Crear el botón
        btn = tk.Button(
            padre,
            text=texto,
            font=("Verdana", 10, "bold"),
            fg=fg,
            bg=bg,
            width=ancho,
            bd=0,
            relief="flat",
            cursor="hand2",
            pady=8,
            padx=10,
            activebackground=hover,
            activeforeground=fg,
            command=comando
        )

        # Efectos hover (resaltar al pasar el mouse)
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))

        return btn

    def crear_titulo_seccion(self, padre, titulo: str, subtitulo: str = "") -> tk.Frame:
        """
        Crea el encabezado de una sección de la aplicación.
        
        Args:
            padre: Frame padre.
            titulo: Título principal de la sección.
            subtitulo: Descripción opcional de la sección.
            
        Returns:
            Frame del encabezado creado.
        """
        # Marco del encabezado
        marco_titulo = tk.Frame(padre, bg=COLORES["fondo"])
        marco_titulo.pack(fill="x", padx=30, pady=(25, 0))

        # Línea decorativa de acento
        linea = tk.Frame(marco_titulo, bg=COLORES["acento"], height=3, width=40)
        linea.pack(anchor="w", pady=(0, 8))

        # Título principal
        tk.Label(
            marco_titulo,
            text=titulo,
            font=("Verdana", 20, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).pack(anchor="w")

        # Subtítulo si se proporcionó
        if subtitulo:
            tk.Label(
                marco_titulo,
                text=subtitulo,
                font=("Verdana", 10),
                fg=COLORES["acento_claro"],
                bg=COLORES["fondo"]
            ).pack(anchor="w", pady=(2, 0))

        return marco_titulo

    def crear_tabla(self, padre, columnas: list, alto: int = 15) -> ttk.Treeview:
        """
        Crea una tabla (Treeview) estilizada para mostrar datos.
        
        Args:
            padre: Frame padre de la tabla.
            columnas: Lista de nombres de columnas.
            alto: Número de filas visibles.
            
        Returns:
            Widget Treeview configurado.
        """
        # Marco contenedor de la tabla con borde negro
        marco_tabla = tk.Frame(padre, bg=COLORES["borde"], bd=1, relief="solid")
        marco_tabla.pack(fill="both", expand=True, padx=30, pady=10)

        # Crear la tabla con las columnas indicadas
        tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="CSR.Treeview",
            height=alto
        )

        # Scrollbar vertical
        scrollbar_v = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=tabla.yview,
            style="CSR.Vertical.TScrollbar"
        )
        tabla.configure(yscrollcommand=scrollbar_v.set)

        # Scrollbar horizontal
        scrollbar_h = ttk.Scrollbar(
            marco_tabla,
            orient="horizontal",
            command=tabla.xview
        )
        tabla.configure(xscrollcommand=scrollbar_h.set)

        # Configurar cada columna
        for col in columnas:
            tabla.heading(col, text=col, anchor="w")
            tabla.column(col, anchor="w", minwidth=80, width=120)

        # Empaquetar tabla y scrollbars
        scrollbar_v.pack(side="right", fill="y")
        scrollbar_h.pack(side="bottom", fill="x")
        tabla.pack(side="left", fill="both", expand=True)

        # Colores alternos de filas
        tabla.tag_configure("fila_normal", background=COLORES["fondo_tabla"])
        tabla.tag_configure("fila_alt",    background=COLORES["fila_alt"])
        tabla.tag_configure("fila_exito",  background="#E8F5E9")
        tabla.tag_configure("fila_error",  background="#FFEBEE")
        tabla.tag_configure("fila_cafe",   background="#FFF8F0")

        return tabla

    def llenar_tabla(self, tabla: ttk.Treeview, datos: list):
        """
        Llena una tabla con los datos proporcionados.
        
        Args:
            tabla: Widget Treeview a llenar.
            datos: Lista de diccionarios con los datos.
        """
        # Limpiar filas existentes
        for item in tabla.get_children():
            tabla.delete(item)

        # Obtener nombres de columnas de la tabla
        columnas = tabla["columns"]

        # Insertar cada fila con color alterno
        for i, registro in enumerate(datos):
            # Extraer valores en el orden de las columnas
            valores = [registro.get(col, "—") for col in columnas]
            # Alternar colores de filas
            tag = "fila_alt" if i % 2 == 1 else "fila_normal"
            tabla.insert("", "end", values=valores, tags=(tag,))

    def mostrar_mensaje(self, titulo: str, mensaje: str, tipo: str = "info"):
        """
        Muestra un mensaje emergente al usuario.
        
        Args:
            titulo: Título de la ventana emergente.
            mensaje: Cuerpo del mensaje.
            tipo: 'info', 'exito' o 'error'.
        """
        if tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "exito":
            messagebox.showinfo(titulo, mensaje)
        else:
            messagebox.showinfo(titulo, mensaje)
