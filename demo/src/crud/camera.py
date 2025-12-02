import re
import streamlit as st
from src.config.db import conn

IP_REGEX = r"^(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?$"
RTSP_REGEX = r"^rtsp://.+"

@st.dialog("Camera")
def add_camera():
    room = st.text_input("Room (max 30 chars):", max_chars=30)
    ip_cam = st.text_input("IP Address (IPv4 or RTSP):", max_chars=200)

    if st.button("Submit"):

        if not room or not ip_cam:
            st.error("Room and IP cannot be empty.")
            return

        # if not (re.match(IP_REGEX, ip_cam) or re.match(RTSP_REGEX, ip_cam)):
        #     st.error("Invalid IP or RTSP format.")
        #     return

        # DB insertion
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cameras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room TEXT,
                    ip TEXT
                );
            """)
            conn.execute(
                "INSERT INTO cameras (room, ip) VALUES (?, ?)",
                (room, ip_cam)
            )
        st.success("Camera added successfully!")
        st.rerun()
