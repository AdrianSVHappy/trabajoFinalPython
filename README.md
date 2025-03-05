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

## Gestión de base de datos

Para gestionar la base de datos partimos de la base de que tenemos un servidor mysql funcionando con una base de datos llamada **pytest** y un usuario que con permisos llamado **pyuser**, al acceder nos pedirá la contraseña. Si quieres usar otro usuario o base de datos debes modificar el documento **dbInit.py** linea 5.

Para hacer el mantenimiento de la base de datos tendremos que acceder por terminal usando el cliente mysql, para ello tendremos que usar el siguiente comando

```
mysql -u pyuser -p pytest
```

Una vez dentro nos aparecerá una interfaz de consola distinta parecido a algo así:

```
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 11
Server version: 8.0.41-0ubuntu0.22.04.1 (Ubuntu)

Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

Usando esta consola podemos hacer varias operaciones usando los comandos CRUD sql clasicos, pero voy a agregar a este documento algunos comando para agilizar algunos procesos:

- Ver las tablas de la base de datos.
    ```
    show tables;
    ---------------------

    mysql> show tables;
    +------------------+
    | Tables_in_pytest |
    +------------------+
    | comentarios      |
    | publicaciones    |
    | seguidos         |
    | usuarios         |
    +------------------+
    4 rows in set (0,01 sec)
    ```

- Eliminar la base de datos.

    ```
    drop database pytest;
    -----------------------

    mysql> drop database pytest;
    Query OK, 4 rows affected (0,21 sec)
    ```

- Crear la base de datos.

    ```
    create database pytest;
    -------------------------

    mysql> create database pytest;
    Query OK, 1 row affected (0,03 sec)
    ```

    Para esta ultima, haremos uso del archivo **CrearTablas.py** para crear las tablas nuevamente.

    ```
    use pytest
    -------------------
    
    mysql> use pytest
    Database changed
    ```

    Y podemos comprobar que las tablas se han creado usando el primer comando.

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

## Funcionamiento
En este apartado explicaremos brevemente el funcionamiento de la aplicación: \
En primer lugar, tenemos la clase dbinit que se encarga de la gestión de la base de datos (ya sea crear, modificar o actualizar) con sus excepciones oportunas. Además, se posee un par de clases auxiliares que permite crear las tablas de la base de datos y eliminar y crear de nuevo la base. \
En segundo lugar, nos encontramos con las clases Comentario, Usuario y Publicación las cuales nos permiten el funcionamiento interno de la aplicación a través de objetos de estos y con los cuales realizaremos las consultas y la implementación del entorno web. Nos ayudan a realizar los diversos métodos que llevaremos a cabo en la red social como pudiera ser guardar usuarios, comprobarlos, crear publicaciones y comentarios, etc. Estas clases empiezan con sus variables y relaciones y posteriormente con sus métodos (sean estáticos o de clase). Además, la clase Usuario posee una subclase denominada seguidos para valorar los seguidores y seguidos.\
En tercer y último lugar tenemos el ejecutable que es app.py el cual posee diversas rutas dadas por el entorno flask que nos derivan a las diferentes plantillas creadas en html en conjunto con jinja2. En este nos encontraremos los siguientes aspectos que junto a los html nos proporcionan la interfaz vista:

- Login: permite al usuario acceder a la aplicación. Para ello buscaremos al usuario en la base de datos sacando los datos dados en el html y comprobaremos con son correcto. En caso positivo nos manda a la pestaña principal denominada home. En caso negativo salta un error y volvemos al login.
- Register: ruta para registrarnos en la app dando los datos por el html correspondiente y creando el usuario en caso afirmativo mandándonos al login, si no mostrará un error y volvemos al register.
- Home: ruta principal donde se nos permite añadir publicaciones (mostrando sus comentarios), ver nuestro perfil o buscar personas de la red social. 
- Profile: encargada de mostrar nuestro perfil con nuestros seguidores y seguidos y donde podremos eliminar las publicaciones.Además, podremos editar perfil o cerrar la sesión a través del html.
- Edit_profile: se centra en modificar los datos del usuario actualizándolos a gusto del consumidor.
- Comment: se ocupa de crear los comentarios de las publicaciones.
- Delete_post: su función es borrar las publicaciones en nuestro perfil.
- Buscar: centrado en encontrar a los usuarios que queramos seguir.
- Seguir_usuario: mecanismo encargado de enlazar los usuarios entre ellos con la clase Seguidos.
- Dejar_seguir: inversa a la anterior.
- Publicaciones_seguido: ruta que proporciona las publicaciones de aquellos usuarios a los que seguimos.
- Seguidores y seguidos: muestran las listas de los seguidores y seguidos.
- Logout: con este cerraremos la sesión


## Capturas de Pantalla
Aquí puedes ver algunas capturas de pantalla de la aplicación en funcionamiento:

 - Interfaz principal: Captura 1

 - Formulario de crear usuario: Captura 2

## Créditos
Este proyecto ha sido desarrollado por:

- **Leandro Carbajo Méndez:** Encargado de la implementación de Flask (app.py), HTML y CSS. [LinkedIn](https://www.linkedin.com/in/leandro-carbajo-m%C3%A9ndez-5b0820239/)

- **Adrián Suárez Valdayo:** Encargado de las clases, relaciones con la base de datos, y la configuración del servidor. [LinkedIn](https://www.linkedin.com/in/adri%C3%A1n-su%C3%A1rez-valdayo-4583a726a/)

## Bibliografía
Aquí incluimos enlaces a recursos que te ayudaron durante el desarrollo del proyecto. Por ejemplo:

[Documentación base de datos](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04)

[Documentación oficial de Flask](https://flask.palletsprojects.com/en/stable/)

[Instalación de Flask](https://phoenixnap.com/kb/install-flask)

[Tutorial de Flask y SQLAlchemy](https://www.youtube.com/watch?v=BP3D03CYFHA)

[Tutorial Flask para aplicaciones web](https://www.youtube.com/watch?v=-1DmVCPB6H8)

[Flask para principiantes](https://www.youtube.com/watch?v=W-SfC_V7P6o)

[Introducción a Flak](https://www.youtube.com/watch?v=2eoEgs5oLxY)

[Gestión de lista de contactos con Flask](https://www.youtube.com/watch?v=tcGtwhaRmok)

[Documentación oficial de Jinja2](https://jinja.palletsprojects.com/en/stable/)
 
[Plantillas de Jinja2](https://codigofacilito.com/articulos/plantillas-jinja2)

