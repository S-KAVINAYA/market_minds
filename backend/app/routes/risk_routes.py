from fastapi import APIRouter
from app.services.risk_engine import calculate_client_risk

router = APIRouter()


@router.get("/risk/{client_id}")
def get_client_risk(client_id: str):
    return calculate_client_risk(client_id)
