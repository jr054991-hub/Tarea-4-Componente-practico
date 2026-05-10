"""
=============================================================
  Vista Clientes - Sistema CSR
  Formulario y tabla para gestionar clientes
=============================================================
"""

import tkinter as tk
from tkinter import messagebox

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


class VistaClientes:
    """
    Vista para gestión completa de clientes:
    - Formulario de registro con validaciones en tiempo real.
    - Tabla de clientes registrados con acciones.
    """

    def __init__(self, padre, app):
        """
        Inicializa la vista de clientes.
        
        Args:
            padre: Frame padre donde se renderizará.
            app: Instancia principal de CSRApp.
        """
        # Referencia al frame padre y a la app
        self.padre = padre
        self.app = app
        # Diccionario de variables de los campos del formulario
        self.campos = {}
        # Tabla de clientes
        self.tabla = None
        # Construir la vista
        self._construir()

    def _construir(self):
        """Construye la vista completa de clientes."""
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
            "Gestión de Clientes",
            "Registro, consulta y administración de clientes del sistema"
        )

        # Formulario de registro
        self._crear_formulario()

        # Separador
        tk.Frame(self.marco, bg=COLORES["separador"], height=1).pack(fill="x", padx=30, pady=15)

        # Tabla de clientes
        self._crear_tabla_clientes()

        # Cargar datos iniciales en la tabla
        self._actualizar_tabla()

    def _crear_formulario(self):
        """Crea el formulario de registro de clientes."""
        # Marco del formulario con borde negro
        marco_form = tk.LabelFrame(
            self.marco,
            text="  Nuevo Cliente  ",
            font=("Verdana", 10, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"],
            bd=1,
            relief="solid",
            labelanchor="nw"
        )
        marco_form.pack(fill="x", padx=30, pady=(15, 0))

        # Marco interno con padding
        interno = tk.Frame(marco_form, bg=COLORES["fondo"])
        interno.pack(fill="x", padx=20, pady=15)

        # Definición de los campos del formulario
        campos_def = [
            ("Nombre Completo *", "nombre",    "Ej: Juan Pérez García"),
            ("Correo Electrónico *", "email",  "Ej: juan@empresa.com"),
            ("Teléfono *",        "telefono",  "Solo dígitos (7-15 caracteres)"),
            ("N° Documento *",    "documento", "Mínimo 5 caracteres"),
        ]

        # Crear campos en cuadrícula de 2 columnas
        for i, (etiqueta, clave, placeholder) in enumerate(campos_def):
            # Calcular posición en la cuadrícula
            fila = i // 2
            columna = (i % 2) * 2

            # Etiqueta del campo
            tk.Label(
                interno,
                text=etiqueta,
                font=("Verdana", 9, "bold"),
                fg=COLORES["texto"],
                bg=COLORES["fondo"]
            ).grid(row=fila * 2, column=columna, sticky="w", pady=(8, 2), padx=(0, 20))

            # Variable de texto del campo
            var = tk.StringVar()
            self.campos[clave] = var

            # Campo de entrada
            entry = tk.Entry(
                interno,
                textvariable=var,
                font=("Verdana", 10),
                fg=COLORES["texto"],
                bg=COLORES["fondo"],
                bd=1,
                relief="solid",
                highlightbackground=COLORES["borde"],
                highlightthickness=1,
                width=32
            )
            entry.grid(row=fila * 2 + 1, column=columna, sticky="ew", padx=(0, 20), pady=(0, 5))

            # Placeholder simulado con texto gris
            entry.insert(0, placeholder)
            entry.configure(fg="#AAAAAA")

            # Funciones para el efecto placeholder
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

        # Configurar peso de columnas para distribución
        interno.columnconfigure(0, weight=1)
        interno.columnconfigure(2, weight=1)

        # Marco de botones del formulario
        marco_botones = tk.Frame(marco_form, bg=COLORES["fondo"])
        marco_botones.pack(fill="x", padx=20, pady=(5, 15))

        # Botón de registrar
        btn_registrar = self.app.crear_boton(
            marco_botones, "Registrar Cliente",
            self._registrar_cliente, ancho=20
        )
        btn_registrar.pack(side="left", padx=(0, 10))

        # Botón de limpiar formulario
        btn_limpiar = self.app.crear_boton(
            marco_botones, "Limpiar",
            self._limpiar_formulario, ancho=12, estilo="secundario"
        )
        btn_limpiar.pack(side="left")

        # Etiqueta de mensaje de resultado
        self.lbl_resultado = tk.Label(
            marco_form,
            text="",
            font=("Verdana", 9),
            bg=COLORES["fondo"]
        )
        self.lbl_resultado.pack(padx=20, pady=(0, 10), anchor="w")

    def _crear_tabla_clientes(self):
        """Crea la tabla de clientes registrados."""
        # Título de la tabla
        marco_titulo_tabla = tk.Frame(self.marco, bg=COLORES["fondo"])
        marco_titulo_tabla.pack(fill="x", padx=30)

        tk.Label(
            marco_titulo_tabla,
            text="Clientes Registrados",
            font=("Verdana", 12, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"]
        ).pack(side="left")

        # Botón de actualizar tabla
        btn_actualizar = self.app.crear_boton(
            marco_titulo_tabla, "↻ Actualizar",
            self._actualizar_tabla, ancho=12, estilo="secundario"
        )
        btn_actualizar.pack(side="right")

        # Columnas de la tabla de clientes
        columnas = ["ID", "Nombre", "Email", "Teléfono", "Documento", "Estado", "Reservas"]

        # Crear la tabla usando el método de la app
        self.tabla = self.app.crear_tabla(self.marco, columnas, alto=10)

        # Marco de acciones sobre la tabla
        marco_acciones = tk.Frame(self.marco, bg=COLORES["fondo"])
        marco_acciones.pack(fill="x", padx=30, pady=(5, 20))

        # Botón de desactivar cliente seleccionado
        btn_desactivar = self.app.crear_boton(
            marco_acciones, "Desactivar Cliente",
            self._desactivar_seleccionado, ancho=18, estilo="peligro"
        )
        btn_desactivar.pack(side="left", padx=(0, 10))

        # Contador de clientes
        self.lbl_conteo = tk.Label(
            marco_acciones,
            text="",
            font=("Verdana", 9),
            fg=COLORES["acento_claro"],
            bg=COLORES["fondo"]
        )
        self.lbl_conteo.pack(side="left")

    def _registrar_cliente(self):
        """Ejecuta el registro de un nuevo cliente desde el formulario."""
        # Obtener placeholders para ignorarlos
        placeholders = {
            "nombre":    "Ej: Juan Pérez García",
            "email":     "Ej: juan@empresa.com",
            "telefono":  "Solo dígitos (7-15 caracteres)",
            "documento": "Mínimo 5 caracteres",
        }

        # Extraer valores del formulario (ignorar placeholders)
        datos = {}
        for clave, var in self.campos.items():
            valor = var.get()
            datos[clave] = "" if valor == placeholders.get(clave, "") else valor

        # Llamar al controlador para registrar el cliente
        resultado = self.app.controlador.registrar_cliente(
            datos["nombre"], datos["email"],
            datos["telefono"], datos["documento"]
        )

        # Mostrar resultado al usuario
        if resultado["exito"]:
            # Éxito: mensaje verde y actualizar tabla
            self.lbl_resultado.configure(
                text=f"✓ {resultado['mensaje']}",
                fg=COLORES["exito"]
            )
            self.app.actualizar_estado(resultado["mensaje"], "exito")
            self._limpiar_formulario()
            self._actualizar_tabla()
        else:
            # Error: mensaje rojo
            self.lbl_resultado.configure(
                text=f"✗ {resultado['mensaje']}",
                fg=COLORES["error"]
            )
            self.app.actualizar_estado(resultado["mensaje"], "error")

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        # Restablecer placeholders de cada campo
        placeholders = {
            "nombre":    "Ej: Juan Pérez García",
            "email":     "Ej: juan@empresa.com",
            "telefono":  "Solo dígitos (7-15 caracteres)",
            "documento": "Mínimo 5 caracteres",
        }
        for clave, var in self.campos.items():
            var.set(placeholders.get(clave, ""))
        # Limpiar mensaje de resultado
        self.lbl_resultado.configure(text="")

    def _actualizar_tabla(self):
        """Recarga los datos de la tabla de clientes."""
        # Obtener lista de clientes del controlador
        clientes = self.app.controlador.obtener_clientes()
        # Convertir a lista de diccionarios para la tabla
        datos = [c.to_dict() for c in clientes]
        # Llenar la tabla con los datos
        self.app.llenar_tabla(self.tabla, datos)
        # Actualizar contador
        self.lbl_conteo.configure(
            text=f"Total: {len(clientes)} cliente(s)"
        )

    def _desactivar_seleccionado(self):
        """Desactiva el cliente seleccionado en la tabla."""
        # Obtener el item seleccionado en la tabla
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Seleccione un cliente de la tabla.")
            return

        # Obtener el ID del cliente seleccionado
        valores = self.tabla.item(seleccionado[0], "values")
        id_cliente = valores[0]

        # Confirmar la acción con el usuario
        confirmar = messagebox.askyesno(
            "Confirmar desactivación",
            f"¿Desea desactivar al cliente '{valores[1]}'?\n"
            f"El cliente no podrá realizar nuevas reservas."
        )

        if confirmar:
            # Ejecutar desactivación
            resultado = self.app.controlador.eliminar_cliente(id_cliente)
            if resultado["exito"]:
                self.app.actualizar_estado(resultado["mensaje"], "exito")
                messagebox.showinfo("Éxito", resultado["mensaje"])
            else:
                self.app.actualizar_estado(resultado["mensaje"], "error")
                messagebox.showerror("Error", resultado["mensaje"])
            # Actualizar la tabla
            self._actualizar_tabla()
