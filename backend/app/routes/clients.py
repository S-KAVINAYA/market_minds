from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.post("/add-client")
def add_client(client_data: dict):
    df = pd.read_csv("data/client_portfolios.csv")
    df = pd.concat([df, pd.DataFrame([client_data])])
    df.to_csv("data/client_portfolios.csv", index=False)
    return {"status": "Client added"}
