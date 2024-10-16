from sqlalchemy.orm import Session
from app.domain.models import Estudiante, Curso
from typing import List
from pydantic import BaseModel

class EstudianteCreate(BaseModel):
    nombre: str
    email: str

def crear_estudiantes_bulk(db: Session, curso_id: str, estudiantes: List[EstudianteCreate]) -> List[Estudiante]:
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise ValueError("El curso especificado no existe")

    nuevos_estudiantes = []
    for estudiante_data in estudiantes:
        nuevo_estudiante = Estudiante(
            nombre=estudiante_data.nombre,
            email=estudiante_data.email,
            curso_id=curso_id
        )
        db.add(nuevo_estudiante)
        nuevos_estudiantes.append(nuevo_estudiante)
    
    db.commit()
    for estudiante in nuevos_estudiantes:
        db.refresh(estudiante)
    return nuevos_estudiantes

def listar_estudiantes_por_curso(db: Session, curso_id: str) -> List[Estudiante]:
    return db.query(Estudiante).filter(Estudiante.curso_id == curso_id).all()
