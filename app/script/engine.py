import json
import os
from typing import Dict, Any
from app.common.llm_client import LLMClient

class ScriptEngine:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def write_script(self, story_data: Dict[str, Any], job_id: str, job_dir="jobs") -> Dict[str, Any]:
        print("AI is writing the final narration script...")
        
        system_prompt = "You are a professional documentary scriptwriter. Write scripts that sound human, authoritative, and cinematic. Avoid AI clichés. Use concise, powerful sentences."
        user_prompt = f"Transform this story structure into a final narration script: {json.dumps(story_data)}. Return a JSON object with: 'full_script' (the complete text), 'estimated_duration_seconds', and 'pacing' (e.g., 'Slower for tension', 'Fast for action')."
        
        response = self.llm.ask(system_prompt, user_prompt)
        
        try:
            cleaned_response = response.strip().replace("```json", "").replace("```", "").strip()
            script_data = json.loads(cleaned_response)
        except:
            script_data = {"full_script": response, "estimated_duration_seconds": 600}
        
        # Save as text and json
        job_path = os.path.join(job_dir, job_id)
        with open(os.path.join(job_path, "script.txt"), "w") as f:
            f.write(script_data.get("full_script", ""))
            
        with open(os.path.join(job_path, "script.json"), "w") as f:
            json.dump(script_data, f, indent=2)
            
        return script_data
