"""Modelo de dominio para el ciclo de vida de reservas.

Implementa la clase ``Reserva`` heredando de ``EntidadSistema``, integrando
un ``Cliente``, un ``Servicio``, duración, máquina de estados
(``PENDIENTE``, ``CONFIRMADA``, ``PROCESADA``, ``CANCELADA``) y manejo
avanzado de excepciones con bloques ``try/except/else/finally`` y
encadenamiento explícito.
"""

import math
from typing import Any

from src.excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ParametrosFaltantesError,
    ReservaIncorrectaError,
    ServicioNoDisponibleError,
)
from src.modelos.cliente import Cliente
from src.modelos.entidad_base import EntidadSistema
from src.modelos.servicio_base import Servicio
from src.modelos.servicio_equipo import ServicioAlquilerEquipo


class Reserva(EntidadSistema):
    """Representa una reserva de servicio realizada por un cliente.

    Controla el ciclo completo desde su creación en estado ``PENDIENTE`` hasta
    su confirmación, procesamiento financiero o cancelación, protegiendo las
    transiciones de estado e impidiendo operaciones sobre recursos inactivos.
    """

    ESTADOS_VALIDOS: tuple[str, ...] = (
        "PENDIENTE",
        "CONFIRMADA",
        "PROCESADA",
        "CANCELADA",
    )

    def __init__(
        self,
        id_entidad: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float,
        activo: bool = True,
    ) -> None:
        """Inicializa una reserva validando cliente, servicio y duración.

        Args:
            id_entidad: Identificador único de la reserva (ej. ``RES-001``).
            cliente: Instancia válida y activa de ``Cliente``.
            servicio: Instancia válida y disponible de ``Servicio``.
            duracion: Tiempo contratado en horas/unidades (mayor a 0).
            activo: Indica si el registro de reserva está habilitado.

        Raises:
            ParametrosFaltantesError: Si cliente, servicio o duración son nulos.
            DatosInvalidosError: Si los tipos no corresponden a ``Cliente``/``Servicio``.
            ReservaIncorrectaError: Si el cliente está inactivo o la duración es inválida.
            ServicioNoDisponibleError: Si el servicio no está activo, disponible o sin stock.
        """
        super().__init__(id_entidad=id_entidad, activo=activo)

        self._estado: str = "PENDIENTE"
        self._costo_total: float = 0.0
        self._motivo_cancelacion: str | None = None
        # Bandera interna que indica si se descontó inventario en confirmación de equipo.
        self._recurso_comprometido: bool = False

        # La asignación mediante setters valida inmediatamente integridad y disponibilidad.
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

        self.validar()

        # Solo asocia la reserva al historial del cliente cuando todas las validaciones pasan.
        self._cliente.agregar_reserva(self)
        self._logger.info(
            "Reserva [%s] creada en estado %s | Cliente: %s | Servicio: %s | Duración: %.2f h",
            self._id_entidad,
            self._estado,
            self._cliente.id_entidad,
            self._servicio.id_entidad,
            self._duracion,
        )

    @property
    def cliente(self) -> Cliente:
        """Retorna el cliente titular de la reserva."""
        return self._cliente

    @cliente.setter
    def cliente(self, valor: Cliente) -> None:
        """Valida que el cliente sea instancia válida de Cliente y se encuentre activo."""
        if valor is None:
            raise ParametrosFaltantesError(
                "El cliente asociado a la reserva es obligatorio.",
                contexto={"id_reserva": self._id_entidad, "campo": "cliente"},
            )
        if not isinstance(valor, Cliente):
            raise DatosInvalidosError(
                "El cliente proporcionado debe ser una instancia válida de Cliente.",
                contexto={"campo": "cliente", "tipo": type(valor).__name__},
            )
        if not valor.activo:
            raise ReservaIncorrectaError(
                f"No se puede crear reserva para el cliente inactivo [{valor.id_entidad}].",
                contexto={"id_reserva": self._id_entidad, "id_cliente": valor.id_entidad},
            )
        self._cliente = valor

    @property
    def servicio(self) -> Servicio:
        """Retorna el servicio contratado en la reserva."""
        return self._servicio

    @servicio.setter
    def servicio(self, valor: Servicio) -> None:
        """Valida instancia de Servicio, disponibilidad general y stock si es equipo."""
        if valor is None:
            raise ParametrosFaltantesError(
                "El servicio asociado a la reserva es obligatorio.",
                contexto={"id_reserva": self._id_entidad, "campo": "servicio"},
            )
        if not isinstance(valor, Servicio):
            raise DatosInvalidosError(
                "El servicio proporcionado debe heredar de la clase abstracta Servicio.",
                contexto={"campo": "servicio", "tipo": type(valor).__name__},
            )
        if not valor.activo or not valor.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio [{valor.id_entidad} - {valor.nombre_servicio}] no está disponible.",
                contexto={"id_reserva": self._id_entidad, "id_servicio": valor.id_entidad},
            )
        if isinstance(valor, ServicioAlquilerEquipo):
            valor.verificar_stock(1)
        self._servicio = valor

    @property
    def duracion(self) -> float:
        """Retorna la duración contratada del servicio."""
        return self._duracion

    @duracion.setter
    def duracion(self, valor: Any) -> None:
        """Valida que la duración sea numérica, finita y estrictamente positiva."""
        if valor is None:
            raise ParametrosFaltantesError(
                "La duración de la reserva es obligatoria.",
                contexto={"id_reserva": self._id_entidad, "campo": "duracion"},
            )
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ReservaIncorrectaError(
                "La duración de la reserva debe ser un valor numérico.",
                contexto={"id_reserva": self._id_entidad, "valor": valor},
            )
        duracion_float = float(valor)
        if not math.isfinite(duracion_float) or duracion_float <= 0:
            raise ReservaIncorrectaError(
                "La duración de la reserva debe ser mayor a cero.",
                contexto={"id_reserva": self._id_entidad, "duracion": valor},
            )
        self._duracion = duracion_float

    @property
    def estado(self) -> str:
        """Retorna el estado actual dentro del ciclo de vida de la reserva."""
        return self._estado

    @property
    def costo_total(self) -> float:
        """Retorna el monto calculado al procesar la reserva (0.0 mientras no se procese)."""
        return self._costo_total

    @property
    def motivo_cancelacion(self) -> str | None:
        """Retorna el motivo registrado si la reserva fue cancelada."""
        return self._motivo_cancelacion

    def confirmar_reserva(self) -> None:
        """Transiciona la reserva de ``PENDIENTE`` a ``CONFIRMADA`` validando disponibilidad.

        Raises:
            OperacionNoPermitidaError: Si la reserva no está en estado ``PENDIENTE``.
            ServicioNoDisponibleError: Si el servicio dejó de estar disponible o sin stock.
        """
        # Impide confirmar reservas canceladas, procesadas o ya confirmadas.
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva [{self._id_entidad}] desde el estado '{self._estado}'.",
                contexto={"id_reserva": self._id_entidad, "estado_actual": self._estado},
            )

        if not self._servicio.activo or not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio [{self._servicio.id_entidad}] ya no está disponible para confirmar.",
                contexto={"id_reserva": self._id_entidad, "id_servicio": self._servicio.id_entidad},
            )

        # Descuenta una unidad de inventario si el servicio es de alquiler de equipos.
        if isinstance(self._servicio, ServicioAlquilerEquipo):
            self._servicio.asignar_unidades(1)
            self._recurso_comprometido = True

        self._estado = "CONFIRMADA"
        self._logger.info(
            "Reserva [%s] confirmada correctamente para cliente [%s].",
            self._id_entidad,
            self._cliente.id_entidad,
        )

    def procesar_reserva(
        self,
        tasa_impuesto: float = 0.19,
        porcentaje_descuento: float = 0.0,
        **cargos_extra: float,
    ) -> float:
        """Calcula el costo total mediante el método sobrecargado y procesa la reserva.

        Implementa un bloque ``try / except / else / finally`` completo y
        **encadenamiento de excepciones** (``raise ... from ...``) si falla el
        cálculo de costos.

        Raises:
            OperacionNoPermitidaError: Si la reserva no se encuentra en estado ``CONFIRMADA``.
            ReservaIncorrectaError: Si ocurre un error financiero o de cálculo (encadenado).
        """
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas en estado 'CONFIRMADA' (actual: '{self._estado}').",
                contexto={"id_reserva": self._id_entidad, "estado_actual": self._estado},
            )

        try:
            # Invoca el método sobrecargado del servicio pasando impuestos, descuentos y extras.
            costo_calculado = self._servicio.calcular_costo(
                self._duracion,
                tasa_impuesto,
                porcentaje_descuento,
                **cargos_extra,
            )
        except (CalculoInconsistenteError, DatosInvalidosError, ParametrosFaltantesError) as error_calculo:
            # Encadenamiento de excepciones: conserva la causa matemática original en __cause__.
            self._logger.error(
                "Error de cálculo al procesar reserva [%s]: %s",
                self._id_entidad,
                error_calculo,
            )
            raise ReservaIncorrectaError(
                f"No fue posible procesar la reserva [{self._id_entidad}] debido a un cálculo inválido.",
                contexto={"id_reserva": self._id_entidad, "id_servicio": self._servicio.id_entidad},
            ) from error_calculo
        else:
            # Solo cambia el estado a PROCESADA si el cálculo financiero finalizó sin excepciones.
            self._costo_total = costo_calculado
            self._estado = "PROCESADA"
            self._logger.info(
                "Reserva [%s] procesada exitosamente. Total facturado: $%.2f",
                self._id_entidad,
                self._costo_total,
            )
            return self._costo_total
        finally:
            # El bloque finally deja registro de cierre del intento de procesamiento en cualquier escenario.
            self._logger.info(
                "Finalizó intento de procesamiento de reserva [%s] (estado actual: %s).",
                self._id_entidad,
                self._estado,
            )

    def cancelar_reserva(self, motivo: str) -> None:
        """Cancela una reserva ``PENDIENTE`` o ``CONFIRMADA`` y libera recursos reservados.

        Raises:
            ParametrosFaltantesError: Si el motivo es ``None`` o vacío.
            DatosInvalidosError: Si el motivo no es texto.
            OperacionNoPermitidaError: Si la reserva ya está ``PROCESADA`` o ``CANCELADA``.
        """
        if motivo is None:
            raise ParametrosFaltantesError(
                "Debe indicar un motivo para cancelar la reserva.",
                contexto={"id_reserva": self._id_entidad},
            )
        if not isinstance(motivo, str):
            raise DatosInvalidosError(
                "El motivo de cancelación debe ser una cadena de texto.",
                contexto={"id_reserva": self._id_entidad, "tipo": type(motivo).__name__},
            )
        motivo_limpio = motivo.strip()
        if not motivo_limpio:
            raise ParametrosFaltantesError(
                "El motivo de cancelación no puede estar vacío.",
                contexto={"id_reserva": self._id_entidad},
            )

        # Regla de negocio: una reserva ya procesada o previamente cancelada no admite cancelación.
        if self._estado in ("PROCESADA", "CANCELADA"):
            raise OperacionNoPermitidaError(
                f"No es posible cancelar la reserva [{self._id_entidad}] porque su estado es '{self._estado}'.",
                contexto={"id_reserva": self._id_entidad, "estado_actual": self._estado},
            )

        # Si había unidades comprometidas al confirmar un equipo, las restituye al inventario.
        if self._recurso_comprometido and isinstance(self._servicio, ServicioAlquilerEquipo):
            self._servicio.liberar_unidades(1)
            self._recurso_comprometido = False

        self._motivo_cancelacion = motivo_limpio
        self._estado = "CANCELADA"
        self._logger.warning(
            "Reserva [%s] cancelada. Motivo: %s",
            self._id_entidad,
            self._motivo_cancelacion,
        )

    def validar(self) -> bool:
        """Verifica que la reserva mantenga cliente, servicio, duración y estado válidos."""
        return bool(
            isinstance(self._cliente, Cliente)
            and isinstance(self._servicio, Servicio)
            and self._duracion > 0
            and self._estado in self.ESTADOS_VALIDOS
        )

    def mostrar_resumen(self) -> str:
        """Devuelve un resumen legible con los datos clave y estado de la reserva."""
        detalle_extra = (
            f" | Motivo: {self._motivo_cancelacion}"
            if self._estado == "CANCELADA" and self._motivo_cancelacion
            else ""
        )
        return (
            f"Reserva [{self._id_entidad}] Estado: {self._estado} | "
            f"Cliente: {self._cliente.nombre} ({self._cliente.id_entidad}) | "
            f"Servicio: {self._servicio.nombre_servicio} ({self._servicio.id_entidad}) | "
            f"Duración: {self._duracion:.1f} h | Total: ${self._costo_total:,.2f}{detalle_extra}"
        )
