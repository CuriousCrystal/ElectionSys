# Deployment Architecture & Workflow

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                                 │
│                    https://your-site.netlify.app                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                    HTTPS / TLS Encrypted
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      NETLIFY (CDN)                                  │
│                                                                     │
│  📦 Static Site Hosting                                            │
│  ├─ React Application (Built with Vite)                            │
│  ├─ Login Page                                                     │
│  ├─ Dashboard UI                                                   │
│  ├─ Alerts Panel                                                   │
│  └─ Analytics Interface                                            │
│                                                                     │
│  ✅ Features:                                                       │
│  ├─ Global CDN (Fast loading worldwide)                            │
│  ├─ Automatic SSL/HTTPS                                            │
│  ├─ Continuous Deployment                                          │
│  └─ 100GB bandwidth/month (Free)                                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                    API Calls (JSON/REST)
                    https://your-api.onrender.com
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        RENDER (Backend API)                         │
│                                                                     │
│  🐍 FastAPI Python Application                                     │
│  ├─ Authentication Service (JWT)                                   │
│  ├─ Zone Management API                                            │
│  ├─ Analytics Engine                                               │
│  ├─ Alert System                                                   │
│  └─ AI Integration (xAI/Grok)                                      │
│                                                                     │
│  📊 Background Tasks:                                               │
│  ├─ Crowd Simulation (Every 5 seconds)                             │
│  ├─ Alert Generation                                               │
│  └─ Database Updates                                               │
│                                                                     │
│  ✅ Features:                                                       │
│  ├─ Auto-scaling                                                    │
│  ├─ Health Checks                                                  │
│  ├─ Automatic HTTPS                                                │
│  └─ 750 hours/month (Free)                                         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                         SQLAlchemy
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     SQLite Database                                 │
│                                                                     │
│  📁 Tables:                                                         │
│  ├─ zone_snapshots (Historical metrics)                            │
│  ├─ alerts (Notification records)                                  │
│  └─ audit_logs (User activity tracking)                            │
│                                                                     │
│  ⚠️ Note: On free tier, data may not persist across restarts       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Deployment Workflow

### Step-by-Step Process

```
┌──────────────┐
│  DEVELOPMENT │
│   (Local)    │
└──────┬───────┘
       │
       │ 1. Code & Test Locally
       │    ├─ Backend: uvicorn data_engine:app --reload
       │    └─ Frontend: cd dashboard && npm run dev
       │
       ▼
┌──────────────┐
│     GIT      │
│   (GitHub)   │
└──────┬───────┘
       │
       │ 2. Push Code
       │    git add .
       │    git commit -m "Ready"
       │    git push origin main
       │
       ▼
┌──────────────────────────────────────────┐
│         TRIGGER DEPLOYMENTS              │
└──────┬───────────────────────────┬───────┘
       │                           │
       │                           │
       ▼                           ▼
┌──────────────┐          ┌──────────────┐
│   NETLIFY    │          │    RENDER    │
│  (Frontend)  │          │  (Backend)   │
└──────┬───────┘          └──────┬───────┘
       │                         │
       │ 3a. Build React         │ 3b. Install Python deps
       │     npm run build       │     pip install -r reqs
       │                         │
       │ 4a. Deploy to CDN       │ 4b. Start FastAPI
       │     Auto HTTPS          │     Auto HTTPS
       │                         │
       ▼                         ▼
┌──────────────┐          ┌──────────────┐
│    LIVE      │          │    LIVE      │
│  Frontend    │◄────────►│   Backend    │
│              │   API    │              │
│ your-site    │  Calls   │ your-api     │
│ .netlify.app │◄────────►│ .onrender.com│
└──────────────┘          └──────────────┘
```

---

## Data Flow

### User Login Flow
```
User → Netlify (Login Page)
   ↓
Enter credentials
   ↓
POST /api/auth/login → Render
   ↓
Verify password (bcrypt)
   ↓
Generate JWT token
   ↓
Return token → Netlify → User Browser
   ↓
Store in localStorage
```

### Dashboard Data Flow
```
User opens dashboard
   ↓
React app loads from Netlify
   ↓
Fetch user info: GET /api/auth/me → Render
   ↓
Fetch zones: GET /api/zones → Render
   ↓
Return live data → Display on dashboard
   ↓
Auto-refresh every 3 seconds
```

### Alert Generation Flow
```
Background Task (Every 5s)
   ↓
Simulate crowd data
   ↓
Check thresholds
   ├─ Density > 60%? → Create alert
   ├─ Wait time > 10min? → Create alert
   └─ Status = Bottleneck? → Create alert
   ↓
Save to database
   ↓
Frontend polls: GET /api/alerts/recent
   ↓
Display in AlertsPanel
   ↓
User clicks → Mark as read
```

