import plotly.express as px
import streamlit as st


def allocation_chart(portfolio):
    fig = px.pie(names=list(portfolio.keys()), values=list(portfolio.values()), hole=0.4, title="Asset Allocation")
    st.plotly_chart(fig, use_container_width=True)


def trend_chart(df):
    fig = px.line(df, x="Date", y="Value", title="Portfolio Trend")
    st.plotly_chart(fig, use_container_width=True)


def stock_time_series_chart(df, symbol):
    fig = px.line(df, x="Date", y="Price", title=f"{symbol} Time Series")
    st.plotly_chart(fig, use_container_width=True)


def customer_comparison_chart(df):
    fig = px.line(df, x="Date", y="Value", color="Client", title="Customer Portfolio Time Series Comparison")
    st.plotly_chart(fig, use_container_width=True)


def client_value_comparison_chart(client):
    fig = px.bar(
        x=["Invested", "Current"],
        y=[client["invested_value"], client["current_value"]],
        title=f"Client {client['client_id']} Invested vs Current Value",
        labels={"x": "Value Type", "y": "Amount (₹)"},
    )
    st.plotly_chart(fig, use_container_width=True)


def ticker_exposure_chart(holdings):
    fig = px.bar(holdings, x="symbol", y="value", color="sector", title="Ticker-wise Exposure")
    st.plotly_chart(fig, use_container_width=True)


def forecast_chart(df, symbol):
    fig = px.line(df, x="Date", y="Price", color="Type", title=f"{symbol} Historical + Forecast")
    st.plotly_chart(fig, use_container_width=True)


def asset_time_series_chart(df, title):
    fig = px.line(df, x="Date", y="Value", color="Asset", title=title)
    st.plotly_chart(fig, use_container_width=True)
