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

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=[
        {"type": "text", "text": "Vision Testing"},
        {
            "type": "image",
            "data": base64.b64encode(im_data).decode('utf-8'),
            "mime_type": "image/png"
        },
    ]
)

print(interaction.output_text)