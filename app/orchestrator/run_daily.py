import os
import uuid
import json
from datetime import datetime
from typing import List, Dict

from app.common.llm_client import LLMClient
from app.topic_discovery.engine import TopicDiscoveryEngine
from app.research.engine import ResearchEngine
from app.fact_check.engine import FactCheckEngine
from app.story.engine import StoryEngine
from app.script.engine import ScriptEngine
from app.voice.engine import VoiceEngine
from app.visual_director.engine import VisualDirector

class DailyOrchestrator:
    def __init__(self, job_dir="jobs"):
        self.job_dir = job_dir
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)
        
        # Initialize Global LLM Client (GLM 5.3 Flash)
        self.llm = LLMClient()
        
        # Initialize Engines with the LLM Client
        self.topic_engine = TopicDiscoveryEngine(self.llm)
        self.research_engine = ResearchEngine(self.llm)
        self.fact_engine = FactCheckEngine(self.llm)
        self.story_engine = StoryEngine(self.llm)
        self.script_engine = ScriptEngine(self.llm)
        self.voice_engine = VoiceEngine()
        self.visual_engine = VisualDirector()

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
        
        if all(s == "PASS" for s in state["stages"].values()):
            state["status"] = "COMPLETED"
        elif any(s == "FAILED_TERMINAL" for s in state["stages"].values()):
            state["status"] = "FAILED"
            
        with open(job_path, "w") as f:
            json.dump(state, f, indent=2)

    def run_production_cycle(self):
        job_id = self.create_job()
        print(f"Starting production cycle for {job_id}...")
        
        try:
            # 1. Topic Discovery
            topic_data = self.topic_engine.discover_topic(job_id, self.job_dir)
            self.update_stage(job_id, "topic_discovery", "PASS")
            
            # 2. Research
            research_data = self.research_engine.conduct_research(topic_data["topic"], job_id, self.job_dir)
            self.update_stage(job_id, "research", "PASS")
            
            # 3. Fact Check
            verified_data = self.fact_engine.verify_research(research_data, job_id, self.job_dir)
            self.update_stage(job_id, "fact_check", "PASS")
            
            # 4. Story Construction
            story_data = self.story_engine.construct_story(verified_data, job_id, self.job_dir)
            self.update_stage(job_id, "story", "PASS")
            
            # 5. Script Writing
            script_data = self.script_engine.write_script(story_data, job_id, self.job_dir)
            self.update_stage(job_id, "script", "PASS")
            
            # 6. Voice Generation
            voice_file = self.voice_engine.generate_voiceover(script_data["full_script"], job_id, self.job_dir)
            self.update_stage(job_id, "voice", "PASS")
            
            # 7. Visual Planning
            scene_plan = self.visual_engine.create_scene_plan(script_data, job_id, self.job_dir)
            self.update_stage(job_id, "visual_director", "PASS")
            
            print(f"Intelligence and Asset Generation completed for {job_id}. Ready for Video Gen.")
            
        except Exception as e:
            print(f"Production cycle failed: {e}")

if __name__ == "__main__":
    orchestrator = DailyOrchestrator()
    orchestrator.run_production_cycle()
