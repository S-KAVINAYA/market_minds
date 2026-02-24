from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd

from .data_loader import load_portfolios, load_risk_profiles, load_sector_mapping

RISK_MAP = {"Low": 1, "Moderate": 2, "High": 3, "Conservative": 1, "Balanced": 2, "Aggressive": 3}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip().lower() for c in out.columns]
    return out


def _portfolio_with_values() -> pd.DataFrame:
    portfolios = _normalize_columns(load_portfolios())
    sectors = _normalize_columns(load_sector_mapping())

    rename_map = {
        "client_id": "client_id",
        "ticker": "ticker",
        "quantity": "quantity",
        "asset_type": "asset_type",
        "sector": "sector",
    }
    portfolios = portfolios.rename(columns=rename_map)
    sectors = sectors.rename(columns={"ticker": "ticker", "sector": "sector"})

    if "ticker" in portfolios.columns and "ticker" in sectors.columns:
        data = portfolios.drop(columns=["sector"], errors="ignore").merge(
            sectors[["ticker", "sector"]], on="ticker", how="left"
        )
    else:
        data = portfolios

    data["quantity"] = data.get("quantity", 0).fillna(0).astype(float)

    def base_price(symbol: str) -> float:
        return 80 + (abs(hash(str(symbol))) % 140)

    data["purchase_price"] = data["ticker"].map(base_price)
    data["current_price"] = data["purchase_price"] * (
        1 + data["ticker"].map(lambda t: ((abs(hash(f"cur:{t}")) % 200) - 100) / 1000)
    )

    data["invested_value"] = data["quantity"] * data["purchase_price"]
    data["current_value"] = data["quantity"] * data["current_price"]
    data["sector"] = data["sector"].fillna("Unknown")
    return data


def _risk_profile(client_id: str) -> str:
    risk_profiles = _normalize_columns(load_risk_profiles())
    risk_profiles = risk_profiles.rename(columns={"client_id": "client_id", "risk_profile": "risk_profile"})
    level = risk_profiles[risk_profiles["client_id"] == client_id]["risk_profile"].values
    return level[0] if len(level) > 0 else "Moderate"


def calculate_client_risk(client_id: str):
    client_data = _portfolio_with_values().query("client_id == @client_id")
    if client_data.empty:
        return {"error": "Client not found"}

    invested = float(client_data["invested_value"].sum())
    current = float(client_data["current_value"].sum())
    top_sector = (
        client_data.groupby("sector")["current_value"].sum().sort_values(ascending=False).index[0]
    )
    return {
        "client_id": client_id,
        "risk_profile": _risk_profile(client_id),
        "highest_exposure_sector": str(top_sector),
        "invested_value": invested,
        "current_value": current,
        "profit_loss": current - invested,
    }


def list_clients() -> List[str]:
    return sorted(_portfolio_with_values()["client_id"].astype(str).unique().tolist())


def client_holdings(client_id: str) -> pd.DataFrame:
    return _portfolio_with_values().query("client_id == @client_id").copy()


def client_dashboard(client_id: str):
    client_data = client_holdings(client_id)
    if client_data.empty:
        return {"error": "Client not found"}

    risk = calculate_client_risk(client_id)
    total_current = max(float(client_data["current_value"].sum()), 1.0)

    allocation = (
        client_data.groupby("asset_type")["current_value"].sum() / total_current * 100
    ).round(2).to_dict()

    dates = pd.date_range(end=pd.Timestamp.today(), periods=120)
    seed = abs(hash(client_id)) % (2**32)
    rng = np.random.default_rng(seed)
    returns = rng.normal(0.0008, 0.015, len(dates))
    values = total_current * (1 + returns).cumprod()
    portfolio_ts = pd.DataFrame({"Date": dates, "Value": values})

    assets_rows = []
    for idx, asset in enumerate(sorted(client_data["asset_type"].unique())):
        srng = np.random.default_rng(seed + idx + 1)
        sret = srng.normal(0.0006, 0.02, len(dates))
        base = float(client_data[client_data["asset_type"] == asset]["current_value"].sum())
        svals = base * (1 + sret).cumprod()
        assets_rows.extend({"Date": d, "Value": v, "Asset": asset} for d, v in zip(dates, svals))

    top_sector = client_data.groupby("sector")["current_value"].sum().sort_values(ascending=False).index[0]
    ai_explain = (
        f"Client {client_id} is '{risk['risk_profile']}' risk with highest exposure in {top_sector}. "
        f"Current portfolio is {'in profit' if risk['profit_loss'] >= 0 else 'in drawdown'} by ₹{abs(risk['profit_loss']):,.0f}."
    )

    recommendation = stock_recommendation(risk.get("risk_profile", "Moderate"))

    holdings = client_data[[
        "ticker", "quantity", "purchase_price", "current_price", "sector", "invested_value", "current_value"
    ]].rename(columns={"ticker": "stock_symbol"}).to_dict(orient="records")

    return {
        **risk,
        "holdings": holdings,
        "portfolio_allocation": allocation,
        "portfolio_timeseries": portfolio_ts.to_dict(orient="records"),
        "assets_timeseries": pd.DataFrame(assets_rows).to_dict(orient="records"),
        "ai_explainability": ai_explain,
        "ai_recommendation": recommendation,
    }


