# Deployment Guide: Frontend on Netlify, Backend on Google Cloud Run

This repository is configured as an Election Assistant app (August) with:
- **Frontend:** Static React site hosted on Netlify.
- **Backend:** Python FastAPI service hosted on Google Cloud Run.

---

## 1. Backend Deployment (Google Cloud Run)

### Prerequisites
- Google Cloud SDK installed and authenticated.
- A Google Cloud Project created.
- Billing enabled for the project.

### Setup Secret Manager (Recommended)
Store your sensitive API keys securely in GCP Secret Manager:

1. **Create the secret**:
   ```bash
   gcloud secrets create XAI_API_KEY --replication-policy="automatic"
   ```

2. **Add your API key value**:
   ```bash
   echo -n "YOUR_XAI_API_KEY" | gcloud secrets versions add XAI_API_KEY --data-file=-
   ```

3. **Ensure the Cloud Run service account** has the `Secret Manager Secret Accessor` role.

### Deploy to Cloud Run

1. **Configure your project**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Build and push the container image** using Cloud Build:
   ```bash
   cd backend
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/election-assistant-backend
   ```

3. **Deploy the service**:
   ```bash
   gcloud run deploy election-assistant-backend \
     --image gcr.io/YOUR_PROJECT_ID/election-assistant-backend \
     --platform managed \
     --region YOUR_REGION \
     --allow-unauthenticated \
     --set-env-vars GCP_PROJECT_ID=YOUR_PROJECT_ID,CORS_ORIGINS=https://YOUR_NETLIFY_SITE_URL
   ```
   *Note: The backend is now configured to automatically fetch `XAI_API_KEY` from Secret Manager if `GCP_PROJECT_ID` is set.*

4. **Copy the Service URL** provided after deployment (e.g., `https://election-assistant-backend-abc-de.a.run.app`).

---

## 2. Frontend Deployment (Netlify)

1. **Build and Deploy**:
   - Connect your GitHub repo to Netlify for automatic deployments, OR
   - Deploy manually:
     ```bash
     cd frontend
     npm install
     npm run build
     netlify deploy --prod --dir=dist
     ```

2. **Configure Environment Variables in Netlify**:
   - Go to Site Settings > Environment Variables.
   - Add `VITE_API_URL`: Set this to your **Cloud Run Service URL** from Step 1.4.

---

## 3. Local Development

### Backend
```bash
cd backend
python -m pip install -r requirements.txt
# Create a .env file with XAI_API_KEY
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
# Update .env or use the default localhost URL
npm run dev
```

---

## 4. Troubleshooting

### CORS Errors
- Ensure your Netlify URL (including `https://`) is correctly set in the `CORS_ORIGINS` environment variable of your Cloud Run service.

### AI Assistant Not Responding
- Check the Cloud Run logs in the GCP Console.
- Verify that the `XAI_API_KEY` exists in Secret Manager and that the service account has access.
- Ensure `GCP_PROJECT_ID` is correctly set in the Cloud Run environment variables.
