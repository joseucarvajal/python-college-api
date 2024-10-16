from fastapi import FastAPI, Request
from app.interfaces.routes import router
from app.infrastructure.database import init_db, engine
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.domain.models import Base, Curso, Estudiante
from sqlalchemy import inspect


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field_name = error["loc"][-1]
        if error["type"] == "missing":
            error_msg = f"El valor '{field_name}' es requerido"
        else:
            error_msg = error["msg"]
        errors.append({"campo": field_name, "mensaje": error_msg})
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )

def create_tables():
    inspector = inspect(engine)
    if not inspector.has_table("cursos"):
        Curso.__table__.create(engine)
    if not inspector.has_table("estudiantes"):
        Estudiante.__table__.create(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    create_tables()
    yield

# Crea las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
