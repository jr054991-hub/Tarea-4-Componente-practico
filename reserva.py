
import datetime  # Para manejar fechas y horas de la reserva - Yenifer Gonzalez
from exceptions import (
    ReservaInvalidaError, EstadoReservaError,
    ServicioNoDisponibleError, ParametroFaltanteError
)


class Reserva:
    """
    Clase que representa una reserva en el sistema CSR.
    Integra un cliente con un servicio específico,
    gestiona estados y aplica manejo robusto de excepciones.
    
    Estados posibles:
        - PENDIENTE: Creada pero no confirmada
        - CONFIRMADA: Aprobada y activa
        - CANCELADA: Anulada por el cliente o el sistema
        - COMPLETADA: Servicio prestado exitosamente
    """

    # Estados válidos de una reserva _ Yenifer Gonzalez
    ESTADOS_VALIDOS = ["PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"]

    # Contador estático para generar IDs de reserva _ Yenifer Gonzalez
    _contador = 1

    def __init__(self, cliente, servicio, duracion_horas: float,
                fecha_reserva: str = None, parametros_extra: dict = None):
        """
        Inicializa una reserva con cliente, servicio y duración.
        
        Args:
            cliente: Objeto Cliente asociado a la reserva.
            servicio: Objeto Servicio a reservar.
            duracion_horas: Duración del servicio en horas.
            fecha_reserva: Fecha y hora deseada (formato YYYY-MM-DD HH:MM).
            parametros_extra: Parámetros adicionales según el tipo de servicio.
            
        Raises:
            ParametroFaltanteError: Si cliente o servicio son None.
            ReservaInvalidaError: Si la duración es inválida.
            ServicioNoDisponibleError: Si el servicio no está disponible.
        """
        # Validar que el cliente sea válido _   Yenifer Gonzalez
        if cliente is None:
            raise ParametroFaltanteError("cliente")

        # Validar que el servicio sea válido _  Yenifer Gonzalez
        if servicio is None:
            raise ParametroFaltanteError("servicio")

        # Validar que la duración sea positiva _  Yenifer Gonzalez
        if duracion_horas <= 0:
            raise ReservaInvalidaError(
                f"La duración debe ser mayor a cero. Recibido: {duracion_horas}"
            )

        # Verificar que el cliente esté activo _  Yenifer Gonzalez
        if not cliente.activo:
            raise ReservaInvalidaError(
                f"El cliente '{cliente.nombre}' está inactivo y no puede realizar reservas."
            )

        # Verificar que el servicio esté disponible _  Yenifer Gonzalez
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible para reservar."
            )

        # Generar ID único de reserva _ Yenifer Gonzalez
        self.__id = f"RES-{Reserva._contador:04d}"
        Reserva._contador += 1

        # Asignar referencias a cliente y servicio _  Yenifer Gonzalez
        self.__cliente = cliente
        self.__servicio = servicio

        # Atributos de la reserva _  Yenifer Gonzalez
        self.__duracion_horas = duracion_horas
        self.__parametros_extra = parametros_extra or {}
        self.__estado = "PENDIENTE"                           # Estado inicial
        self.__fecha_creacion = datetime.datetime.now()       # Fecha de creación
        self.__costo_calculado = 0.0                          # Costo (se calcula al confirmar)
        self.__notas = ""                                     # Notas adicionales

        # Asignar fecha de la reserva _  Yenifer Gonzalez
        if fecha_reserva:
            try:
                # Intentar parsear la fecha proporcionada _  Yenifer Gonzalez
                self.__fecha_reserva = datetime.datetime.strptime(fecha_reserva, "%Y-%m-%d %H:%M")
            except ValueError:
                # Si el formato es incorrecto, usar la fecha actual + 1 día _  Yenifer Gonzalez
                self.__fecha_reserva = datetime.datetime.now() + datetime.timedelta(days=1)
        else:
            # Si no se proporciona fecha, usar mañana como fecha por defecto _  Yenifer Gonzalez
            self.__fecha_reserva = datetime.datetime.now() + datetime.timedelta(days=1)

    # Propiedades  _ Yenifer Gonzalez

    @property
    def id(self) -> str:
        """Identificador único de la reserva."""
        return self.__id

    @property
    def cliente(self):
        """Cliente asociado a la reserva."""
        return self.__cliente

    @property
    def servicio(self):
        """Servicio reservado."""
        return self.__servicio

    @property
    def duracion_horas(self) -> float:
        """Duración de la reserva en horas."""
        return self.__duracion_horas

    @property
    def estado(self) -> str:
        """Estado actual de la reserva."""
        return self.__estado

    @property
    def fecha_creacion(self) -> datetime.datetime:
        """Fecha en que fue creada la reserva."""
        return self.__fecha_creacion

    @property
    def fecha_reserva(self) -> datetime.datetime:
        """Fecha programada para la reserva."""
        return self.__fecha_reserva

    @property
    def costo_calculado(self) -> float:
        """Costo total calculado de la reserva."""
        return self.__costo_calculado

    @property
    def notas(self) -> str:
        """Notas adicionales de la reserva."""
        return self.__notas

    @notas.setter
    def notas(self, valor: str):
        """Setter para agregar notas a la reserva."""
        self.__notas = str(valor).strip()

    # ---- Métodos de gestión de estados ----

    def calcular_costo_preview(self) -> float:
        """
        Calcula un preview del costo sin confirmar la reserva.
        
        Returns:
            Costo estimado con IVA en pesos.
        """
        try:
            # Intentar calcular el costo con los parámetros actuales _  Yenifer Gonzalez
            costo = self.__servicio.calcular_costo_con_iva(
                self.__duracion_horas, **self.__parametros_extra
            )
            return costo
        except Exception as e:
            # Si hay error al calcular, relanzar como ReservaInvalidaError _  Yenifer Gonzalez
            raise ReservaInvalidaError(
                f"No se pudo calcular el costo: {e}"
            ) from e

    def confirmar(self) -> float:
        """
        Confirma la reserva, calcula el costo final y la registra al cliente.
        
        Returns:
            Costo total confirmado de la reserva.
            
        Raises:
            EstadoReservaError: Si la reserva no está en estado PENDIENTE.
            ReservaInvalidaError: Si hay un error al procesar la reserva.
        """
        try:
            # Verificar que la reserva esté en estado PENDIENTE _  Yenifer Gonzalez
            if self.__estado != "PENDIENTE":
                raise EstadoReservaError(self.__estado, "confirmar")

            # Validar parámetros del servicio antes de confirmar _  Yenifer Gonzalez
            self.__servicio.validar_parametros(
                duracion_horas=self.__duracion_horas,
                **self.__parametros_extra
            )

            # Calcular el costo final con IVA _  Yenifer Gonzalez
            costo = self.__servicio.calcular_costo_con_iva(
                self.__duracion_horas, **self.__parametros_extra
            )

            # Asignar el costo calculado _  Yenifer Gonzalez
            self.__costo_calculado = costo

            # Cambiar estado a CONFIRMADA _  Yenifer Gonzalez
            self.__estado = "CONFIRMADA"

            # Registrar la reserva en el cliente _  Yenifer Gonzalez
            self.__cliente.agregar_reserva(self)

            return costo

        except EstadoReservaError:
            # Re-lanzar excepciones de estado sin modificar _  Yenifer Gonzalez
            raise
        except (ServicioNoDisponibleError, ReservaInvalidaError):
            # Re-lanzar excepciones de servicio o reserva sin modificar _  Yenifer Gonzalez
            raise
        except Exception as e:
            # Encadenar cualquier otro error como ReservaInvalidaError _  Yenifer Gonzalez
            raise ReservaInvalidaError(
                f"Error inesperado al confirmar la reserva: {e}"
            ) from e

    def cancelar(self, motivo: str = "") -> bool:
        """
        Cancela la reserva si está en estado PENDIENTE o CONFIRMADA.
        
        Args:
            motivo: Razón de la cancelación.
            
        Returns:
            True si la cancelación fue exitosa.
            
        Raises:
            EstadoReservaError: Si el estado no permite cancelación.
        """
        # Solo se pueden cancelar reservas PENDIENTES o CONFIRMADAS _  Yenifer Gonzalez
        if self.__estado not in ["PENDIENTE", "CONFIRMADA"]:
            raise EstadoReservaError(self.__estado, "cancelar")

        # Cambiar estado a CANCELADA _  Yenifer Gonzalez
        self.__estado = "CANCELADA"

        # Registrar motivo como nota si se proporcionó _  Yenifer Gonzalez  
        if motivo:
            self.__notas = f"Cancelada: {motivo}"

        return True

    def completar(self) -> bool:
        """
        Marca la reserva como completada. Solo posible desde CONFIRMADA.
        
        Returns:
            True si la operación fue exitosa.
            
        Raises:
            EstadoReservaError: Si la reserva no está CONFIRMADA.
        """
        # Solo las reservas CONFIRMADAS pueden completarse _  Yenifer Gonzalez
        if self.__estado != "CONFIRMADA":
            raise EstadoReservaError(self.__estado, "completar")

        # Cambiar estado a COMPLETADA _  Yenifer Gonzalez
        self.__estado = "COMPLETADA"
        return True

    def procesar(self) -> dict:
        """
        Procesa completamente la reserva: confirma, valida y retorna resumen.
        Usa try/except/else/finally para manejo completo de excepciones.
        
        Returns:
            Diccionario con el resumen del procesamiento.
        """
        resultado = {
            "exito": False,
            "id_reserva": self.__id,
            "mensaje": "",
            "costo": 0.0
        }

        try:
            # Intentar confirmar la reserva _  Yenifer Gonzalez
            costo = self.confirmar()

        except EstadoReservaError as e:
            # Error por estado incorrecto de la reserva _  Yenifer Gonzalez
            resultado["mensaje"] = f"Error de estado: {e}"

        except (ServicioNoDisponibleError, ReservaInvalidaError) as e:
            # Error en servicio o parámetros de reserva _  Yenifer Gonzalez
            resultado["mensaje"] = f"Error en reserva: {e}"

        except Exception as e:
            # Cualquier otro error inesperado _  Yenifer Gonzalez
            resultado["mensaje"] = f"Error inesperado: {e}"

        else:
            # Se ejecuta solo si NO hubo excepción (reserva exitosa) _  Yenifer Gonzalez
            resultado["exito"] = True
            resultado["costo"] = costo
            resultado["mensaje"] = (
                f"Reserva {self.__id} confirmada exitosamente. "
                f"Costo total: ${costo:,.2f}"
            )

        finally:
            # Se ejecuta siempre, haya o no excepción _  Yenifer Gonzalez
            resultado["estado_final"] = self.__estado

        return resultado

    # Métodos de información _  Yenifer Gonzalez

    def describir(self) -> str:
        """Descripción completa de la reserva."""
        return (
            f"Reserva [{self.__id}] - Estado: {self.__estado} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion_horas}h | "
            f"Costo: ${self.__costo_calculado:,.2f} | "
            f"Fecha: {self.__fecha_reserva.strftime('%Y-%m-%d %H:%M')}"
        )

    def to_dict(self) -> dict:
        """Convierte la reserva a diccionario para la UI."""
        return {
            "ID": self.__id,
            "Estado": self.__estado,
            "Cliente": self.__cliente.nombre,
            "Servicio": self.__servicio.nombre,
            "Tipo Servicio": self.__servicio.tipo_servicio(),
            "Duración": f"{self.__duracion_horas}h",
            "Costo Total": f"${self.__costo_calculado:,.2f}",
            "Fecha Reserva": self.__fecha_reserva.strftime("%Y-%m-%d %H:%M"),
            "Fecha Creación": self.__fecha_creacion.strftime("%Y-%m-%d %H:%M"),
            "Notas": self.__notas or "—"
        }

    def __str__(self) -> str:
        """Representación en cadena de la reserva."""
        return self.describir()
