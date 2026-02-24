from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
PORTFOLIO_FILE = DATA_DIR / "client_portfolios.csv"
RISK_PROFILE_FILE = DATA_DIR / "client_risk_profile.csv"
SECTOR_FILE = DATA_DIR / "sector_mapping.csv"


def load_portfolios() -> pd.DataFrame:
    return pd.read_csv(PORTFOLIO_FILE)


def load_risk_profiles() -> pd.DataFrame:
    return pd.read_csv(RISK_PROFILE_FILE)


def load_sector_mapping() -> pd.DataFrame:
    return pd.read_csv(SECTOR_FILE)
