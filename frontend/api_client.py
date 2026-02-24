import json
import random
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

MANAGER_FILE = Path(__file__).resolve().parent / "managers.json"


def _ensure_manager_store():
    if not MANAGER_FILE.exists():
        MANAGER_FILE.write_text("{}", encoding="utf-8")


def load_managers():
    _ensure_manager_store()
    try:
        raw = MANAGER_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return {}
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        MANAGER_FILE.write_text("{}", encoding="utf-8")
        return {}


def save_managers(data):
    _ensure_manager_store()
    MANAGER_FILE.write_text(json.dumps(data), encoding="utf-8")


def signup_manager_api(username, password):
    managers = load_managers()
    username = username.strip()

    if username == "":
        return {"status": "error", "message": "Manager ID cannot be empty"}

    if username in managers:
        return {"status": "error", "message": "Manager ID already exists"}

    managers[username] = password
    save_managers(managers)
    return {"status": "success"}


def login_manager_api(username, password):
    managers = load_managers()
    if username in managers and managers[username] == password:
        return {"status": "success", "manager_id": username}
    return {"status": "error", "message": "Invalid credentials"}


def _stock_catalog():
    return [
        {"symbol": "AAPL", "name": "Apple", "risk_level": "Moderate", "sector": "Technology"},
        {"symbol": "MSFT", "name": "Microsoft", "risk_level": "Low", "sector": "Technology"},
        {"symbol": "TSLA", "name": "Tesla", "risk_level": "High", "sector": "Automotive"},
        {"symbol": "NVDA", "name": "NVIDIA", "risk_level": "High", "sector": "Technology"},
        {"symbol": "JPM", "name": "JPMorgan", "risk_level": "Low", "sector": "Financials"},
        {"symbol": "SPY", "name": "S&P 500 ETF", "risk_level": "Low", "sector": "ETF"},
        {"symbol": "QQQ", "name": "Nasdaq 100 ETF", "risk_level": "Moderate", "sector": "ETF"},
    ]


def fetch_stock_universe(risk_level="All"):
    stocks = _stock_catalog()
    return stocks if risk_level == "All" else [s for s in stocks if s["risk_level"] == risk_level]


def fetch_clients(manager_id):
    clients = []
    rng = random.Random(abs(hash(manager_id)) % (2**32))
    stocks = _stock_catalog()

    for i in range(1, 51):
        invested = rng.randint(100000, 500000)
        current = invested - rng.randint(-20000, 60000)
        risk_level = rng.choice(["Low", "Moderate", "High"])
        risk_asset = rng.choice(["Stocks", "Bonds", "ETFs"])

        chosen = rng.sample(stocks, 3)
        raw_weights = [rng.randint(10, 50) for _ in chosen]
        weight_sum = sum(raw_weights)
        holdings = []
        for stock, wt in zip(chosen, raw_weights):
            allocation = wt / weight_sum
            holdings.append({
                "symbol": stock["symbol"],
                "sector": stock["sector"],
                "allocation": round(allocation * 100, 2),
                "value": round(current * allocation, 2),
            })

        clients.append({
            "client_id": f"C{i:04}",
            "risk_level": risk_level,
            "risk_asset": risk_asset,
            "invested_value": invested,
            "current_value": current,
            "portfolio": {
                "Stocks": rng.randint(30, 70),
                "Bonds": rng.randint(10, 40),
                "ETFs": rng.randint(5, 20),
                "Cash": rng.randint(5, 20),
            },
            "holdings": holdings,
        })

    return clients


@lru_cache(maxsize=128)
def fetch_clients_cached(manager_id):
    return fetch_clients(manager_id)


def fetch_client_trend(client_id, periods=180):
    rng = np.random.default_rng(abs(hash(f"client:{client_id}")) % (2**32))
    dates = pd.date_range(end=pd.Timestamp.today(), periods=periods)
    returns = rng.normal(0.001, 0.02, periods)
    values = 100000 * (1 + returns).cumprod()
    return pd.DataFrame({"Date": dates, "Value": values})


def fetch_stock_trend(symbol, periods=180):
    rng = np.random.default_rng(abs(hash(symbol)) % (2**32))
    dates = pd.date_range(end=pd.Timestamp.today(), periods=periods)
    base = 100 + rng.integers(0, 70)
    drift = rng.normal(0.0007, 0.0005)
    volatility = rng.uniform(0.01, 0.03)
    returns = rng.normal(drift, volatility, periods)
    prices = base * (1 + returns).cumprod()
    return pd.DataFrame({"Date": dates, "Price": prices, "Symbol": symbol})


