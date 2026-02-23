import streamlit as st

MANAGER_CREDENTIALS = {
    "manager": "secure123"
}

def authenticate(username, password):
    return MANAGER_CREDENTIALS.get(username) == password


def login_page():
    st.title("AI-Driven Investment Management and Decision Intelligence System")
    st.subheader("Manager Login Portal")

    with st.form("login_form"):
        username = st.text_input("Manager ID")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.manager = username
                st.success("Access Granted")
                st.rerun()
            else:
                st.error("Invalid Manager Credentials")
