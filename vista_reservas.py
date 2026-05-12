""
=============================================================
  Vista Reservas - Sistema CSR
  Creación y gestión de reservas con cálculo de costos
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


class VistaReservas:
    """
    Vista para la gestión de reservas del sistema CSR.
    Permite crear, cancelar y completar reservas.
    """

    def __init__(self, padre, app):
        """
        Inicializa la vista de reservas.
        
        Args:
            padre: Frame padre.
            app: Instancia de CSRApp.
        """
        self.padre = padre
        self.app = app
        # Variables del formulario de reserva
        self.var_cliente = tk.StringVar()
        self.var_servicio = tk.StringVar()
        self.var_duracion = tk.StringVar()
        self.var_param_extra = tk.StringVar()
        # Tabla de reservas
        self.tabla = None
        # Construir la vista
        self._construir()

    def _construir(self):
        """Construye la vista de reservas."""
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
            "Gestión de Reservas",
            "Cree, consulte y administre reservas de servicios"
        )

        # Formulario de reserva
        self._crear_formulario()

        # Separador
        tk.Frame(self.marco, bg=COLORES["separador"], height=1).pack(fill="x", padx=30, pady=10)

        # Tabla de reservas
        self._crear_tabla_reservas()
        self._actualizar_tabla()

    def _crear_formulario(self):
        """Crea el formulario para crear una nueva reserva."""
        # LabelFrame del formulario
        frame = tk.LabelFrame(
            self.marco,
            text="  Nueva Reserva  ",
            font=("Verdana", 10, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"],
            bd=1, relief="solid"
        )
        frame.pack(fill="x", padx=30, pady=15)

        interno = tk.Frame(frame, bg=COLORES["fondo"])
        interno.pack(fill="x", padx=20, pady=15)

        # ---- Fila 1: Cliente y Servicio ----

        # Etiqueta y selector de Cliente
        tk.Label(interno, text="Cliente *", font=("Verdana", 9, "bold"),
                 fg=COLORES["texto"], bg=COLORES["fondo"]
                 ).grid(row=0, column=0, sticky="w", pady=(0, 2))

        self.combo_clientes = ttk.Combobox(
            interno, textvariable=self.var_cliente,
            font=("Verdana", 10), state="readonly", width=30
        )
        self.combo_clientes.grid(row=1, column=0, sticky="ew", padx=(0, 20))

        # Etiqueta y selector de Servicio
        tk.Label(interno, text="Servicio *", font=("Verdana", 9, "bold"),
                 fg=COLORES["texto"], bg=COLORES["fondo"]
                 ).grid(row=0, column=2, sticky="w", pady=(0, 2))

        self.combo_servicios = ttk.Combobox(
            interno, textvariable=self.var_servicio,
            font=("Verdana", 10), state="readonly", width=30
        )
        self.combo_servicios.grid(row=1, column=2, sticky="ew", padx=(0, 20))

        # ---- Fila 2: Duración y Parámetro Extra ----

        tk.Label(interno, text="Duración (horas) *", font=("Verdana", 9, "bold"),
                 fg=COLORES["texto"], bg=COLORES["fondo"]
                 ).grid(row=2, column=0, sticky="w", pady=(10, 2))

        entry_duracion = tk.Entry(
            interno, textvariable=self.var_duracion,
            font=("Verdana", 10), fg="#AAAAAA",
            bg=COLORES["fondo"], bd=1, relief="solid", width=30
        )
        entry_duracion.insert(0, "Ej: 2 (número de horas)")
        entry_duracion.grid(row=3, column=0, sticky="ew", padx=(0, 20))

        # Funciones placeholder para duración
        def en_duracion(e):
            if entry_duracion.get() == "Ej: 2 (número de horas)":
                entry_duracion.delete(0, "end")
                entry_duracion.configure(fg=COLORES["texto"])

        def sal_duracion(e):
            if not entry_duracion.get():
                entry_duracion.insert(0, "Ej: 2 (número de horas)")
                entry_duracion.configure(fg="#AAAAAA")

        entry_duracion.bind("<FocusIn>", en_duracion)
        entry_duracion.bind("<FocusOut>", sal_duracion)

        # Parámetro extra (personas, cantidad, sesiones)
        tk.Label(interno, text="Parámetro Extra (personas / cantidad / sesiones)",
                 font=("Verdana", 9, "bold"),
                 fg=COLORES["texto"], bg=COLORES["fondo"]
                 ).grid(row=2, column=2, sticky="w", pady=(10, 2))

        entry_extra = tk.Entry(
            interno, textvariable=self.var_param_extra,
            font=("Verdana", 10), fg="#AAAAAA",
            bg=COLORES["fondo"], bd=1, relief="solid", width=30
        )
        entry_extra.insert(0, "Ej: 5 (opcional)")
        entry_extra.grid(row=3, column=2, sticky="ew", padx=(0, 20))

        def en_extra(e):
            if entry_extra.get() == "Ej: 5 (opcional)":
                entry_extra.delete(0, "end")
                entry_extra.configure(fg=COLORES["texto"])

        def sal_extra(e):
            if not entry_extra.get():
                entry_extra.insert(0, "Ej: 5 (opcional)")
                entry_extra.configure(fg="#AAAAAA")

        entry_extra.bind("<FocusIn>", en_extra)
        entry_extra.bind("<FocusOut>", sal_extra)

        # Configurar columnas
        interno.columnconfigure(0, weight=1)
        interno.columnconfigure(2, weight=1)

        # ---- Botones del formulario ----
        marco_botones = tk.Frame(frame, bg=COLORES["fondo"])
        marco_botones.pack(fill="x", padx=20, pady=(5, 5))

        # Botón de cargar opciones desde el sistema
        btn_cargar = self.app.crear_boton(
            marco_botones, "↻ Cargar Opciones",
            self._cargar_opciones, ancho=16, estilo="secundario"
        )
        btn_cargar.pack(side="left", padx=(0, 10))

        # Botón de calcular costo preview
        btn_calcular = self.app.crear_boton(
            marco_botones, "Calcular Costo",
            self._calcular_preview, ancho=14, estilo="secundario"
        )
        btn_calcular.pack(side="left", padx=(0, 10))

        # Botón de crear reserva
        btn_crear = self.app.crear_boton(
            marco_botones, "Crear Reserva",
            self._crear_reserva, ancho=16
        )
        btn_crear.pack(side="left")

        # Etiqueta de preview de costo
        self.lbl_costo = tk.Label(
            frame,
            text="",
            font=("Verdana", 11, "bold"),
            bg=COLORES["fondo"],
            fg=COLORES["acento"]
        )
        self.lbl_costo.pack(padx=20, pady=(3, 5), anchor="w")

        # Etiqueta de resultado
        self.lbl_resultado = tk.Label(
            frame, text="", font=("Verdana", 9), bg=COLORES["fondo"]
        )
        self.lbl_resultado.pack(padx=20, pady=(0, 12), anchor="w")

        # Cargar opciones iniciales
        self._cargar_opciones()

    def _cargar_opciones(self):
        """Carga los clientes y servicios disponibles en los ComboBox."""
        try:
            # Cargar clientes activos
            clientes = self.app.controlador.obtener_clientes()
            opciones_clientes = [
                f"{c.id} - {c.nombre}"
                for c in clientes if c.activo
            ]
            self.combo_clientes["values"] = opciones_clientes
            if opciones_clientes:
                self.combo_clientes.set(opciones_clientes[0])

            # Cargar servicios disponibles
            servicios = self.app.controlador.obtener_servicios()
            opciones_servicios = [
                f"{s.id} - {s.nombre} ({s.tipo_servicio()})"
                for s in servicios if s.disponible
            ]
            self.combo_servicios["values"] = opciones_servicios
            if opciones_servicios:
                self.combo_servicios.set(opciones_servicios[0])

            self.app.actualizar_estado("Opciones actualizadas.", "info")

        except Exception as e:
            self.app.actualizar_estado(f"Error cargando opciones: {e}", "error")

    def _obtener_ids_seleccionados(self):
        """
        Extrae los IDs de cliente y servicio desde los ComboBox.
        
        Returns:
            Tupla (id_cliente, id_servicio) o (None, None) si hay error.
        """
        try:
            # Extraer el ID del cliente (formato "CLI-0001 - Nombre")
            texto_cliente = self.var_cliente.get()
            id_cliente = texto_cliente.split(" - ")[0].strip() if texto_cliente else None

            # Extraer el ID del servicio (formato "SRV-0001 - Nombre (Tipo)")
            texto_servicio = self.var_servicio.get()
            id_servicio = texto_servicio.split(" - ")[0].strip() if texto_servicio else None

            return id_cliente, id_servicio
        except Exception:
            return None, None

    def _calcular_preview(self):
        """Calcula y muestra el costo estimado de la reserva."""
        try:
            id_cliente, id_servicio = self._obtener_ids_seleccionados()
            if not id_cliente or not id_servicio:
                self.lbl_costo.configure(text="Seleccione cliente y servicio.", fg=COLORES["error"])
                return

            # Obtener duración
            duracion_str = self.var_duracion.get()
            if duracion_str in ["", "Ej: 2 (número de horas)"]:
                self.lbl_costo.configure(text="Ingrese la duración en horas.", fg=COLORES["error"])
                return
            duracion = float(duracion_str)

            # Buscar el servicio
            servicio = self.app.controlador.buscar_servicio_por_id(id_servicio)
            if not servicio:
                self.lbl_costo.configure(text="Servicio no encontrado.", fg=COLORES["error"])
                return

            # Armar parámetros extra
            params = self._armar_params_extra(servicio.tipo_servicio())

            # Calcular costo con IVA
            costo = servicio.calcular_costo_con_iva(duracion, **params)
            self.lbl_costo.configure(
                text=f"Costo estimado (con IVA 19%): ${costo:,.2f}",
                fg=COLORES["acento"]
            )

        except ValueError:
            self.lbl_costo.configure(text="La duración debe ser un número.", fg=COLORES["error"])
        except Exception as e:
            self.lbl_costo.configure(text=f"Error: {e}", fg=COLORES["error"])

    def _armar_params_extra(self, tipo_servicio: str) -> dict:
        """
        Arma el diccionario de parámetros extra según el tipo de servicio.
        
        Args:
            tipo_servicio: Nombre del tipo de servicio.
            
        Returns:
            Diccionario con los parámetros adicionales correspondientes.
        """
        params = {}
        # Obtener el valor del parámetro extra ingresado
        val_extra = self.var_param_extra.get()
        if val_extra not in ["", "Ej: 5 (opcional)"]:
            try:
                valor_num = int(val_extra)
                # Asignar al parámetro correcto según el tipo
                if "Sala" in tipo_servicio:
                    params["personas"] = valor_num
                elif "Equipo" in tipo_servicio:
                    params["cantidad"] = valor_num
                elif "Asesoría" in tipo_servicio:
                    params["sesiones"] = valor_num
            except ValueError:
                pass  # Ignorar si no es número
        return params

    def _crear_reserva(self):
        """Ejecuta la creación de una nueva reserva."""
        try:
            id_cliente, id_servicio = self._obtener_ids_seleccionados()

            # Validar selección de cliente y servicio
            if not id_cliente or not id_servicio:
                self.lbl_resultado.configure(
                    text="✗ Seleccione un cliente y un servicio.",
                    fg=COLORES["error"]
                )
                return

            # Validar duración
            duracion_str = self.var_duracion.get()
            if duracion_str in ["", "Ej: 2 (número de horas)"]:
                self.lbl_resultado.configure(
                    text="✗ Ingrese la duración en horas.",
                    fg=COLORES["error"]
                )
                return

            duracion = float(duracion_str)

            # Buscar tipo de servicio para armar params
            servicio = self.app.controlador.buscar_servicio_por_id(id_servicio)
            params_extra = self._armar_params_extra(
                servicio.tipo_servicio() if servicio else ""
            )

            # Crear la reserva a través del controlador
            resultado = self.app.controlador.crear_reserva(
                id_cliente=id_cliente,
                id_servicio=id_servicio,
                duracion_horas=duracion,
                parametros_extra=params_extra
            )

            if resultado["exito"]:
                self.lbl_resultado.configure(
                    text=f"✓ {resultado['mensaje']}", fg=COLORES["exito"]
                )
                self.lbl_costo.configure(
                    text=f"Costo final confirmado: ${resultado['costo']:,.2f}",
                    fg=COLORES["exito"]
                )
                self.app.actualizar_estado(resultado["mensaje"], "exito")
                self._actualizar_tabla()
            else:
                self.lbl_resultado.configure(
                    text=f"✗ {resultado['mensaje']}", fg=COLORES["error"]
                )
                self.app.actualizar_estado(resultado["mensaje"], "error")

        except ValueError:
            self.lbl_resultado.configure(
                text="✗ La duración debe ser un número válido.", fg=COLORES["error"]
            )
        except Exception as e:
            self.lbl_resultado.configure(
                text=f"✗ Error inesperado: {e}", fg=COLORES["error"]
            )

    def _crear_tabla_reservas(self):
        """Crea la tabla de reservas del sistema."""
        marco_titulo = tk.Frame(self.marco, bg=COLORES["fondo"])
        marco_titulo.pack(fill="x", padx=30)

        tk.Label(
            marco_titulo,
            text="Reservas del Sistema",
            font=("Verdana", 12, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).pack(side="left")

        btn_actualizar = self.app.crear_boton(
            marco_titulo, "↻ Actualizar",
            self._actualizar_tabla, ancho=12, estilo="secundario"
        )
        btn_actualizar.pack(side="right")

        # Columnas de la tabla
        columnas = ["ID", "Estado", "Cliente", "Servicio", "Tipo Servicio",
                    "Duración", "Costo Total", "Fecha Reserva", "Notas"]
        self.tabla = self.app.crear_tabla(self.marco, columnas, alto=10)

        # Acciones sobre reservas
        marco_acciones = tk.Frame(self.marco, bg=COLORES["fondo"])
        marco_acciones.pack(fill="x", padx=30, pady=(5, 20))

        btn_cancelar = self.app.crear_boton(
            marco_acciones, "Cancelar Reserva",
            self._cancelar_seleccionada, ancho=18, estilo="peligro"
        )
        btn_cancelar.pack(side="left", padx=(0, 10))

        btn_completar = self.app.crear_boton(
            marco_acciones, "Marcar Completada",
            self._completar_seleccionada, ancho=18, estilo="exitoso"
        )
        btn_completar.pack(side="left", padx=(0, 10))

        # Contador de reservas
        self.lbl_conteo = tk.Label(
            marco_acciones, text="", font=("Verdana", 9),
            fg=COLORES["acento_claro"], bg=COLORES["fondo"]
        )
        self.lbl_conteo.pack(side="left")

    def _actualizar_tabla(self):
        """Recarga los datos de la tabla de reservas."""
        reservas = self.app.controlador.obtener_reservas()
        datos = [r.to_dict() for r in reservas]
        self.app.llenar_tabla(self.tabla, datos)
        self.lbl_conteo.configure(text=f"Total: {len(reservas)} reserva(s)")

    def _cancelar_seleccionada(self):
        """Cancela la reserva seleccionada en la tabla."""
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione una reserva de la tabla.")
            return

        valores = self.tabla.item(seleccionado[0], "values")
        id_reserva = valores[0]
        estado_actual = valores[1]

        # Verificar que sea cancelable
        if estado_actual in ["CANCELADA", "COMPLETADA"]:
            messagebox.showwarning(
                "No permitido",
                f"No se puede cancelar una reserva en estado '{estado_actual}'."
            )
            return

        # Confirmar cancelación
        motivo = tk.simpledialog_motivo(self.marco) if False else ""
        confirmar = messagebox.askyesno(
            "Confirmar cancelación",
            f"¿Cancelar la reserva '{id_reserva}' del cliente '{valores[2]}'?"
        )

        if confirmar:
            resultado = self.app.controlador.cancelar_reserva(id_reserva, "Cancelada por usuario")
            if resultado["exito"]:
                self.app.actualizar_estado(resultado["mensaje"], "exito")
                messagebox.showinfo("Éxito", resultado["mensaje"])
            else:
                self.app.actualizar_estado(resultado["mensaje"], "error")
                messagebox.showerror("Error", resultado["mensaje"])
            self._actualizar_tabla()

    def _completar_seleccionada(self):
        """Marca como completada la reserva seleccionada."""
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione una reserva de la tabla.")
            return

        valores = self.tabla.item(seleccionado[0], "values")
        id_reserva = valores[0]
        estado_actual = valores[1]

        # Solo las confirmadas pueden completarse
        if estado_actual != "CONFIRMADA":
            messagebox.showwarning(
                "No permitido",
                f"Solo reservas CONFIRMADAS pueden completarse. Estado actual: '{estado_actual}'."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Marcar la reserva '{id_reserva}' como completada?"
        )

        if confirmar:
            resultado = self.app.controlador.completar_reserva(id_reserva)
            if resultado["exito"]:
                self.app.actualizar_estado(resultado["mensaje"], "exito")
                messagebox.showinfo("Éxito", resultado["mensaje"])
            else:
                self.app.actualizar_estado(resultado["mensaje"], "error")
                messagebox.showerror("Error", resultado["mensaje"])
            self._actualizar_tabla()
