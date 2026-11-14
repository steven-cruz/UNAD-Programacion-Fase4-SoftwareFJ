"""Jerarquía de excepciones personalizadas de negocio.

Define la excepción raíz y las excepciones especializadas
requeridas para capturar, identificar y encadenar fallos de validación, parámetros
faltantes, reglas de reserva, disponibilidad de servicios, operaciones ilegales
y cálculos inconsistentes sin detener la ejecución del sistema.
"""

from typing import Any

class SoftwareFJError(Exception):
    """Excepción base de dominio para todos los errores controlados.

    Encapsula un código identificador del error, un mensaje descriptivo y un
    contexto opcional con metadatos de diagnóstico. Es totalmente compatible con
    el encadenamiento nativo de Python.
    """

    # Código identificador por defecto; cada subclase sobrescribe este valor.
    CODIGO_POR_DEFECTO: str = "ERR_SISTEMA_FJ"

    def __init__(
        self,
        mensaje: str,
        codigo_error: str | None = None,
        contexto: dict[str, Any] | str | None = None,
    ) -> None:
        """Inicializa la excepción con mensaje, código identificador y contexto.

        Args:
            mensaje: Explicación clara del error ocurrido en la operación.
            codigo_error: Código estándar del error; si se omite, usa ``CODIGO_POR_DEFECTO``.
            contexto: Información adicional (ej. ID de entidad, campo o valor recibido).
        """
        self.mensaje = mensaje
        # Selecciona el código específico de la subclase cuando no se provee uno manual.
        self.codigo_error = codigo_error or self.CODIGO_POR_DEFECTO
        self.contexto = contexto
        # Propaga el mensaje ya formateado hacia Exception para trazas y logs uniformes.
        super().__init__(self.formatear_mensaje())

    def formatear_mensaje(self) -> str:
        """Construye la cadena formateada del error con su código y contexto opcional.

        Returns:
            Cadena con el formato ``[CODIGO] mensaje`` y ``(Contexto: ...)`` si aplica.
        """
        base = f"[{self.codigo_error}] {self.mensaje}"
        # Adjunta el contexto solo cuando aporta datos útiles de diagnóstico.
        if self.contexto is not None and self.contexto != "" and self.contexto != {}:
            return f"{base} (Contexto: {self.contexto})"
        return base

    def __str__(self) -> str:
        """Devuelve la representación legible de la excepción para consola y logs."""
        return self.formatear_mensaje()


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando un dato tiene tipo incorrecto, formato inválido o valor fuera de rango.

    Escenarios de negocio: correo electrónico sin formato válido, teléfono con
    caracteres no permitidos, categoría de cliente desconocida o capacidades negativas.
    """

    CODIGO_POR_DEFECTO: str = "ERR_DATOS_INVALIDOS"


class ParametrosFaltantesError(SoftwareFJError):
    """Se lanza cuando un parámetro o atributo obligatorio es ``None`` o cadena vacía.

    Escenarios de negocio: intento de registrar un cliente sin nombre o documento,
    crear un servicio sin código identificador o enviar un motivo de cancelación vacío.
    """

    CODIGO_POR_DEFECTO: str = "ERR_PARAMETROS_FALTANTES"


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza ante acciones prohibidas por las reglas de negocio o ciclo de estados.

    Escenarios de negocio: registrar un ID duplicado, confirmar una reserva cancelada,
    procesar una reserva sin confirmación previa o cancelar una reserva ya procesada.
    """

    CODIGO_POR_DEFECTO: str = "ERR_OPERACION_NO_PERMITIDA"


class ReservaIncorrectaError(SoftwareFJError):
    """Se lanza cuando una reserva incumple condiciones estructurales o de vigencia.

    Escenarios de negocio: duración menor o igual a cero, cliente inactivo o
    fallo propagado mediante encadenamiento al crear o procesar la reserva.
    """

    CODIGO_POR_DEFECTO: str = "ERR_RESERVA_INCORRECTA"


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando el servicio solicitado no está habilitado o no tiene stock.

    Escenarios de negocio: sala marcada como inactiva/ocupada, inventario en cero
    en alquiler de equipos o asesoría técnica sin disponibilidad vigente.
    """

    CODIGO_POR_DEFECTO: str = "ERR_SERVICIO_NO_DISPONIBLE"


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza ante inconsistencias aritméticas o financieras en el cálculo de costos.

    Escenarios de negocio: descuentos superiores al 100%, tasas de impuesto negativas,
    tarifas base corruptas o costo total resultante menor que cero.
    """

    CODIGO_POR_DEFECTO: str = "ERR_CALCULO_INCONSISTENTE"
