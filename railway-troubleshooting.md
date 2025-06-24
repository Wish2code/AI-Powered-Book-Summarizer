# 🚂 Railway Deployment Troubleshooting

## Your Build Was Successful! ✅
The log shows "Successfully Built!" which means your Docker image was created correctly.

## Common Runtime Issues & Solutions

### 1. **Port Configuration Issue**
**Problem:** App not listening on the correct port
**Solution:** Make sure your FastAPI app uses the PORT environment variable

Check your `api/main.py` - it should look like this:
```python
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=False)
```

### 2. **Memory Issues (Most Common)**
**Problem:** AI models require more memory than Railway's free tier provides
**Solution:** 
- Upgrade to Railway's paid plan ($5/month)
- Or use a smaller model in `api/summarizer.py`

### 3. **Model Download Timeout**
**Problem:** Hugging Face models take too long to download
**Solution:** Add model caching or use smaller models

### 4. **Missing Dependencies**
**Problem:** Some packages not installed correctly
**Solution:** Check your `requirements.txt` is complete

## Quick Fixes to Try

### Fix 1: Update your Procfile
Make sure your `Procfile` contains:
```
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### Fix 2: Add startup script
Create `start.sh`:
```bash
#!/bin/bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### Fix 3: Use smaller model
In `api/summarizer.py`, change default model to:
```python
def __init__(self, model_name: str = "t5-small"):  # Smaller, faster model
```

## How to Check Railway Logs

1. Go to your Railway dashboard
2. Click on your project
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Check "Logs" for runtime errors

## Common Error Messages & Solutions

| Error | Solution |
|-------|----------|
| `Port already in use` | Check Procfile uses `$PORT` |
| `Out of memory` | Upgrade Railway plan or use smaller model |
| `Model download failed` | Use smaller model or add retry logic |
| `Module not found` | Check requirements.txt |
| `NLTK data missing` | Add NLTK download to startup |

## Quick Test

Try this minimal test first:
1. Temporarily comment out model loading in `api/main.py`
2. Deploy to Railway
3. If it works, the issue is with the AI model loading
4. Then gradually add back the AI functionality

## Alternative: Use Hugging Face Spaces

If Railway continues to have issues, consider deploying to Hugging Face Spaces:
- Free GPU support
- Optimized for AI models
- Automatic deployment from GitHub
- Better for transformer models

## Need Help?

1. Check Railway logs for specific error messages
2. Try the quick fixes above
3. Consider upgrading Railway plan for more resources
4. Or switch to Hugging Face Spaces for AI-specific hosting 