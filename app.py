import streamlit as st
# from src.login import sync_google
from src.dashboard import dashboard

st.set_page_config(page_title="TverEyNg", page_icon="👋", layout="wide")

# if "synced" not in st.session_state:
#     sync_google()

# if st.user.is_logged_in:
#     dashboard()

dashboard()