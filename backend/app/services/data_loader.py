import pandas as pd

PORTFOLIO_FILE = "data/client_portfolios.csv"
RISK_PROFILE_FILE = "data/client_risk_profile.csv"
SECTOR_FILE = "data/sector_mapping.csv"


def load_portfolios():
    return pd.read_csv(PORTFOLIO_FILE)


def load_risk_profiles():
    return pd.read_csv(RISK_PROFILE_FILE)


def load_sector_mapping():
    return pd.read_csv(SECTOR_FILE)
