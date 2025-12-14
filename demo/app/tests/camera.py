import streamlit as st
import asyncio
import time
from bot.telegram_bot import alert
import controllers.camera as camera_controller

TIMEOUT = 10 
LAST_ALERT = 0

async def is_alert(results, annotated_frame):
    """Trigger alert if class 0 is detected and timeout has passed."""
    global LAST_ALERT, TIMEOUT
    now = time.time()

    for r in results:
        if 0 in r.boxes.cls and now - LAST_ALERT >= TIMEOUT:
            alert_task = asyncio.create_task(alert(annotated_frame))
            await alert_task
            LAST_ALERT = now

@st.cache_resource
async def display_camera():
    """ Display all camera """
    display_frame = st.empty()

    for results, annotated_frame in camera_controller.open_camera():
        display_frame.image(annotated_frame, caption="Processed Frame", width="stretch", channels="BGR")
        asyncio.sleep(0.1)
        # await is_alert(results, annotated_frame)
       

