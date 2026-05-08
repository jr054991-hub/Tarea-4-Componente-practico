
from abc import ABC, abstractmethod  # Para clases y métodos abstractos _ Yenifer Gonzalez
from exceptions import (
    ServicioNoDisponibleError, CapacidadExcedidaError,
    DuracionInvalidaError, ParametroFaltanteError
)


class Servicio(ABC):
    """
    Clase abstracta base para todos los servicios de Software FJ.
    Define la interfaz común que todos los servicios deben implementar.
    """

    # Tasa de IVA estándar aplicada a todos los servicios _ Yenifer Gonzalez
    IVA = 0.19

    # Contador estático para generar IDs de servicio _ Yenifer Gonzalez
    _contador = 1

    def __init__(self, nombre: str, descripcion: str, precio_base: float, disponible: bool = True):
        """
        Inicializa el servicio con sus atributos fundamentales.
        
        Args:
            nombre: Nombre del servicio.
            descripcion: Descripción breve del servicio.
            precio_base: Precio base por hora del servicio (en pesos).
            disponible: Estado de disponibilidad del servicio.
            
        Raises:
            ParametroFaltanteError: Si nombre o descripción están vacíos.
            ServicioNoDisponibleError: Si el precio base es inválido.
        """
        # Validar que el nombre no esté vacío _ Yenifer Gonzalez
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("nombre del servicio")
        # Validar que el precio base sea positivo _ Yenifer Gonzalez
        if precio_base <= 0:
            raise ServicioNoDisponibleError(
                f"El precio base debe ser mayor a cero. Recibido: {precio_base}"
            )

        # Generar ID único para el servicio _ Yenifer Gonzalez
        self._id = f"SRV-{Servicio._contador:04d}"
        Servicio._contador += 1

        # Atributos protegidos del servicio _ Yenifer Gonzalez
        self._nombre = nombre.strip()                  # Nombre del servicio
        self._descripcion = descripcion.strip()        # Descripción del servicio
        self._precio_base = precio_base                # Precio base por hora
        self._disponible = disponible                  # Estado de disponibilidad
        self._categoria = "General"                    # Categoría (se sobreescribe en hijos)

    # ---- Propiedades ---- _ yenifer Gonzalez

    @property
    def id(self) -> str:
        """Identificador único del servicio."""
        return self._id

    @property
    def nombre(self) -> str:
        """Nombre del servicio."""
        return self._nombre

    @property
    def descripcion(self) -> str:
        """Descripción del servicio."""
        return self._descripcion

    @property
    def precio_base(self) -> float:
        """Precio base por hora del servicio."""
        return self._precio_base

    @property
    def disponible(self) -> bool:
        """Estado de disponibilidad del servicio."""
        return self._disponible

    @property
    def categoria(self) -> str:
        """Categoría del servicio."""
        return self._categoria

    # ---- Métodos abstractos (polimorfismo) ---- _ Yenifer Gonzalez

    @abstractmethod
    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        """
        Calcula el costo total del servicio.
        Cada servicio implementa su propia lógica de cálculo.
        
        Args:
            duracion_horas: Duración del servicio en horas.
            **kwargs: Parámetros opcionales (descuentos, personas, etc.)
        """
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        """
        Valida los parámetros específicos del servicio.
        Cada tipo de servicio tiene sus propias reglas de validación.
        """
        pass

    @abstractmethod
    def tipo_servicio(self) -> str:
        """Retorna el tipo/categoría del servicio."""
        pass

    # ---- Métodos concretos compartidos ---- _ Yenifer Gonzalez

    def calcular_costo_con_iva(self, duracion_horas: float, **kwargs) -> float:
        """
        Método sobrecargado: calcula el costo incluyendo IVA.
        
        Args:
            duracion_horas: Duración en horas.
            **kwargs: Parámetros adicionales.
            
        Returns:
            Costo total con IVA aplicado.
        """
        # Obtener el costo base del servicio _ Yenifer Gonzalez
        costo_base = self.calcular_costo(duracion_horas, **kwargs)
        # Aplicar IVA al costo base _ Yenifer Gonzalez
        return round(costo_base * (1 + self.IVA), 2)

    def calcular_costo_con_descuento(self, duracion_horas: float,
                                      porcentaje_descuento: float, **kwargs) -> float:
        """
        Método sobrecargado: calcula el costo con descuento aplicado.
        
        Args:
            duracion_horas: Duración en horas.
            porcentaje_descuento: Porcentaje de descuento (0-100).
            **kwargs: Parámetros adicionales.
            
        Returns:
            Costo con descuento e IVA incluidos.
        """
        # Validar que el descuento esté en rango válido _ Yenifer Gonzalez
        if not (0 <= porcentaje_descuento <= 100):
            raise ServicioNoDisponibleError(
                f"El descuento debe estar entre 0% y 100%. Recibido: {porcentaje_descuento}%"
            )
        # Calcular costo base _ Yenifer Gonzalez
        costo_base = self.calcular_costo(duracion_horas, **kwargs)
        # Aplicar descuento _ Yenifer Gonzalez
        descuento = costo_base * (porcentaje_descuento / 100)
        costo_con_descuento = costo_base - descuento
        # Aplicar IVA sobre el valor con descuento _ Yenifer Gonzalez
        return round(costo_con_descuento * (1 + self.IVA), 2)

    def activar(self):
        """Activa el servicio para que pueda ser reservado."""
        self._disponible = True

    def desactivar(self):
        """Desactiva el servicio temporalmente."""
        self._disponible = False

    def describir(self) -> str:
        """Descripción general del servicio."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[{self._id}] {self._nombre} ({self._categoria}) - "
            f"${self._precio_base:,.0f}/hora - {estado}"
        )

    def to_dict(self) -> dict:
        """Convierte el servicio a diccionario para la UI."""
        return {
            "ID": self._id,
            "Nombre": self._nombre,
            "Tipo": self.tipo_servicio(),
            "Descripción": self._descripcion,
            "Precio Base": f"${self._precio_base:,.0f}/hora",
            "Estado": "Disponible" if self._disponible else "No disponible"
        }

    def __str__(self) -> str:
        """Representación en cadena del servicio."""
        return self.describir()


# ----------------------------
#  SERVICIO 1: Reserva de Sala _ Yenifer Gonzalez
# ----------------------------

class ReservaSala(Servicio):
    """
    Servicio especializado: Reserva de salas de reunión o conferencia.
    Hereda de Servicio e implementa lógica específica para salas.
    """

    def __init__(self, nombre: str, capacidad_max: int, precio_base: float,
                tiene_proyector: bool = False, tiene_videoconferencia: bool = False):
        """
        Inicializa una sala de reuniones/conferencias.
        
        Args:
            nombre: Nombre identificador de la sala.
            capacidad_max: Número máximo de personas permitidas.
            precio_base: Precio base por hora en pesos.
            tiene_proyector: Indica si la sala tiene proyector.
            tiene_videoconferencia: Indica si tiene sistema de videoconferencia.
        """
        # Validar capacidad máxima antes de inicializar _ Yenifer Gonzalez
        if capacidad_max <= 0:
            raise ServicioNoDisponibleError(
                f"La capacidad máxima debe ser mayor a cero. Recibido: {capacidad_max}"
            )

        # Llamar al constructor de la clase padre _ Yenifer Gonzalez
        descripcion = f"Sala para hasta {capacidad_max} personas"
        super().__init__(nombre, descripcion, precio_base)

        # Atributos específicos de la sala _ Yenifer Gonzalez
        self.__capacidad_max = capacidad_max              # Capacidad máxima
        self.__tiene_proyector = tiene_proyector          # Si tiene proyector
        self.__tiene_videoconferencia = tiene_videoconferencia  # Si tiene videoconf
        self._categoria = "Reserva de Sala"               # Categoría del servicio

    @property
    def capacidad_max(self) -> int:
        """Capacidad máxima de la sala."""
        return self.__capacidad_max

    @property
    def tiene_proyector(self) -> bool:
        """Indica si la sala tiene proyector."""
        return self.__tiene_proyector

    @property
    def tiene_videoconferencia(self) -> bool:
        """Indica si la sala tiene sistema de videoconferencia."""
        return self.__tiene_videoconferencia

    def calcular_costo(self, duracion_horas: float, personas: int = 1, **kwargs) -> float:
        """
        Calcula el costo de la reserva de sala.
        El precio puede aumentar según la cantidad de personas.
        
        Args:
            duracion_horas: Horas de reserva.
            personas: Número de personas que usarán la sala.
            
        Returns:
            Costo total de la reserva en pesos.
        """
        # Validar los parámetros antes de calcular _ Yenifer Gonzalez
        self.validar_parametros(duracion_horas=duracion_horas, personas=personas)

        # Costo base: precio por hora × número de horas _ Yenifer Gonzalez
        costo = self._precio_base * duracion_horas

        # Costo adicional si se supera la mitad de la capacidad _ Yenifer Gonzalez
        if personas > self.__capacidad_max // 2:
            costo *= 1.15  # Incremento del 15% por alta ocupación _ Yenifer Gonzalez

        return round(costo, 2)

    def validar_parametros(self, **kwargs) -> bool:
        """
        Valida los parámetros específicos de la sala.
        
        Raises:
            DuracionInvalidaError: Si la duración es inválida.
            CapacidadExcedidaError: Si el número de personas excede la capacidad.
            ServicioNoDisponibleError: Si el servicio no está disponible.
        """
        # Verificar disponibilidad del servicio _   Yenifer Gonzalez
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"La sala '{self._nombre}' no está disponible actualmente."
            )

        # Validar duración si se proporcionó _ Yenifer Gonzalez
        duracion = kwargs.get("duracion_horas", 1)
        if duracion <= 0 or duracion > 24:
            raise DuracionInvalidaError(
                f"La duración debe estar entre 0.5 y 24 horas. Recibido: {duracion}"
            )

        # Validar número de personas si se proporcionó _ Yenifer Gonzalez
        personas = kwargs.get("personas", 1)
        if personas > self.__capacidad_max:
            raise CapacidadExcedidaError(self.__capacidad_max)

        return True

    def tipo_servicio(self) -> str:
        """Retorna el tipo de servicio."""
        return "Reserva de Sala"

    def describir(self) -> str:
        """Descripción detallada de la sala."""
        extras = []
        if self.__tiene_proyector:
            extras.append("Proyector")
        if self.__tiene_videoconferencia:
            extras.append("Videoconferencia")
        extras_str = ", ".join(extras) if extras else "Sin extras"
        base = super().describir()
        return f"{base} | Cap: {self.__capacidad_max} personas | Extras: {extras_str}"

    def to_dict(self) -> dict:
        """Convierte la sala a diccionario extendido para la UI."""
        d = super().to_dict()
        d["Capacidad"] = f"{self.__capacidad_max} personas"
        d["Proyector"] = "Sí" if self.__tiene_proyector else "No"
        d["Videoconferencia"] = "Sí" if self.__tiene_videoconferencia else "No"
        return d


# -------------------------------
#  SERVICIO 2: Alquiler de Equipo
# -------------------------------

class AlquilerEquipo(Servicio):
    """
    Servicio especializado: Alquiler de equipos tecnológicos.
    Hereda de Servicio con lógica específica para equipos.
    """

    # Tipos de equipos válidos _ Yenifer Gonzalez
    TIPOS_VALIDOS = ["laptop", "proyector", "camara", "impresora", "tablet", "servidor"]

    def __init__(self, nombre: str, tipo_equipo: str, precio_base: float,
                cantidad_disponible: int = 1, requiere_deposito: bool = True):
        """
        Inicializa un equipo disponible para alquiler.
        
        Args:
            nombre: Nombre o modelo del equipo.
            tipo_equipo: Tipo de equipo (laptop, proyector, etc.)
            precio_base: Precio de alquiler por hora.
            cantidad_disponible: Unidades disponibles para alquiler.
            requiere_deposito: Si requiere depósito de garantía.
        """
        # Validar que el tipo de equipo sea válido _ Yenifer Gonzalez
        if tipo_equipo.lower() not in self.TIPOS_VALIDOS:
            raise ServicioNoDisponibleError(
                f"Tipo de equipo inválido: '{tipo_equipo}'. "
                f"Tipos válidos: {', '.join(self.TIPOS_VALIDOS)}"
            )
        # Validar cantidad disponible _ Yenifer Gonzalez
        if cantidad_disponible < 0:
            raise ServicioNoDisponibleError(
                "La cantidad disponible no puede ser negativa."
            )

        # Descripción automática del equipo _ Yenifer Gonzalez
        descripcion = f"Alquiler de {tipo_equipo} - {nombre}"
        super().__init__(nombre, descripcion, precio_base)

        # Atributos específicos del equipo _ Yenifer Gonzalez
        self.__tipo_equipo = tipo_equipo.lower()            # Tipo de equipo
        self.__cantidad_disponible = cantidad_disponible     # Unidades disponibles
        self.__requiere_deposito = requiere_deposito         # Requiere depósito
        self.__deposito_monto = precio_base * 2              # Depósito = 2x precio hora
        self._categoria = "Alquiler de Equipo"               # Categoría

    @property
    def tipo_equipo(self) -> str:
        """Tipo de equipo."""
        return self.__tipo_equipo

    @property
    def cantidad_disponible(self) -> int:
        """Unidades disponibles para alquiler."""
        return self.__cantidad_disponible

    @property
    def requiere_deposito(self) -> bool:
        """Indica si se requiere depósito de garantía."""
        return self.__requiere_deposito

    def calcular_costo(self, duracion_horas: float, cantidad: int = 1, **kwargs) -> float:
        """
        Calcula el costo del alquiler de equipo.
        
        Args:
            duracion_horas: Tiempo de alquiler en horas.
            cantidad: Número de unidades a alquilar.
            
        Returns:
            Costo total del alquiler en pesos.
        """
        # Validar parámetros antes de calcular _ Yenifer Gonzalez
        self.validar_parametros(duracion_horas=duracion_horas, cantidad=cantidad)

        # Costo = precio por hora × horas × cantidad de equipos _ Yenifer Gonzalez
        costo = self._precio_base * duracion_horas * cantidad

        # Agregar depósito si aplica (una sola vez por equipo) _ Yenifer Gonzalez
        if self.__requiere_deposito:
            deposito_total = self.__deposito_monto * cantidad
            costo += deposito_total

        return round(costo, 2)

    def calcular_costo_sin_deposito(self, duracion_horas: float, cantidad: int = 1) -> float:
        """
        Método sobrecargado: calcula el costo sin incluir el depósito.
        
        Args:
            duracion_horas: Tiempo de alquiler en horas.
            cantidad: Número de unidades.
        """
        # Solo precio de alquiler sin depósito _ Yenifer Gonzalez
        return round(self._precio_base * duracion_horas * cantidad, 2)

    def validar_parametros(self, **kwargs) -> bool:
        """
        Valida los parámetros del alquiler de equipo.
        
        Raises:
            ServicioNoDisponibleError: Si no hay stock disponible.
            DuracionInvalidaError: Si la duración es inválida.
        """
        # Verificar disponibilidad general del servicio _   Yenifer Gonzalez
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El equipo '{self._nombre}' no está disponible."
            )

        # Validar duración _ Yenifer Gonzalez
        duracion = kwargs.get("duracion_horas", 1)
        if duracion <= 0 or duracion > 72:
            raise DuracionInvalidaError(
                f"La duración para alquiler de equipos debe ser entre 1 y 72 horas. "
                f"Recibido: {duracion}"
            )

        # Validar cantidad solicitada vs disponible _ Yenifer Gonzalez
        cantidad = kwargs.get("cantidad", 1)
        if cantidad <= 0:
            raise ServicioNoDisponibleError("La cantidad debe ser mayor a cero.")
        if cantidad > self.__cantidad_disponible:
            raise ServicioNoDisponibleError(
                f"Solo hay {self.__cantidad_disponible} unidades disponibles. "
                f"Solicitadas: {cantidad}"
            )

        return True

    def tipo_servicio(self) -> str:
        """Retorna el tipo de servicio."""
        return "Alquiler de Equipo"

    def describir(self) -> str:
        """Descripción detallada del equipo."""
        deposito_info = f"Depósito: ${self.__deposito_monto:,.0f}" if self.__requiere_deposito else "Sin depósito"
        base = super().describir()
        return (
            f"{base} | Tipo: {self.__tipo_equipo.capitalize()} | "
            f"Stock: {self.__cantidad_disponible} | {deposito_info}"
        )

    def to_dict(self) -> dict:
        """Convierte el equipo a diccionario extendido para la UI."""
        d = super().to_dict()
        d["Tipo de Equipo"] = self.__tipo_equipo.capitalize()
        d["Stock"] = str(self.__cantidad_disponible)
        d["Depósito"] = f"${self.__deposito_monto:,.0f}" if self.__requiere_deposito else "No aplica"
        return d


# -----------------------------------
#  SERVICIO 3: Asesoría Especializada
# -----------------------------------

class AsesoriEspecializada(Servicio):
    """
    Servicio especializado: Asesorías por expertos en distintas áreas.
    Hereda de Servicio con lógica de cobro por sesión y por experto.
    """

    # Áreas de especialización disponibles  _ Yenifer Gonzalez
    AREAS_VALIDAS = [
        "tecnologia", "software", "bases_de_datos", "redes",
        "ciberseguridad", "gestion_proyectos", "cloud", "ia"
    ]

    def __init__(self, nombre: str, area: str, precio_base: float,
                nombre_asesor: str, nivel_experto: str = "junior"):
        """
        Inicializa una asesoría especializada.
        
        Args:
            nombre: Nombre de la asesoría.
            area: Área de especialización.
            precio_base: Precio base por hora.
            nombre_asesor: Nombre del asesor asignado.
            nivel_experto: Nivel del asesor (junior, senior, experto).
        """
        # Validar área de especialización _ Yenifer Gonzalez
        if area.lower() not in self.AREAS_VALIDAS:
            raise ServicioNoDisponibleError(
                f"Área inválida: '{area}'. "
                f"Áreas válidas: {', '.join(self.AREAS_VALIDAS)}"
            )
        # Validar nombre del asesor _ Yenifer Gonzalez
        if not nombre_asesor or not nombre_asesor.strip():
            raise ParametroFaltanteError("nombre_asesor")

        # Validar nivel del experto _ Yenifer Gonzalez
        niveles_validos = ["junior", "senior", "experto"]
        if nivel_experto.lower() not in niveles_validos:
            raise ServicioNoDisponibleError(
                f"Nivel inválido: '{nivel_experto}'. Válidos: {', '.join(niveles_validos)}"
            )

        # Descripción automática de la asesoría _:  Yenifer Gonzalez
        descripcion = f"Asesoría en {area} con {nombre_asesor} ({nivel_experto})"
        super().__init__(nombre, descripcion, precio_base)

        # Atributos específicos de la asesoría _ Yenifer Gonzalez
        self.__area = area.lower()                           # Área de especialización
        self.__nombre_asesor = nombre_asesor.strip().title() # Nombre del asesor
        self.__nivel_experto = nivel_experto.lower()         # Nivel del asesor
        self._categoria = "Asesoría Especializada"           # Categoría

        # Multiplicadores de precio según nivel del experto _ Yenifer Gonzalez
        self.__multiplicadores = {
            "junior": 1.0,    # Precio base sin modificación
            "senior": 1.5,    # 50% adicional
            "experto": 2.0    # Doble del precio base
        }

    @property
    def area(self) -> str:
        """Área de especialización."""
        return self.__area

    @property
    def nombre_asesor(self) -> str:
        """Nombre del asesor."""
        return self.__nombre_asesor

    @property
    def nivel_experto(self) -> str:
        """Nivel del asesor."""
        return self.__nivel_experto

    def calcular_costo(self, duracion_horas: float, sesiones: int = 1, **kwargs) -> float:
        """
        Calcula el costo de la asesoría.
        El precio varía según el nivel del experto.
        
        Args:
            duracion_horas: Duración de cada sesión en horas.
            sesiones: Número de sesiones a contratar.
            
        Returns:
            Costo total de las sesiones en pesos.
        """
        # Validar parámetros antes de calcular _ Yenifer Gonzalez
        self.validar_parametros(duracion_horas=duracion_horas, sesiones=sesiones)

        # Aplicar multiplicador según nivel del experto _ Yenifer Gonzalez
        multiplicador = self.__multiplicadores.get(self.__nivel_experto, 1.0)

        # Costo = precio base × multiplicador × horas × sesiones _Yenifer Gonzalez
        costo = self._precio_base * multiplicador * duracion_horas * sesiones

        return round(costo, 2)

    def calcular_costo_paquete(self, sesiones: int, horas_por_sesion: float,
                                descuento_paquete: float = 0.10) -> float:
        """
        Método sobrecargado: calcula costo de paquete de sesiones con descuento.
        
        Args:
            sesiones: Número de sesiones en el paquete.
            horas_por_sesion: Horas por cada sesión.
            descuento_paquete: Descuento porcentual (por defecto 10%).
            
        Returns:
            Costo total del paquete con descuento e IVA.
        """
        # Calcular costo sin descuento primero _Yenifer Gonzalez
        costo_base = self.calcular_costo(horas_por_sesion, sesiones)
        # Aplicar descuento de paquete _    Yenifer Gonzalez
        descuento = costo_base * descuento_paquete
        costo_con_descuento = costo_base - descuento
        # Aplicar IVA   -- _Yenifer Gonzalez
        return round(costo_con_descuento * (1 + self.IVA), 2)

    def validar_parametros(self, **kwargs) -> bool:
        """
        Valida los parámetros de la asesoría.
        
        Raises:
            ServicioNoDisponibleError: Si el servicio no está disponible.
            DuracionInvalidaError: Si la duración es inválida.
        """
        # Verificar disponibilidad _  Yenifer Gonzalez
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"La asesoría '{self._nombre}' no está disponible actualmente."
            )

        # Validar duración de la sesión -- _Yenifer Gonzalez
        duracion = kwargs.get("duracion_horas", 1)
        if duracion < 0.5 or duracion > 8:
            raise DuracionInvalidaError(
                f"La duración de asesoría debe ser entre 0.5 y 8 horas. Recibido: {duracion}"
            )

        # Validar número de sesiones _  Yenifer Gonzalez
        sesiones = kwargs.get("sesiones", 1)
        if sesiones < 1 or sesiones > 50:
            raise ServicioNoDisponibleError(
                f"El número de sesiones debe ser entre 1 y 50. Recibido: {sesiones}"
            )

        return True

    def tipo_servicio(self) -> str:
        """Retorna el tipo de servicio."""
        return "Asesoría Especializada"

    def describir(self) -> str:
        """Descripción detallada de la asesoría."""
        multiplicador = self.__multiplicadores.get(self.__nivel_experto, 1.0)
        base = super().describir()
        return (
            f"{base} | Área: {self.__area.replace('_', ' ').title()} | "
            f"Asesor: {self.__nombre_asesor} ({self.__nivel_experto.title()}) | "
            f"Tarifa x{multiplicador}"
        )

    def to_dict(self) -> dict:
        """Convierte la asesoría a diccionario extendido para la UI."""
        d = super().to_dict()
        d["Área"] = self.__area.replace("_", " ").title()
        d["Asesor"] = self.__nombre_asesor
        d["Nivel"] = self.__nivel_experto.title()
        return d
