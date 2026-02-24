from fastapi import APIRouter

from app.models.schemas import RiskResponse, RiskSummary
from app.services.risk_engine import (
    calculate_client_risk,
    clients_by_ticker,
    risk_summary,
    stock_recommendation,
    ticker_drop_alerts,
)

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/{client_id}", response_model=RiskResponse)
def get_client_risk(client_id: str):
    return calculate_client_risk(client_id)


@router.get("/summary/metrics", response_model=RiskSummary)
def get_risk_summary():
    return risk_summary()


@router.get("/summary/by-ticker")
def get_ticker_grouping():
    return clients_by_ticker()


@router.get("/summary/alerts")
def get_ticker_alerts(drop_threshold: float = -0.05):
    return ticker_drop_alerts(drop_threshold)


@router.get("/recommendation/{risk_level}")
def get_recommendation(risk_level: str):
    return stock_recommendation(risk_level)
