# 🚀 Render Deployment Guide

## Prerequisites

- ✅ GitHub account
- ✅ Render account (https://render.com)
- ✅ Your code pushed to GitHub

## Step-by-Step Deployment

### 1. Push Your Code to GitHub

```bash
cd /Users/gowreeshvt/Documents/GitHub/Hack-A-Cure
git add .
git commit -m "Add improved RAG with scores and query expansion"
git push origin main
```

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository: `Gowreesh-VT/Hack-A-Cure`
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

#### Option B: Manual Deployment

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `hackacure-api`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Set Environment Variables

In Render Dashboard → Your Service → Environment, add these **secret** variables:

#### Required Secrets (click "Add Environment Variable"):

```bash
GOOGLE_API_KEY=AIzaSyCuIuOfNCrcYuccS00tVfiFgrUABKP5obs
QDRANT_URL=https://3b2c4f4c-4034-40e7-b04a-cfcf7ce68a8f.europe-west3-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.1YbxjeThyBUT9b4YkfZ82RCmROfeh3rq1JTRq3PqYB0
FIRST_SUPERUSER_PASSWORD=your-secure-password
JWT_USER_PASSWORD=your-secure-password
```

All other environment variables are already configured in `render.yaml`.

### 4. Deploy!

Click **"Create Web Service"** or **"Apply Blueprint"**

Render will:
1. ✅ Clone your repository
2. ✅ Install dependencies
3. ✅ Start your API
4. ✅ Provide a public URL

### 5. Your Deployed API

After deployment, your API will be available at:
```
https://hackacure-api.onrender.com
```

**Test it:**
```bash
curl -X POST https://hackacure-api.onrender.com/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is diabetes?",
    "top_k": 3,
    "use_query_expansion": true
  }'
```

### 6. API Documentation

Access Swagger docs at:
```
https://hackacure-api.onrender.com/docs
```

## Important Notes

### Free Tier Limitations

⚠️ Render's free tier:
- **Spins down after 15 minutes of inactivity**
- **Cold start takes ~30 seconds** on first request
- **750 hours/month** of runtime

### Keeping Your Service Active

To keep it warm, you can:

1. **Use a cron job** (e.g., cron-job.org):
   ```
   */10 * * * * curl https://hackacure-api.onrender.com/docs
   ```

2. **Upgrade to paid tier** ($7/month) for always-on service

## Features Deployed

✅ **Similarity Scores** - Every query returns relevance scores  
✅ **Query Expansion** - Medical term expansion for better retrieval  
✅ **Score Filtering** - Filter by minimum similarity threshold  
✅ **Optimized Chunking** - Better text splitting for medical content  
✅ **Gemini 2.0 Flash Exp** - Latest AI model  
✅ **Vertex AI Embeddings** - High-quality embeddings  

## Monitoring

1. **Logs:** Render Dashboard → Your Service → Logs
2. **Metrics:** Render Dashboard → Your Service → Metrics
3. **Health Check:** `GET /docs` (automatically monitored by Render)

## Updating Your Deployment

To update:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically redeploy! 🎉

## Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility

### Service Won't Start
- Check environment variables are set correctly
- View logs in Render Dashboard

### API Returns 502/503
- Service is spinning up (wait 30 seconds)
- Check logs for errors

### Low Scores
- Use `"use_query_expansion": true` in requests
- Adjust `score_threshold` parameter
- Consider re-ingesting data with optimized chunking

## Cost Optimization

**Free tier is sufficient for:**
- Development
- Testing
- Low traffic applications
- Demos

**Upgrade when you need:**
- 24/7 availability
- Higher traffic
- Better performance
- Custom domains

## Next Steps

1. ✅ Deploy to Render
2. ✅ Test your API endpoints
3. ✅ Share your public URL
4. ✅ Monitor usage and performance
5. Consider adding:
   - Rate limiting
   - API authentication
   - Custom domain
   - Database backup

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Your API Docs: https://hackacure-api.onrender.com/docs

---

**Your API is production-ready!** 🚀
