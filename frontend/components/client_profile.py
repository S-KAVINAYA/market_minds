import streamlit as st
from components.charts import allocation_chart, trend_chart
from api_client import fetch_client_trend

def display_client_profile(client):

    st.subheader(f"Client {client['client_id']} Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Risk Level: {client['risk_level']}")
        st.write(f"Risk Asset: {client['risk_asset']}")
        st.write(f"Invested Value: ₹{client['invested_value']}")
        st.write(f"Current Value: ₹{client['current_value']}")

    with col2:
        allocation_chart(client["portfolio"])

    df = fetch_client_trend(client["client_id"])
    trend_chart(df)
