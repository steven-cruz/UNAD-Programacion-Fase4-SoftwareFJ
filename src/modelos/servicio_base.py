"""Clase abstracta de dominio para el catálogo de servicios.

Define la clase abstracta ``Servicio`` (subclase de ``EntidadSistema``) con el
contrato polimórfico obligatorio para ``calcular_costo_base``,
``describir_servicio`` y ``validar_parametros``, además de implementar la
sobrecarga de ``calcular_costo`` con impuestos, descuentos y cargos extra.
"""

from abc import ABC, abstractmethod
import math
from typing import Any, overload

from src.excepciones import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    ParametrosFaltantesError,
)
from src.modelos.entidad_base import EntidadSistema

class Servicio(EntidadSistema, ABC):
    """Clase abstracta base para todos los servicios ofrecidos.

    Sirve como padre común de ``ServicioReservaSala``, ``ServicioAlquilerEquipo``
    y ``ServicioAsesoriaEspecializada``, unificando encapsulación de tarifa,
    control de disponibilidad y cálculo polimórfico sobrecargado de costos.
    """

    LONGITUD_MINIMA_NOMBRE: int = 3

    def __init__(
        self,
        id_entidad: str,
        nombre_servicio: str,
        tarifa_base: float,
        disponible: bool = True,
        activo: bool = True,
    ) -> None:
        """Inicializa los atributos comunes encapsulados de cualquier servicio.

        Args:
            id_entidad: Código identificador único del servicio (ej. ``SALA-01``).
            nombre_servicio: Nombre comercial descriptivo del servicio.
            tarifa_base: Valor base por unidad o por hora (debe ser mayor a 0).
            disponible: Indica si el servicio admite nuevas reservas en este momento.
            activo: Indica si el servicio está habilitado en el catálogo.

        Raises:
            ParametrosFaltantesError: Si falta algún parámetro obligatorio.
            DatosInvalidosError: Si los tipos o rangos iniciales son inválidos.
        """
        super().__init__(id_entidad=id_entidad, activo=activo)

        # Las asignaciones activan los setters validados de cada propiedad.
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @staticmethod
    def _validar_numero(valor: Any, nombre_campo: str) -> float:
        """Valida que un valor sea numérico finito y no booleano."""
        if valor is None:
            raise ParametrosFaltantesError(
                f"El parámetro numérico '{nombre_campo}' es obligatorio.",
                contexto={"campo": nombre_campo, "valor": valor},
            )
        # Se excluye bool explícitamente porque en Python bool es subclase de int.
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise DatosInvalidosError(
                f"El parámetro '{nombre_campo}' debe ser numérico (int o float).",
                contexto={"campo": nombre_campo, "tipo": type(valor).__name__},
            )

        numero = float(valor)
        if not math.isfinite(numero):
            raise CalculoInconsistenteError(
                f"El parámetro '{nombre_campo}' debe ser un número finito.",
                contexto={"campo": nombre_campo, "valor": valor},
            )
        return numero

    @staticmethod
    def validar_duracion(duracion: Any) -> float:
        """Valida que la duración de la reserva o servicio sea numérica y mayor a cero."""
        duracion_num = Servicio._validar_numero(duracion, "duracion")
        if duracion_num <= 0:
            raise DatosInvalidosError(
                "La duración del servicio debe ser mayor a cero.",
                contexto={"campo": "duracion", "valor": duracion},
            )
        return duracion_num

    @staticmethod
    def _normalizar_proporcion(valor: Any, nombre_campo: str) -> float:
        """Valida tasas/porcentajes en rango [0, 100] y los normaliza a [0.0, 1.0].

        Permite pasar tanto proporciones decimales (ej. ``0.19`` para 19 %)
        como porcentajes enteros o reales mayores a 1 (ej. ``19`` para 19 %).
        """
        numero = Servicio._validar_numero(valor, nombre_campo)
        if numero < 0 or numero > 100.0:
            raise CalculoInconsistenteError(
                f"El valor de '{nombre_campo}' debe estar entre 0 y 100 (o 0.0 y 1.0).",
                contexto={"campo": nombre_campo, "valor": valor},
            )
        # Valores en [0.0, 1.0] se interpretan como proporción directa; > 1.0 como porcentaje.
        return numero if numero <= 1.0 else numero / 100.0

    @property
    def nombre_servicio(self) -> str:
        """Retorna el nombre descriptivo del servicio."""
        return self._nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor: str) -> None:
        """Valida que el nombre del servicio sea texto no vacío con longitud mínima."""
        if valor is None:
            raise ParametrosFaltantesError(
                "El nombre del servicio es obligatorio y no puede ser nulo.",
                contexto={"campo": "nombre_servicio", "valor": valor},
            )
        if not isinstance(valor, str):
            raise DatosInvalidosError(
                "El nombre del servicio debe ser una cadena de texto.",
                contexto={"campo": "nombre_servicio", "tipo": type(valor).__name__},
            )
        nombre_limpio = valor.strip()
        if not nombre_limpio:
            raise ParametrosFaltantesError(
                "El nombre del servicio es obligatorio y no puede estar vacío.",
                contexto={"campo": "nombre_servicio", "valor": valor},
            )
        if len(nombre_limpio) < self.LONGITUD_MINIMA_NOMBRE:
            raise DatosInvalidosError(
                f"El nombre del servicio debe tener al menos {self.LONGITUD_MINIMA_NOMBRE} caracteres.",
                contexto={"campo": "nombre_servicio", "valor": nombre_limpio},
            )
        self._nombre_servicio = nombre_limpio

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base por unidad o por hora del servicio."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        """Valida que la tarifa base sea numérica y estrictamente positiva."""
        tarifa_num = self._validar_numero(valor, "tarifa_base")
        if tarifa_num <= 0:
            raise DatosInvalidosError(
                "La tarifa base del servicio debe ser mayor a cero.",
                contexto={"campo": "tarifa_base", "valor": valor},
            )
        self._tarifa_base = round(tarifa_num, 2)

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para ser reservado."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Valida estrictamente que la disponibilidad sea un valor booleano."""
        if not isinstance(valor, bool):
            raise DatosInvalidosError(
                "La disponibilidad del servicio debe ser un valor booleano (True/False).",
                contexto={"campo": "disponible", "valor": valor},
            )
        self._disponible = valor

    def _actualizar_disponibilidad(self, disponible: bool) -> None:
        """Actualiza el indicador de disponibilidad y deja traza en el log."""
        self._disponible = disponible
        etiqueta = "disponible" if disponible else "no disponible"
        self._logger.info(
            "Servicio [%s - %s] marcado como %s.",
            self._id_entidad,
            self._nombre_servicio,
            etiqueta,
        )

    def marcar_disponible(self) -> None:
        """Habilita la disponibilidad del servicio para nuevas reservas."""
        self._actualizar_disponibilidad(True)

    def marcar_no_disponible(self) -> None:
        """Marca el servicio como temporalmente no disponible."""
        self._actualizar_disponibilidad(False)

    @abstractmethod
    def calcular_costo_base(self, duracion: float) -> float:
        """Calcula el costo base polimórfico propio de cada tipo de servicio."""

    @abstractmethod
    def describir_servicio(self) -> str:
        """Devuelve una descripción detallada y específica del servicio concreto."""

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Valida los parámetros particulares exigidos por cada servicio especializado."""

    # --- Sobrecarga de método mediante @overload + parámetros por defecto y **kwargs ---
    # En Python no existen múltiples definiciones en tiempo de ejecución con el mismo nombre;
    # @overload documenta y tipa estáticamente las variantes de llamada admitidas.
    @overload
    def calcular_costo(self, duracion: float) -> float: ...

    @overload
    def calcular_costo(self, duracion: float, tasa_impuesto: float) -> float: ...

    @overload
    def calcular_costo(
        self,
        duracion: float,
        tasa_impuesto: float,
        porcentaje_descuento: float,
        **cargos_extra: float,
    ) -> float: ...

    def calcular_costo(
        self,
        duracion: float,
        tasa_impuesto: float = 0.0,
        porcentaje_descuento: float = 0.0,
        **cargos_extra: float,
    ) -> float:
        """Calcula el costo final del servicio soportando múltiples variantes de parámetros.

        Variantes de sobrecarga soportadas:
            1. ``calcular_costo(duracion)``: Solo costo base por duración.
            2. ``calcular_costo(duracion, tasa_impuesto)``: Costo base más impuesto.
            3. ``calcular_costo(duracion, tasa_impuesto, porcentaje_descuento)``:
               Aplica descuento sobre el costo base y luego calcula el impuesto.
            4. ``calcular_costo(duracion, ..., **cargos_extra)``: Suma conceptos
               adicionales (ej. ``soporte=20000``, ``seguro=15000``).

        Raises:
            ParametrosFaltantesError: Si algún argumento obligatorio es ``None``.
            DatosInvalidosError: Si la duración o tipos numéricos son inválidos.
            CalculoInconsistenteError: Si hay tasas fuera de rango, cargos negativos
                o resultados financieros inconsistentes.
        """
        duracion_valida = self.validar_duracion(duracion)
        prop_impuesto = self._normalizar_proporcion(tasa_impuesto, "tasa_impuesto")
        prop_descuento = self._normalizar_proporcion(
            porcentaje_descuento,
            "porcentaje_descuento",
        )

        # Valida todos los cargos adicionales recibidos por **kwargs antes de sumarlos.
        total_extras = 0.0
        for nombre_cargo, valor_cargo in cargos_extra.items():
            monto = self._validar_numero(valor_cargo, f"cargos_extra[{nombre_cargo}]")
            if monto < 0:
                raise CalculoInconsistenteError(
                    f"El cargo adicional '{nombre_cargo}' no puede ser negativo.",
                    contexto={"cargo": nombre_cargo, "valor": valor_cargo},
                )
            total_extras += monto

        # Invocación polimórfica: cada subclase determina su propio costo base.
        costo_base = self.calcular_costo_base(duracion_valida)
        if not isinstance(costo_base, (int, float)) or isinstance(costo_base, bool) or costo_base <= 0:
            raise CalculoInconsistenteError(
                "El costo base calculado por el servicio debe ser mayor a cero.",
                contexto={"id_servicio": self._id_entidad, "costo_base": costo_base},
            )

        # Aplica primero el descuento sobre el costo base y luego el impuesto sobre el subtotal.
        subtotal_con_descuento = float(costo_base) * (1.0 - prop_descuento)
        impuestos = subtotal_con_descuento * prop_impuesto
        total = round(subtotal_con_descuento + impuestos + total_extras, 2)

        if total < 0:
            raise CalculoInconsistenteError(
                "El cálculo final arrojó un monto negativo inconsistente.",
                contexto={"id_servicio": self._id_entidad, "total": total},
            )

        self._logger.info(
            "Costo calculado para servicio [%s]: base=%.2f, desc=%.2f%%, imp=%.2f%%, extras=%.2f -> total=%.2f",
            self._id_entidad,
            costo_base,
            prop_descuento * 100,
            prop_impuesto * 100,
            total_extras,
            total,
        )
        return total

    def validar(self) -> bool:
        """Valida atributos base heredados y delega en ``validar_parametros()``."""
        atributos_base_ok = bool(
            self._id_entidad and self._nombre_servicio and self._tarifa_base > 0
        )
        return atributos_base_ok and bool(self.validar_parametros())

    def mostrar_resumen(self) -> str:
        """Delega el resumen general de la entidad al método polimórfico ``describir_servicio``."""
        return self.describir_servicio()
