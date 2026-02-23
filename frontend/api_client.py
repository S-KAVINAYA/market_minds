import json
import os
import random
import pandas as pd
import numpy as np

# ---------------------------
# MANAGER STORAGE (Persistent)
# ---------------------------

MANAGER_FILE = "managers.json"

# Create file if not exists
if not os.path.exists(MANAGER_FILE):
    with open(MANAGER_FILE, "w") as f:
        json.dump({}, f)


def load_managers():
    with open(MANAGER_FILE, "r") as f:
        return json.load(f)


def save_managers(data):
    with open(MANAGER_FILE, "w") as f:
        json.dump(data, f)


# ---------------------------
# SIGNUP (Unique Manager ID)
# ---------------------------

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


# ---------------------------
# LOGIN
# ---------------------------

def login_manager_api(username, password):

    managers = load_managers()

    if username in managers and managers[username] == password:
        return {"status": "success", "manager_id": username}

    return {"status": "error", "message": "Invalid credentials"}


# ---------------------------
# CLIENT DATA (Backend Mock)
# ---------------------------

def fetch_clients(manager_id):
    """
    Simulates backend response.
    Each manager can later have up to 5000 clients.
    """

    clients = []

    for i in range(1, 51):  # Change to 5001 for scaling
        invested = random.randint(100000, 500000)
        current = invested - random.randint(-20000, 60000)

        risk_level = random.choice(["Low", "Moderate", "High"])
        risk_asset = random.choice(["Stocks", "Bonds", "ETFs"])

        clients.append({
            "client_id": f"C{i:04}",
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


# ---------------------------
# TREND DATA (Backend Mock)
# ---------------------------

def fetch_client_trend(client_id):

    dates = pd.date_range(end=pd.Timestamp.today(), periods=180)
    returns = np.random.normal(0.001, 0.02, 180)
    values = 100000 * (1 + returns).cumprod()

    return pd.DataFrame({
        "Date": dates,
        "Value": values
    })
