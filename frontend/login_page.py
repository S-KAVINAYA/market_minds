import requests
BASE_URL = "http://127.0.0.1:8000"
if st.button("Login"):
    st.write("LOGIN BUTTON CLICKED")

    try:
        response = requests.post(
            f"{BASE_URL}/manager/login",
            json={
                "username": username,
                "password": password
            },
            timeout=5
        )

        if response.status_code == 200:
            st.session_state.page = "dashboard"
        elif response.status_code == 401:
            st.error("Invalid username or password")
        else:
            st.error(f"Server error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Is uvicorn running?")

    except requests.exceptions.Timeout:
        st.error("Backend request timed out.")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
