# Importar las librerías necesarias
from flask import Flask, render_template, request, redirect, url_for, session as flask_session, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbInit import Base, session as db_session  # Importamos la sesión y base de datos ya configuradas
from Usuario import Seguidos, Usuario  # Importamos los modelos para usuarios y seguimiento
from Pubicacion import Publicacion  # Importamos el modelo de publicaciones
from Comentario import Comentario  # Importamos el modelo de comentarios
import os  # Para manejar las rutas y archivos

# Inicializamos la aplicación Flask
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Establece una clave secreta para la sesión, que debe ser cambiada en producción

# Ruta de inicio (Login)
@app.route("/", methods=["GET", "POST"])  # Ruta para el login
def login():
    if request.method == "POST":  # Si es una petición POST
        username = request.form["username"]  # Obtenemos el nombre de usuario del formulario
        password = request.form["password"]  # Obtenemos la contraseña del formulario
        user = db_session.query(Usuario).filter_by(nombre=username).first()  # Buscamos el usuario en la base de datos

        if Usuario.comprobar(username, password):  # Verificamos si el usuario y la contraseña son correctos
            flask_session["user_id"] = user.id  # Almacenamos el id del usuario en la sesión
            flask_session["username"] = user.nombre  # Almacenamos el nombre del usuario en la sesión
            return redirect(url_for("home"))  # Redirigimos a la página principal (home)
        else:
            flash("Usuario o contraseña incorrectos", "error")  # Mostramos un mensaje de error

    return render_template("login.html")  # Si no es POST, mostramos el formulario de login

# Ruta de registro (Registro)
@app.route("/register", methods=["GET", "POST"])  # Ruta para el registro de nuevos usuarios
def register():
    if request.method == "POST":  # Si es una petición POST
        username = request.form["username"]  # Obtenemos el nombre de usuario del formulario
        password = request.form["password"]  # Obtenemos la contraseña del formulario
        confirm_password = request.form["confirm_password"]  # Obtenemos la confirmación de la contraseña
        bio = request.form.get("bio")  # Obtenemos la biografía (opcional)
        photo = request.files.get("photo")  # Obtenemos la foto (opcional)

        img = True if photo and photo.filename.strip() != "" else False  # Si hay foto, la marcamos como True
        mensaje = Usuario.crear(username, password, confirm_password, img, bio)  # Intentamos crear al usuario
        
        if mensaje != "OK":  # Si hay un error al crear el usuario
            flash(mensaje, "error_register")  # Mostramos el mensaje de error
            return render_template("register.html")  # Volvemos a mostrar el formulario de registro
        
        user = db_session.query(Usuario).filter_by(nombre=username).first()  # Buscamos al usuario recién creado

        if img:  # Si hay foto
            user_image_path = os.path.join("static/images", f"{user.id}.jpg")  # Definimos la ruta de la foto
            print(f"Saving image to: {user_image_path}")  # Imprime la ruta
            photo.save(user_image_path)  # Guardamos la foto en el servidor
        
        return redirect(url_for("login"))  # Redirigimos al login después de registrar al usuario

    return render_template("register.html")  # Si no es POST, mostramos el formulario de registro

# Ruta de la página principal (con publicaciones y comentarios)
@app.route("/home", methods=["GET", "POST"])  # Ruta para la página principal
def home():
    if "user_id" not in flask_session:  # Si no hay un usuario logueado
        return redirect(url_for("login"))  # Redirigimos al login

    if request.method == "POST":  # Si se envió un formulario para crear una publicación
        texto = request.form["content"]  # Obtenemos el contenido de la publicación
        foto = request.files.get("photo")  # Obtenemos la foto de la publicación (opcional)

        if foto and foto.filename:  # Si hay foto en la publicación
            foto_filename = f"{flask_session['user_id']}_{texto[:10]}.jpg"  # Definimos el nombre de la foto
            foto_path = os.path.join("static/publicaciones", foto_filename)  # Ruta donde se guardará la foto
            foto.save(foto_path)  # Guardamos la foto
            # Creamos la publicación con foto
            Publicacion.crear(flask_session["user_id"], texto, foto_filename)
        else:
            # Creamos la publicación sin foto
            Publicacion.crear(flask_session["user_id"], texto)

        return redirect(url_for("home"))  # Redirigimos para que se recargue la página principal

    # Obtenemos las publicaciones del usuario actual
    posts_mis_publicaciones = Publicacion.mostrarUs(flask_session["user_id"])

    # Mostramos los comentarios para cada publicación
    for post in posts_mis_publicaciones:
        post.comments = Publicacion.mostrarCom(post.id)  # Obtenemos los comentarios de cada publicación
        if post.foto:  # Si la publicación tiene foto
            computed_foto_filename = f"{post.id_usuario}_{post.texto[:10]}.jpg"  # Definimos el nombre de la foto
            ruta_completa = os.path.join("static/publicaciones", computed_foto_filename)  # Ruta completa de la foto
            if os.path.exists(ruta_completa):  # Si la foto existe en el servidor
                post.computed_foto_path = computed_foto_filename  # Asignamos la ruta de la foto
            else:
                post.computed_foto_path = None  # Si la foto no existe, asignamos None
        else:
            post.computed_foto_path = None  # Si no hay foto, asignamos None

    return render_template("home.html", user=flask_session, posts=posts_mis_publicaciones)  # Mostramos la página principal con las publicaciones

