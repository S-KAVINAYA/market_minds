import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def generate_performance():
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=180)
    returns = np.random.normal(0.001, 0.02, 180)
    portfolio_value = 100000 * (1 + returns).cumprod()
    df = pd.DataFrame({"Date": dates, "Portfolio Value": portfolio_value})
    volatility = np.std(returns) * (252 ** 0.5)
    return df, volatility

def performance_trend():
    df, volatility = generate_performance()

    fig = px.line(
        df,
        x="Date",
        y="Portfolio Value",
        title="Portfolio Performance Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    return volatility
