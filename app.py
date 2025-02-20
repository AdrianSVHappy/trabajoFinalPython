from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbInit import Base, session as db_session
from Usuario import Usuario
from Pubicacion import Publicacion
from Comentario import Comentario
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Cambiar por algo más seguro en producción

# Ruta de inicio (Login)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db_session.query(Usuario).filter_by(nombre=username).first()

        # Verificar la contraseña directamente sin hashing
        if user and user.passw == password:  # Compara la contraseña directamente
            session["user_id"] = user.id
            session["username"] = user.nombre
            return redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrectos", "error")

    return render_template("login.html")

# Ruta de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        bio = request.form.get("bio")
        photo = request.files.get("photo")

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for("register"))

      

        # Guardar la imagen de perfil si se sube una
        photo_filename = None
        if photo and photo.filename != "":
            photo_filename = f"{username}.jpg"
            photo.save(os.path.join("static/images", photo_filename))

        Usuario.guardar(username, password, bio)  # Almacenar la contraseña directamente
        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Ruta de la página principal (con publicaciones y comentarios)
@app.route("/home", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        texto = request.form["content"]
        Publicacion.crear(session["user_id"], texto)

    publicaciones = db_session.query(Publicacion).join(Usuario).all()
    return render_template("home.html", user=session, posts=publicaciones)

# Ruta para ver el perfil del usuario
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db_session.query(Usuario).filter_by(id=session["user_id"]).first()
    publicaciones = db_session.query(Publicacion).filter_by(id_usuario=user.id).all()

    return render_template("profile.html", user=user, posts=publicaciones)

# Ruta para editar perfil
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db_session.query(Usuario).filter_by(id=session["user_id"]).first()

    if request.method == "POST":
        user.nombre = request.form["username"]
        user.bio = request.form.get("bio")

        photo = request.files.get("photo")
        if photo and photo.filename != "":
            photo_filename = f"{user.nombre}.jpg"
            photo.save(os.path.join("static/images", photo_filename))

        db_session.commit()
        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for("profile"))

    return render_template("edit_profile.html", user=user)

# Ruta para añadir comentarios a una publicación
@app.route("/comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    texto = request.form["comment_text"]
    Comentario.crear(session["user_id"], post_id, texto)

    return redirect(url_for("home"))

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
