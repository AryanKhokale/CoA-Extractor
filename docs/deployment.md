# Deployment Guide

This project is architected for zero-cost deployment across modern free-tier platforms:
- **Frontend**: Vercel (Edge CDN)
- **Backend**: Render (FastAPI Web Service)
- **Database**: PostgreSQL (Neon / Supabase / Render PostgreSQL) or SQLite for standalone deployment

---

## 1. Backend Deployment on Render

### Step 1: Push Repository to GitHub
Ensure the codebase is committed to a Git repository.

### Step 2: Create a Web Service on Render
1. Sign in to [Render](https://render.com).
2. Click **New +** &rarr; **Web Service**.
3. Select your GitHub repository.
4. Configure service parameters:
   - **Name**: `coa-directory-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

### Step 3: Set Environment Variables on Render
Under **Environment Variables**, add:
```env
PYTHON_VERSION=3.10.11
COA_BASE_URL=https://www.coa.gov.in
MAX_CONCURRENCY=5
REQUESTS_PER_SECOND=2.0
REQUEST_TIMEOUT=30
MAX_RETRIES=3
BATCH_SIZE=50
CORS_ORIGINS=https://<your-vercel-domain>.vercel.app,http://localhost:5173
```
*Note: If connecting a PostgreSQL database, add `DATABASE_URL=postgresql://user:pass@host:5432/dbname`.*

### Step 4: Deploy & Test
Once Render finishes deploying, test the health check:
```bash
curl https://<your-render-url>.onrender.com/api/health
```

---

## 2. Frontend Deployment on Vercel

### Step 1: Import Project in Vercel
1. Sign in to [Vercel](https://vercel.com).
2. Click **Add New...** &rarr; **Project**.
3. Import your repository.
4. Configure project settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 2: Configure Environment Variables on Vercel
Under **Environment Variables**, add:
```env
VITE_API_BASE_URL=https://<your-render-url>.onrender.com
```

### Step 3: Deploy
Click **Deploy**. Vercel will build the React application and distribute it across its global CDN.

---

## 3. Render Blueprint (`render.yaml`)
A `render.yaml` specification is included at the root of the repository for single-click infrastructure-as-code deployment.
