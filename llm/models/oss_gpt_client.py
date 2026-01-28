
# !pip install groq

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class OssGptClient:
    """
    Replaced local Mistral with Groq API client.
    Maintains the same methods (route, generate, load_model) for compatibility.
    """

    def __init__(self):
        # Initialize Groq client
        # It will look for api_key here or in os.environ["GROQ_API_KEY"]
        key = os.getenv("OSS_GPT_KEY")
        self.client = Groq(api_key=key)
        
        # You can change this to "llama3-70b-8192" or "mixtral-8x7b-32768"
        self.model_name = "openai/gpt-oss-120b" 

    def load_model(self, model_path: str):
        
        pass

    # --------------------------------------------------
    # ROUTING (classifier-style)
    # --------------------------------------------------
    def route(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            temperature=0.0,
            max_tokens=100,
            # reasoning={"effort": "none"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a routing classifier. "
                        # "Return exactly one lowercase word: "
                        # "answer_directly or extract_from_graph"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        if not chat_completion.choices:
            raise RuntimeError(f"No choices returned:\n{chat_completion}")

        msg = chat_completion.choices[0].message
        raw = msg.content

        if not raw or not raw.strip():
            raise RuntimeError(
                f"Empty text returned by model.\nFull response:\n{chat_completion}"
            )

        cleaned = raw.lower().replace("answer:", "").strip()

        if "\n" in cleaned:
            cleaned = cleaned.splitlines()[-1].strip()

        return cleaned


    # --------------------------------------------------
    # ANSWER / INTERPRETATION
    # --------------------------------------------------
    def generate(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
        model=self.model_name,
        temperature=0.2,
        max_tokens=512,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert analyst. "
                    "Provide clear and complete explanations."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )

        if not chat_completion.choices:
            raise RuntimeError(f"No choices returned:\n{chat_completion}")

        msg = chat_completion.choices[0].message

        # Prefer content, but fall back defensively
        if msg.content and msg.content.strip():
            return msg.content.strip()

        # Optional fallback (last resort)
        if hasattr(msg, "reasoning") and msg.reasoning:
            return msg.reasoning.strip()

        raise RuntimeError(f"Empty output from model:\n{chat_completion}")
