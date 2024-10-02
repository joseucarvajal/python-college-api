from fastapi import FastAPI
from app.interfaces.routes import router
from app.infrastructure.database import init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)