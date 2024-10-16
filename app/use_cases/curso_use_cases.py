from sqlalchemy.orm import Session
from app.domain.models import Curso
from typing import List
from datetime import date

def crear_curso(db: Session, curso: Curso) -> Curso:
    if not curso.nombre or not curso.nombre.strip():
        raise ValueError("El nombre del curso no puede estar vacío")
    
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

def listar_cursos(db: Session) -> List[Curso]:
    return db.query(Curso).all()