# Ruta para ver el perfil del usuario
@app.route("/profile")  # Ruta para ver el perfil de usuario
def profile():
    if "user_id" not in flask_session:  # Si no hay un usuario logueado
        return redirect(url_for("login"))  # Redirigimos al login

    user = db_session.query(Usuario).filter_by(id=flask_session["user_id"]).first()  # Buscamos al usuario
    publicaciones = db_session.query(Publicacion).filter_by(id_usuario=user.id).order_by(Publicacion.fecha.desc()).all()  # Obtenemos las publicaciones del usuario, ordenadas por fecha descendente

    # Obtener el número de seguidores y seguidos
    seguidores_count = Seguidos.contar_seguidores(user.id)  # Contamos los seguidores del usuario
    seguidos_count = Seguidos.contar_seguidos(user.id)  # Contamos a quién sigue el usuario

    for post in publicaciones:
        post.comments = Publicacion.mostrarCom(post.id)  # Obtenemos los comentarios de cada publicación

    return render_template("profile.html", user=user, posts=publicaciones, seguidores_count=seguidores_count, seguidos_count=seguidos_count)  # Mostramos la página de perfil del usuario

# Ruta para editar perfil
@app.route("/edit_profile", methods=["GET", "POST"])  # Ruta para editar el perfil
def edit_profile():
    if "user_id" not in flask_session:  # Si no hay un usuario logueado
        return redirect(url_for("login"))  # Redirigimos al login

    user = db_session.query(Usuario).filter_by(id=flask_session["user_id"]).first()  # Buscamos al usuario logueado

    if request.method == "POST":  # Si se envió un formulario para editar el perfil
        nuevo_nombre = request.form.get("username")  # Obtenemos el nuevo nombre (opcional)
        nueva_bio = request.form.get("bio")  # Obtenemos la nueva biografía (opcional)
        nueva_foto = request.files.get("photo")  # Obtenemos la nueva foto (opcional)
        current_password = request.form["current_password"]  # Obtenemos la contraseña actual
        new_password = request.form.get("new_password")  # Obtenemos la nueva contraseña (opcional)
        confirm_password = request.form.get("confirm_password")  # Confirmamos la nueva contraseña (opcional)
        remove_photo = request.form.get("remove_photo")  # Capturamos si el checkbox para eliminar la foto está marcado

        # Verificamos si la contraseña actual es correcta
        if not Usuario.comprobar(user.nombre, current_password):
            flash("Contraseña actual incorrecta.", "error")
            return render_template("edit_profile.html", user=user)

        # Verificamos si las nuevas contraseñas coinciden
        if new_password and confirm_password:
            if new_password != confirm_password:
                flash("Las nuevas contraseñas no coinciden.", "error")
                return render_template("edit_profile.html", user=user)
            Usuario.cambiarPass(user.id, current_password, new_password)  # Cambiamos la contraseña

        # Modificamos los datos del perfil si se han proporcionado nuevos valores
        if nuevo_nombre:
            Usuario.modificar(user.id, nombre=nuevo_nombre)  # Actualizamos el nombre
        if nueva_bio:
            Usuario.modificar(user.id, bio=nueva_bio)  # Actualizamos la biografía

        # Manejo de la foto de perfil
        if remove_photo == "on":  # Si se marcó la opción para eliminar la foto
            foto_path = os.path.join("static/images", f"{user.id}.jpg")
            if os.path.exists(foto_path):
                os.remove(foto_path)  # Eliminamos la foto
            # Colocamos la foto predeterminada
            foto_default_path = os.path.join("static/images", "default.jpg")
            foto_default_destino = os.path.join("static/images", f"{user.id}.jpg")
            if os.path.exists(foto_default_path):
                with open(foto_default_path, 'rb') as default_file:
                    with open(foto_default_destino, 'wb') as user_file:
                        user_file.write(default_file.read())
            Usuario.modificar(user.id, foto=False)  # Marcamos que el usuario no tiene foto
        elif nueva_foto:  # Si se subió una nueva foto
            nueva_foto_path = os.path.join("static/images", f"{user.id}.jpg")
            nueva_foto.save(nueva_foto_path)  # Guardamos la nueva foto
            Usuario.modificar(user.id, foto=True)  # Marcamos que el usuario tiene foto
        else:
            Usuario.modificar(user.id, foto=False)  # Si no se subió ni eliminó foto, dejamos foto=False

        flash("Perfil actualizado correctamente.", "success")
        return redirect(url_for("profile"))  # Redirigimos a la página de perfil

    return render_template("edit_profile.html", user=user)  # Si no es POST, mostramos el formulario de edición

