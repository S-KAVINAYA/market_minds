import streamlit as st
from auth import login_page
from dashboard import dashboard_page

st.set_page_config(
    page_title="AI-Driven Investment Management System",
    layout="wide"
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    dashboard_page()
else:
    login_page()
