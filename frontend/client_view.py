import streamlit as st
import requests
import pandas as pd
import plotly.express as px

BASE_URL = "http://127.0.0.1:8000"

def show_client_dashboard(client_id):

    response = requests.get(f"{BASE_URL}/clients/{client_id}")
    data = response.json()

    if not data:
        st.error("No data found")
        return

    df = pd.DataFrame(data)

    st.title(f"Client {client_id} Dashboard")

    risk_profile = df["Risk_Profile"].iloc[0]

    col1, col2 = st.columns(2)
    col1.metric("Risk Profile", risk_profile)
    col2.metric("Holdings", len(df))

    st.markdown("---")

    # ---------------- Portfolio Comparison ----------------
    st.subheader("Portfolio Growth Comparison (Indexed to 100)")

    all_data = []

    for _, row in df.iterrows():
        ticker = row["Ticker"]
        market = requests.get(f"{BASE_URL}/market/{ticker}").json()

        if market:
            mdf = pd.DataFrame(market)
            mdf["Normalized"] = (mdf["Close"] / mdf["Close"].iloc[0]) * 100
            mdf["Ticker"] = ticker
            all_data.append(mdf[["Date", "Normalized", "Ticker"]])

    if all_data:
        final_df = pd.concat(all_data)
        fig = px.line(final_df, x="Date", y="Normalized", color="Ticker")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ---------------- Individual Stocks ----------------
    st.subheader("Individual Stock Analysis")

    for _, row in df.iterrows():
        ticker = row["Ticker"]

        st.markdown(f"### {ticker}")

        market = requests.get(f"{BASE_URL}/market/{ticker}").json()
        if market:
            mdf = pd.DataFrame(market)
            fig = px.line(mdf, x="Date", y="Close")
            st.plotly_chart(fig, use_container_width=True)

            # Risk
            risk = requests.get(f"{BASE_URL}/stock-risk/{ticker}").json()["risk"]

            if risk == "High":
                st.error(f"⚠ {ticker} HIGH RISK")
            elif risk == "Moderate":
                st.warning(f"{ticker} Moderate Risk")
            else:
                st.success(f"{ticker} Low Risk")

            # Prediction
            prediction = requests.get(f"{BASE_URL}/predict/{ticker}").json()
            if prediction:
                pdf = pd.DataFrame(prediction)
                fig2 = px.line(pdf, x="Date", y="Predicted",
                               title="30 Day Prediction")
                st.plotly_chart(fig2, use_container_width=True)

    if st.button("⬅ Back"):
        st.session_state.page = "overview"
        st.rerun()
