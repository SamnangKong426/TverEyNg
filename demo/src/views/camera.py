import streamlit as st
import src.controllers.camera as camera_controller
import asyncio
from src.bot.telegram_bot import alert
import time


async def display_camera():
    display_frame = st.empty()
    timeout = 10 # 1 min
    last_alert = 0

    for results, annotated_frame in camera_controller.open_camera():
        display_frame.image(annotated_frame, caption="Processed Frame", width="stretch", channels="BGR")
        for r in results:
            now = time.time()
            if 0 in r.boxes.cls and now - last_alert >= timeout:
                alert_task = asyncio.create_task(alert(annotated_frame))
                await alert_task
                last_alert = now


