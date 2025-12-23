import asyncio
import os
import threading
import time

from .bot import alert

TIMEOUT = TIMEOUT = int(os.getenv("TIMEOUT", 30))
LAST_ALERT = 0


def play_sound(sound_path="assets/thief_sound.mp3"):
    def play():
        os.system("mpg123 " + sound_path)

    threading.Thread(target=play).start()


def process_alert(results, annotated_frame):
    global LAST_ALERT
    now = time.time()
    for r in results:
        if 0 in r.boxes.cls and now - LAST_ALERT >= TIMEOUT:
            play_sound()
            alert_thread = threading.Thread(
                target=lambda: asyncio.run(alert(annotated_frame))
            )
            alert_thread.start()
            LAST_ALERT = now
