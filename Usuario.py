from dbInit import Base, session, guardar
from sqlalchemy import Boolean, Column, Integer, VARCHAR, Text, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
import hashlib
import Publicacion

class Usuario(Base):
    
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(VARCHAR(50), nullable=False)
    passw = Column(VARCHAR(255), nullable=False)
    bio = Column(Text)
    foto = Column(Boolean)
    
    publicaciones = relationship("Publicacion", back_populates="user")

    """
    def __init__(self, id,  name, passw, bio, foto, seguidos, seguidores):
        self.id = id
        self.name = name
        self.passw = passw
        self.bio = bio
        self.foto = foto
        self.seguidos = seguidos
        self.seguidores = seguidores
    """    
        
    @staticmethod
    def guardar(nombre, passw, bio, img):
        nuevo = Usuario(nombre=nombre, passw=passw, bio=bio, foto=img)
        guardar(nuevo)
        
        
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
            
    @staticmethod
    def crear(nom, passw1, passw2, foto, bio=None):
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
    
    @staticmethod
    def modificar(id, nombre="", bio="", foto=""):
        user = session.query(Usuario).filter_by(id=id).first()
        if nombre:
            user.nombre = nombre
            
        if bio:
            user.bio = bio
            
        if foto:
            user.foto = foto
            
        session.commit()
        
    @staticmethod
    def cambiarPass(id, antigua, nueva):
        user = session.query(Usuario).filter_by(id=id).first()
        
        if hashlib.sha256(antigua.encode()).hexdigest() == user.passw:
            user.passw = hashlib.sha256(nueva.encode()).hexdigest()
            
        session.commit()
        
    @staticmethod
    def eliminar(id):

        publicaciones = session.query(Publicacion).filter_by(id_usuario=id).all()
  
        for p in publicaciones:
            Publicacion.eliminar(p.id)
        
        user = session.query(Usuario).filter_by(id=id).delete()
        


class Seguidos(Base):
 
    __tablename__ = "seguidos"
    
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_seguidor = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    @staticmethod
    def crear(us, se):
        nuevo = Seguidos(id_usuario=us, id_seguidor=se)
        guardar(nuevo)
        
    @staticmethod
    def listarSeguidores(us):
        lista = session.query(Seguidos).filter_by(id_usuario=us).all()
        return lista
        
    @staticmethod
    def listarSeguidos(se):
        lista = session.query(Seguidos).filter_by(id_seguidor=se).all()
        return lista