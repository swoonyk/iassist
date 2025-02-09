# iAssist 👁️

## overview
iAssist is an ai-powered vision assistant designed to provide real-time navigation for visually impaired individuals

## 🚀 key features
- **real-time object detection**: instant obstacle recognition and path guidance
- **priority-based navigation**: employs deque and priority queues to ensure urgent alerts are processed first
- **bidirectional voice interaction**: combines **text-to-speech (TTS)** and **speech-to-text (STT)** for a hands-free experience via voice commands

## 💡 inspiration & approach
traditional navigation aids like guide dogs and specialized devices can be expensive, require training, and aren’t always accessible. iAssist bridges this gap by offering an affordable, AI-driven alternative that runs on a smartphone, reducing financial and logistical barriers
## 🛠 tech stack
### core ai components
- **object detection**: [utralytics yolo11](https://docs.ultralytics.com/models/yolo11/)
- **audio feedback (TTS)**: [hugging face `Kokoro-82M`](https://huggingface.co/hexgrad/Kokoro-82M)
- **speech recognition (STT)**: [groq API](https://api.groq.com/openai/v1/audio/translations)
- **ai framework**: [ollama] (https://ollama.com/)

## 🧠 technical architecture
iAssist integrates a combination of computer vision, voice processing, and optimized algorithms to deliver fast, reliable, and accessible navigation assistance, integrating:
- data flow buffering 
- adaptive audio feedback
- advanced machine learning models

## 📦 installation
```bash
# clone the repository
git clone https://github.com/swoonyk/iassist.git
# highly recommend using a virtual environment 😉
# install dependencies
pip install -r requirements.txt
```
## 🚦 quick start
```python
coming soon 🤭
```
---
**disclaimer**: iAssist is an assistive tool and should not replace professional mobility training. Users should exercise caution while navigating unfamiliar environments
