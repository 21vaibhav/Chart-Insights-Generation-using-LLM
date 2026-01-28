from openai import OpenAI
import base64
import io
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("LLAMAV_KEY")

class LlamavClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=key,  
            base_url="https://api.groq.com/openai/v1",  
        )
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"  

    def load_model(self, model_path: str = None):
        pass  # API-based

    def _encode_image(self, image: Image.Image) -> str:
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def analyze(self, image: Image.Image, prompt: str) -> str:
        image_base64 = self._encode_image(image)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert data analyst who interprets charts and graphs.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            },
                        },
                    ],
                },
            ],
            temperature=0.2,
            max_tokens=512,
        )

        return response.choices[0].message.content

