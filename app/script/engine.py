import json
import os
from typing import Dict, Any

class ScriptEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def write_script(self, story_data: Dict[str, Any], job_id: str, job_dir="jobs") -> Dict[str, Any]:
        print("Writing final narration script...")
        
        # Convert story structure into a professional script
        script_text = f"{story_data['structure']['hook']}\n\n{story_data['structure']['context']}\n\n{story_data['structure']['rise']}\n\n{story_data['structure']['conflict']}\n\n{story_data['structure']['turning_point']}\n\n{story_data['structure']['consequences']}\n\n{story_data['structure']['conclusion']}"
        
        script_data = {
            "full_script": script_text,
            "estimated_duration_seconds": 600, # 10 mins
            "pacing": "Documentary"
        }
        
        # Save as text and json
        job_path = os.path.join(job_dir, job_id)
        with open(os.path.join(job_path, "script.txt"), "w") as f:
            f.write(script_text)
            
        with open(os.path.join(job_path, "script.json"), "w") as f:
            json.dump(script_data, f, indent=2)
            
        return script_data
