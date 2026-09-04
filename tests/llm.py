import os
import dotenv
from google import genai

dotenv.load_dotenv()

client = genai.Client(api_key=os.getenv("APIKEY"))

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="LLM Testing"
)

print(interaction.output_text)