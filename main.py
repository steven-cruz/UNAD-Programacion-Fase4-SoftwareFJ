"""Punto de entrada principal del Sistema Integral.

Ejecuta una batería secuencial de 12 simulaciones completas (casos válidos e
inválidos) sobre clientes, servicios especializados y reservas, demostrando la
aplicación práctica de abstracción, herencia, polimorfismo, sobrecarga,
encapsulación y manejo avanzado de excepciones sin uso de bases de datos.
"""

import logging
from typing import Any

from src.excepciones import SoftwareFJError
from src.gestion import SistemaSoftwareFJ
from src.modelos import (
    Servicio,
    ServicioAlquilerEquipo,
    ServicioAsesoriaEspecializada,
    ServicioReservaSala,
)
from src.utils import RUTA_ARCHIVO_LOG, RUTA_DIRECTORIO_LOGS, obtener_logger


def _formatear_total(monto: float | None) -> str:
    """Formatea de forma segura el total calculado evitando fallos si es None."""
    return f"${monto:,.2f}" if monto is not None else "No procesada"


def _imprimir_encabezado(
    logger: logging.Logger,
    numero: int,
    titulo: str,
    tipo: str,
) -> None:
    """Imprime un separador visual en consola y deja traza de inicio en el log."""
    separador = "=" * 72
    encabezado = f"SIMULACIÓN {numero:02d} [{tipo.upper()}] - {titulo}"
    print(f"\n{separador}\n{encabezado}\n{separador}")
    logger.info(">>> INICIO %s", encabezado)


def _crear_y_registrar_servicio(
    sistema: SistemaSoftwareFJ,
    logger: logging.Logger,
    clase_servicio: type[Servicio],
    *args: Any,
    **kwargs: Any,
) -> Servicio | None:
    """Instancia y registra un servicio absorbiendo errores de construcción.

    Implementa ``try / except / else / finally`` para demostrar que incluso
    cuando falla la creación directa de un servicio con parámetros erróneos,
    el error se audita en ``logs/software_fj.log`` y la aplicación continúa.
    """
    servicio: Servicio | None = None
    try:
        servicio = clase_servicio(*args, **kwargs)
    except SoftwareFJError as err:
        # Registra el fallo de instanciación sin interrumpir el flujo principal.
        logger.error("Error controlado al instanciar %s: %s", clase_servicio.__name__, err)
        print(f"  [Error controlado al crear servicio]: {err}")
        return None
    else:
        return sistema.registrar_servicio(servicio)
    finally:
        logger.info("Finalizó intento de creación de %s.", clase_servicio.__name__)


