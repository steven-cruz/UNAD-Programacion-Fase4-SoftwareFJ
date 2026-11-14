"""Paquete de utilidades transversales del sistema"""

from src.utils.logger import (
    RUTA_ARCHIVO_LOG,
    RUTA_DIRECTORIO_LOGS,
    obtener_logger,
)

__all__ = [
    "obtener_logger",
    "RUTA_ARCHIVO_LOG",
    "RUTA_DIRECTORIO_LOGS",
]
