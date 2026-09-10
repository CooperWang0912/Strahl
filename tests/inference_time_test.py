import time

import os
import dotenv
from google import genai
import pyautogui
from io import BytesIO
import base64

screenshot = pyautogui.screenshot()

screenshot = screenshot.resize((768, 768))

output = BytesIO()
screenshot.save(output, format='PNG')
im_data = output.getvalue()

dotenv.load_dotenv()

client = genai.Client(api_key=os.getenv("APIKEY"))

start_time = time.perf_counter()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=[
        {"type": "text", "text": "Vision Testing"},
        {
            "type": "image",
            "data": base64.b64encode(im_data).decode('utf-8'),
            "mime_type": "image/png"
        },
    ],
    stream=True
)

for event in interaction:
    if event.event_type == "step.delta":
        if event.delta.type == "text":
            print(event.delta.text, end="", flush=True)
