# UNAD - PROGRAMACIÓN FASE 4
# DESARROLLO DEL SISTEMA SOFTWAREFJ

## 1. Presentación del proyecto

El presente proyecto corresponde al desarrollo de un sistema de gestión llamado SoftwareFJ, realizado como parte de las actividades académicas de la Fase 4 del curso de programación de la Universidad Nacional Abierta y a Distancia (UNAD).

La idea principal de este trabajo es desarrollar una aplicación que permita administrar clientes, servicios y reservas de una manera organizada, utilizando el lenguaje de programación Python. Durante su elaboración se tuvieron en cuenta los conocimientos adquiridos en las actividades anteriores, buscando aplicarlos en un programa que permita realizar diferentes operaciones y resolver situaciones que se pueden presentar durante su funcionamiento.

A lo largo del desarrollo se trabajaron diferentes clases y métodos para representar los elementos principales del sistema. También se implementaron validaciones para evitar que se ingresen datos incorrectos y excepciones personalizadas para controlar los errores que puedan aparecer.

Además de la programación, se tiene en cuenta la importancia de organizar el trabajo mediante herramientas como Git y GitHub. Estas herramientas permiten guardar los avances, realizar cambios sin afectar directamente la versión principal y mantener un historial de las actividades desarrolladas.

## 2. ¿En qué consiste SoftwareFJ?

SoftwareFJ es un sistema que permite gestionar diferentes servicios que pueden ser solicitados por los clientes. Su funcionamiento se basa en registrar la información de los usuarios, administrar los servicios disponibles y controlar las reservas que se realizan.

El programa cuenta con tres tipos principales de servicios: reserva de salas, alquiler de equipos y asesorías especializadas. Cada uno tiene características diferentes y por esta razón sus operaciones y cálculos se realizan teniendo en cuenta sus propias condiciones.

Por ejemplo, cuando se realiza una reserva de una sala, el sistema debe tener en cuenta la duración y el valor correspondiente. En el caso del alquiler de equipos, también se debe revisar que exista disponibilidad. Para las asesorías se deben considerar las condiciones del servicio contratado.

Otra parte importante del sistema es el manejo de situaciones incorrectas. El programa valida los datos antes de realizar determinadas operaciones, evitando que se registren clientes con información incompleta o que se generen reservas que no cumplan las condiciones establecidas.

El sistema se ejecuta desde el archivo principal `main.py`, en el cual se encuentran diferentes simulaciones que permiten observar cómo funcionan las operaciones y cómo responde el programa ante situaciones válidas e inválidas.

## 3. Justificación

El desarrollo de este proyecto permite poner en práctica los conocimientos de programación mediante la creación de una aplicación que reúne diferentes funcionalidades en un solo sistema.

En muchas aplicaciones es necesario manejar información de usuarios, productos, servicios y operaciones. Por esta razón es importante aprender a organizar el código, separar las responsabilidades y crear métodos que permitan realizar cada tarea de manera ordenada.

Con SoftwareFJ se busca demostrar que mediante Python es posible construir un sistema que permita administrar diferentes procesos, validar información y controlar errores.

También es importante utilizar herramientas de control de versiones, porque durante el desarrollo de un programa pueden realizarse muchos cambios. Git y GitHub permiten guardar esos avances y mantener una organización que facilita el trabajo individual y colaborativo.

## 4. Objetivo general

Desarrollar un sistema de gestión en Python que permita administrar clientes, servicios y reservas, aplicando los conceptos de programación orientada a objetos, validación de datos, manejo de excepciones y control de versiones mediante Git y GitHub.

## 5. Objetivos específicos

- Crear una estructura organizada para desarrollar el sistema.
- Diseñar clases que permitan representar los clientes, servicios y reservas.
- Implementar diferentes tipos de servicios con sus respectivas características.
- Desarrollar funcionalidades para registrar y administrar clientes.
- Permitir la creación, confirmación, procesamiento y cancelación de reservas.
- Controlar la disponibilidad de los servicios y los equipos.
- Realizar cálculos relacionados con tarifas, impuestos, descuentos y cargos adicionales.
- Validar la información ingresada para evitar errores.
- Implementar excepciones personalizadas para controlar situaciones incorrectas.
- Registrar los eventos del sistema mediante archivos de log.
- Aplicar los principios de programación orientada a objetos.
- Organizar los cambios del proyecto utilizando ramas, commits y Pull Requests.
- Mantener una documentación que facilite la comprensión y ejecución del programa.