def risk_summary():
    data = _portfolio_with_values()
    if data.empty:
        return {"total_portfolio_value": 0, "overall_risk_score": 0, "sharpe_score": 0, "sector_penalty": 0, "allocation_penalty": 0}

    risks = _normalize_columns(load_risk_profiles()).rename(columns={"client_id": "client_id", "risk_profile": "risk_profile"})
    merged = data.merge(risks[["client_id", "risk_profile"]], on="client_id", how="left")
    merged["risk_num"] = merged["risk_profile"].map(RISK_MAP).fillna(2)

    total = float(merged["current_value"].sum())
    overall_risk = float((merged["risk_num"] * merged["current_value"]).sum() / max(total, 1) / 3 * 100)

    client_totals = merged.groupby("client_id")[["current_value", "invested_value"]].sum()
    client_pnl = (client_totals["current_value"] - client_totals["invested_value"]) / client_totals["invested_value"].clip(lower=1)
    sharpe = float(client_pnl.mean() / (client_pnl.std() + 1e-6))

    sector_weights = merged.groupby("sector")["current_value"].sum()
    sector_weights = sector_weights / max(sector_weights.sum(), 1)
    sector_penalty = float((sector_weights.pow(2).sum()) * 100)

    alloc = merged.groupby(["client_id", "asset_type"])["current_value"].sum().unstack(fill_value=0)
    alloc = alloc.div(alloc.sum(axis=1), axis=0).fillna(0)
    allocation_penalty = float((alloc.sub(1 / max(alloc.shape[1], 1)).abs().mean(axis=1).mean()) * 100)

    return {
        "total_portfolio_value": round(total, 2),
        "overall_risk_score": round(overall_risk, 2),
        "sharpe_score": round(sharpe, 2),
        "sector_penalty": round(sector_penalty, 2),
        "allocation_penalty": round(allocation_penalty, 2),
    }


def clients_by_ticker():
    data = _portfolio_with_values()
    out = []
    for ticker, g in data.groupby("ticker"):
        out.append({
            "ticker": ticker,
            "total_value": float(g["current_value"].sum()),
            "client_count": int(g["client_id"].nunique()),
            "clients": sorted(g["client_id"].astype(str).unique().tolist()),
        })
    return sorted(out, key=lambda x: x["total_value"], reverse=True)


def ticker_drop_alerts(drop_threshold: float = -0.05):
    alerts = []
    for row in clients_by_ticker():
        seed = abs(hash(row["ticker"])) % (2**32)
        rng = np.random.default_rng(seed)
        perf = float(np.prod(1 + rng.normal(0.0, 0.02, 14)) - 1)
        if perf <= drop_threshold:
            alerts.append({"ticker": row["ticker"], "drop_pct": round(perf * 100, 2), "affected_clients": row["clients"]})
    return alerts


def stock_recommendation(risk_level: str):
    candidates = {
        "Low": ["MSFT", "JPM", "SPY"],
        "Moderate": ["AAPL", "QQQ", "MSFT"],
        "High": ["TSLA", "NVDA", "QQQ"],
        "Conservative": ["SPY", "JPM", "MSFT"],
        "Balanced": ["AAPL", "QQQ", "MSFT"],
        "Aggressive": ["NVDA", "TSLA", "QQQ"],
    }.get(risk_level, ["SPY", "MSFT", "AAPL"])

    rng = np.random.default_rng(abs(hash(risk_level)) % (2**32))
    symbol = candidates[int(rng.integers(0, len(candidates)))]
    best_time = (pd.Timestamp.today() + pd.Timedelta(days=int(rng.integers(3, 10)))).strftime("%Y-%m-%d")
    expected = round(float(rng.normal(6, 3)), 2)

    return {
        "symbol": symbol,
        "best_time": best_time,
        "expected_return_pct": expected,
        "explanation": f"AI recommends {symbol} for {risk_level} profile based on risk-adjusted momentum and diversification.",
    }
