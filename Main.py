from Usuario import Usuario, Seguidos
from Pubicacion import Publicacion
from Comentario import Comentario
from dbInit import Base, engine


Base.metadata.create_all(engine)

#Usuario.crear("Happy", "guay")

#Publicacion.crear("1", "Viva la vida")

#Comentario.crear(1, 1, "viva tu")

#Seguidos.crear(2, 1)


for i in Seguidos.listarSeguidores(2):
    print (i);
