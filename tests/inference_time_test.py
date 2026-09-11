import time

import os
import dotenv
from google import genai
import pyautogui
from io import BytesIO
import base64

import genie_tts as genie
from stt import record_once

genie.load_predefined_character('thirtyseven')

speech = record_once()

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
        {"type": "text", "text": speech},
        {
            "type": "image",
            "data": base64.b64encode(im_data).decode('utf-8'),
            "mime_type": "image/png"
        },
    ],
)

output = interaction.output_text

genie.tts(
    character_name='thirtyseven',
    text=output,
    play=True,
)

genie.wait_for_playback_done()
