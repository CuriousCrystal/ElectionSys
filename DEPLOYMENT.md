# Deployment Guide: Frontend on Netlify, Backend on Cloud Run

This repo is now configured as an election-assistant app with:
- **Frontend:** static React site hosted on Netlify
- **Backend:** Python FastAPI service hosted on Google Cloud Run or another Python-capable cloud provider

---

## Frontend Deployment (Netlify)

1. Build the frontend:

```bash
cd frontend
npm install
npm run build
```

2. Deploy to Netlify:

- Use the [Netlify app](https://app.netlify.com) and connect your GitHub repository, or
- Use the Netlify CLI:

```bash
npm install -g netlify-cli
netlify login
cd frontend
netlify deploy --prod
```

3. Set environment variables in Netlify:

- `VITE_API_URL` = `https://YOUR_BACKEND_URL`

4. Ensure the publish directory is `dist`.

---

## Backend Deployment (Google Cloud Run)

1. Install Google Cloud SDK and authenticate:

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. Build and push a container image:

```bash
cd backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/election-assistant-backend
```

3. Deploy to Cloud Run:

```bash
gcloud run deploy election-assistant-backend \
  --image gcr.io/YOUR_PROJECT_ID/election-assistant-backend \
  --platform managed \
  --region YOUR_REGION \
  --allow-unauthenticated \
  --set-env-vars XAI_API_KEY=YOUR_API_KEY,CORS_ORIGINS=https://YOUR_NETLIFY_SITE_URL
```

4. Update the frontend `VITE_API_URL` to point to the Cloud Run service URL.

---

## Environment Configuration

Copy the example env file and update the values:

```bash
cp .env.example .env
```

Required variables:

- `GCP_PROJECT_ID`
- `GOOGLE_APPLICATION_CREDENTIALS`
- `XAI_API_KEY`
- `CORS_ORIGINS`

> Do not commit service account credentials or `.env` files to source control.

---

## Notes on Compatibility

- **Netlify cannot host the Python backend**. The frontend is static and compatible with Netlify, but the backend requires a container or dedicated Python runtime.
- **Use Cloud Run or similar** for the FastAPI API, or host on any provider that supports Python web services.
- **CORS must be configured** to allow the Netlify frontend origin in the backend settings.

---

## Security Considerations

- Keep secret keys out of source control.
- Restrict `CORS_ORIGINS` to only trusted frontend domains.
- Do not store sensitive production credentials in client-side code.
- Set `GOOGLE_APPLICATION_CREDENTIALS` on the backend host only.

---

## Local Development

Run backend locally:

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run frontend locally:

```bash
cd frontend
npm install
npm run dev
```

Open the site at `http://localhost:5173`.


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
