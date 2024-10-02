from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db, init_db
from app.domain.models import Curso
from app.use_cases.curso_use_cases import crear_curso, listar_cursos
from pydantic import BaseModel
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

@app.get("/")
async def root():
    return {"message": "Hola Mundo"}

@app.post("/cursos")
async def crear_nuevo_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    return crear_curso(db, **curso.dict())

@app.get("/cursos")
async def obtener_cursos(db: Session = Depends(get_db)):
    return listar_cursos(db)