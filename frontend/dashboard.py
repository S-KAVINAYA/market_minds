import streamlit as st
from components.portfolio import portfolio_allocation
from components.trend import performance_trend
from components.risk import calculate_risk
from components.alerts import alert_section
from config import CLIENT_PROFILES

def dashboard_page():

    st.title("📊 Portfolio Intelligence Dashboard")

    st.sidebar.write(f"Logged in as: {st.session_state.manager}")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    selected_client = st.sidebar.selectbox(
        "Select Client Profile",
        list(CLIENT_PROFILES.keys())
    )

    risk_profile = st.sidebar.selectbox(
        "Risk Profile",
        ["Conservative", "Moderate", "Aggressive"]
    )

    client_portfolio = CLIENT_PROFILES[selected_client]

    col1, col2 = st.columns(2)

    with col1:
        portfolio_allocation(client_portfolio, risk_profile)

    with col2:
        volatility = performance_trend()

    risk_score = calculate_risk(volatility)

    st.markdown("---")

    alert_section(risk_profile, risk_score)

    st.markdown("### Decision Intelligence Log")

    st.json({
        "Manager": st.session_state.manager,
        "Client": selected_client,
        "Risk Profile": risk_profile,
        "Risk Level": risk_score,
        "Status": "Monitoring Active"
    })
