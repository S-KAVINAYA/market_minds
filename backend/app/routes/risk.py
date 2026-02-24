from fastapi import APIRouter
from app.services.risk_engine import evaluate_client

router = APIRouter()

@router.get("/risk/{client_id}")
def get_risk(client_id: str):
    return evaluate_client(client_id)
