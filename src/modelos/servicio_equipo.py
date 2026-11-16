"""Servicio especializado para el alquiler de equipos tecnológicos.

Implementa la subclase concreta ``ServicioAlquilerEquipo`` heredando de
``Servicio`` con control encapsulado de inventario/stock, verificación de
disponibilidad por unidades y cálculo polimórfico incluyendo seguro obligatorio.
"""

from typing import Any
import unicodedata

from src.excepciones import (
    DatosInvalidosError,
    ParametrosFaltantesError,
    ServicioNoDisponibleError,
)
from src.modelos.servicio_base import Servicio


def _normalizar_sin_tildes(texto: str) -> str:
    """Convierte a minúsculas y elimina tildes para comparar categorías de forma uniforme."""
    descompuesto = unicodedata.normalize("NFKD", texto.strip().lower())
    return "".join(ch for ch in descompuesto if not unicodedata.combining(ch))

class ServicioAlquilerEquipo(Servicio):
    """Servicio concreto para el préstamo de hardware y equipamiento técnico.

    Gestiona existencias disponibles mediante ``verificar_stock``,
    ``asignar_unidades`` y ``liberar_unidades``, sincronizando la disponibilidad
    del servicio cuando el inventario llega a cero.
    """

    CATEGORIAS_EQUIPO_VALIDAS: tuple[str, ...] = (
        "Portátil Alto Rendimiento",
        "Servidor",
        "Kit Redes",
        "Estación Gráfica",
    )
    _MAPA_CATEGORIAS: dict[str, str] = {
        _normalizar_sin_tildes(cat): cat for cat in CATEGORIAS_EQUIPO_VALIDAS
    }
    PORCENTAJE_SEGURO_OBLIGATORIO: float = 0.12

    def __init__(
        self,
        id_entidad: str,
        nombre_servicio: str,
        tarifa_base: float,
        categoria_equipo: str,
        cantidad_disponible: int = 1,
        requiere_seguro: bool = True,
        disponible: bool = True,
        activo: bool = True,
    ) -> None:
        """Inicializa un servicio de alquiler de equipos con control de stock.

        Args:
            id_entidad: Código identificador del equipo o lote (ej. ``EQ-01``).
            nombre_servicio: Nombre descriptivo del equipo.
            tarifa_base: Tarifa por unidad de tiempo (hora/jornada).
            categoria_equipo: Categoría del inventario tecnológico.
            cantidad_disponible: Unidades en stock disponibles (>= 0).
            requiere_seguro: Indica si aplica recargo del 12 % por póliza de garantía.
            disponible: Disponibilidad inicial del servicio.
            activo: Indica si el servicio está habilitado en el catálogo.
        """
        super().__init__(
            id_entidad=id_entidad,
            nombre_servicio=nombre_servicio,
            tarifa_base=tarifa_base,
            disponible=disponible,
            activo=activo,
        )

        self.categoria_equipo = categoria_equipo
        self.cantidad_disponible = cantidad_disponible
        self.requiere_seguro = requiere_seguro

        # Si el servicio fue creado explícitamente no disponible o sin stock, prevalece False.
        if not disponible or self._cantidad_disponible == 0:
            self._disponible = False

        self.validar_parametros()
        self._logger.info(
            "Equipo [%s - %s] (%s, stock=%d, seguro=%s) registrado correctamente.",
            self._id_entidad,
            self._nombre_servicio,
            self._categoria_equipo,
            self._cantidad_disponible,
            self._requiere_seguro,
        )

    @staticmethod
    def _validar_entero(valor: Any, nombre_campo: str) -> int:
        """Valida que un valor sea entero no nulo ni booleano."""
        if valor is None:
            raise ParametrosFaltantesError(
                f"El campo '{nombre_campo}' es obligatorio.",
                contexto={"campo": nombre_campo, "valor": valor},
            )
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise DatosInvalidosError(
                f"El campo '{nombre_campo}' debe ser un número entero.",
                contexto={"campo": nombre_campo, "tipo": type(valor).__name__},
            )
        return valor

    @property
    def categoria_equipo(self) -> str:
        """Retorna la categoría normalizada del equipo."""
        return self._categoria_equipo

    @categoria_equipo.setter
    def categoria_equipo(self, valor: str) -> None:
        """Valida que la categoría pertenezca al catálogo permitido (insensible a tildes)."""
        if valor is None:
            raise ParametrosFaltantesError(
                "La categoría del equipo es obligatoria y no puede ser nula.",
                contexto={"campo": "categoria_equipo", "valor": valor},
            )
        if not isinstance(valor, str):
            raise DatosInvalidosError(
                "La categoría del equipo debe ser una cadena de texto.",
                contexto={"campo": "categoria_equipo", "tipo": type(valor).__name__},
            )

        categoria_limpia = valor.strip()
        if not categoria_limpia:
            raise ParametrosFaltantesError(
                "La categoría del equipo es obligatoria y no puede estar vacía.",
                contexto={"campo": "categoria_equipo", "valor": valor},
            )

        categoria_normalizada = self._MAPA_CATEGORIAS.get(
            _normalizar_sin_tildes(categoria_limpia)
        )
        if categoria_normalizada is None:
            raise DatosInvalidosError(
                "Categoría de equipo no válida. Opciones permitidas: "
                f"{', '.join(self.CATEGORIAS_EQUIPO_VALIDAS)}.",
                contexto={"campo": "categoria_equipo", "valor": valor},
            )
        self._categoria_equipo = categoria_normalizada

    @property
    def cantidad_disponible(self) -> int:
        """Retorna las unidades actualmente disponibles en inventario."""
        return self._cantidad_disponible

    @cantidad_disponible.setter
    def cantidad_disponible(self, valor: Any) -> None:
        """Valida stock >= 0 y sincroniza automáticamente la disponibilidad del servicio."""
        cantidad = self._validar_entero(valor, "cantidad_disponible")
        if cantidad < 0:
            raise DatosInvalidosError(
                "La cantidad disponible no puede ser negativa.",
                contexto={"campo": "cantidad_disponible", "valor": valor},
            )

        self._cantidad_disponible = cantidad
        # Sincroniza la disponibilidad: 0 unidades bloquea reservas; >0 reactiva si está activo.
        if cantidad == 0:
            self._disponible = False
        elif self._activo:
            self._disponible = True

    @property
    def requiere_seguro(self) -> bool:
        """Indica si el préstamo exige póliza de seguro obligatoria."""
        return self._requiere_seguro

    @requiere_seguro.setter
    def requiere_seguro(self, valor: Any) -> None:
        """Valida estrictamente que el indicador de seguro sea booleano."""
        if not isinstance(valor, bool):
            raise DatosInvalidosError(
                "El indicador 'requiere_seguro' debe ser un valor booleano (True/False).",
                contexto={"campo": "requiere_seguro", "valor": valor},
            )
        self._requiere_seguro = valor

    def verificar_stock(self, unidades: int = 1) -> bool:
        """Comprueba si existen suficientes unidades disponibles para reservar.

        Args:
            unidades: Cantidad solicitada (entero positivo, por defecto 1).

        Raises:
            DatosInvalidosError: Si ``unidades`` no es entero mayor a 0.
            ServicioNoDisponibleError: Si el servicio no está disponible o el stock es insuficiente.
        """
        unidades_validas = self._validar_entero(unidades, "unidades")
        if unidades_validas <= 0:
            raise DatosInvalidosError(
                "La cantidad de unidades solicitadas debe ser mayor a cero.",
                contexto={"campo": "unidades", "valor": unidades},
            )

        if not self._disponible or self._cantidad_disponible == 0:
            raise ServicioNoDisponibleError(
                f"El equipo '{self._nombre_servicio}' no cuenta con unidades disponibles.",
                contexto={
                    "id_servicio": self._id_entidad,
                    "stock_actual": self._cantidad_disponible,
                },
            )

        if self._cantidad_disponible < unidades_validas:
            raise ServicioNoDisponibleError(
                f"Stock insuficiente para '{self._nombre_servicio}': "
                f"solicitadas={unidades_validas}, disponibles={self._cantidad_disponible}.",
                contexto={
                    "id_servicio": self._id_entidad,
                    "solicitadas": unidades_validas,
                    "stock_actual": self._cantidad_disponible,
                },
            )
        return True

    def asignar_unidades(self, unidades: int = 1) -> None:
        """Descuenta unidades del inventario tras validar stock disponible."""
        self.verificar_stock(unidades)
        # Reutiliza el setter para actualizar automáticamente _disponible si el stock llega a 0.
        self.cantidad_disponible = self._cantidad_disponible - unidades
        self._logger.info(
            "Asignadas %d unidad(es) de [%s]. Stock restante: %d.",
            unidades,
            self._id_entidad,
            self._cantidad_disponible,
        )

    def liberar_unidades(self, unidades: int = 1) -> None:
        """Reintegra unidades al inventario (ej. por cancelación o devolución)."""
        unidades_validas = self._validar_entero(unidades, "unidades")
        if unidades_validas <= 0:
            raise DatosInvalidosError(
                "La cantidad de unidades a liberar debe ser mayor a cero.",
                contexto={"campo": "unidades", "valor": unidades},
            )

        self.cantidad_disponible = self._cantidad_disponible + unidades
        self._logger.info(
            "Liberadas %d unidad(es) de [%s]. Stock actual: %d.",
            unidades_validas,
            self._id_entidad,
            self._cantidad_disponible,
        )

    def validar_parametros(self) -> bool:
        """Sobrescritura polimórfica: verifica categoría válida, stock >= 0 y booleano de seguro."""
        if self._categoria_equipo not in self.CATEGORIAS_EQUIPO_VALIDAS:
            raise DatosInvalidosError(
                "Categoría de equipo inválida al validar parámetros.",
                contexto={"id_servicio": self._id_entidad, "categoria": self._categoria_equipo},
            )
        if self._cantidad_disponible < 0:
            raise DatosInvalidosError(
                "El stock del equipo no puede ser negativo.",
                contexto={"id_servicio": self._id_entidad, "stock": self._cantidad_disponible},
            )
        if not isinstance(self._requiere_seguro, bool):
            raise DatosInvalidosError(
                "El indicador de seguro debe ser booleano.",
                contexto={"id_servicio": self._id_entidad},
            )
        return True

    def calcular_costo_base(self, duracion: float) -> float:
        """Sobrescritura polimórfica: calcula el costo por duración más seguro obligatorio (12 %)."""
        duracion_valida = self.validar_duracion(duracion)
        subtotal = self._tarifa_base * duracion_valida

        # Aplica el recargo de póliza de garantía cuando el equipo requiere seguro.
        if self._requiere_seguro:
            subtotal *= 1.0 + self.PORCENTAJE_SEGURO_OBLIGATORIO

        return round(subtotal, 2)

    def describir_servicio(self) -> str:
        """Sobrescritura polimórfica: retorna la ficha técnica y de inventario del equipo."""
        estado = "Disponible" if self._disponible else "No disponible"
        seguro = "Sí (+12%)" if self._requiere_seguro else "No"
        return (
            f"Equipo [{self._id_entidad}] {self._nombre_servicio} | "
            f"Categoría: {self._categoria_equipo} | Stock: {self._cantidad_disponible} | "
            f"Seguro: {seguro} | Tarifa base: ${self._tarifa_base:,.2f}/h | "
            f"Estado: {estado}"
        )
