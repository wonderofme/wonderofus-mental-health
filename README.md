# 🧠 🏥 🤖 WonderOfUs - AI Mental Health Companion

<div align="center">

**An AI-powered mental health triage companion designed for the TELUS Health ecosystem, featuring privacy-first edge inference.**

---

## 👥 Team

**Team Name**: WonderOfUs  
**Members**:
- **Ayoola Opere**
- **Mujah Sokoro**

**Hackathon**: TELUS Hackathon 2025 - AI at the Edge of Innovation  
**Track**: AI + Healthcare & Wellness  
**Theme**: Technology that heals and helps

---

[![Next.js](https://img.shields.io/badge/Next.js-14.2-black?logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.3-38bdf8?logo=tailwind-css)](https://tailwindcss.com/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-yellow?logo=huggingface)](https://huggingface.co/)

</div>

---

## 🎯 Why This Matters

**Current mental health wait times are too long.** In Canada, the average wait time for mental health services can be weeks or months. During this critical waiting period, individuals often have no immediate support, leading to worsening conditions and crisis situations.

**WonderOfUs acts as an "Immediate Companion"** - providing 24/7 AI-powered mental health support while users wait for professional care. It's not a replacement for therapy, but a crucial bridge that:

- ✅ Provides **immediate emotional support** when needed most
- ✅ **Detects crisis situations** and connects users to resources instantly
- ✅ **Tracks patterns** to help identify triggers and improvements
- ✅ **Maintains privacy** with local AI processing (HIPAA-compliant design)
- ✅ **Scales to millions** through TELUS Health's infrastructure

---

## ✨ Key Features

### ✅ Real-time Sentiment Analysis
Instant mood detection from text input using advanced NLP models

### ✅ Multi-Emotion Detection
Identifies joy, sadness, anxiety, anger, fear, and more with confidence scores

### ✅ Crisis Intervention
Automatically detects high-risk situations and provides immediate resources

### ✅ Pattern Recognition
Identifies mood trends, time-of-day patterns, and emotional triggers

### ✅ Privacy-First Architecture
All AI processing happens locally - no data sent to external APIs (HIPAA-ready)

### ✅ Interactive Dashboard
Beautiful visualizations showing mood trends, patterns, and insights

### ✅ Personalized Recommendations
AI-generated wellness strategies based on individual mood patterns

### ✅ Face Scanning Mood Detection
Real-time emotion detection from webcam or uploaded images

### ✅ TELUS AI Factory Integration
Enhanced AI capabilities using TELUS AI Factory models:
- **gemma-3-27b**: Personalized empathetic recommendations
- **deepseekv32**: Advanced crisis detection reasoning

---

## 🏗️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Frontend** | Next.js 14, React, TypeScript, Tailwind CSS, face-api.js |
| **Backend** | Python 3.10+, FastAPI, Uvicorn |
| **AI/ML** | Hugging Face Transformers, PyTorch, TELUS AI Factory (gemma-3-27b, deepseekv32) |
| **Data Visualization** | Recharts |
| **Architecture** | RESTful API, Component-based UI |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm/yarn
- Git

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🧪 Test Prompts

Copy and paste these prompts to test different AI capabilities:

| Category | Test Prompt | What It Tests |
|----------|-------------|---------------|
| **Positive** | `I'm feeling really great today! I just got a promotion at work and I'm so excited about the future.` | Positive sentiment, high mood score, joy detection |
| **Negative** | `I'm feeling really anxious about my upcoming exam. I can't stop worrying about whether I'll pass or not.` | Negative sentiment, anxiety detection, low mood score |
| **Crisis** | `I feel hopeless and don't see a way out of this situation. Nothing matters anymore.` | Crisis detection, automatic resource provision, HIGH risk level |
| **Mixed** | `I'm feeling conflicted. Part of me is excited about the new opportunity, but I'm also scared of the change.` | Complex emotions, mixed sentiment |
| **Neutral** | `Just another regular day. Nothing special happened, feeling pretty neutral about everything.` | Neutral sentiment detection |
| **Anger** | `I'm so angry right now! Someone cut me off in traffic and I'm still fuming about it.` | Specific emotion detection (anger) |
| **Sadness** | `Feeling really sad after watching a movie. It brought up some old memories that made me emotional.` | Sadness detection, emotional triggers |

**💡 Tip**: After analyzing multiple prompts, check the Dashboard tab to see mood trends and pattern recognition!

---

## 📊 Project Structure

```
TELUS-Hackathon/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── services/
│   │   │   ├── ai_service.py    # AI/ML services (privacy-compliant)
│   │   │   └── mood_service.py   # Mood tracking & patterns
│   │   └── routes/
│   │       ├── mood.py          # Mood analysis endpoints
│   │       ├── insights.py      # Insights & recommendations
│   │       ├── crisis.py         # Crisis detection
│   │       └── dev.py            # Demo data seeder
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                # Next.js app directory
│   │   ├── components/          # React components
│   │   │   ├── MoodAnalyzer.tsx
│   │   │   ├── MoodDashboard.tsx
│   │   │   ├── CrisisResources.tsx
│   │   │   └── TestPrompts.tsx
│   │   └── services/            # API services
│   └── package.json
└── README.md
```

---

## 🔒 Privacy & Security

### HIPAA-Compliant Design
- **Local AI Processing**: All models run on the server (Hugging Face Transformers)
- **No External APIs**: No data sent to OpenAI, Google, or other third-party services
- **Inference-Only**: Models are downloaded and run locally
- **Data Encryption**: Ready for encrypted database storage in production
- **User Control**: Users can delete their data at any time

### What This Means
Your mental health data stays private. The AI analyzes your text locally, and no one else sees it.

---

## 🎯 TELUS Health Integration

### Built for TELUS Health Ecosystem

This solution is designed to integrate seamlessly with TELUS Health's digital health platform:

- **Scalability**: Can handle TELUS Health's patient base (millions of users)
- **Telemedicine**: Integrates with virtual care platforms
- **IoT Ready**: Can connect with wearable devices for comprehensive monitoring
- **Enterprise Architecture**: Production-ready, secure, and compliant
- **Patient Engagement**: Complements TELUS Health's patient engagement tools

### Integration Points
- Patient portal integration
- Telemedicine provider connections
- Wearable device data (heart rate, sleep, activity)
- Electronic health records (EHR) systems
- Care provider dashboards

---

## 📈 Impact & Use Cases

### Individual Users
- **24/7 Support**: Immediate emotional support when professional help isn't available
- **Early Detection**: Identifies mental health patterns before they become crises
- **Privacy-Preserving**: Safe space to express feelings without judgment
- **Progress Tracking**: Visual insights into mood improvements over time

### Healthcare Providers
- **Patient Engagement**: Tool for patients to track mood between appointments
- **Remote Monitoring**: Identify patients who need immediate attention
- **Data-Driven Insights**: Understand patient patterns to improve treatment
- **Telemedicine Integration**: Companion tool for virtual care sessions

### TELUS Health
- **Scalable Platform**: Ready for deployment across TELUS Health's network
- **Cost Reduction**: Reduces emergency room visits through early intervention
- **Patient Outcomes**: Improves mental health outcomes through continuous support
- **Innovation Leadership**: Demonstrates TELUS's commitment to digital health innovation

---

## 🛠️ API Endpoints

### Mood Analysis
- `POST /api/mood/analyze` - Analyze text for sentiment and emotions
- `GET /api/mood/history` - Get mood history for a user
- `POST /api/mood/predict` - Predict future mood trends

### Insights
- `GET /api/insights/patterns` - Get identified mood patterns
- `GET /api/insights/recommendations` - Get personalized recommendations

### Crisis
- `POST /api/crisis/check` - Check for crisis indicators
- `GET /api/crisis/resources` - Get crisis support resources

### Development
- `POST /api/dev/seed` - Seed demo data for presentation

---

## 🎬 Demo Features

### Demo Data Seeder
The application includes a demo data seeder that creates 14 days of realistic mood entries showing a recovery arc. This allows judges to see the full capabilities of the dashboard and pattern recognition features.

**To use**: Click "Load Demo Data for Presentation" on the Dashboard tab.

### Sample Messages
The application includes a "Sample Messages" feature with pre-written test prompts to demonstrate different AI capabilities (positive, negative, crisis, mixed emotions). Click the "Sample Messages" button in the Mood Analyzer to access them.

---

## 🚧 Future Roadmap

### Phase 1 (Current - Hackathon MVP) ✅
- Real-time sentiment analysis
- Mood tracking dashboard
- Basic pattern recognition
- Crisis detection
- TELUS AI Factory integration (gemma-3-27b, deepseekv32)
- Face scanning mood detection

### Phase 2 (Post-Hackathon)
- Voice input analysis
- Wearable device integration (IoT)
- Advanced predictive models
- Multi-language support
- Mobile app (iOS/Android)

### Phase 3 (Enterprise Integration)
- TELUS Health platform integration
- Telemedicine provider connections
- HIPAA compliance certification
- Scalable cloud deployment
- EHR system integration

---

## 📝 License

This project was developed for the TELUS Hackathon 2025 competition.

---

## 🙏 Acknowledgments

- **TELUS Health** for inspiring healthcare innovation
- **Hugging Face** for open-source AI models
- **The mental health community** for their ongoing advocacy
- **Crisis Services Canada** and other support organizations

---

<div align="center">

**Built with ❤️ by Team WonderOfUs for TELUS Hackathon 2025**

*AI at the Edge of Innovation*

</div>
