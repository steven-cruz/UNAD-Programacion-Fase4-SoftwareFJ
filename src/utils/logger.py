"""Configuración centralizada del sistema de logging.

Provee la función ``obtener_logger`` para que todos los módulos registren
eventos operativos y trazas de error en el archivo ``logs/software_fj.log``
con codificación UTF-8 y sin duplicar handlers.
"""

import logging
from pathlib import Path

# Resuelve la raíz del proyecto subiendo dos niveles desde src/utils/logger.py.
RUTA_RAIZ = Path(__file__).resolve().parents[2]
RUTA_DIRECTORIO_LOGS = RUTA_RAIZ / "logs"
RUTA_ARCHIVO_LOG = RUTA_DIRECTORIO_LOGS / "software_fj.log"

# Formato uniforme para auditar fecha, severidad, módulo origen y mensaje.
FORMATO_LOG = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"


def obtener_logger(
    nombre_modulo: str = "SoftwareFJ",
    mostrar_en_consola: bool = False,
) -> logging.Logger:
    """Obtiene o inicializa un logger configurado hacia archivo (y opcionalmente consola).

    Args:
        nombre_modulo: Identificador del módulo o clase que origina el evento.
        mostrar_en_consola: Si es True, también imprime los registros en salida estándar.

    Returns:
        Instancia de ``logging.Logger`` lista para registrar eventos y errores.
    """
    # Garantiza que el directorio logs/ exista antes de abrir el FileHandler.
    RUTA_DIRECTORIO_LOGS.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(nombre_modulo)
    logger.setLevel(logging.DEBUG)
    # Evita que los mensajes suban al root logger y se impriman duplicados.
    logger.propagate = False

    # Configura los handlers una sola vez aunque se solicite el mismo logger varias veces.
    if not logger.handlers:
        formateador = logging.Formatter(FORMATO_LOG, datefmt=FORMATO_FECHA)

        # Persiste los eventos y excepciones en UTF-8 para preservar tildes y caracteres especiales.
        manejador_archivo = logging.FileHandler(
            RUTA_ARCHIVO_LOG,
            mode="a",
            encoding="utf-8",
        )
        manejador_archivo.setLevel(logging.INFO)
        manejador_archivo.setFormatter(formateador)
        logger.addHandler(manejador_archivo)

        if mostrar_en_consola:
            manejador_consola = logging.StreamHandler()
            manejador_consola.setLevel(logging.INFO)
            manejador_consola.setFormatter(formateador)
            logger.addHandler(manejador_consola)

    return logger
