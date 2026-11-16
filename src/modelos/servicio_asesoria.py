"""Servicio especializado para asesorías técnicas.

Implementa la subclase concreta ``ServicioAsesoriaEspecializada`` heredando de
``Servicio``, aplicando polimorfismo en la validación de área, nivel del
consultor y modalidad, así como en el cálculo dinámico de tarifas.
"""

from typing import Any

from src.excepciones import DatosInvalidosError, ParametrosFaltantesError
from src.modelos.servicio_base import Servicio


class ServicioAsesoriaEspecializada(Servicio):
    """Servicio concreto para consultoría y asesoría técnica especializada.

    Ajusta polimórficamente el costo base aplicando un factor multiplicador según
    la experiencia del consultor y un cargo logístico cuando la modalidad es
    presencial.
    """

    NIVELES_CONSULTOR_VALIDOS: tuple[str, ...] = (
        "Junior",
        "Senior",
        "Arquitecto Experto",
    )
    _MAPA_NIVELES: dict[str, str] = {
        nivel.lower(): nivel for nivel in NIVELES_CONSULTOR_VALIDOS
    }
    FACTOR_POR_NIVEL: dict[str, float] = {
        "Junior": 1.0,
        "Senior": 1.35,
        "Arquitecto Experto": 1.75,
    }

    MODALIDADES_VALIDAS: tuple[str, ...] = ("Remota", "Presencial")
    _MAPA_MODALIDADES: dict[str, str] = {
        mod.lower(): mod for mod in MODALIDADES_VALIDAS
    }
    CARGO_LOGISTICO_PRESENCIAL: float = 45000.0
    LONGITUD_MINIMA_AREA: int = 2

    def __init__(
        self,
        id_entidad: str,
        nombre_servicio: str,
        tarifa_base: float,
        area_especialidad: str,
        nivel_consultor: str = "Senior",
        modalidad: str = "Remota",
        disponible: bool = True,
        activo: bool = True,
    ) -> None:
        """Inicializa una asesoría especializada validando sus parámetros propios.

        Args:
            id_entidad: Código identificador del servicio (ej. ``ASE-01``).
            nombre_servicio: Título comercial de la asesoría.
            tarifa_base: Tarifa base por hora antes de aplicar factor de nivel.
            area_especialidad: Área técnica (ej. ``Arquitectura Cloud``, ``Ciberseguridad``).
            nivel_consultor: Experiencia (``Junior``, ``Senior`` o ``Arquitecto Experto``).
            modalidad: Forma de atención (``Remota`` o ``Presencial``).
            disponible: Indica si el servicio admite nuevas reservas.
            activo: Indica si el servicio está habilitado en el catálogo.
        """
        super().__init__(
            id_entidad=id_entidad,
            nombre_servicio=nombre_servicio,
            tarifa_base=tarifa_base,
            disponible=disponible,
            activo=activo,
        )

        self.area_especialidad = area_especialidad
        self.nivel_consultor = nivel_consultor
        self.modalidad = modalidad

        self.validar_parametros()
        self._logger.info(
            "Asesoría [%s - %s] (Área: %s, Nivel: %s, Modalidad: %s) registrada correctamente.",
            self._id_entidad,
            self._nombre_servicio,
            self._area_especialidad,
            self._nivel_consultor,
            self._modalidad,
        )

    @staticmethod
    def _validar_texto_no_vacio(valor: Any, nombre_campo: str) -> str:
        """Valida que el valor recibido sea cadena de texto no nula ni vacía."""
        if valor is None:
            raise ParametrosFaltantesError(
                f"El campo '{nombre_campo}' es obligatorio y no puede ser nulo.",
                contexto={"campo": nombre_campo, "valor": valor},
            )
        if not isinstance(valor, str):
            raise DatosInvalidosError(
                f"El campo '{nombre_campo}' debe ser una cadena de texto.",
                contexto={"campo": nombre_campo, "tipo": type(valor).__name__},
            )
        texto_limpio = valor.strip()
        if not texto_limpio:
            raise ParametrosFaltantesError(
                f"El campo '{nombre_campo}' es obligatorio y no puede estar vacío.",
                contexto={"campo": nombre_campo, "valor": valor},
            )
        return texto_limpio

    @property
    def area_especialidad(self) -> str:
        """Retorna el área de especialidad técnica de la asesoría."""
        return self._area_especialidad

    @area_especialidad.setter
    def area_especialidad(self, valor: str) -> None:
        """Valida que el área de especialidad no sea vacía y tenga longitud mínima."""
        area_limpia = self._validar_texto_no_vacio(valor, "area_especialidad")
        if len(area_limpia) < self.LONGITUD_MINIMA_AREA:
            raise DatosInvalidosError(
                f"El área de especialidad debe tener al menos {self.LONGITUD_MINIMA_AREA} caracteres.",
                contexto={"campo": "area_especialidad", "valor": area_limpia},
            )
        self._area_especialidad = area_limpia

    @property
    def nivel_consultor(self) -> str:
        """Retorna el nivel de seniority normalizado del consultor."""
        return self._nivel_consultor

    @nivel_consultor.setter
    def nivel_consultor(self, valor: str) -> None:
        """Valida que el nivel pertenezca a las categorías permitidas."""
        nivel_limpio = self._validar_texto_no_vacio(valor, "nivel_consultor")
        nivel_normalizado = self._MAPA_NIVELES.get(nivel_limpio.lower())
        if nivel_normalizado is None:
            raise DatosInvalidosError(
                "Nivel de consultor no válido. Opciones permitidas: "
                f"{', '.join(self.NIVELES_CONSULTOR_VALIDOS)}.",
                contexto={"campo": "nivel_consultor", "valor": valor},
            )
        self._nivel_consultor = nivel_normalizado

    @property
    def modalidad(self) -> str:
        """Retorna la modalidad de prestación del servicio (Remota o Presencial)."""
        return self._modalidad

    @modalidad.setter
    def modalidad(self, valor: str) -> None:
        """Valida que la modalidad sea 'Remota' o 'Presencial'."""
        modalidad_limpia = self._validar_texto_no_vacio(valor, "modalidad")
        modalidad_normalizada = self._MAPA_MODALIDADES.get(modalidad_limpia.lower())
        if modalidad_normalizada is None:
            raise DatosInvalidosError(
                f"Modalidad inválida. Opciones permitidas: {', '.join(self.MODALIDADES_VALIDAS)}.",
                contexto={"campo": "modalidad", "valor": valor},
            )
        self._modalidad = modalidad_normalizada

    def validar_parametros(self) -> bool:
        """Sobrescritura polimórfica: verifica área no vacía, nivel y modalidad válidos."""
        if not self._area_especialidad or len(self._area_especialidad.strip()) < self.LONGITUD_MINIMA_AREA:
            raise ParametrosFaltantesError(
                "El área de especialidad de la asesoría es obligatoria.",
                contexto={"id_servicio": self._id_entidad},
            )
        if self._nivel_consultor not in self.FACTOR_POR_NIVEL:
            raise DatosInvalidosError(
                "Nivel de consultor inválido al validar la asesoría.",
                contexto={"id_servicio": self._id_entidad, "nivel": self._nivel_consultor},
            )
        if self._modalidad not in self.MODALIDADES_VALIDAS:
            raise DatosInvalidosError(
                "Modalidad inválida al validar la asesoría.",
                contexto={"id_servicio": self._id_entidad, "modalidad": self._modalidad},
            )
        return True

    def calcular_costo_base(self, duracion: float) -> float:
        """Sobrescritura polimórfica: aplica multiplicador de seniority y cargo presencial.

        Multiplica la tarifa base por la duración y el factor del nivel del
        consultor; si la modalidad es ``Presencial``, suma el cargo logístico.
        """
        duracion_valida = self.validar_duracion(duracion)
        factor_nivel = self.FACTOR_POR_NIVEL[self._nivel_consultor]
        costo = self._tarifa_base * factor_nivel * duracion_valida

        # Agrega el costo fijo de desplazamiento/logística para asesorías presenciales.
        if self._modalidad == "Presencial":
            costo += self.CARGO_LOGISTICO_PRESENCIAL

        return round(costo, 2)

    def describir_servicio(self) -> str:
        """Sobrescritura polimórfica: devuelve la ficha técnica de la asesoría."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"Asesoría [{self._id_entidad}] {self._nombre_servicio} | "
            f"Área: {self._area_especialidad} | Nivel: {self._nivel_consultor} | "
            f"Modalidad: {self._modalidad} | Tarifa base: ${self._tarifa_base:,.2f}/h | "
            f"Estado: {estado}"
        )
