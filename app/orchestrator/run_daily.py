import os
import uuid
import json
from datetime import datetime
from typing import List, Dict

class DailyOrchestrator:
    def __init__(self, job_dir="jobs"):
        self.job_dir = job_dir
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)

    def create_job(self) -> str:
        job_id = f"JOB_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        job_path = os.path.join(self.job_dir, job_id)
        os.makedirs(job_path)
        
        state = {
            "job_id": job_id,
            "created_at": datetime.now().isoformat(),
            "status": "PENDING",
            "stages": {
                "topic_discovery": "PENDING",
                "research": "PENDING",
                "fact_check": "PENDING",
                "story": "PENDING",
                "script": "PENDING",
                "voice": "PENDING",
                "semantic_timeline": "PENDING",
                "visual_director": "PENDING",
                "video_generation": "PENDING",
                "qc": "PENDING",
                "publishing": "PENDING",
                "cleanup": "PENDING"
            }
        }
        
        with open(os.path.join(job_path, "job.json"), "w") as f:
            json.dump(state, f, indent=2)
            
        return job_id

    def update_stage(self, job_id: str, stage: str, status: str):
        job_path = os.path.join(self.job_dir, job_id, "job.json")
        with open(job_path, "r") as f:
            state = json.load(f)
        
        state["stages"][stage] = status
        
        # If all stages are PASS, mark job as completed
        if all(s == "PASS" for s in state["stages"].values()):
            state["status"] = "COMPLETED"
        elif any(s == "FAILED_TERMINAL" for s in state["stages"].values()):
            state["status"] = "FAILED"
            
        with open(job_path, "w") as f:
            json.dump(state, f, indent=2)

    def run_production_cycle(self):
        job_id = self.create_job()
        print(f"Starting production cycle for {job_id}...")
        
        # This is where the sequence of stage calls will happen
        # For now, this is a skeleton that will be populated as we build each module
        stages = [
            ("topic_discovery", self.stage_topic_discovery),
            ("research", self.stage_research),
            ("fact_check", self.stage_fact_check),
            # ... other stages
        ]
        
        for stage_name, stage_func in stages:
            try:
                print(f"Executing {stage_name}...")
                success = stage_func(job_id)
                if success:
                    self.update_stage(job_id, stage_name, "PASS")
                else:
                    self.update_stage(job_id, stage_name, "FAILED_RETRYABLE")
                    break # Stop cycle on failure
            except Exception as e:
                print(f"Error in {stage_name}: {e}")
                self.update_stage(job_id, stage_name, "FAILED_TERMINAL")
                break

    def stage_topic_discovery(self, job_id):
        # Placeholder for topic discovery logic
        print(f"Topic discovery for {job_id}...")
        return True

    def stage_research(self, job_id):
        # Placeholder for research logic
        print(f"Research for {job_id}...")
        return True

    def stage_fact_check(self, job_id):
        # Placeholder for fact check logic
        print(f"Fact checking for {job_id}...")
        return True

if __name__ == "__main__":
    orchestrator = DailyOrchestrator()
    orchestrator.run_production_cycle()