---

## Environment Variables

### Frontend (Netlify)
```
VITE_API_URL=https://your-api.onrender.com
```

### Backend (Render)
```
XAI_API_KEY=sk-or-v1-xxxxx
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./event_management.db
PORT=10000 (auto-set by Render)
```

---

## File Structure After Deployment

### What's on Netlify
```
/ (Netlify CDN)
├── index.html
├── vite.svg
├── assets/
│   ├── index-CTmieQTu.js      (React app - 204KB)
│   └── index-P25ZQmKd.css     (Styles - 2.8KB)
└── _redirects                  (SPA routing)
```

### What's on Render
```
/ (Render Server)
├── data_engine.py              (Main app)
├── auth.py                     (Authentication)
├── analytics.py                (Analytics API)
├── alerts.py                   (Alert system)
├── database.py                 (Database models)
├── config.py                   (Config loader)
├── requirements.txt            (Dependencies)
├── event_management.db         (SQLite database)
└── __pycache__/                (Compiled Python)
```

---

## Communication Protocols

```
Browser ←→ Netlify
  Protocol: HTTPS (TLS 1.3)
  Content: Static files (HTML, CSS, JS)
  Port: 443

Netlify ←→ Render
  Protocol: HTTPS (TLS 1.3)
  Content: JSON API requests
  Port: 443
  
Render ←→ Database
  Protocol: SQLite (File-based)
  Content: SQL queries
  Location: Local file system
```

---

## Security Layers

```
┌─────────────────────────────────────┐
│  Layer 1: HTTPS/TLS                 │
│  ├─ Netlify auto-SSL                │
│  └─ Render auto-SSL                 │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  Layer 2: CORS Policy               │
│  └─ Only allow your Netlify domain  │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  Layer 3: JWT Authentication        │
│  ├─ Token required for API calls    │
│  └─ 30-minute expiration            │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  Layer 4: Role-Based Access         │
│  ├─ Admin: Full access              │
│  ├─ Manager: View + reports         │
│  └─ Viewer: Read-only               │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  Layer 5: Password Hashing          │
│  └─ bcrypt (salt rounds: 12)        │
└─────────────────────────────────────┘
```

---

## Deployment Timeline

```
Minute 0:  Push to GitHub
           │
Minute 1:  ├─ Netlify detects change
           ├─ Render detects change
           │
Minute 2:  ├─ Netlify: npm install
           ├─ Render: pip install
           │
Minute 3:  ├─ Netlify: npm run build
           ├─ Render: Start uvicorn
           │
Minute 4:  ├─ Netlify: Deploy to CDN
           ├─ Render: Health check passes
           │
Minute 5:  ✓ Both services live!
```

**Total deployment time: ~5 minutes** ⚡

---

## Monitoring & Logs

### Netlify
- **Dashboard:** https://app.netlify.com
- **Logs:** Deploy logs, function logs
- **Analytics:** Visitor stats, bandwidth usage

### Render
- **Dashboard:** https://dashboard.render.com
- **Logs:** Real-time application logs
- **Metrics:** CPU, memory, response time

---

## Cost Comparison

### Free Tier
```
Netlify: $0                Render: $0
├─ 100GB bandwidth         ├─ 750 hours/month
├─ Unlimited sites         ├─ Auto-sleep after 15min
├─ Auto SSL                ├─ SQLite storage
└─ Continuous deploy       └─ Basic monitoring
```

### Production Tier
```
Netlify Pro: $19/mo        Render Starter: $7/mo
├─ Unlimited bandwidth     ├─ Always-on service
├─ Advanced analytics      ├─ PostgreSQL database
├─ Password protection     ├─ Priority support
└─ Team collaboration      └─ Better performance

Total: $26/month
```

---

## Quick Decision Tree

```
Need to deploy?
    │
    ├─ Just frontend changes?
    │   └─ Push to GitHub → Netlify auto-deploys
    │
    ├─ Just backend changes?
    │   └─ Push to GitHub → Render auto-deploys
    │
    └─ Both changed?
        └─ Push to GitHub → Both auto-deploy
            └─ Update VITE_API_URL if backend URL changed
```

---

## Success Indicators

✅ **Deployment Successful:**
- Netlify: "Published" status
- Render: "Live" status
- Health check: 200 OK
- Can access frontend URL
- Can login successfully

❌ **Deployment Failed:**
- Check build logs
- Verify environment variables
- Review error messages
- Test locally first

---

**Ready to deploy?** Follow the steps in `DEPLOYMENT.md` or run `.\deploy.ps1`!
