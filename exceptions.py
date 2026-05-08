
class CSRBaseException(Exception):
    """Excepción base del sistema CSR. Todas las excepciones heredan de esta."""

    def __init__(self, mensaje: str, codigo: str = "CSR-000"):
        # Llamar al constructor de la clase padre _ Yenifer Gonzalez
        super().__init__(mensaje)
        # Código identificador del error _ Yenifer Gonzalez
        self.codigo = codigo
        # Mensaje descriptivo del error _ Yenifer Gonzalez
        self.mensaje = mensaje

    def __str__(self):
        """Representación en cadena de la excepción."""
        return f"[{self.codigo}] {self.mensaje}"


class ClienteInvalidoError(CSRBaseException):
    """Se lanza cuando los datos de un cliente son inválidos o incompletos."""

    def __init__(self, mensaje: str):
        # Inicializar con código específico de cliente _ Yenifer Gonzalez
        super().__init__(mensaje, codigo="CSR-101")


class ServicioNoDisponibleError(CSRBaseException):
    """Se lanza cuando un servicio no está disponible o sus parámetros son incorrectos."""

    def __init__(self, mensaje: str):
        # Inicializar con código específico de servicio _Yenifer Gonzalez
        super().__init__(mensaje, codigo="CSR-201")


class ReservaInvalidaError(CSRBaseException):
    """Se lanza cuando una reserva no puede procesarse por datos incorrectos."""

    def __init__(self, mensaje: str):
        # Inicializar con código específico de reserva_ Yenifer Gonzalez
        super().__init__(mensaje, codigo="CSR-301")


class ParametroFaltanteError(CSRBaseException):
    """Se lanza cuando falta un parámetro obligatorio en cualquier operación."""

    def __init__(self, parametro: str):
        # Construir mensaje descriptivo indicando qué parámetro falta _ Yenifer Gonzalez
        mensaje = f"El parámetro '{parametro}' es obligatorio y no fue proporcionado."
        super().__init__(mensaje, codigo="CSR-401")
        # Guardar referencia al nombre del parámetro faltante _ Yenifer Gonzalez
        self.parametro = parametro


class CapacidadExcedidaError(CSRBaseException):
    """Se lanza cuando se supera la capacidad máxima de un servicio."""

    def __init__(self, capacidad_max: int):
        # Mensaje con la capacidad máxima permitida _ Yenifer Gonzalez
        mensaje = f"La capacidad máxima permitida es {capacidad_max} personas."
        super().__init__(mensaje, codigo="CSR-501")


class DuracionInvalidaError(CSRBaseException):
    """Se lanza cuando la duración de una reserva es inválida."""

    def __init__(self, mensaje: str):
        # Inicializar con código específico de duración _   Yenifer Gonzalez
        super().__init__(mensaje, codigo="CSR-601")


class EstadoReservaError(CSRBaseException):
    """Se lanza cuando se intenta una operación no permitida según el estado de la reserva."""

    def __init__(self, estado_actual: str, operacion: str):
        # Mensaje explicando el conflicto de estado _ Yenifer Gonzalez
        mensaje = f"No se puede '{operacion}' una reserva en estado '{estado_actual}'."
        super().__init__(mensaje, codigo="CSR-701")
