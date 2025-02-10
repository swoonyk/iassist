# iAssist 👁️

## overview
> iAssist is an ai-powered vision assistant designed to provide real-time navigation for visually impaired individuals

![Image](https://github.com/user-attachments/assets/99750507-600b-45f8-a779-f43d26903a82)

## 🚀 key features
- **real-time object detection**: instant obstacle recognition and path guidance
- **priority-based navigation**: employs deque and priority queues to ensure urgent alerts are processed first
- **voice interaction**: utilizes **text-to-speech (TTS)** for a hands-free experience via audio guidance

## 💡 inspiration & approach
traditional navigation aids like guide dogs and specialized devices can be expensive, require training, and aren’t always accessible. iAssist bridges this gap by offering an affordable, AI-driven alternative that runs on a smartphone, reducing financial and logistical barriers
## 🛠 tech stack
### core ai components
- **object detection**: [utralytics yolo11](https://docs.ultralytics.com/models/yolo11/)
- **audio feedback (TTS)**: [hugging face `Kokoro-82M`](https://huggingface.co/hexgrad/Kokoro-82M)
- **ai framework**: [ollama](https://ollama.com/)

## 🧠 technical architecture
iAssist integrates a combination of computer vision, voice processing, and optimized algorithms to deliver fast, reliable, and accessible navigation assistance, integrating:
- data flow buffering 
- adaptive audio feedback
- advanced machine learning models

## 📦 installation
```bash
# clone the repository
git clone https://github.com/swoonyk/iassist.git

# create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```
## 🚦 quick start

### Option 1: Run Full Web Application
1. Install dependencies:
```bash
# Activate virtual environment if not already active
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Server dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
```

2. Start the application:
```bash
# Start the backend server (in the server directory)
cd server
python3 server.py

# In a new terminal, start the frontend (in the frontend directory)
cd frontend
npm run dev
```

### Option 2: Run Visual Tracking Standalone (IN DEVELOPING)
If you only want to run the visual tracking system without the web interface:

```bash
# Activate virtual environment if not already active
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Run the visual tracking system
cd vision
python3 main.py
```

Note: Make sure your camera is accessible and properly connected when running the visual tracking system.

---
**disclaimer**: iAssist is an assistive tool and should not replace professional mobility training. Users should exercise caution while navigating unfamiliar environments