## 6. Descripción de las funcionalidades

El sistema está compuesto por diferentes funcionalidades que trabajan en conjunto para permitir la administración de los servicios.

### 6.1. Registro y administración de clientes

Una de las primeras partes del sistema es la gestión de clientes. Esta funcionalidad permite registrar la información necesaria para identificar a las personas que utilizan los servicios.

También se realizan validaciones para comprobar que los datos ingresados cumplan con las condiciones establecidas.

Entre las actividades relacionadas con esta funcionalidad se encuentran:

- Registrar nuevos clientes.
- Guardar la información de cada cliente.
- Consultar los clientes registrados.
- Validar los datos de contacto.
- Comprobar que los datos obligatorios estén completos.
- Controlar el estado de los clientes.
- Evitar que se realicen operaciones con clientes que no cumplan las condiciones.

### 6.2. Administración de los servicios

El sistema permite trabajar con diferentes servicios. Cada uno tiene sus propias características y se administra mediante una clase específica.

Los servicios implementados son los siguientes:

**Servicio de reserva de salas**

Permite gestionar la reserva de espacios. Para realizar esta operación se tienen en cuenta las condiciones del servicio y la duración de la reserva, con el fin de calcular el valor correspondiente.

**Servicio de alquiler de equipos**

Permite administrar el alquiler de equipos. En este caso es importante revisar la disponibilidad y controlar que no se realicen reservas cuando no existan unidades suficientes.

**Servicio de asesorías especializadas**

Permite gestionar servicios de asesoría. Esta funcionalidad cuenta con sus propias condiciones y permite realizar los cálculos correspondientes según el servicio solicitado.

### 6.3. Creación y administración de reservas

La gestión de reservas es una de las partes principales del sistema, porque permite relacionar a los clientes con los servicios disponibles.

El programa permite crear reservas y verificar que los datos necesarios sean correctos antes de continuar con el proceso.

Las operaciones relacionadas con las reservas incluyen:

- Crear una nueva reserva.
- Asociar una reserva con un cliente.
- Seleccionar el servicio correspondiente.
- Comprobar que el cliente exista.
- Revisar que el cliente se encuentre activo.
- Validar la duración de la reserva.
- Confirmar las reservas.
- Procesar las operaciones.
- Cancelar reservas.
- Recuperar la disponibilidad cuando se cancela una reserva, según corresponda.

### 6.4. Cálculo de costos

El programa realiza diferentes operaciones matemáticas para determinar el valor de los servicios.

Estos cálculos permiten tener en cuenta las tarifas establecidas y las condiciones de cada operación.

Entre los elementos que se consideran están:

- Valor de cada servicio.
- Duración de las reservas.
- Impuestos.
- Descuentos.
- Beneficios para clientes VIP.
- Cargos adicionales.
- Valor total de la operación.

También se realizan controles para evitar resultados incorrectos, como descuentos superiores al porcentaje permitido o valores de impuestos negativos.

### 6.5. Control de disponibilidad

Otra funcionalidad importante es comprobar que los servicios y equipos se encuentren disponibles antes de realizar una reserva.

Esto permite evitar que se asignen recursos que no se encuentran disponibles y ayuda a mantener un mejor control de las operaciones.

### 6.6. Validación de datos

Durante el funcionamiento del sistema se realizan comprobaciones para evitar que se utilice información incorrecta.

Algunos de los casos que se tienen en cuenta son:

- Correos electrónicos con formatos incorrectos.
- Números de teléfono inválidos.
- Información obligatoria sin completar.
- Parámetros faltantes.
- Valores nulos o vacíos.
- Capacidades negativas.
- Tarifas que no cumplen las condiciones.
- Duraciones de reserva iguales a cero.
- Clientes inexistentes o inactivos.
- Operaciones duplicadas.

### 6.7. Manejo de errores y excepciones

El sistema utiliza excepciones personalizadas para identificar diferentes problemas que pueden aparecer durante la ejecución.

