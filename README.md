# Election Process Assistant

A focused, interactive assistant that helps users understand election processes, timelines, and voting steps in an easy-to-follow way.

This repo contains:
- a React frontend help center and chat widget
- a FastAPI backend AI chat endpoint
- simple deployment guidance for Netlify (frontend) and Google Cloud Run (backend)

---

## 🚀 Quick Start

### Run the backend
```bash
cd backend
python -m pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run the frontend
```bash
cd frontend
npm install
npm run dev
```

### Open the app
- Frontend: http://localhost:5173
- Backend health check: http://localhost:8000/api/health

---

## 🔧 Project Structure

```
ElectionSys/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── main.py
│   │   ├── middleware/
│   │   │   └── rate_limit.py
│   │   ├── routers/
│   │   │   └── chat.py
│   │   └── __init__.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api/
│   │   │   └── apiService.js
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   │   └── ChatWidget.jsx
│   │   │   └── layout/
│   │   │       ├── Header.jsx
│   │   │       ├── Layout.jsx
│   │   │       └── Sidebar.jsx
│   │   ├── index.css
│   │   ├── index.html
│   │   ├── main.jsx
│   │   └── pages/
│   │       └── HelpPage.jsx
│   ├── netlify.toml
│   └── package.json
├── .env.example
├── DEPLOYMENT.md
└── README.md
```

---

## 💡 What changed

- Removed legacy dashboard/auth/data persistence files from the active backend and frontend stack.
- Kept the app focused on an election assistant experience with chat and help content.
- Switched deployment guidance to Netlify for frontend and Google Cloud Run (or equivalent) for backend.
- Removed database and JWT implementation from the main flow.

---

## 📌 Notes

- The backend is a stateless AI chat service and does not require a local database.
- The frontend is static and compatible with Netlify hosting.
- The Python backend must be hosted in a Python-capable environment (Google Cloud Run, Render, etc.).
- Keep secrets and service account credentials out of version control.
