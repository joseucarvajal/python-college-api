from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.domain.models import Curso, Estudiante
from app.use_cases.curso_use_cases import crear_curso, listar_cursos
from app.use_cases.estudiante_use_cases import crear_estudiantes_bulk, listar_estudiantes_por_curso, EstudianteCreate
from pydantic import BaseModel
from datetime import date
from typing import List
import uuid

router = APIRouter()

class CursoCreate(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_finalizacion: date
    porcentaje_corte_1: float
    porcentaje_corte_2: float
    porcentaje_corte_3: float

class CursoResponse(BaseModel):
    id: uuid.UUID
    nombre: str
    fecha_inicio: date
    fecha_finalizacion: date
    porcentaje_corte_1: float
    porcentaje_corte_2: float
    porcentaje_corte_3: float

    class Config:
        orm_mode = True

class EstudianteResponse(BaseModel):
    id: uuid.UUID
    nombre: str
    email: str
    curso_id: uuid.UUID

    class Config:
        orm_mode = True

@router.post("/cursos", response_model=CursoResponse)
def crear_nuevo_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    nuevo_curso = Curso(**curso.model_dump())
    return crear_curso(db, nuevo_curso)

@router.get("/cursos", response_model=List[CursoResponse])
def obtener_cursos(db: Session = Depends(get_db)):
    return listar_cursos(db)

@router.post("/cursos/{curso_id}/estudiantes", response_model=List[EstudianteResponse])
def crear_estudiantes_en_bulk(curso_id: str, estudiantes: List[EstudianteCreate], db: Session = Depends(get_db)):
    try:
        nuevos_estudiantes = crear_estudiantes_bulk(db, curso_id, estudiantes)
        return nuevos_estudiantes
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/cursos/{curso_id}/estudiantes", response_model=List[EstudianteResponse])
def obtener_estudiantes_por_curso(curso_id: str, db: Session = Depends(get_db)):
    estudiantes = listar_estudiantes_por_curso(db, curso_id)
    if not estudiantes:
        raise HTTPException(status_code=404, detail="No se encontraron estudiantes para este curso")
    return estudiantes
