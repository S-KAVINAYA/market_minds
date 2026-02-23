import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI-Driven Investment Management System",
    layout="wide"
)

# Main Title
st.title("AI-Driven Investment Management and Decision Intelligence System")

st.markdown("---")

# Sidebar
st.sidebar.header("Portfolio Control Panel")
client = st.sidebar.selectbox(
    "Select Client Portfolio",
    ["Client A", "Client B", "Client C"]
)

risk_profile = st.sidebar.selectbox(
    "Risk Profile",
    ["Conservative", "Moderate", "Aggressive"]
)

st.sidebar.markdown("---")
st.sidebar.write("Monitoring Status: Active")

# Dashboard Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚨 Alerts")
    st.error("No sector concentration risk detected.")
    st.warning("Volatility exposure within acceptable limits.")

with col2:
    st.subheader("💡 Recommendations")
    st.info("Maintain current allocation.")
    st.success("Portfolio aligned with risk tolerance.")

st.markdown("---")

st.subheader("📜 Decision Intelligence Logs")

st.json({
    "client": client,
    "risk_profile": risk_profile,
    "sector_exposure": "Balanced",
    "volatility_score": 0.22,
    "ai_decision": "No rebalancing required",
    "status": "Human review pending"
})
