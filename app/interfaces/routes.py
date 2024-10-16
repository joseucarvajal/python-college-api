from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.domain.models import Curso
from app.use_cases.curso_use_cases import crear_curso, listar_cursos
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

@router.post("/cursos", response_model=CursoResponse)
def crear_nuevo_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    nuevo_curso = Curso(**curso.model_dump())
    return crear_curso(db, nuevo_curso)

@router.get("/cursos", response_model=List[CursoResponse])
def obtener_cursos(db: Session = Depends(get_db)):
    return listar_cursos(db)