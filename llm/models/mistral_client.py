# llm/models/mistral_client.py
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)


class MistralClient:
    """
    Central brain LLM.
    Used for:
    - routing
    - simple answers
    - interpretation of tool outputs

    LangGraph-safe (NO HuggingFacePipeline)
    """

    def __init__(
        self,
        model_id: str = "mistralai/Mistral-7B-Instruct-v0.2",
        dtype=torch.float16,
    ):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=dtype,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    # --------------------------------------------------
    # INTERNAL GENERATION CORE
    # --------------------------------------------------
    def _generate(
        self,
        prompt: str,
        max_new_tokens: int,
        temperature: float,
        do_sample: bool,
    ) -> str:
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
        ).to(self.model.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        decoded = self.tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True,
        )

        # Return ONLY the generated completion
        return decoded[len(prompt):].strip()

    # --------------------------------------------------
    # ROUTING (classifier-style)
    # --------------------------------------------------
    def route(self, prompt: str) -> str:
        """
        Deterministic, short output.
        """
        return self._generate(
            prompt=prompt,
            max_new_tokens=32,
            temperature=0.0,
            do_sample=False,
        ).lower()

    # --------------------------------------------------
    # ANSWER / INTERPRETATION
    # --------------------------------------------------
    def generate(self, prompt: str) -> str:
        """
        Used for:
        - simple answers
        - vision interpretation
        - SQL interpretation
        """
        return self._generate(
            prompt=prompt,
            max_new_tokens=512,
            temperature=0.2,
            do_sample=True,
        )

    # --- add at bottom of file ---

    _mistral_instance = None


    def get_mistral():
        """
        Lazy-loaded singleton for MistralClient.
        """
        global _mistral_instance
        if _mistral_instance is None:
            _mistral_instance = MistralClient()
        return _mistral_instance
