from sqlalchemy import create_engine, text
from sqlalchemy.orm import  declarative_base, sessionmaker

engine = create_engine(f"mysql+pymysql://pyuser:Usuario.22@localhost:3306/pytest")

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

def guardar(nuevo):
    session.add(nuevo)
    session.commit()#Guardar en la base de datos // se debe cambiar por try-cach