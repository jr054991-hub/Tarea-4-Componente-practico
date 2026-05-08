
from abc import ABC, abstractmethod  # Para clases y métodos abstractos _ Yenifer Gonzalez
import re                            # Para validaciones con expresiones regulares _ Yenifer Gonzalez
from exceptions import (
    ClienteInvalidoError, ParametroFaltanteError
)


class EntidadBase(ABC):
    """
    Clase abstracta base del sistema.
    Toda entidad del sistema debe heredar de esta clase
    e implementar los métodos abstractos definidos aquí.
    """

    def __init__(self, id_entidad: str):
        """
        Inicializa la entidad con su identificador único.
        
        Args:
            id_entidad: Identificador único de la entidad.
        """
        # Identificador protegido de la entidad _ yenifer Gonzalez
        self._id = id_entidad

    @property
    def id(self) -> str:
        """Propiedad de solo lectura para el identificador."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """
        Método abstracto: cada entidad debe describirse a sí misma.
        Debe ser implementado por las clases derivadas.
        """
        pass

    @abstractmethod
    def validar(self) -> bool:
        """
        Método abstracto: cada entidad debe poder validar sus propios datos.
        Debe ser implementado por las clases derivadas.
        """
        pass

    def __str__(self) -> str:
        """Representación en cadena usando el método describir."""
        return self.describir()


class Cliente(EntidadBase):
    """
    Clase que representa a un cliente de Software FJ.
    Implementa encapsulación total de datos personales con
    propiedades y validaciones robustas.
    """

    # Contador estático para generar IDs automáticos _ Yenifer Gonzalez
    _contador = 1

    def __init__(self, nombre: str, email: str, telefono: str, documento: str):
        """
        Inicializa un cliente con sus datos personales validados.
        
        Args:
            nombre: Nombre completo del cliente.
            email: Correo electrónico válido.
            telefono: Número de teléfono (solo dígitos, 7-15 caracteres).
            documento: Número de documento de identidad.
            
        Raises:
            ParametroFaltanteError: Si algún campo obligatorio está vacío.
            ClienteInvalidoError: Si algún dato tiene formato inválido.
        """
        # Validar todos los campos antes de asignar _ Yenifer Gonzalez
        self._validar_campos(nombre, email, telefono, documento)

        # Generar ID único automáticamente _ Yenifer Gonzalez
        id_generado = f"CLI-{Cliente._contador:04d}"
        Cliente._contador += 1

        # Llamar al constructor de la clase base _ Yenifer Gonzalez
        super().__init__(id_generado)

        # Asignar atributos privados (encapsulación) _ Yenifer Gonzalez
        self.__nombre = nombre.strip().title()       # Nombre formateado
        self.__email = email.strip().lower()          # Email en minúsculas
        self.__telefono = telefono.strip()            # Teléfono limpio
        self.__documento = documento.strip()          # Documento limpio
        self.__activo = True                          # Estado activo por defecto
        self.__reservas = []                          # Lista de reservas del cliente

    # ---- Propiedades (Encapsulación) ---- _ Yenifer Gonzalez

    @property
    def nombre(self) -> str:
        """Nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Setter del nombre con validación."""
        if not valor or not valor.strip():
            raise ParametroFaltanteError("nombre")
        self.__nombre = valor.strip().title()

    @property
    def email(self) -> str:
        """Correo electrónico del cliente."""
        return self.__email

    @email.setter
    def email(self, valor: str):
        """Setter del email con validación de formato."""
        if not self._es_email_valido(valor):
            raise ClienteInvalidoError(f"El email '{valor}' no tiene un formato válido.")
        self.__email = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Teléfono del cliente."""
        return self.__telefono

    @property
    def documento(self) -> str:
        """Documento de identidad del cliente."""
        return self.__documento

    @property
    def activo(self) -> bool:
        """Estado activo/inactivo del cliente."""
        return self.__activo

    @property
    def reservas(self) -> list:
        """Lista de reservas asociadas al cliente (copia protegida)."""
        return self.__reservas.copy()

    # ---- Métodos de negocio ---- _ Yenifer Gonzalez

    def agregar_reserva(self, reserva):
        """
        Agrega una reserva a la lista interna del cliente.
        
        Args:
            reserva: Objeto Reserva a asociar con el cliente.
        """
        # Verificar que el cliente esté activo antes de agregar _ Yenifer Gonzalez
        if not self.__activo:
            raise ClienteInvalidoError(f"El cliente '{self.__nombre}' está inactivo.")
        # Agregar la reserva a la lista interna _ Yenifer Gonzalez
        self.__reservas.append(reserva)

    def desactivar(self):
        """Desactiva el cliente en el sistema."""
        self.__activo = False

    def activar(self):
        """Reactiva el cliente en el sistema."""
        self.__activo = True

    def total_reservas(self) -> int:
        """Retorna el número total de reservas del cliente."""
        return len(self.__reservas)

    # ---- Validaciones ----

    @staticmethod
    def _es_email_valido(email: str) -> bool:
        """
        Valida el formato de un email usando expresión regular.
        
        Args:
            email: Cadena a validar.
            
        Returns:
            True si el email es válido, False en caso contrario.
        """
        # Patrón básico de validación de email _ Yenifer Gonzalez
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return bool(re.match(patron, email.strip()))

    @staticmethod
    def _es_telefono_valido(telefono: str) -> bool:
        """
        Valida que el teléfono contenga solo dígitos y longitud correcta.
        
        Args:
            telefono: Cadena a validar.
        """
        # Solo dígitos, entre 7 y 15 caracteres _ Yenifer Gonzalez
        return telefono.strip().isdigit() and 7 <= len(telefono.strip()) <= 15

    def _validar_campos(self, nombre: str, email: str, telefono: str, documento: str):
        """
        Valida todos los campos del cliente antes de crear el objeto.
        
        Raises:
            ParametroFaltanteError: Si algún campo está vacío.
            ClienteInvalidoError: Si algún dato tiene formato inválido.
        """
        # Verificar que ningún campo esté vacío _ Yenifer Gonzalez
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("nombre")
        if not email or not email.strip():
            raise ParametroFaltanteError("email")
        if not telefono or not telefono.strip():
            raise ParametroFaltanteError("telefono")
        if not documento or not documento.strip():
            raise ParametroFaltanteError("documento")

        # Validar formato del email _ Yenifer Gonzalez
        if not self._es_email_valido(email):
            raise ClienteInvalidoError(f"Email inválido: '{email}'. Use formato usuario@dominio.com")

        # Validar formato del teléfono _ Yenifer Gonzalez
        if not self._es_telefono_valido(telefono):
            raise ClienteInvalidoError(
                f"Teléfono inválido: '{telefono}'. Solo dígitos, entre 7 y 15 caracteres."
            )

        # Validar que el documento no esté vacío y tenga mínimo 5 caracteres _ Yenifer Gonzalez
        if len(documento.strip()) < 5:
            raise ClienteInvalidoError(
                f"Documento inválido: '{documento}'. Mínimo 5 caracteres."
            )

    # ---- Métodos abstractos implementados ----_ Yenifer Gonzalez

    def describir(self) -> str:
        """Descripción completa del cliente."""
        estado = "Activo" if self.__activo else "Inactivo"
        return (
            f"Cliente [{self._id}] - {self.__nombre} | "
            f"Email: {self.__email} | Tel: {self.__telefono} | "
            f"Doc: {self.__documento} | Estado: {estado} | "
            f"Reservas: {len(self.__reservas)}"
        )

    def validar(self) -> bool:
        """Retorna True si el cliente tiene datos válidos y está activo."""
        try:
            # Re-validar todos los campos actualmente almacenados _ Yenifer Gonzalez
            self._validar_campos(self.__nombre, self.__email, self.__telefono, self.__documento)
            return True
        except (ClienteInvalidoError, ParametroFaltanteError):
            return False

    def to_dict(self) -> dict:
        """Convierte el cliente a diccionario para mostrar en la UI."""
        return {
            "ID": self._id,
            "Nombre": self.__nombre,
            "Email": self.__email,
            "Teléfono": self.__telefono,
            "Documento": self.__documento,
            "Estado": "Activo" if self.__activo else "Inactivo",
            "Reservas": len(self.__reservas)
        }
