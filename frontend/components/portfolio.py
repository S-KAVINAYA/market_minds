import streamlit as st
import plotly.express as px
import pandas as pd

def portfolio_allocation(base_portfolio, risk_profile):

    portfolio = base_portfolio.copy()

    if risk_profile == "Conservative":
        portfolio["Stocks"] -= 15
        portfolio["Bonds"] += 10
        portfolio["Cash"] += 5

    elif risk_profile == "Aggressive":
        portfolio["Stocks"] += 15
        portfolio["Bonds"] -= 10
        portfolio["Cash"] -= 5

    df = pd.DataFrame({
        "Asset": portfolio.keys(),
        "Allocation (%)": portfolio.values()
    })

    fig = px.pie(
        df,
        values="Allocation (%)",
        names="Asset",
        hole=0.4,
        title="Portfolio Allocation"
    )

    st.plotly_chart(fig, use_container_width=True)