def fetch_customer_comparison_trend(client_ids, periods=180):
    if not client_ids:
        return pd.DataFrame(columns=["Date", "Value", "Client"])

    dates = pd.date_range(end=pd.Timestamp.today(), periods=periods)
    rows = []
    for client_id in client_ids:
        rng = np.random.default_rng(abs(hash(client_id)) % (2**32))
        returns = rng.normal(0.001, 0.018, periods)
        values = 100000 * (1 + returns).cumprod()
        rows.extend({"Date": d, "Value": v, "Client": client_id} for d, v in zip(dates, values))
    return pd.DataFrame(rows)


def fetch_client_asset_timeseries(client, periods=180):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=periods)
    rows = []
    for asset, alloc in client["portfolio"].items():
        rng = np.random.default_rng(abs(hash(f"{client['client_id']}:{asset}")) % (2**32))
        drift = 0.0004 + (alloc / 10000)
        vol = 0.008 + (alloc / 8000)
        returns = rng.normal(drift, vol, periods)
        base = client["invested_value"] * (alloc / 100)
        values = base * (1 + returns).cumprod()
        rows.extend({"Date": d, "Value": v, "Asset": asset} for d, v in zip(dates, values))
    return pd.DataFrame(rows)


def fetch_risk_level_asset_timeseries(clients, periods=120):
    if not clients:
        return pd.DataFrame(columns=["Date", "Value", "Asset", "Risk"])

    out = []
    grouped = {"Low": [], "Moderate": [], "High": []}
    for c in clients:
        grouped[c["risk_level"]].append(c)

    for risk, risk_clients in grouped.items():
        if not risk_clients:
            continue
        dates = pd.date_range(end=pd.Timestamp.today(), periods=periods)
        for asset in ["Stocks", "Bonds", "ETFs", "Cash"]:
            avg_alloc = np.mean([c["portfolio"].get(asset, 0) for c in risk_clients]) / 100
            total_value = sum(c["current_value"] for c in risk_clients)
            rng = np.random.default_rng(abs(hash(f"risk:{risk}:{asset}")) % (2**32))
            drift = 0.0003 + avg_alloc / 1500
            vol = 0.005 + avg_alloc / 800
            returns = rng.normal(drift, vol, periods)
            values = (total_value * avg_alloc) * (1 + returns).cumprod()
            out.extend(
                {"Date": d, "Value": v, "Asset": asset, "Risk": risk}
                for d, v in zip(dates, values)
            )

    return pd.DataFrame(out)


def build_risk_dashboard_metrics(clients):
    if not clients:
        return {"total_portfolio_value": 0, "overall_risk_score": 0, "sharpe_score": 0, "sector_penalty": 0, "allocation_penalty": 0}

    total_portfolio = sum(c["current_value"] for c in clients)
    risk_map = {"Low": 1, "Moderate": 2, "High": 3}
    weighted_risk = sum(risk_map[c["risk_level"]] * c["current_value"] for c in clients) / max(total_portfolio, 1)
    returns = np.array([(c["current_value"] - c["invested_value"]) / max(c["invested_value"], 1) for c in clients])

    sector_values = {}
    allocation_penalties = []
    for client in clients:
        for h in client.get("holdings", []):
            sector_values[h["sector"]] = sector_values.get(h["sector"], 0) + h["value"]
        allocation_penalties.append(sum(abs(client["portfolio"].get(k, 0) - 25) for k in ["Stocks", "Bonds", "ETFs", "Cash"]) / 4)

    sector_weights = np.array(list(sector_values.values())) / max(sum(sector_values.values()), 1)
    return {
        "total_portfolio_value": round(total_portfolio, 2),
        "overall_risk_score": round((weighted_risk / 3) * 100, 2),
        "sharpe_score": round(float(np.mean(returns) / (np.std(returns) + 1e-6)), 2),
        "sector_penalty": round(float(np.sum(sector_weights**2) * 100), 2),
        "allocation_penalty": round(float(np.mean(allocation_penalties)), 2),
    }


