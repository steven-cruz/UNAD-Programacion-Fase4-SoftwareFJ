"""Modelo de dominio para la gestión de clientes.

Implementa la clase ``Cliente`` heredando de ``EntidadSistema``, garantizando
encapsulación mediante propiedades, historial interno de reservas protegido
y validaciones estrictas de nombre, correo electrónico, teléfono y categoría.
"""

import re

from typing import Any

from src.excepciones import (
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ParametrosFaltantesError,
)
from src.modelos.entidad_base import EntidadSistema

class Cliente(EntidadSistema):
    """Representa un cliente registrado dentro del sistema.

    Encapsula los datos personales y de contacto aplicando validaciones
    inmediatas en cada propiedad, además de mantener una lista interna con
    el historial de reservas asociadas al cliente.
    """

    TIPOS_CLIENTE_VALIDOS: tuple[str, ...] = ("Corporativo", "Particular", "VIP")
    _MAPA_TIPOS_CLIENTE: dict[str, str] = {
        tipo.lower(): tipo for tipo in TIPOS_CLIENTE_VALIDOS
    }
    LONGITUD_MINIMA_NOMBRE: int = 3
    LONGITUD_MINIMA_TELEFONO: int = 7
    LONGITUD_MAXIMA_TELEFONO: int = 10

    # Valida estructura estándar usuario@dominio.ext sin espacios en blanco.
    _PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    # Permite signo '+' opcional al inicio seguido únicamente de dígitos, espacios o guiones.
    _PATRON_TELEFONO_CARACTERES = re.compile(r"^\+?[\d\s-]+$")

    def __init__(
        self,
        id_entidad: str,
        nombre: str,
        email: str,
        telefono: str,
        tipo_cliente: str = "Particular",
        activo: bool = True,
    ) -> None:
        """Inicializa un nuevo cliente validando todos sus datos obligatorios.

        Args:
            id_entidad: Documento de identidad o NIT único del cliente.
            nombre: Nombre completo o razón social (mínimo 3 caracteres).
            email: Correo electrónico de contacto con formato válido.
            telefono: Número telefónico con entre 7 y 10 dígitos numéricos.
            tipo_cliente: Categoría del cliente (``Corporativo``, ``Particular`` o ``VIP``).
            activo: Indica si el cliente se encuentra habilitado para reservar.

        Raises:
            ParametrosFaltantesError: Si algún campo obligatorio es ``None`` o vacío.
            DatosInvalidosError: Si algún campo incumple las reglas de formato o tipo.
        """
        super().__init__(id_entidad=id_entidad, activo=activo)

        # La asignación a través de las propiedades ejecuta las validaciones estrictas.
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.tipo_cliente = tipo_cliente

        # Lista interna encapsulada para almacenar objetos Reserva asociados al cliente.
        self._historial_reservas: list[Any] = []

        self.validar()
        self._logger.info(
            "Cliente [%s - %s] (%s) registrado correctamente.",
            self._id_entidad,
            self._nombre,
            self._tipo_cliente,
        )

    @staticmethod
    def _validar_texto_obligatorio(valor: Any, nombre_campo: str) -> str:
        """Valida que un campo sea cadena de texto no vacía y devuelve su versión limpia."""
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
    def nombre(self) -> str:
        """Retorna el nombre completo o razón social del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida longitud mínima y formato textual del nombre del cliente."""
        nombre_limpio = self._validar_texto_obligatorio(valor, "nombre")
        if len(nombre_limpio) < self.LONGITUD_MINIMA_NOMBRE:
            raise DatosInvalidosError(
                f"El nombre del cliente debe tener al menos {self.LONGITUD_MINIMA_NOMBRE} caracteres.",
                contexto={"campo": "nombre", "valor": nombre_limpio},
            )
        self._nombre = nombre_limpio

    @property
    def email(self) -> str:
        """Retorna el correo electrónico normalizado en minúsculas."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        """Valida estructura del correo electrónico mediante expresión regular."""
        email_limpio = self._validar_texto_obligatorio(valor, "email").lower()
        if not self._PATRON_EMAIL.match(email_limpio):
            raise DatosInvalidosError(
                "El correo electrónico no tiene un formato válido (usuario@dominio.ext).",
                contexto={"campo": "email", "valor": valor},
            )
        self._email = email_limpio

    @property
    def telefono(self) -> str:
        """Retorna el número telefónico validado del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida caracteres permitidos y cantidad de dígitos en el teléfono."""
        telefono_limpio = self._validar_texto_obligatorio(valor, "telefono")
        if not self._PATRON_TELEFONO_CARACTERES.match(telefono_limpio):
            raise DatosInvalidosError(
                "El teléfono solo puede contener dígitos, espacios, guiones y un '+' opcional al inicio.",
                contexto={"campo": "telefono", "valor": valor},
            )

        # Extrae solo los dígitos numéricos para comprobar el rango de longitud real.
        solo_digitos = re.sub(r"\D", "", telefono_limpio)
        if not (self.LONGITUD_MINIMA_TELEFONO <= len(solo_digitos) <= self.LONGITUD_MAXIMA_TELEFONO):
            raise DatosInvalidosError(
                f"El teléfono debe contener entre {self.LONGITUD_MINIMA_TELEFONO} y "
                f"{self.LONGITUD_MAXIMA_TELEFONO} dígitos numéricos.",
                contexto={"campo": "telefono", "digitos_encontrados": len(solo_digitos)},
            )
        self._telefono = telefono_limpio

    @property
    def tipo_cliente(self) -> str:
        """Retorna la categoría comercial asignada al cliente."""
        return self._tipo_cliente

    @tipo_cliente.setter
    def tipo_cliente(self, valor: str) -> None:
        """Normaliza y valida que el tipo de cliente pertenezca al catálogo permitido."""
        tipo_limpio = self._validar_texto_obligatorio(valor, "tipo_cliente")
        tipo_normalizado = self._MAPA_TIPOS_CLIENTE.get(tipo_limpio.lower())
        if tipo_normalizado is None:
            raise DatosInvalidosError(
                f"Tipo de cliente no válido. Opciones permitidas: {', '.join(self.TIPOS_CLIENTE_VALIDOS)}.",
                contexto={"campo": "tipo_cliente", "valor": valor},
            )
        self._tipo_cliente = tipo_normalizado

    @property
    def historial_reservas(self) -> list[Any]:
        """Devuelve una copia superficial para impedir modificaciones externas directas."""
        return list(self._historial_reservas)

    def agregar_reserva(self, reserva: Any) -> None:
        """Asocia una reserva al historial interno verificando que no sea nula ni duplicada.

        Args:
            reserva: Instancia de ``Reserva`` vinculada al cliente.

        Raises:
            ParametrosFaltantesError: Si ``reserva`` es ``None``.
            OperacionNoPermitidaError: Si la reserva ya figura en el historial del cliente.
        """
        if reserva is None:
            raise ParametrosFaltantesError(
                "No se puede agregar una reserva nula al historial del cliente.",
                contexto={"id_cliente": self._id_entidad},
            )

        id_nueva_reserva = getattr(reserva, "id_entidad", None)
        # Impide duplicar la misma instancia o dos reservas con idéntico identificador.
        ya_registrada = reserva in self._historial_reservas or (
            id_nueva_reserva is not None
            and any(
                getattr(existente, "id_entidad", None) == id_nueva_reserva
                for existente in self._historial_reservas
            )
        )
        if ya_registrada:
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra registrada en el historial del cliente.",
                contexto={"id_cliente": self._id_entidad, "id_reserva": id_nueva_reserva},
            )

        self._historial_reservas.append(reserva)
        self._logger.info(
            "Reserva [%s] agregada al historial del cliente [%s].",
            id_nueva_reserva or repr(reserva),
            self._id_entidad,
        )

    def obtener_cantidad_reservas(self) -> int:
        """Retorna el número total de reservas asociadas al cliente."""
        return len(self._historial_reservas)

    def validar(self) -> bool:
        """Verifica la integridad completa de los atributos del cliente."""
        return bool(
            self._id_entidad
            and len(self._nombre) >= self.LONGITUD_MINIMA_NOMBRE
            and self._PATRON_EMAIL.match(self._email)
            and self._tipo_cliente in self.TIPOS_CLIENTE_VALIDOS
        )

    def mostrar_resumen(self) -> str:
        """Devuelve una ficha descriptiva legible del cliente y su historial."""
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente [{self._id_entidad}] | {self._nombre} ({self._tipo_cliente}) | "
            f"Email: {self._email} | Tel: {self._telefono} | "
            f"Estado: {estado} | Reservas: {len(self._historial_reservas)}"
        )
