from typing import Dict, List

from pydantic import BaseModel


class RiskResponse(BaseModel):
    client_id: str
    risk_profile: str
    highest_exposure_sector: str
    invested_value: float
    current_value: float
    profit_loss: float


class ClientHolding(BaseModel):
    stock_symbol: str
    quantity: float
    purchase_price: float
    current_price: float
    sector: str
    invested_value: float
    current_value: float


class ClientDashboard(BaseModel):
    client_id: str
    risk_profile: str
    invested_value: float
    current_value: float
    profit_loss: float
    holdings: List[ClientHolding]
    portfolio_allocation: Dict[str, float]
    portfolio_timeseries: List[Dict[str, float]]
    assets_timeseries: List[Dict[str, float]]
    ai_explainability: str
    ai_recommendation: Dict[str, str]


class RiskSummary(BaseModel):
    total_portfolio_value: float
    overall_risk_score: float
    sharpe_score: float
    sector_penalty: float
    allocation_penalty: float
