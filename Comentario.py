from dbInit import Base, guardar
from sqlalchemy import Column, Integer, Text, ForeignKey

class Comentario(Base):
    
    __tablename__ = "comentarios"
    
    id = Column(Integer, primary_key=True)
    id_us = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_pub = Column(Integer, ForeignKey("publicaciones.id"), nullable=False)
    texto = Column(Text)
    
    @staticmethod
    def crear(us, pub, texto):
        nuevo = Comentario(id_us=us, id_pub=pub, texto=texto)
        guardar(nuevo)