De esta manera, cuando una operación no cumple las condiciones necesarias, el programa puede generar una respuesta que permita reconocer el problema y evitar que continúe una operación incorrecta.

### 6.8. Registro de actividades

El proyecto cuenta con un sistema de registro de eventos que permite guardar información sobre las operaciones realizadas.

Estos registros se almacenan en el archivo:

`logs/software_fj.log`

Esta funcionalidad resulta útil cuando se necesita revisar lo que ocurrió durante la ejecución del programa o identificar posibles errores.

## 7. Organización del código y programación orientada a objetos

Para desarrollar el sistema se utilizaron diferentes clases que permiten representar los elementos principales de la aplicación.

La programación orientada a objetos facilita la organización del código, porque permite separar las responsabilidades y trabajar con estructuras que representan situaciones del sistema.

### 7.1. Clases y objetos

Las clases sirven como una estructura para definir las características y comportamientos de los elementos del programa.

En SoftwareFJ se utilizan clases para representar clientes, reservas, servicios y el sistema encargado de administrar las operaciones.

Los objetos son creados a partir de esas clases y permiten trabajar con la información de cada elemento.

### 7.2. Encapsulamiento

Este concepto permite organizar la información dentro de las clases y controlar la manera en que se accede o modifica.

Su aplicación ayuda a mantener el código más organizado y evita que los datos se manejen sin tener en cuenta las condiciones establecidas.

### 7.3. Herencia

La herencia permite crear clases que aprovechan las características y métodos definidos en otras clases.

En el proyecto se utiliza para organizar los diferentes tipos de servicios, compartiendo características comunes y permitiendo que cada uno tenga sus propios comportamientos.

### 7.4. Abstracción

La abstracción permite definir elementos generales que representan características comunes de otros objetos.

En el sistema se utiliza para establecer estructuras base que sirven como referencia para las clases que representan los servicios y otras entidades.

### 7.5. Polimorfismo

El polimorfismo permite que diferentes clases utilicen métodos con el mismo nombre, pero que cada una realice una operación de acuerdo con sus características.

Esto se puede observar en los diferentes tipos de servicios, ya que cada uno puede realizar sus propios cálculos y comportamientos.

### 7.6. Excepciones personalizadas

Se crearon clases de excepciones para representar los diferentes errores que pueden aparecer en el sistema.

Esto permite identificar mejor los problemas y mantener un control más organizado de las operaciones.

## 8. Estructura general del proyecto

El proyecto se encuentra dividido en carpetas y archivos para que cada parte tenga una función determinada.

Esta organización permite encontrar más fácilmente el código, realizar modificaciones y mantener el programa de una manera ordenada.

```text
UNAD-Programacion-Fase4-SoftwareFJ/
│
├── .gitignore
├── README.md
├── main.py
│
├── logs/
│   ├── .gitkeep
│   └── software_fj.log
│
└── src/
    ├── __init__.py
    │
    ├── excepciones/
    │   ├── __init__.py
    │   └── errores_sistema.py
    │
    ├── gestion/
    │   ├── __init__.py
    │   └── gestor_fj.py
    │
    ├── modelos/
    │   ├── __init__.py
    │   ├── cliente.py
    │   ├── entidad_base.py
    │   ├── reserva.py
    │   ├── servicio_asesoria.py
    │   ├── servicio_base.py
    │   ├── servicio_equipo.py
    │   └── servicio_sala.py
    │
    └── utils/
        ├── __init__.py
        └── logger.py
```

## 9. Descripción detallada de los archivos y carpetas

### 9.1. Archivo .gitignore

Este archivo permite indicar cuáles archivos o carpetas no deben incluirse en el control de versiones de Git.

Su función es ayudar a mantener el repositorio organizado y evitar que se suban archivos que no son necesarios para compartir el código fuente.

### 9.2. Archivo README.md

Es el documento principal de presentación del proyecto.

Aquí se explica en qué consiste SoftwareFJ, cuáles son sus funcionalidades, cómo está organizado el código y qué pasos se deben seguir para ejecutar el programa.

También permite documentar el trabajo realizado con Git y GitHub.

### 9.3. Archivo main.py

Es el archivo principal del proyecto y desde él se inicia la ejecución del programa.

