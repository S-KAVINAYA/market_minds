import pandas as pd
import streamlit as st


def display_client_table(clients):
    st.subheader("Client Overview")

    if not clients:
        st.info("No clients available.")
        return None

    overview_df = pd.DataFrame([
        {
            "client_id": c["client_id"],
            "risk_level": c["risk_level"],
            "risk_asset": c["risk_asset"],
            "invested_value": c["invested_value"],
            "current_value": c["current_value"],
        }
        for c in clients
    ])

    st.dataframe(overview_df, use_container_width=True)

    st.markdown("#### Open Client Dashboard")
    cols = st.columns(5)
    selected_client_id = None
    for idx, client in enumerate(clients):
        with cols[idx % 5]:
            if st.button(client["client_id"], key=f"open_{client['client_id']}"):
                selected_client_id = client["client_id"]

    return selected_client_id
