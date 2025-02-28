from dbInit import Base, session, guardar
from sqlalchemy import Boolean, Column, Integer, VARCHAR, Text, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
import hashlib
from Pubicacion import Publicacion


#Clase Usuario, representa un usuario de la red social
class Usuario(Base):
    
    #Nombre de la tabla
    __tablename__ = "usuarios"
    
    #variables o atributos
    id = Column(Integer, primary_key=True)
    nombre = Column(VARCHAR(50), nullable=False)
    passw = Column(VARCHAR(255), nullable=False)
    bio = Column(Text)
    foto = Column(Boolean, default=False) #Este campo guarda en un booleano si el usuario tiene o no foto de usuario
    
    #Relacion que Leandro va a borrar
    publicaciones = relationship("Publicacion", back_populates="user")
    comentarios = relationship("Comentario", back_populates="user")

    """    
    Metodo estatico que guarda un usuario en la base de datos
    nomrbe -> Nomreb de usuario
    passw -> Contraseña del usuario
    bio -> Biografia del usuario
    img -> True si se guarda foto / False si no
    """
    @staticmethod
    def guardar(nombre, passw, bio, img):
        nuevo = Usuario(nombre=nombre, passw=passw, bio=bio, foto=img)
        guardar(nuevo)
        
    """    
    Metodo estatico que comprueba la existencia de un usuario en la base de datos.
    Si metemos la contraseña por parametros, compobamos que la contraseña coincida con la del usuario
    n -> Nombre del usuario
    p -> Contraseña del usuario
    """
    @staticmethod
    def comprobar(n, p=""):
        ret = False
        usuario = None 
         
        if(p == ""):
            usuario = session.query(Usuario).filter_by(nombre=n).all()
        else:
            usuario = session.query(Usuario).filter_by(nombre=n, passw = hashlib.sha256(p.encode()).hexdigest()).all()
         
        if usuario:
            ret = True
    
        return ret
    
    """
    Metodo estatico para crear un usuario con comprobaciones de seguridad
    Retorna un mensaje (string) -> 'OK' si se ha guardado correctamente en la base de datos / de lo contrario 'Error: ' + la causa del error
    nom -> Nombre del usuario
    passw1 -> Contraseña del usuario
    passw2 -> Comrpobar contraseña
    foto -> si se guarda o no foto
    bio -> Biografía del usuario / Por defecto sin biografia 
    """        
    @staticmethod
    def crear(nom, passw1, passw2, foto, bio=""):
        mensaje = "OK"
        segura = ""
        if (passw1 != passw2):
            mensaje = "Error: Las contraseñas no coinciden"
        elif(Usuario.comprobar(nom)):
            mensaje = "Error: El nombre de usuario está en uso"
        else:
            segura = hashlib.sha256(passw1.encode())
            Usuario.guardar(nom, segura.hexdigest(), bio, foto)
        print(mensaje)
        return mensaje
    
    """
    Metodo estatico para modificar un usuario
    id -> Id del usuario que se quiere modificar en la base de datos
    nombre -> Atributo opcional, nuevo nombre del usuario
    bio -> Atributo opcional, nueva biografía del usuario
    foto -> Atributo opcional, nuevo registro de foto del usuario
    """
    @staticmethod
    def modificar(id, nombre="", bio="", foto=""):
        user = session.query(Usuario).filter_by(id=id).first()
        if nombre:
            user.nombre = nombre
            
        if bio:
            user.bio = bio
            
        # Validar la foto y asignar un valor booleano explícito
        if foto is None:  # Si no se ha proporcionado foto
            user.foto= False
        elif foto == "on":  # Si se marca el checkbox para eliminar la foto
            user.foto= False
        else:  # Si hay una foto válida, mantener True
            user.foto = True
            
        session.commit()
        
    """
    Metodo estatico para cambiar la contraseña de un usuario
    id -> Id del usuario que se quiere modificar
    antigua -> Contraseña que tiene el usuario antes de ser modificado
    nueva -> Contraseña nueva que se quiere establecer
    """
    @staticmethod
    def cambiarPass(id, antigua, nueva):
        user = session.query(Usuario).filter_by(id=id).first()
        
        if hashlib.sha256(antigua.encode()).hexdigest() == user.passw:
            user.passw = hashlib.sha256(nueva.encode()).hexdigest()
            
        session.commit()
        
    """
    Metodo estatico para eliminar un usuario
    id -> id del usuario que se quiere eliminar
    """
    @staticmethod
    def eliminar(id):
        session.query(Usuario).filter_by(id=id).delete()
        session.commit()
    
    """
    Metodo de clase para buscar un usuario por su nombre
    nombre -> nombre del usuario al buscar
    """
    @classmethod
    def buscar_por_nombre(cls, nombre):
        return session.query(cls).filter(cls.nombre.ilike(f"%{nombre}%")).all()
        

