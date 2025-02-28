from dbInit import Base, guardar, session
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship


"""
Clase que represenat un comentario de una publicación
id -> id del comentario
id_us -> id del usuario que ha comentado
id_pub -> id de la publicación en la que se ha hecho el comentario
texto -> contenido del comentario
"""
class Comentario(Base):
    
    __tablename__ = "comentarios"
    
    id = Column(Integer, primary_key=True)
    id_us = Column(Integer, ForeignKey("usuarios.id", ondelete='CASCADE'), nullable=False)
    id_pub = Column(Integer, ForeignKey("publicaciones.id", ondelete='CASCADE'), nullable=False)
    texto = Column(Text)
    

    user = relationship("Usuario", back_populates="comentarios")
    
    """
    Metodo estatico para crear un comentario
    us -> Id del usuario que ha hecho el comentario
    pub -> Id de la publicación en la que se hace el comentario
    texto -> Contenido de la publicación
    """
    @staticmethod
    def crear(us, pub, texto):
        nuevo = Comentario(id_us=us, id_pub=pub, texto=texto)
        guardar(nuevo)

    """
    Metodo estatico para modificar un comentario
    id -> Id del comentario que se quiere modificar
    texto -> Atributo opcional, nuevo contenido del comentario
    """
    @staticmethod
    def modificar(id, texto=""):
        com = session.query(Comentario).filter_by(id=id).first()

        if texto:
            com.text = com
            
        session.commit()

    """
    Metodo estatico que elimina un comentario
    id -> Id del comentario que se quiere eliminar
    """
    @staticmethod
    def eliminar(id):
        session.query(Comentario).filterby(id=id).delete()
        session.commit