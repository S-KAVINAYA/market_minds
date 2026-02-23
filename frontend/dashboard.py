import streamlit as st
from components.portfolio import portfolio_allocation
from components.trend import performance_trend
from components.risk import calculate_risk
from components.alerts import alert_section
from config import BASE_PORTFOLIO

def dashboard_page():

    st.title("📊 Portfolio Intelligence Dashboard")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    risk_profile = st.sidebar.selectbox(
        "Risk Profile",
        ["Conservative", "Moderate", "Aggressive"]
    )

    col1, col2 = st.columns(2)

    with col1:
        portfolio_allocation(BASE_PORTFOLIO, risk_profile)

    with col2:
        volatility = performance_trend()

    risk_score = calculate_risk(volatility)

    st.markdown("---")
    alert_section(risk_profile, risk_score)
