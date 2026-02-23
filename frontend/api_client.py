import random
import pandas as pd
import numpy as np

# Simulated persistent managers
MANAGERS = {}

def signup_manager_api(username, password):
    if username in MANAGERS:
        return {"status": "error", "message": "Manager already exists"}
    MANAGERS[username] = password
    return {"status": "success"}

def login_manager_api(username, password):
    if username in MANAGERS and MANAGERS[username] == password:
        return {"status": "success", "manager_id": username}
    return {"status": "error", "message": "Invalid credentials"}


# BACKEND CLIENT DATA STRUCTURE
def fetch_clients(manager_id):

    clients = []

    for i in range(1, 51):  # scalable to 5000 later
        invested = random.randint(100000, 500000)
        current = invested - random.randint(-20000, 60000)

        risk_level = random.choice(["Low", "Moderate", "High"])
        risk_asset = random.choice(["Stocks", "Bonds", "ETFs"])

        clients.append({
            "client_id": f"C{i:03}",
            "risk_level": risk_level,
            "risk_asset": risk_asset,
            "invested_value": invested,
            "current_value": current,
            "portfolio": {
                "Stocks": random.randint(30, 70),
                "Bonds": random.randint(10, 40),
                "ETFs": random.randint(5, 20),
                "Cash": random.randint(5, 20),
            }
        })

    return clients


def fetch_client_trend(client_id):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=180)
    returns = np.random.normal(0.001, 0.02, 180)
    values = 100000 * (1 + returns).cumprod()
    return pd.DataFrame({"Date": dates, "Value": values})
