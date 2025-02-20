from dbInit import Base, session, guardar
from sqlalchemy import Column, Integer, VARCHAR, Text, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

class Usuario(Base):
    
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(VARCHAR(50), nullable=False)
    passw = Column(VARCHAR(255), nullable=False)
    bio = Column(Text)
    foto = Column(LargeBinary)
    
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
    def guardar(nombre, passw, bio):
        nuevo = Usuario(nombre=nombre, passw=passw, bio=bio)
        guardar(nuevo)
        
        
    @staticmethod
    def comprobar(n, p=""):
        ret = False
        usuario = None 
         
        if(p == ""):
            usuario = session.query(Usuario).filter_by(nombre=n).all()
        else:
            usuario = session.query(Usuario).filter_by(nombre=n, passw = p).all()
         
        if usuario:
            ret = True
        
        return ret
            
    @staticmethod
    def crear(nom, passw1, passw2, bio=None):
        mensaje = "OK"
        if (passw1 != passw2):
            mensaje = "Error: Las contraseñas no coinciden"
        elif(Usuario.comprobar(nom)):
            mensaje = "Error: El nombre de usuario está en uso"
        else:
            Usuario.guardar(nom, passw1, bio)

        return mensaje
    
    @staticmethod
    def modificar(id):
        user = session.query(Usuario).filter_by(id=id).first()
        

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