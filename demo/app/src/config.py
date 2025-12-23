import streamlit as st

from .utils import load_json, save_json

FILE_PATH = "database/data.json"
CREDENTIALS_PATH = "database/credentials.json"
cameras = load_json()


@st.dialog("Add your camera")
def add_camera():
    st.session_state.is_setting = 1
    name = st.text_input("Camera Name")
    ip = st.text_input("IP Camera Address:")
    if st.button("Submit"):
        cameras[name] = ip
        save_json(cameras, FILE_PATH)
        st.rerun(scope="app")


@st.dialog("Delete camera")
def delete_camera():
    st.session_state.is_setting = 1
    if not cameras:
        st.warning("No cameras to delete")
        return
    camera_to_delete = st.selectbox("Select camera", list(cameras.keys()))

    if st.button("Delete"):
        del cameras[camera_to_delete]
        save_json(cameras, FILE_PATH)
        st.success(f"Deleted {camera_to_delete}")
        st.rerun()


@st.dialog("Telegram")
def set_telegram():
    st.session_state.is_setting = 1
    bot_token = st.text_input("Bot Token: ")
    group_id = st.text_input("Group ID: ")
    if st.button("Submit"):
        data = {"bot_token": bot_token, "group_id": group_id}
        save_json(data, filename=CREDENTIALS_PATH)
        st.rerun(scope="app")


def set_config():
    with st.container(horizontal=True, vertical_alignment="top"):
        st.title("👋 TverEyNg")

        with st.container(horizontal=True, horizontal_alignment="right"):
            if st.button("Telegram"):
                set_telegram()
            if st.button("Add Camera"):
                add_camera()
            if st.button("Delete Camera"):
                delete_camera()
