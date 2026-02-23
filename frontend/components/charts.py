import plotly.express as px
import streamlit as st

def allocation_chart(portfolio):

    fig = px.pie(
        names=list(portfolio.keys()),
        values=list(portfolio.values()),
        hole=0.4,
        title="Asset Allocation"
    )

    st.plotly_chart(fig, use_container_width=True)


def trend_chart(df):

    fig = px.line(
        df,
        x="Date",
        y="Value",
        title="Portfolio Trend"
    )

    st.plotly_chart(fig, use_container_width=True)
