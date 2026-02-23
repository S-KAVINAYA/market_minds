import streamlit as st

def alert_section(risk_profile, risk_score):

    st.subheader("🚨 Alerts & Decision Intelligence")

    if risk_score == "High":
        st.error("High volatility detected. Consider rebalancing.")
    elif risk_score == "Moderate":
        st.warning("Moderate market risk observed.")
    else:
        st.success("Portfolio risk within acceptable limits.")

    st.markdown("### Decision Log")

    st.json({
        "Risk Profile": risk_profile,
        "Calculated Risk": risk_score,
        "AI Recommendation": "Monitor and adjust if needed",
        "Status": "Active"
    })