Contiene las simulaciones que permiten probar las diferentes funcionalidades del sistema. En este archivo se pueden observar operaciones relacionadas con clientes, servicios, reservas, cálculos y manejo de errores.

Las simulaciones permiten comprobar cómo responde el sistema ante diferentes situaciones.

### 9.4. Carpeta logs

Esta carpeta se utiliza para almacenar los registros generados durante la ejecución del programa.

Contiene dos archivos:

- `.gitkeep`: permite mantener la carpeta dentro del repositorio cuando no tiene otros archivos que deban conservarse.
- `software_fj.log`: almacena los eventos registrados durante el funcionamiento del sistema.

### 9.5. Carpeta src

Esta carpeta contiene los módulos principales del proyecto.

Su propósito es separar el código según las responsabilidades de cada parte del sistema. De esta manera, no es necesario tener todas las clases y funciones dentro de un solo archivo.

Dentro de esta carpeta se encuentran las siguientes secciones:

### 9.6. Carpeta excepciones

Contiene las clases utilizadas para representar los errores personalizados del sistema.

**Archivo `__init__.py`**

Permite identificar la carpeta como un paquete de Python y organizar sus importaciones.

**Archivo `errores_sistema.py`**

Contiene las excepciones personalizadas que utiliza el programa para controlar las situaciones incorrectas.

Entre ellas se encuentran:

- `SoftwareFJError`: excepción base del sistema.
- `DatosInvalidosError`: se utiliza cuando la información ingresada no cumple las condiciones.
- `ParametrosFaltantesError`: permite identificar cuando faltan datos necesarios.
- `OperacionNoPermitidaError`: representa operaciones que no se pueden realizar.
- `ReservaIncorrectaError`: se utiliza cuando una reserva no cumple las condiciones.
- `ServicioNoDisponibleError`: permite identificar servicios que no están disponibles.
- `CalculoInconsistenteError`: permite controlar cálculos que producen resultados incorrectos.

### 9.7. Carpeta gestion

Contiene la parte encargada de administrar las operaciones principales del sistema.

**Archivo `__init__.py`**

Permite organizar el paquete de gestión.

**Archivo `gestor_fj.py`**

Contiene la lógica de administración del sistema. Se encarga de trabajar con los clientes, servicios y reservas, centralizando las operaciones necesarias para el funcionamiento de SoftwareFJ.

### 9.8. Carpeta modelos

Esta carpeta contiene las clases que representan los elementos principales de la aplicación.

Cada archivo se encarga de una parte específica del sistema.

**Archivo `__init__.py`**

Permite organizar los modelos como un paquete de Python.

**Archivo `cliente.py`**

Contiene la clase encargada de representar a los clientes y manejar sus características y datos.

**Archivo `entidad_base.py`**

Contiene la estructura base de las entidades del sistema, permitiendo compartir características comunes.

**Archivo `reserva.py`**

Representa las reservas y permite manejar la información relacionada con las operaciones realizadas por los clientes.

**Archivo `servicio_base.py`**

Contiene la estructura general de los servicios y sirve como base para los diferentes tipos de servicios disponibles.

**Archivo `servicio_asesoria.py`**

Contiene la clase que representa el servicio de asesorías especializadas.

**Archivo `servicio_equipo.py`**

Contiene la clase relacionada con el alquiler de equipos y sus características.

**Archivo `servicio_sala.py`**

Contiene la clase encargada de representar los servicios de reserva de salas.

### 9.9. Carpeta utils

Contiene herramientas de apoyo que pueden utilizarse en diferentes partes del programa.

**Archivo `__init__.py`**

Permite organizar las herramientas como un paquete.

**Archivo `logger.py`**

Contiene las funciones relacionadas con el registro de eventos del sistema. Permite guardar información sobre la ejecución del programa en los archivos de log.

## 10. Simulaciones y pruebas de funcionamiento

Para comprobar el funcionamiento del sistema se incluyeron doce simulaciones dentro del archivo principal.

Estas simulaciones permiten observar cómo responde el programa ante operaciones correctas y situaciones en las que debe controlar algún error.