def group_clients_by_ticker(clients):
    ticker_map = {}
    for client in clients:
        for h in client.get("holdings", []):
            entry = ticker_map.setdefault(h["symbol"], {"total_value": 0, "clients": set()})
            entry["total_value"] += h["value"]
            entry["clients"].add(client["client_id"])

    return sorted([
        {"ticker": s, "total_value": round(v["total_value"], 2), "client_count": len(v["clients"]), "clients": sorted(v["clients"])}
        for s, v in ticker_map.items()
    ], key=lambda x: x["total_value"], reverse=True)


def generate_ticker_drop_alerts(clients, drop_threshold=-0.05):
    alerts = []
    for item in group_clients_by_ticker(clients):
        df = fetch_stock_trend(item["ticker"], periods=14)
        pct = (df["Price"].iloc[-1] - df["Price"].iloc[0]) / max(df["Price"].iloc[0], 1)
        if pct <= drop_threshold:
            alerts.append({"ticker": item["ticker"], "drop_pct": round(pct * 100, 2), "affected_clients": item["clients"]})
    return alerts


def ai_risk_explainability(client):
    delta = client["current_value"] - client["invested_value"]
    top_holding = max(client.get("holdings", []), key=lambda h: h["value"], default={"symbol": "N/A", "sector": "N/A"})
    return (
        f"AI Explainability: {client['client_id']} is {client['risk_level']} risk because concentration is highest in "
        f"{top_holding['symbol']} ({top_holding['sector']}) and key allocation is in {client['risk_asset']}. "
        f"PnL vs invested capital is ₹{delta:,.0f}."
    )


def ai_stock_recommendation(risk_level):
    candidates = fetch_stock_universe(risk_level)
    if not candidates:
        return {"symbol": "N/A", "expected_return_pct": 0, "explanation": "No suitable stock found.", "best_time": "N/A"}

    best = None
    best_score = -1e9
    for stock in candidates:
        hist = fetch_stock_trend(stock["symbol"], periods=120)
        daily = hist["Price"].pct_change().dropna()
        score = float((daily.mean() * 252) / (daily.std() * np.sqrt(252) + 1e-6))
        if score > best_score:
            best_score = score
            best = stock

    forecast = forecast_stock_prices(best["symbol"], horizon=14)
    forecast_only = forecast[forecast["Type"] == "Forecast"].reset_index(drop=True)
    best_idx = int(forecast_only["Price"].argmin())
    best_date = forecast_only.loc[best_idx, "Date"].strftime("%Y-%m-%d")

    expected = float((forecast_only["Price"].iloc[-1] - forecast_only["Price"].iloc[0]) / max(forecast_only["Price"].iloc[0], 1) * 100)
    return {
        "symbol": best["symbol"],
        "expected_return_pct": round(expected, 2),
        "best_time": best_date,
        "explanation": f"AI suggests {best['symbol']} for {risk_level} bucket based on strongest risk-adjusted momentum and forecast trajectory.",
    }


def forecast_stock_prices(symbol, horizon=30):
    hist = fetch_stock_trend(symbol, periods=180)
    daily = hist["Price"].pct_change().dropna()
    drift = float(daily.tail(60).mean())
    last_price = float(hist["Price"].iloc[-1])
    dates = pd.date_range(start=hist["Date"].iloc[-1] + pd.Timedelta(days=1), periods=horizon)

    prices = []
    price = last_price
    for _ in range(horizon):
        price *= (1 + drift)
        prices.append(price)

    forecast = pd.DataFrame({"Date": dates, "Price": prices, "Type": "Forecast"})
    history = hist[["Date", "Price"]].tail(60).copy()
    history["Type"] = "History"
    return pd.concat([history, forecast], ignore_index=True)


def ai_explain_risk_asset_timeseries(df, risk_level):
    subset = df[df["Risk"] == risk_level]
    if subset.empty:
        return "No data available for this risk level."

    latest = subset.sort_values("Date").groupby("Asset")["Value"].last()
    best_asset = latest.idxmax()
    weak_asset = latest.idxmin()
    rec = ai_stock_recommendation(risk_level)
    return (
        f"AI insight ({risk_level}): {best_asset} is currently leading while {weak_asset} is lagging in the risk-bucket time series. "
        f"Suggested action: accumulate {rec['symbol']} around {rec['best_time']} based on forecasted setup."
    )


def recommendation_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
