# Trabajo Final de Python

Este proyecto es un trabajo de clase desarrollado en Python, que incluye una aplicación web utilizando **Flask** para gestionar datos mediante una interfaz amigable. El proyecto ha sido desarrollado por **Adrián Suárez Valdayo** y **Leandro Carbajo Méndez**.

## Descripción

El proyecto consiste en una aplicación web que permite gestionar datos mediante una base de datos relacional. Incluye:
- Un servidor en Flask para manejar las solicitudes HTTP.
- Una interfaz web con HTML y CSS para interactuar con los datos.
- Una base de datos para almacenar y gestionar la información.


## Uso

Abre tu navegador y visita http://10.6.13.105:5000 para ver la aplicación en funcionamiento.

 Una vez que la aplicación esté en ejecución, puedes:

 - Acceder a la interfaz web para gestionar los datos.

 - Realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los datos almacenados en la base de datos.

## Estructura del Proyecto
El repositorio está organizado de la siguiente manera:

```
trabajoFinalPython/
├── app.py                # Archivo principal de la aplicación Flask
├── comandos sql.txt      # Comandos SQL para la configuración de la base de datos
├── Comentario.py         # Clase para gestionar comentarios
├── CrearTablas.py        # Script para crear las tablas en la base de datos
├── dbinit.py             # Inicialización de la base de datos
├── Publication.py        # Clase para gestionar publicaciones
├── update_db.py          # Script para actualizar la base de datos
├── Usuario.py            # Clase para gestionar usuarios
├── static/               # Carpeta con archivos estáticos (CSS, imágenes, etc.)
│   ├── css/              # Archivos CSS para estilos
│   ├── images/           # Imágenes utilizadas en la interfaz
│   └── publication/      # Archivos relacionados con las publicaciones
├── templates/            # Carpeta con los archivos HTML
│   ├── buscar.html       # Página de búsqueda
│   ├── edit_profile.html # Página de edición de perfil
│   ├── home.html         # Página principal
│   ├── home_publicaciones_seguidas.html # Página de publicaciones seguidas
│   ├── login.html        # Página de inicio de sesión
│   ├── profile.html      # Página de perfil de usuario
│   └── register.html     # Página de registro de usuario
└── README.md             # Este archivo
```


## Capturas de Pantalla
Aquí puedes ver algunas capturas de pantalla de la aplicación en funcionamiento:

 - Interfaz principal: Captura 1

 - Formulario de crear usuario: Captura 2

## Créditos
Este proyecto ha sido desarrollado por:

- **Leandro Carbajo Méndez:** Encargado de la implementación de Flask (app.py), HTML y CSS. [LinkedIn](https://www.linkedin.com/in/leandro-carbajo-m%C3%A9ndez-5b0820239/)

- **Adrián Suárez Valdayo:** Encargado de las clases, relaciones con la base de datos, y la configuración del servidor. [LinkedIn](https://www.linkedin.com/in/adri%C3%A1n-su%C3%A1rez-valdayo-4583a726a/)

## Bibliografía
Aquí puedes incluir enlaces a recursos que te ayudaron durante el desarrollo del proyecto. Por ejemplo:

[Documentación base de datos](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04)

[Documentación oficial de Flask]()

[Tutorial de Flask y SQLAlchemy]()

