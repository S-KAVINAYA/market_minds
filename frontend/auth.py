import streamlit as st

def authenticate(username, password):
    return username == "admin" and password == "admin123"

def login_page():
    st.title("AI-Driven Investment Management and Decision Intelligence System")
    st.subheader("Secure Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")
