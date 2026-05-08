

import os
import datetime


class Logger:
    """
    Clase responsable de registrar todos los eventos y errores del sistema.
    Escribe en un archivo de texto plano con marcas de tiempo.
    """

    def __init__(self, ruta_archivo: str = "csr_logs.txt"):
        """
        Inicializa el logger con la ruta del archivo de registro.
        
        Args:
            ruta_archivo: Nombre o ruta del archivo donde se guardarán los logs.
        """
        # Ruta del archivo de logs _ Yenifer Gonzalez
        self.ruta_archivo = ruta_archivo
        # Lista en memoria de todos los registros (tipo, mensaje, timestamp) _ Yenifer Gonzalez
        self.registros = []
        # Crear o verificar el archivo de logs al inicializar _ Yenifer Gonzalez
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        """Crea el archivo de logs si no existe y escribe el encabezado."""
        try:
            # Verificar si el archivo ya existe _ Yenifer Gonzalez
            archivo_existente = os.path.exists(self.ruta_archivo)
            # Abrir en modo append para no borrar registros previos _ Yenifer Gonzalez
            with open(self.ruta_archivo, "a", encoding="utf-8") as f:
                if not archivo_existente:
                    # Escribir encabezado solo si el archivo es nuevo _ Yenifer Gonzalez
                    f.write("=" * 60 + "\n")
                    f.write("  SISTEMA CSR - REGISTRO DE EVENTOS Y ERRORES\n")
                    f.write("  Software FJ\n")
                    f.write("=" * 60 + "\n\n")
                # Registrar inicio de sesión _ Yenifer Gonzalez
                f.write(f"\n--- Nueva sesión: {self._timestamp()} ---\n")
        except IOError as e:
            # Si no se puede crear el archivo, continuar sin logging a disco _ Yenifer Gonzalez
            print(f"Advertencia: No se pudo inicializar el archivo de logs: {e}")

    def _timestamp(self) -> str:
        """Retorna la fecha y hora actual formateada."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def registrar_evento(self, mensaje: str):
        """
        Registra un evento exitoso del sistema.
        
        Args:
            mensaje: Descripción del evento ocurrido.
        """
        # Construir entrada de log con timestamp _ Yenifer Gonzalez
        timestamp = self._timestamp()
        entrada = f"[EVENTO] {timestamp} - {mensaje}"
        # Guardar en memoria con tipo 'evento' _ Yenifer Gonzalez
        self.registros.append(("evento", timestamp, mensaje))
        # Escribir en archivo _ Yenifer Gonzalez
        self._escribir_en_archivo(entrada)

    def registrar_error(self, mensaje: str, excepcion: Exception = None):
        """
        Registra un error del sistema.
        
        Args:
            mensaje: Descripción del error.
            excepcion: Objeto de excepción opcional para más detalle.
        """
        # Construir entrada de log con timestamp _ Yenifer Gonzalez
        timestamp = self._timestamp()
        # Incluir detalle de excepción si se proporcionó _ Yenifer Gonzalez
        detalle = f" | Excepción: {type(excepcion).__name__}: {excepcion}" if excepcion else ""
        entrada = f"[ERROR]  {timestamp} - {mensaje}{detalle}"
        # Guardar en memoria con tipo 'error' _ Yenifer Gonzalez
        self.registros.append(("error", timestamp, f"{mensaje}{detalle}"))
        # Escribir en archivo _ Yenifer Gonzalez
        self._escribir_en_archivo(entrada)

    def _escribir_en_archivo(self, texto: str):
        """Escribe una línea en el archivo de logs."""
        try:
            # Abrir en modo append para agregar al final _ Yenifer Gonzalez
            with open(self.ruta_archivo, "a", encoding="utf-8") as f:
                f.write(texto + "\n")
        except IOError:
            # Si falla la escritura, solo imprimir en consola _ Yenifer Gonzalez
            print(f"[LOG-FALLO] {texto}")

    def obtener_registros(self) -> list:
        """Retorna todos los registros en memoria como lista."""
        return self.registros.copy()

    def limpiar_memoria(self):
        """Limpia los registros en memoria (no borra el archivo)."""
        self.registros.clear()
