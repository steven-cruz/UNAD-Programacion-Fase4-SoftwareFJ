"""Paquete de excepciones personalizadas de negocio."""

from src.excepciones.errores_sistema import (
    CalculoInconsistenteError,
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ParametrosFaltantesError,
    ReservaIncorrectaError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)

__all__ = [
    "SoftwareFJError",
    "DatosInvalidosError",
    "ParametrosFaltantesError",
    "OperacionNoPermitidaError",
    "ReservaIncorrectaError",
    "ServicioNoDisponibleError",
    "CalculoInconsistenteError",
]
