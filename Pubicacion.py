from dbInit import Base, guardar, session
from sqlalchemy import Column, Integer, Text, LargeBinary, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from Comentario import Comentario

class Publicacion(Base):
    
    __tablename__ = "publicaciones"
    
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    foto = Column(LargeBinary)
    texto = Column(Text)
    like = Column(Integer, nullable=False)

    user = relationship("Usuario", back_populates="publicaciones")
    
    @staticmethod
    def crear(idU, texto):
        like = 0
        fecha = datetime.today()
        nuevo = Publicacion(id_usuario=idU, fecha=fecha, texto=texto, like=like)
        guardar(nuevo)
            
    @staticmethod
    def modificar(id, texto=""):
        pub = session.query(Publicacion).filter_by(id=id).first()
        
        if texto:
            pub.texto = texto
            
        session.commit()
    
    @staticmethod    
    def mostrarCom(id):
        return session.query(Comentario).filter_by(id_pub=id).all()
    
    @staticmethod
    def eliminar(id):
        comentarios = Publicacion.mostrarCom(id)
        for c in comentarios:
            Comentario.eliminar(c.id)
            
        session.query(Publicacion).filterby(id=id).delete()
        
        
    
   
"""  
   Investigar como se guardan las fotos
    @staticmethod
    def crear(idU, foto):
        like = 0;
        fecha = datetime.today()
        nuevo = Publicacion(id_usuario=idU, fecha=fecha, foto=foto, like=like)
        guardar(nuevo)
"""   