from sqlalchemy import Column, Integer, Boolean, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Crear la base declarativa
Base = declarative_base()

# Motor de SQLite: crea el archivo resultados.db en la carpeta servidor/
engine = create_engine('sqlite:///servidor/resultados.db', echo=False)
Session = sessionmaker(bind=engine)

class ResultadoNReinas(Base):
    __tablename__ = 'nreinas'
    id = Column(Integer, primary_key=True)
    N = Column(Integer, nullable=False)
    resuelto = Column(Boolean, nullable=False)
    movimientos = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ResultadoCaballo(Base):
    __tablename__ = 'caballo'
    id = Column(Integer, primary_key=True)
    posicion_inicial = Column(String, nullable=False)
    movimientos = Column(Integer, nullable=False)
    completado = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ResultadoHanoi(Base):
    __tablename__ = 'hanoi'
    id = Column(Integer, primary_key=True)
    discos = Column(Integer, nullable=False)
    movimientos = Column(Integer, nullable=False)
    resuelto = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
