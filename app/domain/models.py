from sqlalchemy import Column, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import date

Base = declarative_base()

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(100), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_finalizacion = Column(Date, nullable=False)
    porcentaje_corte_1 = Column(Float, nullable=False)
    porcentaje_corte_2 = Column(Float, nullable=False)
    porcentaje_corte_3 = Column(Float, nullable=False)

    def __init__(self, nombre: str, fecha_inicio: date, fecha_finalizacion: date,
                 porcentaje_corte_1: float, porcentaje_corte_2: float, porcentaje_corte_3: float):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_finalizacion = fecha_finalizacion
        self.porcentaje_corte_1 = porcentaje_corte_1
        self.porcentaje_corte_2 = porcentaje_corte_2
        self.porcentaje_corte_3 = porcentaje_corte_3