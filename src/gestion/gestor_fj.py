"""Gestor central en memoria para el sistema.

Implementa la clase ``SistemaSoftwareFJ`` encargada de administrar las listas
internas de clientes, servicios y reservas (sin motores de bases de datos),
orquestando todas las operaciones mediante bloques ``try/except``,
``try/except/else``, ``try/finally`` y encadenamiento de excepciones para
garantizar continuidad operativa ante cualquier fallo.
"""

from typing import Any, TypeVar

from src.excepciones import (
    DatosInvalidosError,
    OperacionNoPermitidaError,
    ParametrosFaltantesError,
    ReservaIncorrectaError,
    SoftwareFJError,
)
from src.modelos import Cliente, EntidadSistema, Reserva, Servicio
from src.utils import obtener_logger

TEntidad = TypeVar("TEntidad", bound=EntidadSistema)


class SistemaSoftwareFJ:
    """Controlador principal de clientes, servicios y reservas.

    Mantiene la totalidad del estado operativo en listas en memoria y captura
    cualquier error de dominio o inesperado registrándolo en el archivo de logs
    para asegurar que la aplicación nunca interrumpa su ejecución.
    """

    def __init__(self) -> None:
        """Inicializa las listas internas en memoria y el logger del sistema."""
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        self._logger = obtener_logger(self.__class__.__name__)
        self._logger.info("Sistema inicializado en memoria.")

    @property
    def clientes(self) -> list[Cliente]:
        """Devuelve una copia superficial de la lista de clientes registrados."""
        return list(self._clientes)

    @property
    def servicios(self) -> list[Servicio]:
        """Devuelve una copia superficial del catálogo de servicios en memoria."""
        return list(self._servicios)

    @property
    def reservas(self) -> list[Reserva]:
        """Devuelve una copia superficial de las reservas registradas."""
        return list(self._reservas)

    @staticmethod
    def _buscar_por_id(
        coleccion: list[TEntidad],
        id_objetivo: Any,
        nombre_entidad: str,
    ) -> TEntidad:
        """Localiza una entidad por su identificador o lanza excepción de negocio."""
        if id_objetivo is None or (isinstance(id_objetivo, str) and not id_objetivo.strip()):
            raise ParametrosFaltantesError(
                f"El identificador de {nombre_entidad} es obligatorio para la búsqueda.",
                contexto={"entidad": nombre_entidad, "id": id_objetivo},
            )
        if not isinstance(id_objetivo, str):
            raise DatosInvalidosError(
                f"El identificador de {nombre_entidad} debe ser una cadena de texto.",
                contexto={"entidad": nombre_entidad, "tipo": type(id_objetivo).__name__},
            )

        id_limpio = id_objetivo.strip()
        for elemento in coleccion:
            if elemento.id_entidad == id_limpio:
                return elemento

        raise DatosInvalidosError(
            f"No existe {nombre_entidad} con identificador '{id_limpio}'.",
            contexto={"entidad": nombre_entidad, "id": id_limpio},
        )

    @staticmethod
    def _existe_id(coleccion: list[Any], id_objetivo: Any) -> bool:
        """Comprueba si un identificador ya existe en la lista interna."""
        if not isinstance(id_objetivo, str):
            return False
        id_limpio = id_objetivo.strip()
        return any(item.id_entidad == id_limpio for item in coleccion)

    def _registrar_error_resiliente(self, operacion: str, error: Exception) -> None:
        """Registra excepciones (y su causa raíz encadenada) sin detener el sistema."""
        if error.__cause__ is not None:
            # Evidencia explícita de encadenamiento de excepciones en logs/software_fj.log.
            self._logger.error(
                "Error controlado en '%s': %s | Causa raíz: %s",
                operacion,
                error,
                error.__cause__,
            )
        else:
            self._logger.error("Error controlado en '%s': %s", operacion, error)

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        """Busca un cliente por documento/ID dentro de la lista interna."""
        return self._buscar_por_id(self._clientes, id_cliente, "cliente")

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        """Busca un servicio por código dentro del catálogo en memoria."""
        return self._buscar_por_id(self._servicios, id_servicio, "servicio")

    def buscar_reserva(self, id_reserva: str) -> Reserva:
        """Busca una reserva por identificador dentro de la lista interna."""
        return self._buscar_por_id(self._reservas, id_reserva, "reserva")

    def registrar_cliente(
        self,
        id_entidad: str,
        nombre: str,
        email: str,
        telefono: str,
        tipo_cliente: str = "Particular",
        activo: bool = True,
    ) -> Cliente | None:
        """Registra un nuevo cliente en memoria absorbiendo errores sin detener la app."""
        cliente_creado: Cliente | None = None
        try:
            if self._existe_id(self._clientes, id_entidad):
                raise OperacionNoPermitidaError(
                    f"Ya existe un cliente registrado con el identificador '{id_entidad.strip()}'.",
                    contexto={"id_cliente": id_entidad},
                )
            cliente_creado = Cliente(
                id_entidad=id_entidad,
                nombre=nombre,
                email=email,
                telefono=telefono,
                tipo_cliente=tipo_cliente,
                activo=activo,
            )
        except SoftwareFJError as err:
            # Captura errores de validación o duplicidad y permite continuar la ejecución.
            self._registrar_error_resiliente("registrar_cliente", err)
            return None
        except Exception as err_inesperado:
            self._logger.exception(
                "Fallo inesperado en 'registrar_cliente': %s",
                err_inesperado,
            )
            return None
        else:
            # Solo inserta en la lista interna si la construcción y validaciones fueron exitosas.
            self._clientes.append(cliente_creado)
            self._logger.info(
                "Cliente [%s - %s] añadido a la lista interna. Total clientes: %d.",
                cliente_creado.id_entidad,
                cliente_creado.nombre,
                len(self._clientes),
            )
            return cliente_creado
        finally:
            self._logger.info("Fin de operación 'registrar_cliente' para ID=%r.", id_entidad)

    def registrar_servicio(self, servicio: Servicio) -> Servicio | None:
        """Valida e incorpora cualquier servicio polimórfico al catálogo en memoria."""
        try:
            if servicio is None:
                raise ParametrosFaltantesError(
                    "No se puede registrar un servicio nulo.",
                    contexto={"campo": "servicio"},
                )
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError(
                    "El objeto debe ser una instancia derivada de Servicio.",
                    contexto={"tipo": type(servicio).__name__},
                )
            if self._existe_id(self._servicios, servicio.id_entidad):
                raise OperacionNoPermitidaError(
                    f"Ya existe un servicio registrado con código '{servicio.id_entidad}'.",
                    contexto={"id_servicio": servicio.id_entidad},
                )
            # Ejecuta la validación polimórfica específica de la subclase de servicio.
            servicio.validar()
        except SoftwareFJError as err:
            self._registrar_error_resiliente("registrar_servicio", err)
            return None
        except Exception as err_inesperado:
            self._logger.exception(
                "Fallo inesperado en 'registrar_servicio': %s",
                err_inesperado,
            )
            return None
        else:
            self._servicios.append(servicio)
            self._logger.info(
                "Servicio [%s - %s] incorporado al catálogo. Total servicios: %d.",
                servicio.id_entidad,
                servicio.nombre_servicio,
                len(self._servicios),
            )
            return servicio
        finally:
            self._logger.info("Fin de operación 'registrar_servicio'.")

    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion: float,
    ) -> Reserva | None:
        """Crea una reserva buscando referencias en memoria y aplicando encadenamiento."""
        nueva_reserva: Reserva | None = None
        try:
            if self._existe_id(self._reservas, id_reserva):
                raise OperacionNoPermitidaError(
                    f"Ya existe una reserva registrada con el identificador '{id_reserva.strip()}'.",
                    contexto={"id_reserva": id_reserva},
                )

            try:
                cliente = self.buscar_cliente(id_cliente)
                servicio = self.buscar_servicio(id_servicio)
            except (DatosInvalidosError, ParametrosFaltantesError) as err_busqueda:
                # Encadena la excepción de búsqueda inexistente dentro de ReservaIncorrectaError.
                raise ReservaIncorrectaError(
                    f"No se pudo crear la reserva [{id_reserva}] por cliente o servicio inválido.",
                    contexto={
                        "id_reserva": id_reserva,
                        "id_cliente": id_cliente,
                        "id_servicio": id_servicio,
                    },
                ) from err_busqueda

            nueva_reserva = Reserva(
                id_entidad=id_reserva,
                cliente=cliente,
                servicio=servicio,
                duracion=duracion,
            )
        except SoftwareFJError as err:
            # Captura tanto fallos directos como excepciones encadenadas manteniendo estabilidad.
            self._registrar_error_resiliente("crear_reserva", err)
            return None
        except Exception as err_inesperado:
            self._logger.exception(
                "Fallo inesperado en 'crear_reserva': %s",
                err_inesperado,
            )
            return None
        else:
            self._reservas.append(nueva_reserva)
            self._logger.info(
                "Reserva [%s] registrada en memoria. Total reservas: %d.",
                nueva_reserva.id_entidad,
                len(self._reservas),
            )
            return nueva_reserva
        finally:
            self._logger.info("Fin de operación 'crear_reserva' para ID=%r.", id_reserva)

    def confirmar_reserva(self, id_reserva: str) -> bool:
        """Confirma una reserva existente manejando excepciones de disponibilidad o estado."""
        try:
            reserva = self.buscar_reserva(id_reserva)
            reserva.confirmar_reserva()
        except SoftwareFJError as err:
            self._registrar_error_resiliente("confirmar_reserva", err)
            return False
        except Exception as err_inesperado:
            self._logger.exception(
                "Fallo inesperado en 'confirmar_reserva': %s",
                err_inesperado,
            )
            return False
        else:
            return True
        finally:
            self._logger.info("Fin de operación 'confirmar_reserva' para ID=%r.", id_reserva)

    def procesar_reserva(
        self,
        id_reserva: str,
        tasa_impuesto: float = 0.19,
        porcentaje_descuento: float = 0.0,
        **cargos_extra: float,
    ) -> float | None:
        """Procesa el cobro de una reserva confirmada capturando errores encadenados."""
        try:
            reserva = self.buscar_reserva(id_reserva)
            total = reserva.procesar_reserva(
                tasa_impuesto=tasa_impuesto,
                porcentaje_descuento=porcentaje_descuento,
                **cargos_extra,
            )
        except SoftwareFJError as err:
            # Si ocurrió CalculoInconsistenteError dentro de Reserva, aquí se registra la causa raíz.
            self._registrar_error_resiliente("procesar_reserva", err)
            return None
        except Exception as err_inesperado:
            self._logger.exception(
                "Fallo inesperado en 'procesar_reserva': %s",
                err_inesperado,
            )
            return None
        else:
            return total
        finally:
            self._logger.info("Fin de operación 'procesar_reserva' para ID=%r.", id_reserva)

    def cancelar_reserva(self, id_reserva: str, motivo: str) -> bool:
        """Cancela una reserva usando try/except/else y bloque try/finally de cierre."""
        cancelada = False
        try:
            try:
                reserva = self.buscar_reserva(id_reserva)
                reserva.cancelar_reserva(motivo)
            except SoftwareFJError as err:
                self._registrar_error_resiliente("cancelar_reserva", err)
            except Exception as err_inesperado:
                self._logger.exception(
                    "Fallo inesperado en 'cancelar_reserva': %s",
                    err_inesperado,
                )
            else:
                cancelada = True
        finally:
            self._logger.info(
                "Fin de operación 'cancelar_reserva' para ID=%r (resultado=%s).",
                id_reserva,
                cancelada,
            )
        return cancelada

    def generar_reporte_estado(self) -> str:
        """Genera un reporte consolidado del estado en memoria usando try/finally."""
        try:
            conteo_estados = {estado: 0 for estado in Reserva.ESTADOS_VALIDOS}
            total_facturado = 0.0
            for reserva in self._reservas:
                conteo_estados[reserva.estado] = conteo_estados.get(reserva.estado, 0) + 1
                if reserva.estado == "PROCESADA":
                    total_facturado += reserva.costo_total

            lineas = [
                "=== REPORTE DE ESTADO ===",
                f"Clientes registrados : {len(self._clientes)}",
                f"Servicios en catálogo: {len(self._servicios)}",
                f"Reservas totales     : {len(self._reservas)}",
                (
                    "Desglose reservas    : "
                    f"PENDIENTE={conteo_estados['PENDIENTE']} | "
                    f"CONFIRMADA={conteo_estados['CONFIRMADA']} | "
                    f"PROCESADA={conteo_estados['PROCESADA']} | "
                    f"CANCELADA={conteo_estados['CANCELADA']}"
                ),
                f"Total facturado      : ${total_facturado:,.2f}",
                "",
                "--- Detalle de Clientes ---",
                *([c.mostrar_resumen() for c in self._clientes] or ["(Sin clientes)"]),
                "",
                "--- Catálogo de Servicios ---",
                *([s.describir_servicio() for s in self._servicios] or ["(Sin servicios)"]),
                "",
                "--- Detalle de Reservas ---",
                *([r.mostrar_resumen() for r in self._reservas] or ["(Sin reservas)"]),
            ]
            return "\n".join(lineas)
        finally:
            self._logger.info("Reporte consolidado de estado generado correctamente.")
