from fastapi import FastAPI
from app.routes.risk_routes import router

app = FastAPI(title="Investment Risk Backend")

app.include_router(router)
