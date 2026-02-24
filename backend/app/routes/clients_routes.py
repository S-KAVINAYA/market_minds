from fastapi import APIRouter

from app.services.risk_engine import client_dashboard, list_clients

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("")
def get_clients():
    return {"clients": list_clients()}


@router.get("/{client_id}/dashboard")
def get_client_dashboard(client_id: str):
    return client_dashboard(client_id)
