"""Paquete de modelos orientados a objetos (entidades, clientes, servicios y reservas)."""

from src.modelos.cliente import Cliente
from src.modelos.entidad_base import EntidadSistema
from src.modelos.servicio_base import Servicio

__all__ = [
    "EntidadSistema",
    "Cliente",
    "Servicio",
]
