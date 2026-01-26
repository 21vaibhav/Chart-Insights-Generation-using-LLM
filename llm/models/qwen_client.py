# llm/models/qwen_client.py
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image


class QwenClient:
    def __init__(
        self,
        model_name="Qwen/Qwen2-VL-7B-Instruct",
        device="cuda",
        dtype=torch.float16,
    ):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForVision2Seq.from_pretrained(
            model_name,
            torch_dtype=dtype,
            device_map="auto",
        )

    def analyze(self, image_path: str, prompt: str) -> str:
        image = Image.open(image_path).convert("RGB")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": prompt},
                ],
            }
        ]

        inputs = self.processor(
            messages,
            images=image,
            return_tensors="pt",
        ).to(self.model.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.2,
            )

        return self.processor.decode(
            output_ids[0], skip_special_tokens=True
        )

    _qwen_instance = None


    def get_qwen():
        """
        Lazy-loaded singleton for QwenClient.
        """
        global _qwen_instance
        if _qwen_instance is None:
            _qwen_instance = QwenClient()
        return _qwen_instance

    
