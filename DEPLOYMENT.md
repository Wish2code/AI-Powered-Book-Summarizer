# 🚀 Deployment Guide - Book Summarizer AI

This guide will walk you through deploying your Book Summarizer AI project using the recommended strategy: FastAPI backend + Streamlit frontend.

## 📋 Prerequisites

1. **GitHub Account** - For code hosting
2. **Railway Account** - For backend hosting (free tier available)
3. **Streamlit Cloud Account** - For frontend hosting (free)

## 🎯 Deployment Strategy

- **Backend**: FastAPI on Railway (handles AI processing)
- **Frontend**: Streamlit on Streamlit Cloud (user interface)
- **Communication**: HTTP API calls between services

---

## 🔧 Step 1: Deploy FastAPI Backend (Railway)

### 1.1 Prepare Your Repository
Make sure your code is pushed to GitHub with these files:
- `api/` folder (FastAPI backend)
- `requirements.txt`
- `Procfile`
- `runtime.txt`

### 1.2 Deploy to Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Railway will automatically detect it's a Python app**

### 1.3 Configure Environment Variables
In Railway dashboard:
- Go to your project → Variables tab
- Add: `PORT=8000`

### 1.4 Get Your Backend URL
- Railway will provide a URL like: `https://your-app-name.railway.app`
- **Save this URL** - you'll need it for the frontend

---

## 🌐 Step 2: Deploy Streamlit Frontend (Streamlit Cloud)

### 2.1 Prepare Frontend Configuration
Your `app.py` is already configured to use environment variables.

### 2.2 Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in** with GitHub
3. **Click "New app"**
4. **Configure:**
   - **Repository**: Your GitHub repo
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL**: Leave default

### 2.3 Set Environment Variables
In Streamlit Cloud:
1. **Go to your app settings**
2. **Add environment variable:**
   - **Name**: `API_BASE_URL`
   - **Value**: Your Railway backend URL (e.g., `https://your-app-name.railway.app`)

### 2.4 Deploy
Click "Deploy" and wait for the build to complete.

---

## 🔍 Step 3: Test Your Deployment

### 3.1 Test Backend
Visit your Railway URL + `/docs` to see the API documentation:
```
https://your-app-name.railway.app/docs
```

### 3.2 Test Frontend
Visit your Streamlit app URL and test:
1. Upload a PDF
2. Check if API connection works
3. Generate a summary

---

## 🛠️ Troubleshooting

### Backend Issues
- **Model loading errors**: Check Railway logs for memory issues
- **Timeout errors**: Increase timeout settings in Railway
- **CORS errors**: Backend already configured for CORS

### Frontend Issues
- **API connection failed**: Check `API_BASE_URL` environment variable
- **File upload errors**: Check file size limits
- **Model selection errors**: Verify backend is running

### Common Solutions
1. **Restart deployments** if services are unresponsive
2. **Check logs** in both Railway and Streamlit Cloud
3. **Verify environment variables** are set correctly
4. **Test API endpoints** directly using the `/docs` interface

---

## 💰 Cost Considerations

### Free Tiers
- **Railway**: $5/month free tier (sufficient for testing)
- **Streamlit Cloud**: Free tier available
- **Total cost**: $0-5/month

### Scaling Options
- **Railway**: Upgrade for more resources
- **Alternative backends**: Render, Heroku, DigitalOcean
- **Alternative frontends**: Hugging Face Spaces, Vercel

---

## 🔄 Alternative Deployment Options

### Option A: Hugging Face Spaces
- Deploy both frontend and backend together
- Free GPU support
- Automatic deployment from GitHub

### Option B: Google Cloud Run
- Serverless deployment
- Pay-per-use pricing
- Good for production

### Option C: Heroku
- Traditional platform
- Free tier discontinued
- Good for learning

---

## 📞 Support

If you encounter issues:
1. Check the logs in both platforms
2. Verify all environment variables are set
3. Test API endpoints directly
4. Check GitHub issues for similar problems

---

**🎉 Congratulations!** Your Book Summarizer AI is now deployed and accessible worldwide! 