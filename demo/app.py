import streamlit as st
import src.views.camera as camera_view
import src.crud.camera as cam_crud
import asyncio

st.set_page_config(
    page_title="TverEyNg",
    page_icon="👋",
)

asyncio.run(camera_view.display_camera())
