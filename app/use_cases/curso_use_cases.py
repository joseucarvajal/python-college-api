from sqlalchemy.orm import Session
from app.domain.models import Curso
from typing import List
from datetime import date

def crear_curso(db: Session, nombre: str, fecha_inicio: date, fecha_finalizacion: date,
                porcentaje_corte_1: float, porcentaje_corte_2: float, porcentaje_corte_3: float) -> Curso:
    nuevo_curso = Curso(
        nombre=nombre,
        fecha_inicio=fecha_inicio,
        fecha_finalizacion=fecha_finalizacion,
        porcentaje_corte_1=porcentaje_corte_1,
        porcentaje_corte_2=porcentaje_corte_2,
        porcentaje_corte_3=porcentaje_corte_3
    )
    db.add(nuevo_curso)
    db.commit()
    db.refresh(nuevo_curso)
    return nuevo_curso

def listar_cursos(db: Session) -> List[Curso]:
    return db.query(Curso).all()