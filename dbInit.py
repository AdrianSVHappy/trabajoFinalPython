from sqlalchemy import create_engine, text
from sqlalchemy.orm import  declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine(f"mysql+pymysql://pyuser:Usuario.22@localhost:3306/pytest")

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

def guardar(nuevo):
    try:
        session.add(nuevo)
        session.commit() #Guardar en la base de datos
    except IntegrityError as e:
        session.rollback() # Revertimos los cambios
        
def actualizar():
    try:
        session.commit() 
    except IntegrityError as e:
        session.rollback()