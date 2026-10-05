import json
import os
from typing import Dict, Any, List
from app.common.llm_client import LLMClient

class ResearchEngine:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def conduct_research(self, topic: str, job_id: str, job_dir="jobs") -> Dict[str, Any]:
        print(f"AI is conducting deep research on: {topic}...")
        
        system_prompt = "You are an elite investigative journalist. Your goal is to find every critical fact, date, and event related to a business topic. Be exhaustive and precise."
        user_prompt = f"Conduct comprehensive research on the topic: '{topic}'. I need: 1. A list of critical factual claims with their sources. 2. A chronological timeline of major events. Return this as JSON with keys: 'evidence' (list of objects with claim, source, reliability) and 'timeline' (list of objects with date, event)."
        
        response = self.llm.ask(system_prompt, user_prompt)
        
        try:
            cleaned_response = response.strip().replace("```json", "").replace("```", "").strip()
            research_data = json.loads(cleaned_response)
        except:
            research_data = {"evidence": [], "timeline": [], "error": "Parsing failed"}
        
        # Save results
        job_path = os.path.join(job_dir, job_id)
        with open(os.path.join(job_path, "research.json"), "w") as f:
            json.dump(research_data, f, indent=2)
            
        return research_data
