import requests
import streamlit as st

BASE_URL = st.secrets["server"]["server_url"]


@st.dialog("Add your camera")
def add_camera():
    st.session_state.is_setting = 1
    
    name = st.text_input("Camera Name")
    ip = st.text_input("IP Camera Address:")

    if st.button("Submit"):
        payload = {"name": name, "ip": ip, "user_id": st.session_state.user_id}
        try:
            response = requests.post(f"{BASE_URL}/cameras/", json=payload)
            if response.status_code == 200:
                st.success("Camera added successfully!")
        except Exception as e:
            st.error(f"Connection error: {e}")
        
        st.rerun(scope="app")


@st.dialog("Delete camera")
def delete_camera():
    user_id = st.session_state.get("user_id")
    
    if not user_id:
        st.error("User not authenticated")
        return

    try:
        res = requests.get(f"{BASE_URL}/cameras", params={"user_id": user_id})
        res.raise_for_status()
        cameras = res.json() 
    except Exception as e:
        st.error(f"Failed to fetch cameras: {e}")
        cameras = []

    if not cameras:
        st.warning("No cameras found for your account.")
        return
    
    camera_options = {f"{c['name']} - (IP: {c['ip']})": c['id'] for c in cameras}
    camera_to_delete = st.selectbox("Select camera", list(camera_options.keys()))

    if st.button("Delete"):
        target_id = camera_options[camera_to_delete]
        st.success(f"Deleted {camera_to_delete}")
        st.rerun()

@st.dialog("Telegram")
def set_telegram():
    st.session_state.is_setting = 1
    bot_token = st.text_input("Bot Token: ")
    group_id = st.text_input("Group ID: ")

    if st.button("Submit"):
        payload = {"bot_token": bot_token, "group_id": group_id}
        response = requests.post(f"{BASE_URL}/config/telegram", json=payload)
        if response.status_code == 200:
            st.success("Telegram config updated!")
            st.rerun(scope="app")


def set_config():
    with st.container(horizontal=True, vertical_alignment="top"):
        st.title("👋 TverEyNg")

        with st.container(horizontal=True, horizontal_alignment="right"):
            # if st.button("Telegram"):
            #     set_telegram()

            if st.button("Add Camera"):
                add_camera()

            if st.button("Delete Camera"):
                delete_camera()
                
            # if st.button("Log out"):
            #     st.logout()
