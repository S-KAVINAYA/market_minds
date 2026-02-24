import pandas as pd

portfolio_df = pd.read_csv("data/client_portfolios.csv")
risk_df = pd.read_csv("data/client_risk_profile.csv")

def get_all_clients():
    return portfolio_df["client_id"].unique().tolist()

def get_client_portfolio(client_id):
    return portfolio_df[portfolio_df["client_id"] == client_id]

def get_client_risk_profile(client_id):
    return risk_df[risk_df["client_id"] == client_id].iloc[0]
