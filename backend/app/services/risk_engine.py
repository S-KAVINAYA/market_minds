import pandas as pd
from .data_loader import load_portfolios, load_risk_profiles, load_sector_mapping


def calculate_client_risk(client_id):

    portfolios = load_portfolios()
    risk_profiles = load_risk_profiles()
    sector_map = load_sector_mapping()

    client_data = portfolios[portfolios["client_id"] == client_id]

    if client_data.empty:
        return {"error": "Client not found"}

    # Merge sector info
    client_data = client_data.merge(
        sector_map,
        on="stock_symbol",
        how="left"
    )

    total_invested = (client_data["quantity"] * client_data["purchase_price"]).sum()
    total_current = (client_data["quantity"] * client_data["current_price"]).sum()

    # Sector exposure
    client_data["current_value"] = client_data["quantity"] * client_data["current_price"]

    sector_exposure = (
        client_data.groupby("sector")["current_value"]
        .sum()
        .sort_values(ascending=False)
    )

    highest_sector = sector_exposure.index[0]

    risk_level = risk_profiles[
        risk_profiles["client_id"] == client_id
    ]["risk_profile"].values

    risk_profile = risk_level[0] if len(risk_level) > 0 else "Unknown"

    return {
        "client_id": client_id,
        "risk_profile": risk_profile,
        "highest_exposure_sector": highest_sector,
        "invested_value": float(total_invested),
        "current_value": float(total_current),
        "profit_loss": float(total_current - total_invested)
    }
