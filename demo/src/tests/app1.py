import cv2 as cv
import streamlit as st
from bot.telegram_bot import alert
# from services import predict
from app import add_camera

st.set_page_config(
    page_title="TverEyNg",
    page_icon="👋",
)

if st.button("Add Camera"):
    add_camera()


# for idx, (camera_name, ip_cam) in enumerate(ip_cameras.items()):
#     st.image(ip_cam, caption=str(camera_name), width="stretch", output_format="auto", channels="RGB")

# cap = cv.VideoCapture(0)

# if not cap.isOpened():
#     st.error("Error: Could not open the camera.")

# det_frame = st.empty()

# previous_alerted_id = None

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         st.warning("Failed to grab frame, exiting...")
#         break  

#     results= list(predict(frame))
#     annotated_frame = results[0].plot()
#     for r in results:
#         for cls in r.boxes.cls:
#             if cls == 0:  
#                 print("Person detected!")
#                 # asyncio.run(alert(annotated_frame))
#                 previous_alerted_id = cls

#     det_frame.image(annotated_frame, caption="Processed Frame", width="stretch", channels="BGR")