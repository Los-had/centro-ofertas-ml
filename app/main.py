from fastapi import FastAPI

from app import models
from app.api.routes import router
from app.db.database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Central de Ofertas ML",
    description="Sistema de monitoramento, análise e publicação de ofertas.",
    version="0.1.0",
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "status": "online",
        "app": "Central de Ofertas ML",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": "connected",
    }