# Ruta para agregar un comentario a una publicación
@app.route("/comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    if "user_id" not in flask_session:  # Si no hay un usuario logueado
        return redirect(url_for("login"))  # Redirigimos al login

    post = db_session.query(Publicacion).filter_by(id=post_id).first()  # Buscamos la publicación

    if not post:  # Si no existe la publicación
        flash("Publicación no encontrada.", "error")
        return redirect(url_for("home"))  # Redirigimos a la página principal

    # Verificamos si el usuario sigue al autor de la publicación
    if not Seguidos.es_seguidor(flask_session["user_id"], post.id_usuario):
        flash("Solo los seguidores pueden comentar esta publicación.", "error")
        return redirect(url_for("home"))

    texto = request.form["comment_text"]  # Obtenemos el texto del comentario
    Comentario.crear(flask_session["user_id"], post_id, texto)  # Creamos el comentario en la base de datos

    return redirect(url_for("publicaciones_seguidos"))




# Ruta para eliminar una publicación
@app.route("/delete_post/<int:post_id>", methods=["POST"])  # Ruta para eliminar una publicación
def delete_post(post_id):
    if "user_id" not in flask_session:  # Si no hay un usuario logueado
        return redirect(url_for("login"))  # Redirigimos al login

    post = db_session.query(Publicacion).filter_by(id=post_id, id_usuario=flask_session["user_id"]).first()  # Buscamos la publicación que el usuario puede eliminar
    
    if post:  # Si la publicación existe y el usuario tiene permiso para eliminarla
        if post.foto:  # Si la publicación tiene foto, la eliminamos
            foto_path = os.path.join("static/publicaciones", f"{post.id_usuario}_{post.texto[:10]}.jpg")
            if os.path.exists(foto_path):
                os.remove(foto_path)  # Eliminamos la foto

        Publicacion.eliminar(post_id)  # Eliminamos la publicación y sus comentarios

        flash("Publicación eliminada correctamente", "success")  # Mostramos un mensaje de éxito
    else:
        flash("No tienes permiso para eliminar esta publicación", "error")  # Si no se tiene permiso para eliminar

    return redirect(url_for("profile"))  # Redirigimos al perfil del usuario

# Ruta para buscar un usuario
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    if "user_id" not in flask_session:  # Si el usuario no está logueado, redirigimos al login
        return redirect(url_for("login"))

    resultados = []  # Lista donde se almacenarán los resultados de la búsqueda
    if request.method == "POST":  # Si la petición es POST (cuando se envía el formulario de búsqueda)
        termino_busqueda = request.form["termino_busqueda"]  # Obtenemos el término de búsqueda del formulario
        # Realizamos la búsqueda en la base de datos de usuarios cuyo nombre coincida con el término
        resultados = db_session.query(Usuario).filter(Usuario.nombre.ilike(f"%{termino_busqueda}%")).all()

    # Obtenemos los IDs de los usuarios que ya está siguiendo el usuario actual
    seguidos = db_session.query(Seguidos).filter_by(id_seguidor=flask_session["user_id"]).all()  # Buscamos los seguidos
    seguidos_ids = [seguidor.id_usuario for seguidor in seguidos]  # Extraemos los IDs de los usuarios seguidos

    return render_template("buscar.html", resultados=resultados, seguidos_ids=seguidos_ids)

# Ruta para seguir un usuario
@app.route("/seguir_usuario/<int:user_id>", methods=["POST"])
def seguir_usuario(user_id):
    if "user_id" not in flask_session:  # Si el usuario no está logueado, redirigimos al login
        return redirect(url_for("login"))

    user_to_follow = db_session.query(Usuario).filter_by(id=user_id).first()  # Buscamos al usuario a seguir

    if user_to_follow:
        # Verificamos si ya estamos siguiendo a este usuario
        if db_session.query(Seguidos).filter_by(id_seguidor=flask_session["user_id"], id_usuario=user_id).first():
            flash("Ya sigues a este usuario.", "info")  # Si ya lo seguimos, mostramos un mensaje
        else:
            # Si no lo estamos siguiendo, creamos la relación en la tabla "Seguidos"
            nuevo_seguido = Seguidos(id_seguidor=flask_session["user_id"], id_usuario=user_id)
            db_session.add(nuevo_seguido)
            db_session.commit()  # Guardamos los cambios en la base de datos
            flash("Ahora sigues a este usuario.", "success")  # Notificamos que se empezó a seguir al usuario
    else:
        flash("El usuario no existe.", "error")  # Si el usuario no existe, mostramos un mensaje de error

    return redirect(url_for('buscar'))  # Redirigimos a la página de búsqueda

# Ruta para dejar de seguir a un usuario
@app.route("/dejar_de_seguir/<int:usuario_id>", methods=["POST"])
def dejar_de_seguir(usuario_id):
    if "user_id" not in flask_session:  # Si el usuario no está logueado, redirigimos al login
        return redirect(url_for("login"))

    seguidor = db_session.query(Seguidos).filter_by(id_seguidor=flask_session["user_id"], id_usuario=usuario_id).first()  # Buscamos la relación de seguimiento

    if seguidor:
        db_session.delete(seguidor)  # Si existe la relación, la eliminamos
        db_session.commit()  # Guardamos los cambios
        flash("Has dejado de seguir a este usuario.", "success")  # Notificamos que se ha dejado de seguir
    else:
        flash("No estás siguiendo a este usuario.", "error")  # Si no se estaba siguiendo, mostramos un mensaje de error

    return redirect(url_for("home"))  # Redirigimos a la página principal

# Ruta para ver las publicaciones de los seguidos
@app.route('/publicaciones_seguidos', methods=['GET', 'POST'])
def publicaciones_seguidos():
    if "user_id" not in flask_session:  # Si el usuario no está logueado, redirigimos al login
        return redirect(url_for("login"))

    # Obtener el usuario actual desde la sesión
    user = db_session.query(Usuario).filter_by(id=flask_session["user_id"]).first()

    # Obtener los usuarios seguidos
    seguidos = Seguidos.listarSeguidos(flask_session["user_id"])
    seguidos_ids = [seguidos.id_usuario for seguidos in seguidos]  # Extraemos los IDs de los usuarios seguidos

    # Obtener las publicaciones de los usuarios que sigo
    publicaciones_seguidos = []
    for user_id in seguidos_ids:
        publicaciones_seguidos.extend(Publicacion.mostrarUs(user_id))  # Obtenemos las publicaciones de los usuarios seguidos

    # Ordenar las publicaciones por fecha
    publicaciones_seguidos = sorted(publicaciones_seguidos, key=lambda x: x.fecha, reverse=True)

    # Mostrar los comentarios para cada publicación
    for post in publicaciones_seguidos:
        post.comments = Publicacion.mostrarCom(post.id)  # Obtenemos los comentarios de cada publicación
        if post.foto:
            computed_foto_filename = f"{post.id_usuario}_{post.texto[:10]}.jpg"  # Definimos el nombre de la foto
            ruta_completa = os.path.join("static/publicaciones", computed_foto_filename)
            if os.path.exists(ruta_completa):  # Si la foto existe
                post.computed_foto_path = computed_foto_filename
            else:
                post.computed_foto_path = None  # Si no existe, asignamos None
        else:
            post.computed_foto_path = None  # Si no tiene foto, asignamos None

             

    return render_template('home_publicaciones_seguidos.html', user=flask_session, posts_seguidos=publicaciones_seguidos)  # Mostramos las publicaciones

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    flask_session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
