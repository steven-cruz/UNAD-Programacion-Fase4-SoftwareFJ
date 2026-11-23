# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

Aplicación desarrollada en Python bajo el paradigma de Programación Orientada a Objetos y manejo avanzado de excepciones para la Fase 4 del curso Programación 213023 de la Universidad Nacional Abierta y a Distancia, UNAD.

---

## Descripción del Proyecto

El sistema administra la operación de la empresa Software FJ, gestionando clientes, su catálogo de servicios y el ciclo de vida completo de cada reserva a través de los estados `PENDIENTE`, `CONFIRMADA`, `PROCESADA` y `CANCELADA`.

Cuenta con tres líneas de servicios especializadas:

1. **Reserva de salas**, implementada en `ServicioReservaSala`: cubre salas de juntas, laboratorios y auditorios con control de aforo máximo por tipo y recargos del 15 % por equipamiento multimedia y del 10 % para grupos de más de 30 personas.
2. **Alquiler de equipos**, implementado en `ServicioAlquilerEquipo`: gestiona equipos de categorías *Portátil Alto Rendimiento*, *Servidor*, *Kit Redes* y *Estación Gráfica*, controlando existencias por unidades con `verificar_stock`, `asignar_unidades` y `liberar_unidades`, además de un recargo del 12 % cuando requiere seguro obligatorio.
3. **Asesorías especializadas**, implementadas en `ServicioAsesoriaEspecializada`: diferencia el costo por área técnica, nivel del consultor —*Junior* con factor 1.0, *Senior* con 1.35 y *Arquitecto Experto* con 1.75— y modalidad remota o presencial con cargo logístico fijo.

Toda la información se administra en memoria mediante objetos y listas internas, sin motores de bases de datos. El acceso a disco se limita únicamente al registro de eventos y errores en `logs/software_fj.log`.

---

## Características Técnicas

- **Abstracción y herencia:** la jerarquía parte de la clase abstracta `EntidadSistema` y la clase base `Servicio`, de la cual derivan los tres servicios del catálogo.
- **Encapsulación y validaciones:** los atributos de `Cliente`, `Servicio`, `Reserva` y las listas en memoria de `SistemaSoftwareFJ` se protegen mediante propiedades `@property` y copias superficiales.
- **Polimorfismo y sobrecarga:** cada servicio sobrescribe `calcular_costo_base`, `describir_servicio` y `validar_parametros`; además, `calcular_costo` usa `@overload`, parámetros opcionales y `**cargos_extra` para soportar impuestos, descuentos y cargos adicionales.
- **Manejo de excepciones y logging:** define la jerarquía `SoftwareFJError` junto a `DatosInvalidosError`, `ParametrosFaltantesError`, `OperacionNoPermitidaError`, `ReservaIncorrectaError`, `ServicioNoDisponibleError` y `CalculoInconsistenteError`. Combina bloques `try/except`, `try/except/else`, `try/finally` y encadenamiento con `raise ... from ...` para registrar cada fallo con su causa raíz en `logs/software_fj.log` sin detener la ejecución.

---

## Simulaciones en `main.py`

Al ejecutar el archivo principal se corren de forma secuencial 12 simulaciones con casos válidos e inválidos:

| N.º | Tipo | Escenario validado |
| :-: | :--- | :--- |
| 1 | Válida | Registro de clientes corporativos, VIP, particulares e inactivos y alta de los 3 tipos de servicios. |
| 2 | Inválida | Rechazo de clientes con correo sin `@` o teléfono con caracteres inválidos vía `DatosInvalidosError`. |
| 3 | Inválida | Control de parámetros obligatorios vacíos o nulos con `ParametrosFaltantesError`. |
| 4 | Inválida | Bloqueo al crear servicios con capacidad negativa o tarifa base menor o igual a 0. |
| 5 | Válida | Ciclo completo de reserva de sala aplicando cálculo polimórfico y sobrecarga básica. |
| 6 | Válida | Alquiler de equipo con descuento de stock de 1 a 0, IVA, descuento VIP y cargo adicional. |
| 7 | Válida | Asesoría especializada presencial con factor *Senior*, cargo logístico, descuento e IVA. |
| 8 | Inválida | Intento de reserva sobre equipo sin stock y sala no disponible lanzando `ServicioNoDisponibleError`. |
| 9 | Inválida | Reserva con cliente inexistente mediante encadenamiento de excepciones, cliente inactivo y duración 0. |
| 10 | Inválida | Procesamiento fallido por descuento del 150 % e impuesto negativo con `CalculoInconsistenteError` encadenado y recuperación posterior de la reserva. |
| 11 | Inválida | Bloqueo de operaciones ilegales por estado, como cancelar una reserva procesada o procesar una pendiente, y rechazo de cliente duplicado. |
| 12 | Válida | Cancelación legítima de una reserva confirmada con restitución automática de inventario y reporte final en consola. |

---

## Estructura del Proyecto

```text
UNAD-Programacion-Fase4-SoftwareFJ/
├── main.py                        # Punto de entrada y ejecución de las 12 simulaciones
├── logs/
│   └── software_fj.log            # Registro automático de eventos, advertencias y errores
└── src/
    ├── utils/
    │   └── logger.py              # Configuración centralizada de logging en UTF-8
    ├── excepciones/
    │   └── errores_sistema.py     # Jerarquía de excepciones personalizadas de negocio
    ├── modelos/
    │   ├── entidad_base.py        # Clase abstracta general EntidadSistema
    │   ├── cliente.py             # Modelo Cliente con encapsulación y validaciones
    │   ├── servicio_base.py       # Clase abstracta Servicio y sobrecarga de costos
    │   ├── servicio_sala.py       # Servicio especializado de reserva de salas
    │   ├── servicio_equipo.py     # Servicio especializado de alquiler de equipos
    │   ├── servicio_asesoria.py   # Servicio especializado de asesorías
    │   └── reserva.py             # Modelo Reserva y máquina de estados
    └── gestion/
        └── gestor_fj.py           # Controlador SistemaSoftwareFJ en memoria
```

---

## Requisitos Previos

Para ejecutar el proyecto en cualquier máquina solo necesitas **Python 3.10 o superior**, ya que emplea únicamente la biblioteca estándar del lenguaje y no depende de paquetes externos ni motores de bases de datos.

Puedes confirmar tu versión de Python ejecutando:

```bash
python --version
```

---

## Instalación y Ejecución

1. Clona el repositorio y entra en la carpeta del proyecto:

   ```bash
   git clone https://github.com/steven-cruz/UNAD-Programacion-Fase4-SoftwareFJ.git
   cd UNAD-Programacion-Fase4-SoftwareFJ
   ```

2. Ejecuta el archivo principal para correr las 12 simulaciones:

   ```bash
   python main.py
   ```

3. Consulta la auditoría completa de eventos `INFO`, advertencias `WARNING` de cancelación y errores `ERROR` registrados en:

   ```text
   logs/software_fj.log
   ```
