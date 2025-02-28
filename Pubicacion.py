from dbInit import Base, guardar, session
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from Comentario import Comentario
import os

"""
Clase que representa una publicación
id -> id de la publicación
id_usuario -> id del usuario que la ha publicado
fecha -> fecha en la que se ha creado la publicación
foto -> guarda si o no tiene foto la publicación
texto -> contenido de la publicación
"""
class Publicacion(Base):
    
    __tablename__ = "publicaciones"
    
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id",  ondelete='CASCADE'), nullable=False)
    fecha = Column(DateTime, nullable=False)
    foto = Column(Boolean, nullable=True)
    texto = Column(Text)

    user = relationship("Usuario", back_populates="publicaciones")
    
    """
    Metodo estatico para crear una publicación
    idU -> id del usuario que la ha publicado
    texto -> contenido de la publicacion
    (Proximamente foto)
    """
    @staticmethod
    def crear(idU, texto, foto_filename=None):
        like = 0
        fecha = datetime.today()

        # Se marca la publicación como True si se pasó un nombre de archivo, sino False
        foto = True if foto_filename else False

        nuevo = Publicacion(id_usuario=idU, fecha=fecha, texto=texto, like=like, foto=foto)
        guardar(nuevo)

        
            
    """
    Metodo para modificar una publicación
    id -> Id de la publicación que se quiere modificar
    texto -> Nuevo contenido de la publicación
    """
    @staticmethod
    def modificar(id, texto=""):
        pub = session.query(Publicacion).filter_by(id=id).first()
        
        if texto:
            pub.texto = texto
            
        session.commit()
    
    """
    Metodo que devuelve una lista con las publicaciones de un usuario en especifico o de todos
    id -> Atributo opcional, id del usuario que ha subido las publicaciones
    """
    @staticmethod
    def mostrarUs(id=""):
        if id:
            lista = session.query(Publicacion).filter_by(id_usuario=id).order_by(Publicacion.fecha.desc()).all()
        else:
            lista = session.query(Publicacion).order_by(Publicacion.fecha.desc()).all()
            
        return lista
    
    """
    Metodo estatico para mostrar los comentarios de una publicacion
    id -> id de la publicación
    """
    @staticmethod    
    def mostrarCom(id):
        return session.query(Comentario).filter_by(id_pub=id).all()
    
    
    """
    Metodo estatico para eliminar una publicación
    id -> id de la publicación que se va a eliminar
    """
    @staticmethod
    def eliminar(id):
        session.query(Publicacion).filter_by(id=id).delete()
        session.commit()
        
        

    
    