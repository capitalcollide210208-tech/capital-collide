import json
import os
from typing import Dict, Any, List
from app.common.llm_client import LLMClient

class FactCheckEngine:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def verify_research(self, research_data: Dict[str, Any], job_id: str, job_dir="jobs") -> Dict[str, Any]:
        print("AI is running the Fact-Checking Gate...")
        
        system_prompt = "You are a professional fact-checker. Your goal is to eliminate all fabrication and speculation. Only verify claims that are corroborated by reliable evidence."
        user_prompt = f"Verify the following research data: {json.dumps(research_data)}. For each claim, decide if it is 'VERIFIED', 'UNCERTAIN', or 'REJECTED'. Return a JSON list of objects with: 'claim', 'source', 'decision', 'confidence' (0-1)."
        
        response = self.llm.ask(system_prompt, user_prompt)
        
        try:
            cleaned_response = response.strip().replace("```json", "").replace("```", "").strip()
            claim_ledger = json.loads(cleaned_response)
            if not isinstance(claim_ledger, list):
                claim_ledger = claim_ledger.get("ledger", [])
        except:
            claim_ledger = []
            
        verified_data = {
            "job_id": job_id,
            "verified_claims": [c for c in claim_ledger if c.get("decision") == "VERIFIED"],
            "rejected_claims": [c for c in claim_ledger if c.get("decision") != "VERIFIED"],
            "ledger": claim_ledger
        }
        
        # Save to job folder
        job_path = os.path.join(job_dir, job_id)
        with open(os.path.join(job_path, "claim_ledger.json"), "w") as f:
            json.dump(verified_data, f, indent=2)
            
        return verified_data
