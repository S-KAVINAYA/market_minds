import streamlit as st
from api_client import (
    login_manager_api,
    signup_manager_api
)

def login_page():

    st.title("Investment Intelligence System")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # LOGIN
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Manager ID")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                response = login_manager_api(username, password)

                if response["status"] == "success":
                    st.session_state.authenticated = True
                    st.session_state.manager_id = response["manager_id"]
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error(response["message"])

    # SIGNUP
    with tab2:
        with st.form("signup_form"):
            new_username = st.text_input("New Manager ID")
            new_password = st.text_input("New Password", type="password")
            create = st.form_submit_button("Create Account")

            if create:
                response = signup_manager_api(new_username, new_password)

                if response["status"] == "success":
                    st.success("Account created. Please login.")
                else:
                    st.error(response["message"])
