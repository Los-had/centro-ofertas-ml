from fastapi import FastAPI

app = FastAPI(
    title="Central de Ofertas ML",
    description="Sistema de monitoramento, análise e publicação de ofertas.",
    version="0.1.0",
)

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
        "database": "not connected yet",
    }