def ejecutar_simulaciones() -> SistemaSoftwareFJ:
    """Ejecuta las 12 simulaciones completas del sistema"""
    # Reinicia el archivo de logs antes de la corrida para registrar evidencia limpia.
    RUTA_DIRECTORIO_LOGS.mkdir(parents=True, exist_ok=True)
    RUTA_ARCHIVO_LOG.write_text("", encoding="utf-8")

    logger = obtener_logger("SimuladorSoftwareFJ")
    sistema = SistemaSoftwareFJ()

    # ------------------------------------------------------------------
    # SIMULACIÓN 1 (VÁLIDA): Alta de clientes y catálogo de 3 servicios
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        1,
        "Registro válido de clientes y catálogo de los 3 tipos de servicios",
        "Válida",
    )
    sistema.registrar_cliente("CLI-001", "TechSolutions S.A.S.", "proyectos@techsolutions.co", "310-555-0101", "Corporativo")
    sistema.registrar_cliente("CLI-002", "Mariana Restrepo", "mariana.restrepo@vipmail.com", "3004448899", "VIP")
    sistema.registrar_cliente("CLI-003", "Andrés Felipe Gómez", "andres.gomez@correo.co", "3157772211", "Particular")
    # Cliente inactivo usado posteriormente en Simulación 9 para validar rechazo de reservas.
    sistema.registrar_cliente("CLI-004", "Cliente Suspendido", "suspendido@correo.co", "3120001122", "Particular", activo=False)

    _crear_y_registrar_servicio(sistema, logger, ServicioReservaSala, "SALA-01", "Auditorio Innovación FJ", 180000.0, 80, "Auditorio", True)
    _crear_y_registrar_servicio(sistema, logger, ServicioReservaSala, "SALA-02", "Sala Juntas Mantenimiento", 95000.0, 10, "Juntas", False, disponible=False)
    _crear_y_registrar_servicio(sistema, logger, ServicioAlquilerEquipo, "EQ-01", "Servidor GPU NVIDIA H100", 150000.0, "Servidor", cantidad_disponible=1, requiere_seguro=True)
    _crear_y_registrar_servicio(sistema, logger, ServicioAlquilerEquipo, "EQ-02", "Kit Redes Empresarial Cisco", 70000.0, "Kit Redes", cantidad_disponible=2, requiere_seguro=False)
    _crear_y_registrar_servicio(sistema, logger, ServicioAsesoriaEspecializada, "ASE-01", "Consultoría Arquitectura Cloud", 140000.0, "Arquitectura Cloud", nivel_consultor="Senior", modalidad="Presencial")
    _crear_y_registrar_servicio(sistema, logger, ServicioAsesoriaEspecializada, "ASE-02", "Auditoría Ciberseguridad Zero-Trust", 160000.0, "Ciberseguridad", nivel_consultor="Arquitecto Experto", modalidad="Remota")
    print(f"  Clientes activos en memoria : {len(sistema.clientes)}")
    print(f"  Servicios activos en catálogo: {len(sistema.servicios)}")

    # ------------------------------------------------------------------
    # SIMULACIÓN 2 (INVÁLIDA): Datos erróneos al registrar clientes
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        2,
        "Intento de registro de clientes con correo y teléfono inválidos",
        "Inválida",
    )
    res_cli_mail = sistema.registrar_cliente("CLI-ERR1", "Pedro Pérez", "correo-sin-arroba.com", "3001234567")
    res_cli_tel = sistema.registrar_cliente("CLI-ERR2", "Lucía Díaz", "lucia@mail.com", "300ABC45")
    print(f"  Resultado correo inválido   : {res_cli_mail} (error capturado en log)")
    print(f"  Resultado teléfono inválido : {res_cli_tel} (error capturado en log)")

    # ------------------------------------------------------------------
    # SIMULACIÓN 3 (INVÁLIDA): Parámetros faltantes en clientes/servicios
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        3,
        "Intento de registro con parámetros obligatorios vacíos o nulos",
        "Inválida",
    )
    sistema.registrar_cliente("", "Nombre Válido", "valido@mail.com", "3001234567")
    sistema.registrar_cliente("CLI-ERR3", None, "valido@mail.com", "3001234567")  # type: ignore[arg-type]
    _crear_y_registrar_servicio(sistema, logger, ServicioAsesoriaEspecializada, "ASE-ERR1", "Asesoría Sin Área", 100000.0, "", "Senior", "Remota")
    print("  Parámetros faltantes capturados y registrados sin detener la ejecución.")

    # ------------------------------------------------------------------
    # SIMULACIÓN 4 (INVÁLIDA): Creación incorrecta de servicios
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        4,
        "Creación incorrecta de servicios (capacidad negativa y tarifa <= 0)",
        "Inválida",
    )
    _crear_y_registrar_servicio(sistema, logger, ServicioReservaSala, "SALA-ERR1", "Sala Aforo Negativo", 80000.0, -10, "Juntas", False)
    _crear_y_registrar_servicio(sistema, logger, ServicioAlquilerEquipo, "EQ-ERR1", "Equipo Tarifa Cero", 0.0, "Portátil Alto Rendimiento", 3)

    # ------------------------------------------------------------------
    # SIMULACIÓN 5 (VÁLIDA): Reserva de Sala y sobrecarga básica
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        5,
        "Reserva de Sala (cálculo polimórfico y sobrecarga simple)",
        "Válida",
    )
    sistema.crear_reserva("RES-001", "CLI-001", "SALA-01", 3.0)
    sistema.confirmar_reserva("RES-001")
    total_res_1 = sistema.procesar_reserva("RES-001", tasa_impuesto=0.0, porcentaje_descuento=0.0)
    print(f"  Reserva [RES-001] procesada correctamente. Total: {_formatear_total(total_res_1)}")

    # ------------------------------------------------------------------
    # SIMULACIÓN 6 (VÁLIDA): Alquiler de Equipo y sobrecarga completa
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        6,
        "Alquiler de Equipo (sobrecarga con IVA, descuento VIP y cargo extra)",
        "Válida",
    )
    sistema.crear_reserva("RES-002", "CLI-002", "EQ-01", 4.0)
    sistema.confirmar_reserva("RES-002")
    total_res_2 = sistema.procesar_reserva(
        "RES-002",
        tasa_impuesto=0.19,
        porcentaje_descuento=0.10,
        instalacion=35000.0,
    )
    print(f"  Reserva [RES-002] procesada correctamente. Total: {_formatear_total(total_res_2)}")

    # ------------------------------------------------------------------
    # SIMULACIÓN 7 (VÁLIDA): Asesoría Especializada presencial
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        7,
        "Asesoría Especializada presencial (factor Senior + cargo logístico)",
        "Válida",
    )
    sistema.crear_reserva("RES-003", "CLI-001", "ASE-01", 5.0)
    sistema.confirmar_reserva("RES-003")
    total_res_3 = sistema.procesar_reserva("RES-003", tasa_impuesto=0.19, porcentaje_descuento=0.05)
    print(f"  Reserva [RES-003] procesada correctamente. Total: {_formatear_total(total_res_3)}")

    # ------------------------------------------------------------------
    # SIMULACIÓN 8 (INVÁLIDA): Servicios no disponibles / sin stock
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        8,
        "Intento de reserva sobre equipo sin stock y sala no disponible",
        "Inválida",
    )
    res_eq_agotado = sistema.crear_reserva("RES-ERR-EQ", "CLI-003", "EQ-01", 2.0)
    res_sala_inactiva = sistema.crear_reserva("RES-ERR-SAL", "CLI-003", "SALA-02", 2.0)
    print(f"  Reserva equipo sin stock    : {res_eq_agotado} (ServicioNoDisponibleError)")
    print(f"  Reserva sala no disponible  : {res_sala_inactiva} (ServicioNoDisponibleError)")

    # ------------------------------------------------------------------
    # SIMULACIÓN 9 (INVÁLIDA): Reserva incorrecta y encadenamiento
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        9,
        "Reserva con cliente inexistente (encadenamiento), cliente inactivo y duración 0",
        "Inválida",
    )
    # Demuestra encadenamiento explícito: DatosInvalidosError -> ReservaIncorrectaError.
    sistema.crear_reserva("RES-ERR-CLI", "CLI-999", "SALA-01", 2.0)
    sistema.crear_reserva("RES-ERR-INA", "CLI-004", "SALA-01", 2.0)
    sistema.crear_reserva("RES-ERR-DUR", "CLI-003", "SALA-01", 0.0)
    print("  Errores de reserva y encadenamiento (__cause__) registrados en el log.")

    # ------------------------------------------------------------------
    # SIMULACIÓN 10 (INVÁLIDA): Cálculos inconsistentes con encadenamiento
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        10,
        "Procesamiento con descuento > 100% e impuesto negativo (encadenamiento)",
        "Inválida",
    )
    sistema.crear_reserva("RES-004", "CLI-003", "ASE-02", 2.0)
    sistema.confirmar_reserva("RES-004")
    # Fallos controlados que encadenan CalculoInconsistenteError dentro de ReservaIncorrectaError.
    fallo_desc = sistema.procesar_reserva("RES-004", tasa_impuesto=0.19, porcentaje_descuento=150.0)
    fallo_imp = sistema.procesar_reserva("RES-004", tasa_impuesto=-0.19, porcentaje_descuento=0.0)
    print(f"  Procesamiento descuento 150%: {fallo_desc} (CalculoInconsistenteError encadenado)")
    print(f"  Procesamiento impuesto -19% : {fallo_imp} (CalculoInconsistenteError encadenado)")
    # Tras los fallos controlados, la reserva sigue CONFIRMADA y puede procesarse bien.
    total_res_4 = sistema.procesar_reserva("RES-004", tasa_impuesto=0.19, porcentaje_descuento=0.0)
    print(f"  Recuperación exitosa [RES-004] -> Total válido: {_formatear_total(total_res_4)}")

    # ------------------------------------------------------------------
    # SIMULACIÓN 11 (INVÁLIDA): Operaciones no permitidas y duplicados
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        11,
        "Operaciones ilegales por estado (cancelar procesada, procesar pendiente, duplicados)",
        "Inválida",
    )
    cancel_ilegal = sistema.cancelar_reserva("RES-001", "Intento sobre reserva ya procesada")
    sistema.crear_reserva("RES-005", "CLI-003", "EQ-02", 2.0)
    proc_sin_confirmar = sistema.procesar_reserva("RES-005")
    cli_duplicado = sistema.registrar_cliente("CLI-001", "Duplicado", "dup@mail.com", "3001112233")
    print(f"  Cancelar reserva PROCESADA  : {cancel_ilegal} (OperacionNoPermitidaError)")
    print(f"  Procesar sin confirmar      : {proc_sin_confirmar} (OperacionNoPermitidaError)")
    print(f"  Cliente duplicado [CLI-001] : {cli_duplicado} (OperacionNoPermitidaError)")

    # ------------------------------------------------------------------
    # SIMULACIÓN 12 (VÁLIDA): Cancelación legítima y reporte final
    # ------------------------------------------------------------------
    _imprimir_encabezado(
        logger,
        12,
        "Confirmación y cancelación válida con restitución de stock y reporte final",
        "Válida",
    )
    sistema.confirmar_reserva("RES-005")
    cancelada_ok = sistema.cancelar_reserva("RES-005", "Reprogramación de mantenimiento de red")
    print(f"  Cancelación válida [RES-005]: {cancelada_ok}")
    print("\n" + sistema.generar_reporte_estado())
    print(f"\nArchivo de logs generado en: {RUTA_ARCHIVO_LOG}")

    return sistema


if __name__ == "__main__":
    ejecutar_simulaciones()
    logging.shutdown()
