# Deployment Guide: Netlify + Render

This guide will help you deploy your Event Management System with:
- **Frontend (React Dashboard)** → Netlify
- **Backend (FastAPI)** → Render

---

## Part 1: Deploy Backend to Render

### Step 1: Prepare Backend for Deployment

1. **Create a `render.yaml` file** in the root directory:

```yaml
services:
  - type: web
    name: event-management-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn data_engine:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: XAI_API_KEY
        sync: false
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: JWT_ALGORITHM
        value: HS256
      - key: JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30
      - key: DATABASE_URL
        value: sqlite:///./event_management.db
```

2. **Create a `.renderignore` file** (optional):

```
__pycache__/
*.pyc
.env
Responses/
*.md
test_system.py
```

### Step 2: Deploy to Render

1. **Push your code to GitHub:**

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Go to Render:**
   - Visit https://render.com
   - Sign up/Login
   - Click "New +" → "Web Service"

3. **Configure the service:**
   - Connect your GitHub repository
   - Name: `event-management-api`
   - Region: Choose closest to your users
   - Branch: `main`
   - Root Directory: Leave blank
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn data_engine:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables:**
   Click "Advanced" and add:
   - `XAI_API_KEY`: Your xAI API key
   - `JWT_SECRET_KEY`: A strong random string (or let Render generate)
   - `JWT_ALGORITHM`: `HS256`
   - `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
   - `DATABASE_URL`: `sqlite:///./event_management.db`

5. **Click "Create Web Service"**
   - Wait for deployment to complete
   - Copy your backend URL (e.g., `https://event-management-api.onrender.com`)

---

## Part 2: Deploy Frontend to Netlify

### Step 1: Update Environment Variables

1. **Edit `dashboard/.env.production`:**

Replace the backend URL with your Render URL:

```env
VITE_API_URL=https://your-backend-url.onrender.com
```

### Step 2: Deploy to Netlify

#### Option A: Deploy via Netlify CLI (Recommended)

1. **Install Netlify CLI:**

```bash
npm install -g netlify-cli
```

2. **Login to Netlify:**

```bash
netlify login
```

3. **Initialize Netlify:**

```bash
cd dashboard
netlify init
```

   - Choose: "Create & configure a new site"
   - Select your team
   - Site name: `event-management-dashboard` (or your preference)

4. **Deploy:**

```bash
netlify deploy --prod
```

   - Build command: `npm run build`
   - Publish directory: `dist`

#### Option B: Deploy via GitHub Integration

1. **Push to GitHub:**

```bash
git add .
git commit -m "Prepare for Netlify deployment"
git push origin main
```

2. **Go to Netlify:**
   - Visit https://netlify.com
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub
   - Select your repository

3. **Configure build settings:**
   - Base directory: `dashboard`
   - Build command: `npm run build`
   - Publish directory: `dashboard/dist`

4. **Set Environment Variables:**
   - Go to Site settings → Environment variables
   - Add: `VITE_API_URL` = `https://your-backend-url.onrender.com`

5. **Click "Deploy site"**

---

## Part 3: Post-Deployment Configuration

### 1. Update CORS Settings

After deploying, update `data_engine.py` to allow your Netlify URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://your-site.netlify.app",  # Your Netlify URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Test Your Deployment

1. **Visit your Netlify URL:** `https://your-site.netlify.app`
2. **Login with default credentials:**
   - Username: `admin`
   - Password: `admin123`
3. **Verify all features work:**
   - Dashboard loads with zone data
   - Alerts panel shows notifications
   - Analytics endpoints respond

### 3. Set Up Custom Domain (Optional)

**Netlify:**
- Go to Domain settings
- Add your custom domain
- Follow DNS configuration steps

**Render:**
- Go to Settings → Custom Domain
- Add your domain
- Update DNS records

---

## Part 4: Environment-Specific Builds

### Local Development

Create `dashboard/.env.development`:

```env
VITE_API_URL=http://localhost:8000
```

### Production

The `.env.production` file is already configured.

---

## Part 5: Continuous Deployment

Both Netlify and Render support automatic deployments:

- **Netlify:** Automatically deploys on every push to `main`
- **Render:** Automatically rebuilds and deploys on every push

### Deploy Preview (Netlify)

Every pull request gets a unique preview URL:
- No configuration needed
- Share preview links with team
- Automatic cleanup after merge

---

## Troubleshooting

### Backend Issues

**Problem:** Backend not starting
```bash
# Check Render logs
# Go to Render Dashboard → Your Service → Logs
```

**Problem:** Database errors
- SQLite may not persist data on free tier
- Consider upgrading to PostgreSQL on Render

**Problem:** CORS errors
- Verify your Netlify URL is in `allow_origins`
- Check browser console for exact error

### Frontend Issues

**Problem:** Build fails
```bash
# Test build locally
cd dashboard
npm run build
```

**Problem:** API calls fail
- Verify `VITE_API_URL` is set correctly
- Check browser Network tab for errors
- Ensure backend CORS is configured

**Problem:** Environment variables not loading
- Vite requires `VITE_` prefix
- Rebuild after changing env vars
- Clear browser cache

---

## Monitoring & Maintenance

### 1. Set Up Monitoring

**Render:**
- Built-in metrics dashboard
- Log streaming
- Error tracking

**Netlify:**
- Analytics dashboard
- Form submissions (if needed)
- Function logs

### 2. Database Backups

For production, consider:
- Upgrade to PostgreSQL on Render
- Set up automated backups
- Use database migration tools

### 3. SSL/HTTPS

Both Netlify and Render provide:
- Free SSL certificates
- Automatic HTTPS
- No configuration needed

---

## Cost Estimation

### Free Tier (Development)

**Netlify:**
- ✅ Unlimited sites
- ✅ 100GB bandwidth/month
- ✅ Automatic SSL
- ✅ Continuous deployment

**Render:**
- ✅ 1 web service (free tier)
- ⚠️ Spins down after 15 min inactivity
- ⚠️ 750 hours/month limit
- ⚠️ SQLite data may not persist

### Production Tier

**Netlify Pro:** $19/month
- Unlimited bandwidth
- Advanced analytics
- Password protection

**Render Starter:** $7/month
- Always-on service
- PostgreSQL database
- Priority support

---

## Quick Commands Reference

```bash
# Local Development
cd dashboard
npm run dev

# Build for Production
npm run build

# Deploy to Netlify
netlify deploy --prod

# Check Backend Locally
uvicorn data_engine:app --reload

# Test API
curl https://your-backend.onrender.com/api/zones
```

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Netlify
3. ✅ Configure CORS
4. ✅ Test all features
5. ⚠️ Set up monitoring
6. ⚠️ Configure custom domain
7. ⚠️ Set up database backups
8. ⚠️ Add error tracking (Sentry)

Your Event Management System is now live! 🎉
