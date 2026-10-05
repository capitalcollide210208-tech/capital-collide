import json
import os
from typing import Dict, Any
from app.common.llm_client import LLMClient

class TopicDiscoveryEngine:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.categories = [
            "corporate rise and fall",
            "disruptive technology",
            "entrepreneurial strategy",
            "industry transformation",
            "major competitive battles",
            "innovative product failures"
        ]

    def discover_topic(self, job_id: str, job_dir="jobs") -> Dict[str, Any]:
        print("AI is discovering a high-potential documentary topic...")
        
        system_prompt = "You are a world-class business documentary producer for 'Capital Collide'. Your goal is to find a topic that is intellectually stimulating, visually cinematic, and highly likely to go viral."
        user_prompt = f"Analyze current trends in these categories: {', '.join(self.categories)}. Suggest one specific, high-impact topic for a business documentary. Return the result as JSON with keys: 'topic', 'category', 'reasoning', 'potential_visuals'."
        
        response = self.llm.ask(system_prompt, user_prompt)
        
        try:
            # Try to parse JSON from the AI response
            # Simple cleaning in case AI adds markdown code blocks
            cleaned_response = response.strip().replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_response)
        except:
            # Fallback if AI doesn't return perfect JSON
            result = {
                "topic": response,
                "category": "General Business",
                "reasoning": "AI selected this based on current trends.",
                "potential_visuals": "Standard cinematic B-roll"
            }
        
        # Save to job folder
        job_path = os.path.join(job_dir, job_id)
        with open(os.path.join(job_path, "selected_topic.json"), "w") as f:
            json.dump(result, f, indent=2)
            
        return result
