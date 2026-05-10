"""
=============================================================
  Vista Servicios - Sistema CSR
  Formulario con pestañas para los tres tipos de servicios
  y tabla de servicios registrados
=============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox

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
}


class VistaServicios:
    """
    Vista para gestión de los tres tipos de servicios:
    - Reserva de Sala
    - Alquiler de Equipo
    - Asesoría Especializada
    """

    def __init__(self, padre, app):
        """
        Inicializa la vista de servicios.
        
        Args:
            padre: Frame padre.
            app: Instancia de CSRApp.
        """
        # Referencias principales
        self.padre = padre
        self.app = app
        # Tipo de servicio seleccionado actualmente
        self.tipo_servicio = tk.StringVar(value="sala")
        # Tabla de servicios
        self.tabla = None
        # Construir la vista
        self._construir()

    def _construir(self):
        """Construye la vista de servicios."""
        # Canvas scrollable
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

        # Título
        self.app.crear_titulo_seccion(
            self.marco,
            "Gestión de Servicios",
            "Configure y administre los servicios de Software FJ"
        )

        # Selector de tipo de servicio
        self._crear_selector_tipo()

        # Contenedor del formulario dinámico
        self.marco_form = tk.Frame(self.marco, bg=COLORES["fondo"])
        self.marco_form.pack(fill="x", padx=30, pady=(0, 10))

        # Mostrar el formulario del tipo seleccionado por defecto
        self._cambiar_formulario()

        # Separador
        tk.Frame(self.marco, bg=COLORES["separador"], height=1).pack(fill="x", padx=30, pady=10)

        # Tabla de servicios
        self._crear_tabla_servicios()
        self._actualizar_tabla()

    def _crear_selector_tipo(self):
        """Crea los botones de selección de tipo de servicio."""
        # Marco del selector
        marco_selector = tk.Frame(self.marco, bg=COLORES["fila_alt"])
        marco_selector.pack(fill="x", padx=30, pady=15)

        # Título del selector
        tk.Label(
            marco_selector,
            text="Tipo de Servicio:",
            font=("Verdana", 10, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fila_alt"]
        ).pack(side="left", padx=15, pady=10)

        # Definición de tipos de servicio
        tipos = [
            ("Reserva de Sala",   "sala"),
            ("Alquiler de Equipo","equipo"),
            ("Asesoría",          "asesoria"),
        ]

        # Crear botón de radio para cada tipo
        self.botones_tipo = {}
        for texto, valor in tipos:
            rb = tk.Radiobutton(
                marco_selector,
                text=texto,
                variable=self.tipo_servicio,
                value=valor,
                font=("Verdana", 10),
                fg=COLORES["texto"],
                bg=COLORES["fila_alt"],
                selectcolor=COLORES["fondo"],
                activebackground=COLORES["fila_alt"],
                cursor="hand2",
                command=self._cambiar_formulario
            )
            rb.pack(side="left", padx=15, pady=10)
            self.botones_tipo[valor] = rb

    def _cambiar_formulario(self):
        """Actualiza el formulario según el tipo de servicio seleccionado."""
        # Limpiar el formulario actual
        for widget in self.marco_form.winfo_children():
            widget.destroy()
        # Limpiar variables de campos
        self.campos = {}

        # Mostrar el formulario correspondiente
        tipo = self.tipo_servicio.get()
        if tipo == "sala":
            self._formulario_sala()
        elif tipo == "equipo":
            self._formulario_equipo()
        elif tipo == "asesoria":
            self._formulario_asesoria()

    def _crear_entry(self, padre, etiqueta: str, clave: str,
                     fila: int, columna: int, placeholder: str = ""):
        """
        Crea un campo de entrada reutilizable para los formularios.
        
        Args:
            padre: Frame padre.
            etiqueta: Texto de la etiqueta.
            clave: Clave para el diccionario de campos.
            fila: Fila en la cuadrícula.
            columna: Columna en la cuadrícula.
            placeholder: Texto de ayuda.
        """
        # Etiqueta del campo
        tk.Label(
            padre,
            text=etiqueta,
            font=("Verdana", 9, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).grid(row=fila * 2, column=columna, sticky="w", pady=(8, 2), padx=(0, 20))

        # Variable del campo
        var = tk.StringVar()
        self.campos[clave] = var

        # Campo de entrada
        entry = tk.Entry(
            padre,
            textvariable=var,
            font=("Verdana", 10),
            fg="#AAAAAA",
            bg=COLORES["fondo"],
            bd=1,
            relief="solid",
            width=28
        )
        entry.grid(row=fila * 2 + 1, column=columna, sticky="ew", padx=(0, 20))

        # Placeholder
        if placeholder:
            entry.insert(0, placeholder)

        def al_enfocar(event, e=entry, p=placeholder):
            if e.get() == p:
                e.delete(0, "end")
                e.configure(fg=COLORES["texto"])

        def al_desenfocar(event, e=entry, p=placeholder):
            if not e.get():
                e.insert(0, p)
                e.configure(fg="#AAAAAA")

        entry.bind("<FocusIn>", al_enfocar)
        entry.bind("<FocusOut>", al_desenfocar)

    def _crear_check(self, padre, etiqueta: str, clave: str,
                     fila: int, columna: int) -> tk.BooleanVar:
        """
        Crea un campo de tipo checkbox.
        
        Returns:
            Variable booleana del checkbox.
        """
        # Variable booleana
        var = tk.BooleanVar()
        self.campos[clave] = var

        # Checkbox estilizado
        cb = tk.Checkbutton(
            padre,
            text=etiqueta,
            variable=var,
            font=("Verdana", 10),
            fg=COLORES["texto"],
            bg=COLORES["fondo"],
            selectcolor=COLORES["fondo"],
            activebackground=COLORES["fondo"],
            cursor="hand2"
        )
        cb.grid(row=fila, column=columna, sticky="w", pady=5, padx=(0, 20))
        return var

    def _formulario_sala(self):
        """Construye el formulario para registrar una Reserva de Sala."""
        # LabelFrame con borde negro
        frame = tk.LabelFrame(
            self.marco_form,
            text="  Reserva de Sala  ",
            font=("Verdana", 10, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"],
            bd=1, relief="solid"
        )
        frame.pack(fill="x", pady=(5, 0))

        interno = tk.Frame(frame, bg=COLORES["fondo"])
        interno.pack(fill="x", padx=20, pady=10)

        # Campos del formulario de sala - Primera fila
        self._crear_entry(interno, "Nombre de la Sala *", "nombre",       0, 0, "Ej: Sala Innovación")
        self._crear_entry(interno, "Capacidad Máx. (personas) *", "capacidad_max", 0, 2, "Ej: 20")
        
        # Segunda fila
        self._crear_entry(interno, "Precio Base/hora ($) *", "precio_base", 2, 0, "Ej: 150000")

        # Checkboxes para extras - Tercera fila (después del precio)
        self._crear_check(interno, "Tiene Proyector", "tiene_proyector", 6, 0)
        self._crear_check(interno, "Tiene Videoconferencia", "tiene_videoconferencia", 6, 2)

        interno.columnconfigure(0, weight=1)
        interno.columnconfigure(2, weight=1)

        # Botones
        self._crear_botones_formulario(frame, "sala")

    def _formulario_equipo(self):
        """Construye el formulario para registrar un Alquiler de Equipo."""
        frame = tk.LabelFrame(
            self.marco_form,
            text="  Alquiler de Equipo  ",
            font=("Verdana", 10, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"],
            bd=1, relief="solid"
        )
        frame.pack(fill="x", pady=(5, 0))

        interno = tk.Frame(frame, bg=COLORES["fondo"])
        interno.pack(fill="x", padx=20, pady=10)

        # Campos del formulario de equipo
        self._crear_entry(interno, "Nombre/Modelo *",     "nombre",       0, 0, "Ej: Laptop Dell XPS")
        self._crear_entry(interno, "Precio Base/hora ($) *", "precio_base", 0, 2, "Ej: 45000")
        self._crear_entry(interno, "Cantidad Disponible *", "cantidad_disponible", 1, 0, "Ej: 5")

        # Selector de tipo de equipo
        tk.Label(
            interno,
            text="Tipo de Equipo *",
            font=("Verdana", 9, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).grid(row=2, column=2, sticky="w", pady=(8, 2), padx=(0, 20))

        tipos_equipo = ["laptop", "proyector", "camara", "impresora", "tablet", "servidor"]
        var_tipo = tk.StringVar(value="laptop")
        self.campos["tipo_equipo"] = var_tipo

        combo = ttk.Combobox(
            interno,
            textvariable=var_tipo,
            values=tipos_equipo,
            font=("Verdana", 10),
            state="readonly",
            width=26
        )
        combo.grid(row=3, column=2, sticky="ew", padx=(0, 20))

        # Checkbox depósito
        self._crear_check(interno, "Requiere Depósito", "requiere_deposito", 4, 0)

        interno.columnconfigure(0, weight=1)
        interno.columnconfigure(2, weight=1)

        # Botones
        self._crear_botones_formulario(frame, "equipo")

    def _formulario_asesoria(self):
        """Construye el formulario para registrar una Asesoría Especializada."""
        frame = tk.LabelFrame(
            self.marco_form,
            text="  Asesoría Especializada  ",
            font=("Verdana", 10, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"],
            bd=1, relief="solid"
        )
        frame.pack(fill="x", pady=(5, 0))

        interno = tk.Frame(frame, bg=COLORES["fondo"])
        interno.pack(fill="x", padx=20, pady=10)

        # Campos del formulario de asesoría
        self._crear_entry(interno, "Nombre de la Asesoría *", "nombre",     0, 0, "Ej: Consultoría Cloud")
        self._crear_entry(interno, "Nombre del Asesor *",  "nombre_asesor", 0, 2, "Ej: Ing. Torres")
        self._crear_entry(interno, "Precio Base/hora ($) *", "precio_base", 1, 0, "Ej: 200000")

        # Selectores de área y nivel
        tk.Label(interno, text="Área *", font=("Verdana", 9, "bold"),
                 fg=COLORES["texto"], bg=COLORES["fondo"]
                 ).grid(row=2, column=2, sticky="w", pady=(8, 2), padx=(0, 20))

        areas = ["tecnologia", "software", "bases_de_datos", "redes",
                 "ciberseguridad", "gestion_proyectos", "cloud", "ia"]
        var_area = tk.StringVar(value="tecnologia")
        self.campos["area"] = var_area
        combo_area = ttk.Combobox(interno, textvariable=var_area, values=areas,
                                  font=("Verdana", 10), state="readonly", width=26)
        combo_area.grid(row=3, column=2, sticky="ew", padx=(0, 20))

        tk.Label(interno, text="Nivel del Asesor *", font=("Verdana", 9, "bold"),
                 fg=COLORES["texto"], bg=COLORES["fondo"]
                 ).grid(row=4, column=0, sticky="w", pady=(8, 2))

        var_nivel = tk.StringVar(value="junior")
        self.campos["nivel_experto"] = var_nivel
        combo_nivel = ttk.Combobox(interno, textvariable=var_nivel,
                                   values=["junior", "senior", "experto"],
                                   font=("Verdana", 10), state="readonly", width=26)
        combo_nivel.grid(row=5, column=0, sticky="ew", padx=(0, 20))

        interno.columnconfigure(0, weight=1)
        interno.columnconfigure(2, weight=1)

        # Botones
        self._crear_botones_formulario(frame, "asesoria")

    def _crear_botones_formulario(self, padre, tipo: str):
        """
        Crea los botones de acción del formulario.
        
        Args:
            padre: Frame padre.
            tipo: Tipo de servicio para el mensaje del botón.
        """
        marco = tk.Frame(padre, bg=COLORES["fondo"])
        marco.pack(fill="x", padx=20, pady=(5, 15))

        # Botón de agregar servicio
        btn = self.app.crear_boton(
            marco, f"Agregar Servicio",
            lambda: self._agregar_servicio(tipo), ancho=20
        )
        btn.pack(side="left", padx=(0, 10))

        # Botón limpiar
        btn_limpiar = self.app.crear_boton(
            marco, "Limpiar", self._cambiar_formulario, ancho=10, estilo="secundario"
        )
        btn_limpiar.pack(side="left")

        # Etiqueta de resultado
        self.lbl_resultado = tk.Label(
            padre, text="", font=("Verdana", 9), bg=COLORES["fondo"]
        )
        self.lbl_resultado.pack(padx=20, pady=(0, 8), anchor="w")

    def _agregar_servicio(self, tipo: str):
        """
        Ejecuta la creación del servicio desde el formulario actual.
        
        Args:
            tipo: Tipo de servicio a crear ('sala', 'equipo', 'asesoria').
        """
        # Construir kwargs desde los campos del formulario
        placeholders = {
            "nombre": ["Ej: Sala Innovación", "Ej: Laptop Dell XPS", "Ej: Consultoría Cloud"],
            "precio_base": ["Ej: 150000", "Ej: 45000", "Ej: 200000"],
            "capacidad_max": ["Ej: 20"],
            "cantidad_disponible": ["Ej: 5"],
            "nombre_asesor": ["Ej: Ing. Torres"],
        }

        kwargs = {}
        for clave, var in self.campos.items():
            valor = var.get()
            # Ignorar valores que son placeholders
            ph_list = placeholders.get(clave, [])
            if valor in ph_list:
                valor = ""
            kwargs[clave] = valor

        # Validar campos requeridos antes de crear el servicio
        errores = []
        
        # Campos requeridos según el tipo
        campos_requeridos = {
            "sala": ["nombre", "capacidad_max", "precio_base"],
            "equipo": ["nombre", "tipo_equipo", "precio_base"],
            "asesoria": ["nombre", "area", "precio_base", "nombre_asesor"]
        }
        
        for campo in campos_requeridos.get(tipo, []):
            if not kwargs.get(campo, "").strip():
                errores.append(f"El campo '{campo}' es requerido")
        
        # Validar precio_base específicamente
        if kwargs.get("precio_base", "").strip():
            try:
                float(kwargs["precio_base"])
            except ValueError:
                errores.append("El precio base debe ser un número válido")
        
        # Validar capacidad_max para sala
        if tipo == "sala" and kwargs.get("capacidad_max", "").strip():
            try:
                capacidad = int(kwargs["capacidad_max"])
                if capacidad <= 0:
                    errores.append("La capacidad máxima debe ser mayor a 0")
            except ValueError:
                errores.append("La capacidad máxima debe ser un número entero")
        
        # Si hay errores, mostrarlos y salir
        if errores:
            mensaje_error = "Errores encontrados:\n" + "\n".join(f"• {e}" for e in errores)
            self.lbl_resultado.configure(text=f"✗ {mensaje_error}", fg=COLORES["error"])
            self.app.actualizar_estado("Error en formulario", "error")
            return

        # Llamar al controlador para agregar el servicio
        resultado = self.app.controlador.agregar_servicio(tipo, **kwargs)

        if resultado["exito"]:
            self.lbl_resultado.configure(
                text=f"✓ {resultado['mensaje']}", fg=COLORES["exito"]
            )
            self.app.actualizar_estado(resultado["mensaje"], "exito")
            self._actualizar_tabla()
        else:
            self.lbl_resultado.configure(
                text=f"✗ {resultado['mensaje']}", fg=COLORES["error"]
            )
            self.app.actualizar_estado(resultado["mensaje"], "error")

    def _crear_tabla_servicios(self):
        """Crea la tabla de servicios registrados."""
        marco_titulo = tk.Frame(self.marco, bg=COLORES["fondo"])
        marco_titulo.pack(fill="x", padx=30)

        tk.Label(
            marco_titulo,
            text="Servicios Registrados",
            font=("Verdana", 12, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).pack(side="left")

        btn_actualizar = self.app.crear_boton(
            marco_titulo, "↻ Actualizar",
            self._actualizar_tabla, ancho=12, estilo="secundario"
        )
        btn_actualizar.pack(side="right")

        # Columnas de la tabla de servicios
        columnas = ["ID", "Nombre", "Tipo", "Descripción", "Precio Base", "Estado"]
        self.tabla = self.app.crear_tabla(self.marco, columnas, alto=8)

        # Contador de servicios
        self.lbl_conteo = tk.Label(
            self.marco, text="", font=("Verdana", 9),
            fg=COLORES["acento_claro"], bg=COLORES["fondo"]
        )
        self.lbl_conteo.pack(anchor="w", padx=30, pady=(5, 20))

    def _actualizar_tabla(self):
        """Recarga la tabla de servicios."""
        servicios = self.app.controlador.obtener_servicios()
        datos = [s.to_dict() for s in servicios]
        self.app.llenar_tabla(self.tabla, datos)
        self.lbl_conteo.configure(text=f"Total: {len(servicios)} servicio(s)")
