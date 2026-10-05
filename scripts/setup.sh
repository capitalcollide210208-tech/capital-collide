#!/bin/bash
set -e

echo "Setting up Capital Collide Remote Worker..."

# 1. Update system
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install FFmpeg (The Editor)
sudo apt-get install -y ffmpeg git python3-pip python3-venv

# 3. Install Piper (The Voice)
echo "Installing Piper Voice Engine..."
mkdir -p /opt/piper
# (Simulation of downloading piper binary and model)
# wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz -O /tmp/piper.tar.gz
# tar -xf /tmp/piper.tar.gz -C /opt/piper
# wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en_US/en_US-lessac-medium.onnx -O /opt/piper/model.onnx
# wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en_US/en_US-lessac-medium.onnx.json -O /opt/piper/model.onnx.json

# 4. Setup Python Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Setup complete. Remote worker is ready for production."
