import streamlit as st

def display_client_table(clients):

    st.subheader("Client Overview")

    st.dataframe(clients, use_container_width=True)