| N.º | Simulación | Qué se comprueba |
|---|---|---|
| 1 | Registro inicial | Registro de clientes y creación del catálogo de servicios. |
| 2 | Datos de contacto | Validación de correos y teléfonos. |
| 3 | Parámetros | Control de valores faltantes, vacíos o nulos. |
| 4 | Creación de servicios | Validación de capacidades y tarifas. |
| 5 | Reserva de salas | Creación de reservas y cálculo de costos. |
| 6 | Alquiler de equipos | Impuestos, descuentos VIP y cargos adicionales. |
| 7 | Asesorías | Funcionamiento del servicio de asesoría. |
| 8 | Disponibilidad | Control de servicios sin disponibilidad o equipos sin stock. |
| 9 | Reservas incorrectas | Validación de clientes y duración de las reservas. |
| 10 | Cálculos | Control de descuentos e impuestos inconsistentes. |
| 11 | Operaciones | Control de duplicados y operaciones no permitidas. |
| 12 | Cancelaciones | Cancelación de reservas y restitución de disponibilidad. |

Estas pruebas permiten revisar diferentes partes del sistema y comprobar que los controles implementados respondan de manera adecuada.

## 11. Herramientas utilizadas

Para realizar el proyecto se utilizaron diferentes herramientas que facilitaron el desarrollo y la organización del trabajo.

| Herramienta | Utilidad |
|---|---|
| Python | Lenguaje de programación utilizado para construir el sistema. |
| Visual Studio Code | Editor utilizado para escribir, modificar y ejecutar el código. |
| Git | Herramienta que permite guardar y controlar las versiones del proyecto. |
| GitHub | Plataforma utilizada para alojar el repositorio y organizar el trabajo colaborativo. |
| Markdown | Formato utilizado para escribir la documentación del proyecto. |

## 12. Instalación y ejecución

Para ejecutar SoftwareFJ en un equipo se deben realizar los siguientes pasos.

### Paso 1. Descargar el repositorio

Primero se debe ingresar al repositorio de GitHub y copiar su dirección.

Después se puede utilizar el siguiente comando:

```bash
git clone URL_DEL_REPOSITORIO
```

Se debe cambiar `URL_DEL_REPOSITORIO` por la dirección real del repositorio.

### Paso 2. Abrir la carpeta

Una vez descargado el proyecto, se debe abrir la carpeta principal desde Visual Studio Code.

### Paso 3. Abrir la terminal

En Visual Studio Code se debe ingresar al menú Terminal y seleccionar Nueva terminal.

### Paso 4. Comprobar Python

Para verificar que Python está instalado se utiliza:

```bash
python --version
```

### Paso 5. Ejecutar el programa

Ubicándose en la carpeta principal del proyecto, se ejecuta:

```bash
python main.py
```

Al ejecutar este comando comenzarán las simulaciones que se encuentran definidas en el archivo principal.

## 13. Trabajo colaborativo con Git y GitHub

Durante el desarrollo de un proyecto es importante mantener organizados los cambios que se realizan en el código.

Para esto se utiliza Git y GitHub, ya que permiten trabajar con diferentes versiones, guardar avances y revisar las modificaciones antes de integrarlas al proyecto principal.

La idea es que cada funcionalidad se trabaje en una rama independiente. De esta manera, los cambios se pueden organizar mejor y se evita modificar directamente la rama principal.

### 13.1. Rama main

La rama `main` representa la versión principal del proyecto.

En ella se deben integrar los cambios que hayan sido revisados y aceptados mediante los Pull Requests.

### 13.2. Ramas para organizar el desarrollo

Se propone utilizar las siguientes ramas como ejemplo de organización del trabajo:

| Rama | Descripción del trabajo |
|---|---|
| feature/estructura | Organización inicial de carpetas y archivos. |
| feature/clientes | Desarrollo de la gestión de clientes. |
| feature/registro-clientes | Mejoras en el registro de información. |
| feature/servicios | Organización de los servicios disponibles. |
| feature/servicio-salas | Funcionalidades relacionadas con las salas. |
| feature/servicio-equipos | Administración del alquiler de equipos. |
| feature/servicio-asesorias | Organización de las asesorías. |
| feature/reservas | Creación y administración de reservas. |
| feature/cancelaciones | Manejo de cancelaciones. |
| feature/calculos | Cálculo de tarifas e impuestos. |
| feature/descuentos | Aplicación de descuentos y cargos adicionales. |
| feature/inventario | Control de disponibilidad y existencias. |
| feature/validaciones | Comprobación de los datos ingresados. |
| feature/excepciones | Manejo de errores personalizados. |
| feature/logs | Registro de eventos del programa. |
| feature/pruebas | Organización y revisión de las simulaciones. |
| fix/errores | Corrección de errores encontrados. |
| docs/readme | Elaboración y actualización del README. |
| docs/instalacion | Documentación de la instalación y ejecución. |
| docs/estructura | Explicación de la organización del proyecto. |

