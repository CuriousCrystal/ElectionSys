# Quick Deploy Reference Card

## 🚀 Fast Track Deployment (5 minutes)

### Option 1: Use Deploy Script (Windows)
```powershell
.\deploy.ps1
```
Choose option 4 to test build, then option 1 to deploy.

### Option 2: Manual Steps

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Step 2: Deploy Backend to Render
1. Go to https://render.com
2. New → Web Service
3. Connect your repo
4. Settings:
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `uvicorn data_engine:app --host 0.0.0.0 --port $PORT`
5. Add env var: `XAI_API_KEY` = your key
6. Copy your backend URL

#### Step 3: Deploy Frontend to Netlify
1. Update `dashboard/.env.production`:
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```
2. Go to https://netlify.com
3. Drag & drop `dashboard/dist` folder
4. Done! 🎉

---

## 📋 URLs After Deployment

- **Frontend:** `https://your-site.netlify.app`
- **Backend API:** `https://your-api.onrender.com`
- **API Docs:** `https://your-api.onrender.com/docs`

---

## 🔑 Default Login

- Username: `admin`
- Password: `admin123`

---

## 🛠️ Useful Commands

### Local Development
```bash
# Backend
uvicorn data_engine:app --reload

# Frontend
cd dashboard && npm run dev
```

### Build & Deploy
```bash
# Test build
cd dashboard && npm run build

# Deploy to Netlify
netlify deploy --prod

# Check Git status
git status
```

---

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `netlify.toml` | Netlify build config |
| `render.yaml` | Render deployment config |
| `dashboard/.env.production` | Backend API URL |
| `.env` | Backend environment vars |

---

## 🔧 Troubleshooting

### CORS Error
Update `data_engine.py` with your Netlify URL:
```python
allow_origins=["https://your-site.netlify.app"]
```

### Build Fails
```bash
cd dashboard
rm -rf node_modules
npm install
npm run build
```

### API Not Responding
- Check Render logs
- Verify `VITE_API_URL` is correct
- Ensure backend is running

---

## 📊 Service Status

### Free Tier Limits

**Netlify:**
- ✅ 100GB bandwidth/month
- ✅ Unlimited sites
- ✅ Auto SSL

**Render:**
- ⚠️ 750 hours/month
- ⚠️ Sleeps after 15min
- ⚠️ May lose SQLite data

---

## 🎯 Next Steps

- [ ] Deploy backend to Render
- [ ] Update `VITE_API_URL`
- [ ] Deploy frontend to Netlify
- [ ] Test all features
- [ ] Set up custom domain
- [ ] Configure monitoring

---

## 📞 Support

- **Netlify Docs:** https://docs.netlify.com
- **Render Docs:** https://render.com/docs
- **Your Guide:** `DEPLOYMENT.md`

---

**Need help?** Open `DEPLOYMENT.md` for detailed instructions!
