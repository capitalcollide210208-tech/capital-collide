import json
import os
from typing import Dict, Any, List

class FactCheckEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def verify_research(self, research_data: Dict[str, Any], job_id: str, job_dir="jobs") -> Dict[str, Any]:
        print("Running Fact-Checking Gate...")
        
        claim_ledger = []
        for item in research_data.get("evidence", []):
            claim = item["claim"]
            source = item["source"]
            
            # Simulation of verification process
            decision = "VERIFIED" if item["reliability"] == "High" else "UNCERTAIN"
            
            claim_ledger.append({
                "claim": claim,
                "source": source,
                "decision": decision,
                "confidence": 0.9 if decision == "VERIFIED" else 0.5
            })
            
        verified_data = {
            "job_id": job_id,
            "verified_claims": [c for c in claim_ledger if c["decision"] == "VERIFIED"],
            "rejected_claims": [c for c in claim_ledger if c["decision"] != "VERIFIED"],
            "ledger": claim_ledger
        }
        
        # Save to job folder
        job_path = os.path.join(job_dir, job_id)
        with open(os.path.join(job_path, "claim_ledger.json"), "w") as f:
            json.dump(verified_data, f, indent=2)
            
        return verified_data
