from dbInit import Base, guardar
from sqlalchemy import Column, Integer, Text, LargeBinary, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

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
        like = 0;
        fecha = datetime.today()
        nuevo = Publicacion(id_usuario=idU, fecha=fecha, texto=texto, like=like)
        guardar(nuevo)
   
"""  
   Investigar como se guardan las fotos
    @staticmethod
    def crear(idU, foto):
        like = 0;
        fecha = datetime.today()
        nuevo = Publicacion(id_usuario=idU, fecha=fecha, foto=foto, like=like)
        guardar(nuevo)
"""   