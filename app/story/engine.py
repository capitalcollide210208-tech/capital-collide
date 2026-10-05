import json
import os
from typing import Dict, Any
from app.common.llm_client import LLMClient

class StoryEngine:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def construct_story(self, verified_data: Dict[str, Any], job_id: str, job_dir="jobs") -> Dict[str, Any]:
        print("AI is constructing the documentary narrative...")
        
        system_prompt = "You are a master storyteller and documentary writer. Your goal is to transform dry facts into a gripping, cinematic narrative that maintains extreme curiosity."
        user_prompt = f"Using these verified facts: {json.dumps(verified_data)}, construct a story structure. I need a JSON object with a 'structure' key containing: 'hook', 'context', 'rise', 'conflict', 'turning_point', 'consequences', and 'conclusion'. Ensure the narrative flow is high-tension and professional."
        
        response = self.llm.ask(system_prompt, user_prompt)
        
        try:
            cleaned_response = response.strip().replace("```json", "").replace("```", "").strip()
            story = json.loads(cleaned_response)
        except:
            story = {"structure": {"hook": response, "conclusion": "End of story"}}
        
        # Save to job folder
        job_path = os.path.join(job_dir, job_id)
        with open(os.path.join(job_path, "story.json"), "w") as f:
            json.dump(story, f, indent=2)
            
        return story