Cada rama representa una parte del trabajo que se puede desarrollar y revisar de manera independiente. Los nombres anteriores son ejemplos de organización y no significan que todas esas ramas estén creadas actualmente.

### 13.3. Organización de commits

Los commits permiten guardar los cambios realizados en el repositorio. Cada uno debe tener un mensaje que explique de manera clara qué se modificó.

A continuación se presentan ejemplos de mensajes que pueden utilizarse según los cambios que se realicen:

1. Se creó la estructura inicial del proyecto.
2. Se organizaron las carpetas principales.
3. Se agregó el modelo de clientes.
4. Se implementó el registro de clientes.
5. Se agregaron validaciones para los datos de contacto.
6. Se organizaron las clases de servicios.
7. Se agregó el servicio de reserva de salas.
8. Se implementó el servicio de alquiler de equipos.
9. Se agregó la clase de asesorías especializadas.
10. Se mejoró la administración de reservas.
11. Se agregó el proceso de cancelación de reservas.
12. Se implementaron cálculos de tarifas.
13. Se agregaron descuentos para clientes VIP.
14. Se mejoró el control de impuestos y cargos adicionales.
15. Se implementaron controles de disponibilidad.
16. Se agregaron excepciones personalizadas.
17. Se mejoraron las validaciones del sistema.
18. Se organizó el registro de eventos.
19. Se revisaron las simulaciones del programa.
20. Se corrigieron errores encontrados durante las pruebas.
21. Se actualizaron las instrucciones de instalación.
22. Se amplió la documentación del proyecto.
23. Se completó el archivo README.

Estos mensajes son ejemplos de cómo se puede organizar el historial. Para que aparezcan como commits reales, deben ejecutarse después de realizar los cambios correspondientes. No representan commits realizados por el solo hecho de estar escritos en este documento.

### 13.4. Organización de Pull Requests

Los Pull Requests permiten solicitar que los cambios realizados en una rama sean revisados e integrados a otra rama.

Para este proyecto se propone la siguiente organización:

| Pull Request | Rama de origen | Descripción |
|---|---|---|
| PR 1 | feature/estructura | Organización de los archivos principales. |
| PR 2 | feature/clientes | Incorporación de la gestión de clientes. |
| PR 3 | feature/registro-clientes | Mejoras en el registro de información. |
| PR 4 | feature/servicios | Organización de los servicios. |
| PR 5 | feature/servicio-salas | Funcionalidades de reserva de salas. |
| PR 6 | feature/servicio-equipos | Administración de equipos. |
| PR 7 | feature/servicio-asesorias | Gestión de asesorías. |
| PR 8 | feature/reservas | Administración de reservas. |
| PR 9 | feature/cancelaciones | Control de cancelaciones. |
| PR 10 | feature/calculos | Mejoras en los cálculos. |
| PR 11 | feature/descuentos | Descuentos y cargos adicionales. |
| PR 12 | feature/inventario | Control de disponibilidad. |
| PR 13 | feature/validaciones | Validación de información. |
| PR 14 | feature/excepciones | Manejo de excepciones. |
| PR 15 | feature/logs | Registro de eventos. |
| PR 16 | feature/pruebas | Revisión de las simulaciones. |
| PR 17 | fix/errores | Corrección de errores. |
| PR 18 | docs/readme | Actualización de la documentación. |
| PR 19 | docs/instalacion | Instrucciones para ejecutar el programa. |
| PR 20 | docs/estructura | Documentación de las carpetas y archivos. |

Esta distribución permite mostrar cómo se puede dividir el desarrollo en diferentes actividades y cómo se pueden integrar los cambios de forma organizada.

