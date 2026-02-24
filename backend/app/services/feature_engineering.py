import numpy as np

def extract_features(client_df):

    invested = (client_df["quantity"] * client_df["purchase_price"]).sum()
    current = (client_df["quantity"] * client_df["current_price"]).sum()

    returns = (current - invested) / invested
    volatility = np.std(client_df["current_price"])
    concentration = client_df["quantity"].max() / client_df["quantity"].sum()

    return [invested, current, returns, volatility, concentration]
