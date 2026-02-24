import yfinance as yf
import pandas as pd

def fetch_fund_history(ticker):
    data = yf.download(ticker, period="6mo", interval="1d")
    data.reset_index(inplace=True)
    return data[["Date", "Close"]]

def calculate_volatility(ticker):
    data = yf.download(ticker, period="6mo")
    returns = data["Close"].pct_change().dropna()
    return returns.std() * (252 ** 0.5)
