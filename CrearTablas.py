from Usuario import Usuario, Seguidos
from Pubicacion import Publicacion
from Comentario import Comentario
from dbInit import Base, engine


Base.metadata.create_all(engine)
