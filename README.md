# UNAD - Programación Fase 4: SoftwareFJ

## Sistema Integral de Gestión de Servicios, Clientes y Reservas

### Descripción del proyecto

SoftwareFJ es un programa desarrollado en Python que permite llevar el control de clientes, diferentes tipos de servicios y reservas. La idea principal es facilitar la organización de esta información y permitir que los usuarios puedan gestionar todo de una manera más sencilla.

Este proyecto se realizó como parte de la actividad Fase 4 del curso de Programación de la Universidad Nacional Abierta y a Distancia (UNAD), poniendo en práctica los conocimientos aprendidos durante el desarrollo de la actividad.

### Objetivo general

Crear un sistema que permita registrar y administrar clientes, servicios y reservas, utilizando los conceptos de programación orientada a objetos y diferentes herramientas para validar la información y controlar posibles errores.

### Funcionalidades principales

- Registrar y consultar clientes.
- Agregar y administrar diferentes tipos de servicios.
- Crear, confirmar y cancelar reservas.
- Consultar la información de los clientes, servicios y reservas.
- Calcular el costo de cada servicio.
- Aplicar impuestos, descuentos y otros cargos.
- Verificar que la información ingresada sea correcta.
- Controlar los errores que puedan presentarse durante el uso del programa.
- Guardar los registros de actividad y errores en archivos de log.
- Realizar 12 simulaciones para comprobar que el sistema funcione correctamente.

### Tipos de servicios

El programa permite trabajar con tres tipos de servicios:

1. **Reserva de salas:** permite administrar los espacios disponibles y calcular su costo dependiendo del tiempo de uso y la capacidad.
2. **Alquiler de equipos:** permite gestionar los equipos, revisar las existencias y calcular el valor del alquiler.
3. **Asesorías especializadas:** permite organizar las asesorías teniendo en cuenta el nivel del consultor y la modalidad de atención.

### Conceptos de programación orientada a objetos

Durante el desarrollo del proyecto se utilizaron varios conceptos importantes de la programación orientada a objetos:

- **Abstracción:** se utilizaron clases base para organizar y representar los diferentes elementos del sistema.
- **Herencia:** permite compartir información y funcionalidades entre las clases.
- **Encapsulamiento:** ayuda a proteger los datos y controlar la forma en que se accede a ellos.
- **Polimorfismo:** permite que cada tipo de servicio tenga su propia forma de calcular los costos.
- **Sobrecarga:** se utiliza para realizar cálculos teniendo en cuenta diferentes valores, como impuestos, descuentos y cargos adicionales.
- **Manejo de excepciones:** permite identificar y controlar los errores que puedan aparecer mientras se ejecuta el programa.

### Estructura del proyecto

```text
UNAD-Programacion-Fase4-SoftwareFJ/
│
├── main.py
├── README.md
├── .gitignore
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

### Tecnologías utilizadas

Para realizar este proyecto se utilizaron las siguientes herramientas y tecnologías:

- Python 3.10 o superior.
- Programación orientada a objetos.
- Módulos y paquetes de Python.
- Manejo de excepciones para controlar errores.
- Logging para guardar los registros del programa.
- Git y GitHub para guardar y compartir los cambios realizados en el proyecto.

### Instalación y ejecución

Para poner en funcionamiento el programa se deben seguir estos pasos:

1. Descargar o clonar el repositorio.
2. Abrir la carpeta del proyecto en Visual Studio Code.
3. Comprobar que Python esté instalado en el equipo.
4. Abrir una terminal desde la carpeta del proyecto.
5. Ejecutar el siguiente comando:

```bash
python main.py
```

Después de ejecutar el comando, el programa realizará las 12 simulaciones y mostrará los resultados en la consola.

Los registros de actividad y los posibles errores que se presenten se pueden consultar en el siguiente archivo:

```text
logs/software_fj.log
```

### Autoría

Este proyecto fue realizado como parte de la actividad de Programación Fase 4 de la Universidad Nacional Abierta y a Distancia (UNAD).

### Conclusión

Con el desarrollo de SoftwareFJ se pudieron poner en práctica los conocimientos aprendidos sobre programación orientada a objetos, creando un programa que permite gestionar clientes, servicios y reservas. También fue una oportunidad para trabajar con diferentes clases, organizar mejor el código y aprender a controlar los errores que pueden aparecer durante la ejecución del programa.