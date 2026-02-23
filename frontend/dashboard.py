import streamlit as st
from api_client import fetch_clients
from components.client_table import display_client_table
from components.client_profile import display_client_profile

def dashboard_page():

    st.title("Portfolio Intelligence Dashboard")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    risk_filter = st.sidebar.selectbox(
        "Filter by Risk",
        ["All", "Low", "Moderate", "High"]
    )

    clients = fetch_clients(st.session_state.manager_id)

    if risk_filter != "All":
        clients = [c for c in clients if c["risk_level"] == risk_filter]

    display_client_table(clients)

    selected_client_id = st.selectbox(
        "Select Client to View Details",
        [c["client_id"] for c in clients]
    )

    selected_client = next(c for c in clients if c["client_id"] == selected_client_id)

    display_client_profile(selected_client)
