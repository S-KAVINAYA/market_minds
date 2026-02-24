import streamlit as st
from auth import signup


def show_signup():
    st.title("Manager Sign Up")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Create Account"):
        success, message = signup(username, password)
        if success:
            st.success(message)
        else:
            st.error(message)
