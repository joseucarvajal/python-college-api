from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db, init_db
from app.domain.models import Curso
from app.use_cases.curso_use_cases import crear_curso, listar_cursos
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import date

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class CursoCreate(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_finalizacion: date
    porcentaje_corte_1: float
    porcentaje_corte_2: float
    porcentaje_corte_3: float

    @field_validator('nombre')
    def check_nombre(cls, v):
        print("llega pos")
        if v is None or v == "":
            raise ValueError("El nombre es requerido")
        return v





@app.post("/cursos")
async def crear_nuevo_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    try:
        return crear_curso(db, **curso.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cursos")
async def obtener_cursos(db: Session = Depends(get_db)):
    return listar_cursos(db)