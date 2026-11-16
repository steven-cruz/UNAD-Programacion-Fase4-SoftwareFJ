"""Servicio especializado para la gestión y reserva de salas.

Implementa la subclase concreta ``ServicioReservaSala`` heredando de
``Servicio`` y aplicando polimorfismo en la validación de parámetros,
descripción detallada y cálculo de costo base con recargos por multimedia
y alta capacidad.
"""

from typing import Any

from src.excepciones import DatosInvalidosError, ParametrosFaltantesError
from src.modelos.servicio_base import Servicio

class ServicioReservaSala(Servicio):
    """Servicio concreto para el alquiler de salas corporativas y académicas.

    Sobrescribe los métodos abstractos de ``Servicio`` para validar aforo por
    tipo de sala y calcular tarifas dinámicas según equipamiento multimedia.
    """

    TIPOS_SALA_VALIDOS: tuple[str, ...] = ("Juntas", "Auditorio", "Laboratorio")
    _MAPA_TIPOS_SALA: dict[str, str] = {
        tipo.lower(): tipo for tipo in TIPOS_SALA_VALIDOS
    }
    CAPACIDAD_MAXIMA_POR_TIPO: dict[str, int] = {
        "Juntas": 40,
        "Laboratorio": 80,
        "Auditorio": 500,
    }
    UMBRAL_ALTA_CAPACIDAD: int = 30
    RECARGO_MULTIMEDIA: float = 0.15
    RECARGO_ALTA_CAPACIDAD: float = 0.10

    def __init__(
        self,
        id_entidad: str,
        nombre_servicio: str,
        tarifa_base: float,
        capacidad_personas: int,
        tipo_sala: str = "Juntas",
        incluye_multimedia: bool = False,
        disponible: bool = True,
        activo: bool = True,
    ) -> None:
        """Inicializa una sala reservable validando sus parámetros específicos.

        Args:
            id_entidad: Código identificador de la sala (ej. ``SALA-101``).
            nombre_servicio: Nombre descriptivo de la sala.
            tarifa_base: Valor por hora del alquiler de la sala.
            capacidad_personas: Aforo máximo permitido para la sala.
            tipo_sala: Clasificación (``Juntas``, ``Auditorio`` o ``Laboratorio``).
            incluye_multimedia: Indica si cuenta con proyección/audio integrado.
            disponible: Estado de disponibilidad actual de la sala.
            activo: Indica si el servicio está habilitado en el catálogo.
        """
        super().__init__(
            id_entidad=id_entidad,
            nombre_servicio=nombre_servicio,
            tarifa_base=tarifa_base,
            disponible=disponible,
            activo=activo,
        )

        # Se asigna tipo_sala antes que capacidad_personas para validar el aforo máximo por tipo.
        self.tipo_sala = tipo_sala
        self.capacidad_personas = capacidad_personas
        self.incluye_multimedia = incluye_multimedia

        # Verifica de forma integral el contrato específico de la subclase.
        self.validar_parametros()
        self._logger.info(
            "Sala [%s - %s] (%s, cap=%d, multimedia=%s) registrada correctamente.",
            self._id_entidad,
            self._nombre_servicio,
            self._tipo_sala,
            self._capacidad_personas,
            self._incluye_multimedia,
        )

    @property
    def tipo_sala(self) -> str:
        """Retorna el tipo normalizado de la sala."""
        return self._tipo_sala

    @tipo_sala.setter
    def tipo_sala(self, valor: str) -> None:
        """Valida que el tipo de sala pertenezca al catálogo y sea coherente con la capacidad."""
        if valor is None:
            raise ParametrosFaltantesError(
                "El tipo de sala es obligatorio y no puede ser nulo.",
                contexto={"campo": "tipo_sala", "valor": valor},
            )
        if not isinstance(valor, str):
            raise DatosInvalidosError(
                "El tipo de sala debe ser una cadena de texto.",
                contexto={"campo": "tipo_sala", "tipo": type(valor).__name__},
            )

        tipo_limpio = valor.strip()
        if not tipo_limpio:
            raise ParametrosFaltantesError(
                "El tipo de sala es obligatorio y no puede estar vacío.",
                contexto={"campo": "tipo_sala", "valor": valor},
            )

        tipo_normalizado = self._MAPA_TIPOS_SALA.get(tipo_limpio.lower())
        if tipo_normalizado is None:
            raise DatosInvalidosError(
                f"Tipo de sala inválido. Opciones permitidas: {', '.join(self.TIPOS_SALA_VALIDOS)}.",
                contexto={"campo": "tipo_sala", "valor": valor},
            )

        # Si la sala ya tenía un aforo definido, valida que no supere el nuevo máximo permitido.
        if hasattr(self, "_capacidad_personas"):
            max_permitido = self.CAPACIDAD_MAXIMA_POR_TIPO[tipo_normalizado]
            if self._capacidad_personas > max_permitido:
                raise DatosInvalidosError(
                    f"La capacidad actual ({self._capacidad_personas}) excede el máximo de "
                    f"{max_permitido} personas para una sala tipo '{tipo_normalizado}'.",
                    contexto={
                        "campo": "tipo_sala",
                        "capacidad_actual": self._capacidad_personas,
                        "maximo": max_permitido,
                    },
                )
        self._tipo_sala = tipo_normalizado

    @property
    def capacidad_personas(self) -> int:
        """Retorna el aforo máximo configurado para la sala."""
        return self._capacidad_personas

    @capacidad_personas.setter
    def capacidad_personas(self, valor: Any) -> None:
        """Valida que la capacidad sea un entero positivo dentro del límite del tipo de sala."""
        if valor is None:
            raise ParametrosFaltantesError(
                "La capacidad de personas es obligatoria.",
                contexto={"campo": "capacidad_personas", "valor": valor},
            )
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise DatosInvalidosError(
                "La capacidad de personas debe ser un número entero.",
                contexto={"campo": "capacidad_personas", "tipo": type(valor).__name__},
            )

        max_permitido = self.CAPACIDAD_MAXIMA_POR_TIPO[self._tipo_sala]
        if valor <= 0 or valor > max_permitido:
            raise DatosInvalidosError(
                f"La capacidad para una sala tipo '{self._tipo_sala}' debe estar entre 1 y {max_permitido} personas.",
                contexto={
                    "campo": "capacidad_personas",
                    "valor": valor,
                    "tipo_sala": self._tipo_sala,
                },
            )
        self._capacidad_personas = valor

    @property
    def incluye_multimedia(self) -> bool:
        """Indica si la sala incluye equipo audiovisual y multimedia."""
        return self._incluye_multimedia

    @incluye_multimedia.setter
    def incluye_multimedia(self, valor: Any) -> None:
        """Valida estrictamente que el indicador multimedia sea booleano."""
        if not isinstance(valor, bool):
            raise DatosInvalidosError(
                "El indicador 'incluye_multimedia' debe ser un valor booleano (True/False).",
                contexto={"campo": "incluye_multimedia", "valor": valor},
            )
        self._incluye_multimedia = valor

    def validar_parametros(self) -> bool:
        """Sobrescritura polimórfica: verifica consistencia entre tipo de sala, aforo y multimedia."""
        if self._tipo_sala not in self.CAPACIDAD_MAXIMA_POR_TIPO:
            raise DatosInvalidosError(
                "Tipo de sala inválido al validar parámetros.",
                contexto={"id_servicio": self._id_entidad, "tipo_sala": self._tipo_sala},
            )
        max_permitido = self.CAPACIDAD_MAXIMA_POR_TIPO[self._tipo_sala]
        if self._capacidad_personas <= 0 or self._capacidad_personas > max_permitido:
            raise DatosInvalidosError(
                "Capacidad de sala fuera del rango permitido para su tipo.",
                contexto={
                    "id_servicio": self._id_entidad,
                    "capacidad": self._capacidad_personas,
                    "maximo": max_permitido,
                },
            )
        if not isinstance(self._incluye_multimedia, bool):
            raise DatosInvalidosError(
                "El parámetro multimedia debe ser booleano.",
                contexto={"id_servicio": self._id_entidad},
            )
        return True

    def calcular_costo_base(self, duracion: float) -> float:
        """Sobrescritura polimórfica: calcula el costo por horas aplicando recargos de sala.

        Suma un recargo del 15 % si incluye equipamiento multimedia y un 10 %
        adicional cuando la capacidad supera las 30 personas.
        """
        duracion_valida = self.validar_duracion(duracion)
        subtotal = self._tarifa_base * duracion_valida

        # Acumula los recargos porcentuales propios de infraestructura y equipamiento.
        factor_recargo = 1.0
        if self._incluye_multimedia:
            factor_recargo += self.RECARGO_MULTIMEDIA
        if self._capacidad_personas > self.UMBRAL_ALTA_CAPACIDAD:
            factor_recargo += self.RECARGO_ALTA_CAPACIDAD

        return round(subtotal * factor_recargo, 2)

    def describir_servicio(self) -> str:
        """Sobrescritura polimórfica: retorna la ficha descriptiva completa de la sala."""
        estado = "Disponible" if self._disponible else "No disponible"
        multimedia = "Sí" if self._incluye_multimedia else "No"
        return (
            f"Sala [{self._id_entidad}] {self._nombre_servicio} | "
            f"Tipo: {self._tipo_sala} | Capacidad: {self._capacidad_personas} personas | "
            f"Multimedia: {multimedia} | Tarifa base: ${self._tarifa_base:,.2f}/h | "
            f"Estado: {estado}"
        )
