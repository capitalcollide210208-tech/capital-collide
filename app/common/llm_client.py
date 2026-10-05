import os
from openai import OpenAI
from typing import Optional

class LLMClient:
    """
    Unified Client for GLM 5.3 Flash via NVIDIA API.
    Handles all AI requests for the Capital Collide pipeline.
    """
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self.model = os.getenv("NVIDIA_MODEL", "z-ai/glm-5.3-flash")
        
        if not self.api_key:
            # For development/simulation if key is missing
            print("WARNING: NVIDIA_API_KEY not found. Using simulation mode.")
            self.client = None
        else:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )

    def ask(self, system_prompt: str, user_prompt: str, temperature: float = 0.5) -> str:
        if not self.client:
            return f"[SIMULATION] Response to: {user_prompt[:50]}..."

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                top_p=1,
                max_tokens=2048,
                stream=False
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"LLM API Error: {e}")
            return f"Error occurred during AI generation: {str(e)}"
