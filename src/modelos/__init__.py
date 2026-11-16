"""Paquete de modelos orientados a objetos (entidades, clientes, servicios y reservas)."""

from src.modelos.cliente import Cliente
from src.modelos.entidad_base import EntidadSistema
from src.modelos.servicio_base import Servicio
from src.modelos.servicio_equipo import ServicioAlquilerEquipo
from src.modelos.servicio_sala import ServicioReservaSala

__all__ = [
    "EntidadSistema",
    "Cliente",
    "Servicio",
    "ServicioReservaSala",
    "ServicioAlquilerEquipo",
]