"""
Tabla auxiliar para guardar los seguidores de un usuario, esta consta de 3 columnas
id que funciona de identificador
id_usuario que guarda el usuario seguido
id_seguidor que guarda el id del usuario que sigue al otro
"""
class Seguidos(Base):
 
    __tablename__ = "seguidos"
    
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete='CASCADE'), nullable=False)
    id_seguidor = Column(Integer, ForeignKey("usuarios.id", ondelete='CASCADE'), nullable=False)
    
    
    """
    Metodo estatico que guarda el registro de que un usuario sigue a otro
    us -> Id del usuario al que van a seguir
    se -> Id del nuevo seguidor
    """
    @staticmethod
    def crear(us, se):
        nuevo = Seguidos(id_usuario=us, id_seguidor=se)
        guardar(nuevo)
        
        
    """
    Metodo estatico para listar los seguidores de un usuario
    us -> Id del usuario
    """
    @staticmethod
    def listarSeguidores(us):
        lista = session.query(Seguidos).filter_by(id_usuario=us).all()
        return lista
        
    """
    Metodo estatico para listar los seguidos de un usuario
    se -> Id del usuario
    """
    @staticmethod
    def listarSeguidos(se):
        lista = session.query(Seguidos).filter_by(id_seguidor=se).all()
        return lista
    
    """
    Metodo estatico para contar los seguidores de un usuario
    id_usuario -> Id del usuario
    """
    @staticmethod
    def contar_seguidores(id_usuario):
        return session.query(Seguidos).filter_by(id_usuario=id_usuario).count()

    """
    Metodo estatico para contar los seguidos de un usuario
    id_seguidor -> Id del seguidor 
    """
    @staticmethod
    def contar_seguidos(id_seguidor):
        return session.query(Seguidos).filter_by(id_seguidor=id_seguidor).count()

    """
    Metodo de clase para comprobar si un usuario sigue a otro
    id_seguidor -> Id del seguidor
    id_usuario -> Id del usuario
    """
    @classmethod
    def es_seguidor(cls, id_seguidor, id_usuario):
        return session.query(cls).filter_by(id_seguidor=id_seguidor, id_usuario=id_usuario).first() is not None

    """
    Metodo de clase para seguir a un usuario
    id_seguidor -> Id del seguidor
    id_usuario -> Id del usuario
    """
    @classmethod
    def seguir(cls, id_seguidor, id_usuario):
        if not cls.es_seguidor(id_seguidor, id_usuario):
            nuevo_seguimiento = cls(id_seguidor=id_seguidor, id_usuario=id_usuario)
            session.add(nuevo_seguimiento)
            session.commit()

    """
    Metodo de clase para dejar de seguir a un usuario
    id_seguidor -> Id del seguidor
    id_usuario -> Id del usuario
    """
    @classmethod
    def dejar_de_seguir(cls, id_seguidor, id_usuario):
        seguimiento = session.query(cls).filter_by(id_seguidor=id_seguidor, id_usuario=id_usuario).first()
        if seguimiento:
            session.delete(seguimiento)
            session.commit()