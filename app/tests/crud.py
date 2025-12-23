import json
import streamlit as st

FILE_PATH = "app/database/data.json"

def save_json(data, filename="database/data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_json(filename="database/data.json"):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data

cameras = load_json(FILE_PATH)

@st.dialog("Add your camera")
def add_camera():
    name = st.text_input("Camera Name")
    ip = st.text_input("IP Camera Address:")

    if st.button("Submit"):
        cameras[name] = ip
        save_json(cameras, FILE_PATH)
        st.rerun()

@st.dialog("Delete camera")
def delete_camera():
    if not cameras:
        st.warning("No cameras to delete")
        return

    camera_to_delete = st.selectbox(
        "Select camera",
        list(cameras.keys())
    )

    if st.button("Delete"):
        del cameras[camera_to_delete]
        save_json(cameras, FILE_PATH)
        st.success(f"Deleted {camera_to_delete}")
        st.rerun()

if st.button("Add Camera"):
    add_camera()

if st.button("Delete Camera"):
    delete_camera()
