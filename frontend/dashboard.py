import streamlit as st
from api_client import fetch_clients

def dashboard_page():

    st.title("📊 Portfolio Intelligence Dashboard")

    st.sidebar.write(f"Manager: {st.session_state.manager_id}")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    risk_filter = st.sidebar.selectbox(
        "Filter Clients By Risk Level",
        ["All", "Low", "Moderate", "High"]
    )

    clients = fetch_clients(st.session_state.manager_id)

    if risk_filter != "All":
        clients = [c for c in clients if c["risk_level"] == risk_filter]

    st.subheader(f"Clients at {risk_filter} Risk")

    for client in clients:

        with st.expander(f"Client {client['client_id']}"):

            st.write(f"Risk Level: {client['risk_level']}")
            st.write(f"Risk Asset: {client['risk_asset']}")
            st.write(f"Invested Value: ₹{client['invested_value']}")
            st.write(f"Current Value: ₹{client['current_value']}")

            change = client["current_value"] - client["invested_value"]

            if change < 0:
                st.error(f"Loss: ₹{abs(change)}")
            else:
                st.success(f"Profit: ₹{change}")
