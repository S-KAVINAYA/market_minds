from fastapi import FastAPI

from app.routes.clients_routes import router as clients_router
from app.routes.risk_routes import router as risk_router

app = FastAPI(title="Market Minds Backend", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(risk_router)
app.include_router(clients_router)
