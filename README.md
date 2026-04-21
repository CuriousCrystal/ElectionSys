Election Assistant System — Full Restructure
Rebuild the project from a simulated crowd-management demo into a production-ready, API-driven Election Assistant System with MongoDB, an interactive React frontend, and clean architecture — no garbage/hardcoded values.

User Review Required
IMPORTANT

The project name is "Election Assistant System" but the existing code is an Event Crowd Management system (zones, gates, food courts, restrooms). The restructure will rebrand the entire system for election management — polling booths, voter queues, constituency dashboards, result tracking, etc. Please confirm this is the intended direction, or let me know if you'd like to keep the event/crowd theme and just improve the architecture.

IMPORTANT

You mentioned APIs "will be provided later." The restructured backend will expose its own RESTful API and the frontend will consume it. I'll add a clean apiService layer with a configurable base URL so that when you provide external APIs later, you can swap endpoints with zero frontend changes. Does this approach work for you?

WARNING

The existing main.py (voice-based August assistant with Grok/xAI) will be preserved as-is in a separate assistant/ folder but will not be the main entry point. The new system's entry point will be the FastAPI backend + React frontend. Confirm if this is acceptable.

Open Questions
Election domain model — Should the system track:

Polling booths (crowd density, queue wait times, voter throughput)?
Constituencies / Wards?
Candidate & party data?
Vote counting / results?
All of the above?
User roles — Current system has admin, manager, viewer. Should we keep these or change to election-specific roles (e.g., returning_officer, booth_agent, observer)?

MongoDB connection — Do you already have a MongoDB Atlas URI, or should I set it up for local mongodb://localhost:27017?

Proposed Changes
Project Structure (New)
Election Assistant System/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── config.py           # Settings & env vars
│   │   ├── database.py         # MongoDB connection (Motor async)
│   │   ├── models/             # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── booth.py
│   │   │   ├── alert.py
│   │   │   └── analytics.py
│   │   ├── routers/            # API route modules
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── booths.py
│   │   │   ├── alerts.py
│   │   │   ├── analytics.py
│   │   │   └── chat.py         # AI assistant endpoint
│   │   ├── services/           # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── booth_service.py
│   │   │   └── alert_service.py
│   │   └── middleware/
│   │       └── cors.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/                   # React + Vite
│   ├── src/
│   │   ├── api/
│   │   │   └── apiService.js   # Centralized API layer
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── Header.jsx
│   │   │   │   └── Layout.jsx
│   │   │   ├── dashboard/
│   │   │   │   ├── StatsCards.jsx
│   │   │   │   ├── LiveMap.jsx
│   │   │   │   └── RecentAlerts.jsx
│   │   │   ├── booths/
│   │   │   │   ├── BoothList.jsx
│   │   │   │   ├── BoothCard.jsx
│   │   │   │   └── BoothDetail.jsx
│   │   │   ├── analytics/
│   │   │   │   ├── Charts.jsx
│   │   │   │   └── Reports.jsx
│   │   │   ├── alerts/
│   │   │   │   └── AlertsPanel.jsx
│   │   │   ├── chat/
│   │   │   │   └── ChatWidget.jsx
│   │   │   └── auth/
│   │   │       └── Login.jsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── BoothsPage.jsx
│   │   │   ├── AnalyticsPage.jsx
│   │   │   ├── AlertsPage.jsx
│   │   │   └── SettingsPage.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   └── usePolling.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
├── assistant/                  # Preserved August AI (original main.py)
│   ├── main.py
│   ├── config.py
│   └── voice.py
└── .env.example
Backend — MongoDB Migration
[NEW] 
database.py
Replace SQLAlchemy + SQLite with Motor (async MongoDB driver)
Connection via MONGODB_URI env var (default: mongodb://localhost:27017)
Database name: election_assistant
Collections: users, booths, alerts, audit_logs, analytics_snapshots
[NEW] 
models/booth.py
Pydantic models for Polling Booth:
booth_id, name, constituency, capacity, current_voters, queue_length, wait_time_minutes, status (smooth/busy/critical), coordinates, last_updated
No hardcoded/simulated values — all data comes from MongoDB or future API
[NEW] 
models/user.py
User model with username, email, full_name, hashed_password, role, is_active
Users stored in MongoDB users collection (replacing in-memory fake_users_db)
[NEW] 
routers/booths.py
CRUD endpoints for booths:
GET /api/booths — list all booths
GET /api/booths/{id} — get booth detail
POST /api/booths — create booth (admin)
PUT /api/booths/{id} — update booth data
DELETE /api/booths/{id} — remove booth (admin)
GET /api/booths/recommendations — best booth recommendations
[NEW] 
routers/auth.py
Same JWT auth flow but users stored in MongoDB
Registration creates user documents in users collection
Password hashing with bcrypt (same as before)
[NEW] 
routers/chat.py
POST /api/chat — send message to AI assistant, get response
Integrates with the Grok/xAI API (from original main.py)
No voice — pure HTTP request/response for the frontend chat widget
[MODIFY] 
main.py
Clean FastAPI app with:
Router includes for auth, booths, alerts, analytics, chat
CORS middleware
MongoDB startup/shutdown lifecycle events
No simulated data generation — data is managed through the API
Frontend — Interactive Dashboard Rebuild
[NEW] Multi-page routing with react-router-dom
Dashboard — Overview with stat cards, live booth status, recent alerts
Booths — Full CRUD management of polling booths with search/filter
Analytics — Charts (using recharts) showing historical trends
Alerts — Full alerts management page
Settings — User profile & system settings
[NEW] 
apiService.js
Centralized Axios-based API service
Configurable BASE_URL via VITE_API_URL env var
Auto-attaches JWT token from auth context
Interceptors for 401 handling (auto-logout)
Ready for API swap — all endpoints defined in one place
[NEW] 
AuthContext.jsx
React Context for auth state management
Login/logout/token refresh functions
Wraps entire app
[NEW] 
Layout.jsx
Collapsible sidebar navigation with icons
Top header bar with user info, notifications, logout
Glassmorphism dark theme (enhanced from current)
[NEW] 
ChatWidget.jsx
Floating chat bubble in bottom-right corner
Expandable chat panel with message history
Sends messages to /api/chat endpoint
Typing indicators, auto-scroll
Design System Enhancements
Google Fonts: Inter (body) + Space Groteby (headings)
Color palette: Deep navy backgrounds, cyan/purple accents (enhanced from current)
Micro-animations on all interactive elements
Responsive down to mobile
Charts with smooth transitions
Data Management — No Garbage Values
IMPORTANT

All simulated/hardcoded data will be removed. The system will show an empty state when no data exists, with clear CTAs to add data. The old simulate_crowds() background task and hardcoded zones dictionary will be deleted entirely.

Booths are created via the admin UI or API
Alerts are generated based on real booth data thresholds
Analytics are computed from actual MongoDB documents
The frontend shows proper empty states ("No booths configured yet — Add your first booth")
Verification Plan
Automated Tests
pip install -r requirements.txt — verify all dependencies install
uvicorn backend.app.main:app --reload — verify server starts
cd frontend && npm install && npm run dev — verify frontend starts
Test API endpoints via FastAPI Swagger UI at /docs
Manual Verification
Login flow works with MongoDB-stored users
CRUD operations for booths work end-to-end
Dashboard displays real data from MongoDB
Chat widget communicates with AI endpoint
Alerts appear based on booth data thresholds
All pages render correctly on desktop and mobile
