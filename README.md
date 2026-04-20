Event Crowd Management & AI Assistant

What Works (Really Well)
🎤 Voice Assistant ("August")

Listens via microphone, speaks responses
Can fetch live crowd data and make recommendations
Falls back to text input gracefully
Understands commands like "open YouTube" or "what time is it"

Example conversation:
You: "Where's the shortest wait for the restroom?"
August: *fetches wait times from API* 
        "Restrooms North has only a 1 minute wait right now!"
        
🔐 Authentication
Three default users (admin/manager/viewer) with different permissions
JWT tokens with 30-min expiration
Bcrypt password hashing
Proper role-based access control

📊 Dashboard
Real-time zone status display
Alert notifications with badges
Historical analytics (stores data every 5 seconds)
View past data with time-range queries

🚨 Alert System
Configurable thresholds for density/wait times
Three severity levels: Medium, High, Critical
Database persistence of all alerts
Audit logging of user actions


How to Actually Run This
Prerequisites
bash# You need:
- Python 3.8+
- Node.js 16+
- A microphone (for voice features)
- X.AI API key (for Grok)
Backend Setup
bash# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your XAI_API_KEY

# Start the API server
uvicorn data_engine:app --reload
Backend runs on: http://localhost:8000
API docs available at: http://localhost:8000/docs
Frontend Setup
bashcd dashboard

# Install dependencies
npm install

# Start dev server
npm run dev
Dashboard runs on: http://localhost:5173
Run the Voice Assistant
bashpython main.py

Default Credentials
Admin:   admin / admin123       (full access)
Manager: manager / manager123   (view analytics & alerts)
Viewer:  viewer / viewer123     (read-only dashboard)

Project Structure
.
├── main.py                    # Voice assistant entry point
├── data_engine.py             # FastAPI server + crowd simulation
├── auth.py                    # JWT authentication
├── analytics.py               # Historical data & reports
├── alerts.py                  # Alert generation & thresholds
├── database.py                # SQLAlchemy models
├── config.py                  # Environment variable management
├── dashboard/                 # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main app component
│   │   ├── Login.jsx         # Authentication UI
│   │   └── AlertsPanel.jsx   # Alert notifications
│   └── package.json
├── requirements.txt           # Python dependencies
└── .env.example              # Environment template

The Architecture
┌─────────────────────────────────────────────┐
│         User (Voice or Web)                 │
│    "What's the shortest wait?"              │
└──────────────┬──────────────────────────────┘
               │
        ┌──────▼──────┐
        │   August    │
        │   (Grok)    │
        └──────┬──────┘
               │ "I need to check wait times"
       ┌───────▼────────┐
       │  FastAPI       │
       │  /api/zones    │
       │  /api/recommendations
       └───────┬────────┘
               │ (randomly generated data)
        ┌──────▼──────┐
        │  SQLite DB  │
        │  (stores    │
        │  fake data) │
        └─────────────┘

