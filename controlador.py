"""
=============================================================
  Módulo Controlador - Sistema CSR
  Gestiona todas las operaciones del sistema:
  clientes, servicios, reservas y simulaciones
=============================================================
"""

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriEspecializada
from reserva import Reserva
from exceptions import (
    ClienteInvalidoError, ServicioNoDisponibleError,
    ReservaInvalidaError, ParametroFaltanteError, EstadoReservaError
)


class ControladorCSR:
    """
    Controlador central del sistema CSR.
    Gestiona las listas de clientes, servicios y reservas,
    y orquesta todas las operaciones del negocio.
    """

    def __init__(self, logger):
        """
        Inicializa el controlador con las listas vacías y el logger.
        
        Args:
            logger: Instancia del Logger para registrar eventos y errores.
        """
        # Lista interna de clientes registrados
        self.__clientes = []
        # Lista interna de servicios disponibles
        self.__servicios = []
        # Lista interna de todas las reservas
        self.__reservas = []
        # Referencia al sistema de logs
        self.__logger = logger

        # Cargar datos de demostración al iniciar
        self._cargar_datos_demo()

    # ---- Métodos de gestión de Clientes ----

    def registrar_cliente(self, nombre: str, email: str,
                          telefono: str, documento: str) -> dict:
        """
        Registra un nuevo cliente en el sistema con manejo de excepciones.
        
        Args:
            nombre, email, telefono, documento: Datos del cliente.
            
        Returns:
            Diccionario con resultado de la operación.
        """
        resultado = {"exito": False, "mensaje": "", "cliente": None}

        try:
            # Intentar crear el cliente (puede lanzar excepciones)
            nuevo_cliente = Cliente(nombre, email, telefono, documento)
            # Verificar duplicados por documento
            for c in self.__clientes:
                if c.documento == nuevo_cliente.documento:
                    raise ClienteInvalidoError(
                        f"Ya existe un cliente con documento '{documento}'."
                    )
            # Agregar a la lista interna
            self.__clientes.append(nuevo_cliente)

        except ParametroFaltanteError as e:
            # Error por campo vacío
            self.__logger.registrar_error(f"Campo faltante al registrar cliente", e)
            resultado["mensaje"] = str(e)

        except ClienteInvalidoError as e:
            # Error por datos inválidos
            self.__logger.registrar_error(f"Datos inválidos al registrar cliente", e)
            resultado["mensaje"] = str(e)

        except Exception as e:
            # Error inesperado al registrar
            self.__logger.registrar_error("Error inesperado al registrar cliente", e)
            resultado["mensaje"] = f"Error inesperado: {e}"

        else:
            # Éxito: registrar evento y retornar cliente
            self.__logger.registrar_evento(
                f"Cliente registrado: {nuevo_cliente.nombre} [{nuevo_cliente.id}]"
            )
            resultado["exito"] = True
            resultado["cliente"] = nuevo_cliente
            resultado["mensaje"] = (
                f"Cliente '{nuevo_cliente.nombre}' registrado exitosamente [{nuevo_cliente.id}]"
            )

        finally:
            # Siempre retornar el resultado, haya error o no
            return resultado

    def obtener_clientes(self) -> list:
        """Retorna la lista completa de clientes registrados."""
        return self.__clientes.copy()

    def buscar_cliente_por_id(self, id_cliente: str):
        """
        Busca y retorna un cliente por su ID.
        
        Args:
            id_cliente: Identificador del cliente a buscar.
            
        Returns:
            Objeto Cliente o None si no se encuentra.
        """
        for cliente in self.__clientes:
            if cliente.id == id_cliente:
                return cliente
        return None

    def eliminar_cliente(self, id_cliente: str) -> dict:
        """
        Desactiva un cliente del sistema (no elimina, desactiva).
        
        Args:
            id_cliente: ID del cliente a desactivar.
        """
        resultado = {"exito": False, "mensaje": ""}
        try:
            # Buscar el cliente por ID
            cliente = self.buscar_cliente_por_id(id_cliente)
            if not cliente:
                raise ClienteInvalidoError(f"No se encontró cliente con ID '{id_cliente}'")
            # Desactivar el cliente
            cliente.desactivar()
            self.__logger.registrar_evento(f"Cliente desactivado: {cliente.nombre} [{id_cliente}]")
            resultado["exito"] = True
            resultado["mensaje"] = f"Cliente '{cliente.nombre}' desactivado exitosamente."
        except ClienteInvalidoError as e:
            self.__logger.registrar_error("Error al desactivar cliente", e)
            resultado["mensaje"] = str(e)
        finally:
            return resultado

    # ---- Métodos de gestión de Servicios ----

    def agregar_servicio(self, tipo: str, **kwargs) -> dict:
        """
        Agrega un nuevo servicio al sistema.
        
        Args:
            tipo: Tipo de servicio ('sala', 'equipo', 'asesoria').
            **kwargs: Parámetros específicos del tipo de servicio.
            
        Returns:
            Diccionario con resultado de la operación.
        """
        resultado = {"exito": False, "mensaje": "", "servicio": None}

        try:
            # Crear el servicio según el tipo indicado
            if tipo == "sala":
                nuevo_servicio = ReservaSala(
                    nombre=kwargs["nombre"],
                    capacidad_max=int(kwargs["capacidad_max"]),
                    precio_base=float(kwargs["precio_base"]),
                    tiene_proyector=kwargs.get("tiene_proyector", False),
                    tiene_videoconferencia=kwargs.get("tiene_videoconferencia", False)
                )
            elif tipo == "equipo":
                nuevo_servicio = AlquilerEquipo(
                    nombre=kwargs["nombre"],
                    tipo_equipo=kwargs["tipo_equipo"],
                    precio_base=float(kwargs["precio_base"]),
                    cantidad_disponible=int(kwargs.get("cantidad_disponible", 1)),
                    requiere_deposito=kwargs.get("requiere_deposito", True)
                )
            elif tipo == "asesoria":
                nuevo_servicio = AsesoriEspecializada(
                    nombre=kwargs["nombre"],
                    area=kwargs["area"],
                    precio_base=float(kwargs["precio_base"]),
                    nombre_asesor=kwargs["nombre_asesor"],
                    nivel_experto=kwargs.get("nivel_experto", "junior")
                )
            else:
                raise ServicioNoDisponibleError(
                    f"Tipo de servicio desconocido: '{tipo}'. Use: sala, equipo, asesoria"
                )

            # Agregar a la lista interna de servicios
            self.__servicios.append(nuevo_servicio)

        except KeyError as e:
            # Campo requerido no proporcionado
            self.__logger.registrar_error("Parámetro faltante al crear servicio", e)
            resultado["mensaje"] = f"Parámetro faltante: {e}"

        except (ServicioNoDisponibleError, ParametroFaltanteError) as e:
            # Error en los datos del servicio
            self.__logger.registrar_error("Error al crear servicio", e)
            resultado["mensaje"] = str(e)

        except ValueError as e:
            # Error de conversión de tipos (ej: texto donde se espera número)
            self.__logger.registrar_error("Tipo de dato inválido al crear servicio", e)
            resultado["mensaje"] = f"Valor inválido: {e}"

        except Exception as e:
            # Error inesperado
            self.__logger.registrar_error("Error inesperado al crear servicio", e)
            resultado["mensaje"] = f"Error inesperado: {e}"

        else:
            # Éxito al crear el servicio
            self.__logger.registrar_evento(
                f"Servicio creado: {nuevo_servicio.nombre} [{nuevo_servicio.id}]"
            )
            resultado["exito"] = True
            resultado["servicio"] = nuevo_servicio
            resultado["mensaje"] = (
                f"Servicio '{nuevo_servicio.nombre}' creado exitosamente [{nuevo_servicio.id}]"
            )

        finally:
            return resultado

    def obtener_servicios(self) -> list:
        """Retorna la lista completa de servicios."""
        return self.__servicios.copy()

    def buscar_servicio_por_id(self, id_servicio: str):
        """
        Busca un servicio por su ID.
        
        Returns:
            Objeto Servicio o None si no se encuentra.
        """
        for servicio in self.__servicios:
            if servicio.id == id_servicio:
                return servicio
        return None

    # ---- Métodos de gestión de Reservas ----

    def crear_reserva(self, id_cliente: str, id_servicio: str,
                      duracion_horas: float, fecha_reserva: str = None,
                      parametros_extra: dict = None) -> dict:
        """
        Crea y procesa una nueva reserva en el sistema.
        
        Args:
            id_cliente: ID del cliente que reserva.
            id_servicio: ID del servicio a reservar.
            duracion_horas: Duración en horas.
            fecha_reserva: Fecha deseada (YYYY-MM-DD HH:MM).
            parametros_extra: Parámetros adicionales del servicio.
            
        Returns:
            Diccionario con resultado de la operación.
        """
        resultado = {"exito": False, "mensaje": "", "reserva": None, "costo": 0}

        try:
            # Buscar el cliente por ID
            cliente = self.buscar_cliente_por_id(id_cliente)
            if not cliente:
                raise ReservaInvalidaError(
                    f"No se encontró cliente con ID '{id_cliente}'"
                )

            # Buscar el servicio por ID
            servicio = self.buscar_servicio_por_id(id_servicio)
            if not servicio:
                raise ReservaInvalidaError(
                    f"No se encontró servicio con ID '{id_servicio}'"
                )

            # Crear la reserva
            nueva_reserva = Reserva(
                cliente=cliente,
                servicio=servicio,
                duracion_horas=duracion_horas,
                fecha_reserva=fecha_reserva,
                parametros_extra=parametros_extra or {}
            )

            # Procesar la reserva (confirmar automáticamente)
            resultado_proceso = nueva_reserva.procesar()

            if resultado_proceso["exito"]:
                # Agregar a la lista de reservas del sistema
                self.__reservas.append(nueva_reserva)
                resultado["exito"] = True
                resultado["reserva"] = nueva_reserva
                resultado["costo"] = resultado_proceso["costo"]
                resultado["mensaje"] = resultado_proceso["mensaje"]
                self.__logger.registrar_evento(
                    f"Reserva creada: {nueva_reserva.id} | "
                    f"Cliente: {cliente.nombre} | Servicio: {servicio.nombre} | "
                    f"Costo: ${resultado_proceso['costo']:,.2f}"
                )
            else:
                resultado["mensaje"] = resultado_proceso["mensaje"]
                self.__logger.registrar_error(
                    f"Fallo al procesar reserva para {cliente.nombre}", None
                )

        except (ReservaInvalidaError, ServicioNoDisponibleError, EstadoReservaError) as e:
            # Error conocido del dominio
            self.__logger.registrar_error("Error al crear reserva", e)
            resultado["mensaje"] = str(e)

        except Exception as e:
            # Error inesperado
            self.__logger.registrar_error("Error inesperado al crear reserva", e)
            resultado["mensaje"] = f"Error inesperado: {e}"

        finally:
            return resultado

    def cancelar_reserva(self, id_reserva: str, motivo: str = "") -> dict:
        """
        Cancela una reserva existente.
        
        Args:
            id_reserva: ID de la reserva a cancelar.
            motivo: Razón de la cancelación.
        """
        resultado = {"exito": False, "mensaje": ""}
        try:
            # Buscar la reserva por ID
            reserva = self._buscar_reserva_por_id(id_reserva)
            if not reserva:
                raise ReservaInvalidaError(f"No se encontró reserva con ID '{id_reserva}'")

            # Intentar cancelar la reserva
            reserva.cancelar(motivo)
            self.__logger.registrar_evento(
                f"Reserva cancelada: {id_reserva} | Motivo: {motivo or 'Sin motivo'}"
            )
            resultado["exito"] = True
            resultado["mensaje"] = f"Reserva '{id_reserva}' cancelada exitosamente."

        except EstadoReservaError as e:
            # No se puede cancelar por estado actual
            self.__logger.registrar_error("Error al cancelar reserva", e)
            resultado["mensaje"] = str(e)

        except ReservaInvalidaError as e:
            self.__logger.registrar_error("Reserva no encontrada para cancelar", e)
            resultado["mensaje"] = str(e)

        finally:
            return resultado

    def completar_reserva(self, id_reserva: str) -> dict:
        """
        Marca una reserva como completada.
        
        Args:
            id_reserva: ID de la reserva a completar.
        """
        resultado = {"exito": False, "mensaje": ""}
        try:
            reserva = self._buscar_reserva_por_id(id_reserva)
            if not reserva:
                raise ReservaInvalidaError(f"No se encontró reserva con ID '{id_reserva}'")
            reserva.completar()
            self.__logger.registrar_evento(f"Reserva completada: {id_reserva}")
            resultado["exito"] = True
            resultado["mensaje"] = f"Reserva '{id_reserva}' marcada como completada."
        except EstadoReservaError as e:
            self.__logger.registrar_error("Error al completar reserva", e)
            resultado["mensaje"] = str(e)
        except ReservaInvalidaError as e:
            self.__logger.registrar_error("Reserva no encontrada", e)
            resultado["mensaje"] = str(e)
        finally:
            return resultado

    def obtener_reservas(self) -> list:
        """Retorna la lista completa de reservas."""
        return self.__reservas.copy()

    def _buscar_reserva_por_id(self, id_reserva: str):
        """
        Busca una reserva por su ID en la lista interna.
        
        Returns:
            Objeto Reserva o None si no se encuentra.
        """
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva
        return None

    def obtener_estadisticas(self) -> dict:
        """
        Calcula y retorna estadísticas generales del sistema.
        
        Returns:
            Diccionario con métricas del sistema.
        """
        try:
            # Contar reservas por estado
            total_reservas = len(self.__reservas)
            confirmadas = sum(1 for r in self.__reservas if r.estado == "CONFIRMADA")
            canceladas = sum(1 for r in self.__reservas if r.estado == "CANCELADA")
            completadas = sum(1 for r in self.__reservas if r.estado == "COMPLETADA")
            pendientes = sum(1 for r in self.__reservas if r.estado == "PENDIENTE")

            # Calcular ingresos totales (solo reservas confirmadas y completadas)
            ingresos = sum(
                r.costo_calculado for r in self.__reservas
                if r.estado in ["CONFIRMADA", "COMPLETADA"]
            )

            return {
                "total_clientes": len(self.__clientes),
                "clientes_activos": sum(1 for c in self.__clientes if c.activo),
                "total_servicios": len(self.__servicios),
                "servicios_disponibles": sum(1 for s in self.__servicios if s.disponible),
                "total_reservas": total_reservas,
                "confirmadas": confirmadas,
                "canceladas": canceladas,
                "completadas": completadas,
                "pendientes": pendientes,
                "ingresos_totales": ingresos
            }
        except Exception as e:
            self.__logger.registrar_error("Error al calcular estadísticas", e)
            return {}

    # ---- Datos de demostración (10 operaciones simuladas) ----

    def _cargar_datos_demo(self):
        """
        Simula 10 operaciones completas incluyendo casos válidos e inválidos.
        Demuestra el manejo de excepciones en acción.
        """
        self.__logger.registrar_evento("=== Iniciando carga de datos de demostración ===")

        # --- CLIENTES (operaciones 1-4) ---

        # Operación 1: Cliente válido
        self.registrar_cliente("Ana María López", "ana.lopez@email.com", "3001234567", "1023456789")

        # Operación 2: Cliente válido
        self.registrar_cliente("Carlos Rodríguez", "carlos.r@empresa.co", "3112223344", "98765432")

        # Operación 3: Cliente con email inválido (debe generar error)
        self.registrar_cliente("Pedro Inválido", "email_sin_arroba", "3009876543", "11223344")

        # Operación 4: Cliente válido
        self.registrar_cliente("Laura Gómez", "laura.gomez@correo.com", "6014567890", "456789012")

        # --- SERVICIOS (operaciones 5-7) ---

        # Operación 5: Sala de reuniones válida
        self.agregar_servicio("sala",
            nombre="Sala Innovación",
            capacidad_max=20,
            precio_base=150000,
            tiene_proyector=True,
            tiene_videoconferencia=True
        )

        # Operación 6: Equipo con tipo inválido (debe generar error)
        self.agregar_servicio("equipo",
            nombre="Equipo Desconocido",
            tipo_equipo="dron",  # Tipo no válido
            precio_base=50000
        )

        # Operación 7: Asesoría válida
        self.agregar_servicio("asesoria",
            nombre="Consultoría Cloud AWS",
            area="cloud",
            precio_base=200000,
            nombre_asesor="Ing. Felipe Torres",
            nivel_experto="experto"
        )

        # Operación 8: Equipo válido
        self.agregar_servicio("equipo",
            nombre="Laptop Dell XPS",
            tipo_equipo="laptop",
            precio_base=45000,
            cantidad_disponible=5,
            requiere_deposito=True
        )

        # --- RESERVAS (operaciones 9-10) ---
        clientes = self.obtener_clientes()
        servicios = self.obtener_servicios()

        if clientes and servicios:
            # Operación 9: Reserva válida de sala
            self.crear_reserva(
                id_cliente=clientes[0].id,
                id_servicio=servicios[0].id,
                duracion_horas=3,
                parametros_extra={"personas": 10}
            )

            # Operación 10: Reserva de asesoría
            if len(clientes) > 1 and len(servicios) > 1:
                self.crear_reserva(
                    id_cliente=clientes[1].id,
                    id_servicio=servicios[1].id,
                    duracion_horas=2,
                    parametros_extra={"sesiones": 1}
                )

        self.__logger.registrar_evento("=== Datos de demostración cargados exitosamente ===")
