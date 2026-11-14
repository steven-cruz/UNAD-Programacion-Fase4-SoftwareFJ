"""Clase abstracta general para las entidades del dominio.

Define la abstracción base ``EntidadSistema`` usando el módulo ``abc`` para
estandarizar la identificación única, trazabilidad temporal, control de estado
activo, encapsulamiento mediante propiedades y el contrato polimórfico de
validación y resumen para ``Cliente``, ``Servicio`` y ``Reserva``.
"""

from abc import ABC, abstractmethod
from datetime import datetime

from src.excepciones import DatosInvalidosError, ParametrosFaltantesError
from src.utils import obtener_logger

class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad general del sistema.

    No puede instanciarse directamente; obliga a todas las subclases a
    implementar ``validar()`` y ``mostrar_resumen()`` respetando el principio de
    abstracción de la Programación Orientada a Objetos.
    """

    def __init__(
        self,
        id_entidad: str,
        activo: bool = True,
        fecha_registro: datetime | None = None,
    ) -> None:
        """Inicializa los atributos comunes encapsulados de toda entidad.

        Args:
            id_entidad: Identificador único no vacío de la entidad.
            activo: Indica si la entidad está habilitada para operar.
            fecha_registro: Marca de tiempo de creación; usa la actual si es ``None``.

        Raises:
            ParametrosFaltantesError: Si ``id_entidad`` es ``None`` o vacío.
            DatosInvalidosError: Si los tipos de datos de los atributos no son válidos.
        """
        # Logger específico del nombre de la subclase concreta (Cliente, Reserva, etc.).
        self._logger = obtener_logger(self.__class__.__name__)

        # La asignación mediante propiedades dispara inmediatamente las validaciones estrictas.
        self.id_entidad = id_entidad
        self.activo = activo

        # Asigna la fecha actual por defecto o valida el tipo si se proporciona manualmente.
        if fecha_registro is None:
            self._fecha_registro = datetime.now()
        elif isinstance(fecha_registro, datetime):
            self._fecha_registro = fecha_registro
        else:
            raise DatosInvalidosError(
                "La fecha de registro debe ser una instancia de datetime.",
                contexto={
                    "campo": "fecha_registro",
                    "tipo": type(fecha_registro).__name__,
                },
            )

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador único encapsulado de la entidad."""
        return self._id_entidad

    @id_entidad.setter
    def id_entidad(self, valor: str) -> None:
        """Valida y asigna el identificador único impidiendo valores vacíos o no textuales."""
        if valor is None:
            raise ParametrosFaltantesError(
                "El identificador de la entidad es obligatorio y no puede estar vacío.",
                contexto={"campo": "id_entidad", "valor": valor},
            )
        if not isinstance(valor, str):
            raise DatosInvalidosError(
                "El identificador de la entidad debe ser una cadena de texto.",
                contexto={"campo": "id_entidad", "tipo": type(valor).__name__},
            )

        id_limpio = valor.strip()
        # Evita aceptar cadenas compuestas únicamente por espacios en blanco.
        if not id_limpio:
            raise ParametrosFaltantesError(
                "El identificador de la entidad es obligatorio y no puede estar vacío.",
                contexto={"campo": "id_entidad", "valor": valor},
            )
        self._id_entidad = id_limpio

    @property
    def fecha_registro(self) -> datetime:
        """Retorna la fecha y hora de registro (propiedad de solo lectura)."""
        return self._fecha_registro

    @property
    def fecha_registro_formateada(self) -> str:
        """Devuelve la fecha de registro formateada para reportes y resúmenes."""
        return self._fecha_registro.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def activo(self) -> bool:
        """Retorna ``True`` si la entidad se encuentra activa en el sistema."""
        return self._activo

    @activo.setter
    def activo(self, valor: bool) -> None:
        """Valida estrictamente que el estado activo sea booleano."""
        # En Python bool hereda de int; isinstance(..., bool) garantiza exactitud de tipo.
        if not isinstance(valor, bool):
            raise DatosInvalidosError(
                "El estado activo debe ser un valor booleano (True/False).",
                contexto={"campo": "activo", "valor": valor},
            )
        self._activo = valor

    def _actualizar_estado(self, nuevo_estado: bool) -> None:
        """Actualiza el estado activo interno y registra el cambio en el archivo de logs."""
        self._activo = nuevo_estado
        etiqueta = "activada" if nuevo_estado else "desactivada"
        self._logger.info(
            "Entidad %s [%s] %s correctamente.",
            self.__class__.__name__,
            self._id_entidad,
            etiqueta,
        )

    def activar(self) -> None:
        """Habilita la entidad para futuras operaciones del sistema."""
        self._actualizar_estado(True)

    def desactivar(self) -> None:
        """Inhabilita lógicamente la entidad sin eliminar su registro en memoria."""
        self._actualizar_estado(False)

    @abstractmethod
    def validar(self) -> bool:
        """Contrato abstracto para ejecutar las reglas de validación propias de cada subclase."""

    @abstractmethod
    def mostrar_resumen(self) -> str:
        """Contrato abstracto para devolver una ficha legible con los datos de la entidad."""

    def __str__(self) -> str:
        """Delega la representación textual en el método polimórfico ``mostrar_resumen``."""
        return self.mostrar_resumen()

    def __repr__(self) -> str:
        """Devuelve una representación técnica útil para depuración y trazas."""
        return (
            f"{self.__class__.__name__}("
            f"id_entidad={self._id_entidad!r}, activo={self._activo!r})"
        )
