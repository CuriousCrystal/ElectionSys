# Deployment Guide: All-in-One Netlify Deployment

This repository is configured to host both the **React Frontend** and the **FastAPI Backend** on Netlify.

---

## 1. How it Works
- **Frontend:** Built as a static site.
- **Backend:** Converted into a **Netlify Function** using `Mangum`.
- **Routing:** Any request to `/api/*` is automatically redirected to the Python backend function.

---

## 2. Deployment Steps

### Step 1: Push to GitHub
Ensure your latest changes (including `netlify.toml` in the root) are pushed to your GitHub repository.

### Step 2: Connect to Netlify
1. Log in to [Netlify](https://app.netlify.com).
2. Click **"Add new site"** > **"Import an existing project"**.
3. Select your GitHub repository.

### Step 3: Configure Build Settings
Netlify should automatically detect the settings from `netlify.toml`, but verify they match:
- **Build command:** `cd frontend && npm install && npm run build`
- **Publish directory:** `frontend/dist`
- **Functions directory:** `backend/app`

### Step 4: Set Environment Variables
In the Netlify Dashboard (Site Settings > Environment Variables):
1. **`XAI_API_KEY`**: Your Grok/OpenAI API key.
2. **`PYTHON_VERSION`**: Set to `3.11`.

---

## 3. Local Testing
To test the Netlify setup locally, use the Netlify CLI:
```bash
npm install -g netlify-cli
netlify dev
```
This will start both the frontend and the functions and handle the redirects correctly.

---

## 4. Troubleshooting
- **Function Timeout:** Netlify free tier functions have a 10-second timeout. If the AI takes longer to respond, the request may fail.
- **Module Errors:** Ensure all backend dependencies are listed in `backend/requirements.txt`.
