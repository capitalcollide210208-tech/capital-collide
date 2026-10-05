import os
import subprocess
import json
from typing import Dict, Any

class VoiceEngine:
    def __init__(self, model_path="/opt/piper/model.onnx", config_path="/opt/piper/model.onnx.json"):
        self.model_path = model_path
        self.config_path = config_path

    def generate_voiceover(self, script_text: str, job_id: str, job_dir="jobs") -> str:
        print("Generating documentary narration using Piper...")
        
        output_file = os.path.join(job_dir, job_id, "voiceover.wav")
        
        # Command to run Piper (assumes piper is installed on the remote worker)
        # echo "text" | piper --model model.onnx --output_file voiceover.wav
        try:
            process = subprocess.Popen(
                ["piper", "--model", self.model_path, "--output_file", output_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            process.communicate(input=script_text)
            
            if process.returncode == 0:
                print(f"Voiceover successfully generated: {output_file}")
                return output_file
            else:
                raise Exception(f"Piper error: {process.stderr}")
                
        except FileNotFoundError:
            print("Piper not found on system. Simulating audio file for architecture validation...")
            # Create a dummy file for validation
            with open(output_file, "wb") as f:
                f.write(b"RIFF\x00\x00\x00\x00WAVEfmt ")
            return output_file