Los números de Pull Request son una propuesta y no indican que las solicitudes ya estén creadas. Los Pull Requests reales deben consultarse directamente en el repositorio de GitHub.

## 14. Procedimiento para trabajar con ramas

Para crear una rama se debe abrir la terminal de Visual Studio Code y ejecutar los comandos correspondientes.

Primero se debe cambiar a la rama principal y actualizarla:

```bash
git switch main
git pull origin main
```

Después se crea una nueva rama:

```bash
git switch -c feature/clientes
```

Una vez realizados los cambios en los archivos correspondientes, se guardan con Git:

```bash
git add .
```

Luego se crea el commit:

```bash
git commit -m "Se agregó el registro de clientes"
```

Finalmente, se sube la rama al repositorio de GitHub:

```bash
git push -u origin feature/clientes
```

Después se ingresa a GitHub y se crea el Pull Request para solicitar que los cambios de `feature/clientes` se integren a `main`.

Para trabajar en otra funcionalidad se debe repetir el procedimiento, utilizando otro nombre de rama y realizando cambios correspondientes a esa actividad.

Es importante actualizar la rama principal antes de crear una nueva rama, especialmente cuando ya se han integrado cambios mediante otros Pull Requests.

Este procedimiento explica cómo se pueden realizar futuras modificaciones y no significa que todas las ramas y solicitudes indicadas en los ejemplos ya existan.

## 15. Importancia de los commits y Pull Requests

Los commits y los Pull Requests son importantes porque permiten mantener un mejor seguimiento de las modificaciones realizadas.

Con los commits es posible identificar qué cambios se hicieron y en qué momento se guardaron. También permiten regresar a versiones anteriores cuando sea necesario revisar o corregir alguna modificación.

Los Pull Requests permiten revisar el trabajo antes de incorporarlo a la rama principal. También facilitan que otras personas puedan observar los archivos modificados y hacer comentarios sobre el trabajo realizado.

El uso de estas herramientas permite mantener el proyecto más organizado y ayuda a evitar que se pierda información durante el desarrollo.

## 16. Resultados del proyecto

Con el desarrollo de SoftwareFJ se obtiene una aplicación que reúne diferentes operaciones para administrar clientes, servicios y reservas.

El proyecto permite aplicar los conceptos de programación orientada a objetos mediante diferentes clases y métodos que trabajan en conjunto.

También se implementan validaciones y excepciones para controlar situaciones incorrectas, además de un sistema de registros que permite guardar información sobre la ejecución.

Las simulaciones incluidas en el archivo principal permiten observar el comportamiento del programa y comprobar diferentes operaciones.

Por otra parte, la documentación y el uso de GitHub ayudan a mantener una mejor organización del proyecto y permiten llevar un seguimiento de los cambios.

## 17. Conclusiones

El desarrollo de este proyecto permitió fortalecer los conocimientos relacionados con la programación en Python y la programación orientada a objetos.

A través de SoftwareFJ se pudo trabajar con clases, objetos, herencia, encapsulamiento, abstracción y polimorfismo, aplicando estos conceptos en una situación práctica relacionada con la gestión de clientes, servicios y reservas.

También se comprendió la importancia de realizar validaciones y manejar excepciones, porque un programa debe estar preparado para responder cuando se presentan datos incorrectos o cuando una operación no puede realizarse.

Otro aspecto importante fue trabajar con Git y GitHub y reconocer su utilidad para organizar un proyecto. Estas herramientas permiten crear ramas, guardar cambios mediante commits y realizar Pull Requests para revisar las modificaciones antes de integrarlas al proyecto principal.

En general, el desarrollo de SoftwareFJ representa una oportunidad para aplicar los conocimientos adquiridos y comprender mejor cómo se organiza y desarrolla un proyecto de software.

## 18. Información del proyecto

**Nombre:** SoftwareFJ

**Actividad:** Fase 4 - Programación

**Institución:** Universidad Nacional Abierta y a Distancia (UNAD)

**Lenguaje de programación:** Python

**Editor de código:** Visual Studio Code

**Control de versiones:** Git

**Plataforma del repositorio:** GitHub

**Archivo principal:** main.py

**Archivo de documentación:** README.md

**Tipo de aplicación:** Sistema de gestión de clientes, servicios y reservas.
