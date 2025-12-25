import streamlit as st
import requests

BASE_URL = "http://localhost:8000/api"

def sync_google():
    if not st.user.is_logged_in:
        with st.container(horizontal_alignment="center"):
            st.title("🛡️ TverEyNg", text_alignment="center")
            if st.button("Log in with Google"):
                st.login()
                st.session_state.synced = True
            

    else:
        if "synced" not in st.session_state:
            user_data = {
                "email": st.user.email,
                "name": st.user.name,
            }
            with st.spinner("Syncing account..."):
                response = requests.post(f"{BASE_URL}/auth/sync", json=user_data)
                if response.status_code == 200:
                    st.session_state.user_id = response.json().get("user_id")
                    st.session_state.synced = True