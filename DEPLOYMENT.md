# Deploying LogisTech to Render - Complete Guide

## 📋 Prerequisites
- GitHub account
- Render account (free tier available at https://render.com)
- Your project pushed to GitHub

---

## 🚀 Deployment Steps

### Step 1: Push Your Code to GitHub

1. Go to https://github.com and create a new repository
2. Name it: `logistech-warehouse` (or any name you prefer)
3. Keep it **Public** (required for free tier) or **Private** (if you have paid plan)
4. **DO NOT** initialize with README (you already have one)
5. Click "Create repository"

6. In VS Code terminal, run these commands:

```bash
# Check git status
git status

# Add all files
git add .

# Commit changes
git commit -m "Initial commit - LogisTech Warehouse System"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/logistech-warehouse.git

# Push to GitHub
git push -u origin main
```

If it asks for credentials, use your GitHub username and a **Personal Access Token** (not password).

---

### Step 2: Create Render Account

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (recommended) or email
4. Verify your email if needed

---

### Step 3: Deploy on Render

1. **Log in to Render Dashboard**
   - Go to https://dashboard.render.com

2. **Create New Web Service**
   - Click **"New +"** button (top right)
   - Select **"Web Service"**

3. **Connect GitHub Repository**
   - Click **"Connect account"** under GitHub
   - Authorize Render to access your repositories
   - Find and select your `logistech-warehouse` repository
   - Click **"Connect"**

4. **Configure Web Service**

   Fill in these details:

   | Field | Value |
   |-------|-------|
   | **Name** | `logistech-warehouse` (or your choice) |
   | **Region** | Choose closest to you (e.g., Oregon, Frankfurt) |
   | **Branch** | `main` |
   | **Root Directory** | Leave blank |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn api:app --host 0.0.0.0 --port $PORT` |

5. **Select Plan**
   - Choose **"Free"** plan
   - Note: Free tier has limitations (sleeps after 15 min inactivity)

6. **Environment Variables (IMPORTANT!)**
   
   Click **"Advanced"** → **"Add Environment Variable"**
   
   **You DON'T need to add any environment variables** for SQLite!
   
   The `.env` file is ignored (in `.gitignore`), and SQLite doesn't need credentials.
   
   ✅ **No environment variables needed for this project!**

7. **Create Web Service**
   - Click **"Create Web Service"**
   - Render will start building and deploying

---

### Step 4: Monitor Deployment

1. **Watch Build Logs**
   - You'll see real-time logs of the deployment
   - Look for:
     ```
     Installing dependencies from requirements.txt
     Successfully installed fastapi uvicorn...
     ```

2. **Wait for Deployment**
   - First deployment takes 2-5 minutes
   - Status will change from "Building" → "Live"

3. **Get Your URL**
   - Once live, you'll see a URL like:
     ```
     https://logistech-warehouse.onrender.com
     ```

---

## 🎉 Your App is Live!

Visit your Render URL to see your deployed application!

---

## ⚠️ Important Notes About SQLite on Render

### Data Persistence Warning

**SQLite databases are NOT persistent on Render's free tier!**

- Every time your service restarts, the database resets
- Data is lost when the service sleeps (after 15 min inactivity)
- This is because Render uses ephemeral storage

### Solutions:

**Option 1: Accept Data Loss (Good for Demo)**
- Fine for testing and demonstrations
- Database recreates automatically on restart

**Option 2: Upgrade to Persistent Disk (Paid)**
- Add persistent disk in Render dashboard
- Costs extra money
- Keeps data between restarts

**Option 3: Use PostgreSQL (Recommended for Production)**
- Render offers free PostgreSQL database
- Data persists permanently
- Requires code changes (switch from SQLite to PostgreSQL)

---

## 🔧 Environment Variables Reference

For this project with SQLite, you **DON'T need any environment variables**.

If you later switch to PostgreSQL or MySQL, you would add:

| Key | Value | Description |
|-----|-------|-------------|
| `DB_HOST` | `your-db-host` | Database host |
| `DB_USER` | `your-username` | Database username |
| `DB_PASSWORD` | `your-password` | Database password |
| `DB_NAME` | `warehouse` | Database name |

---

## 🐛 Troubleshooting

### Build Failed
- Check build logs for errors
- Verify `requirements.txt` is correct
- Ensure all dependencies are listed

### Application Error
- Check application logs in Render dashboard
- Verify start command is correct
- Check for Python errors in logs

### Database Errors
- SQLite will auto-create on first run
- Check file permissions in logs
- Verify database.py is using SQLite correctly

### 404 Not Found
- Ensure static files are in `static/` folder
- Check `api.py` has correct static file mounting
- Verify paths are relative, not absolute

---

## 🔄 Updating Your Deployment

When you make changes to your code:

1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```

2. **Automatic Deployment:**
   - Render automatically detects the push
   - Rebuilds and redeploys your app
   - Takes 1-3 minutes

3. **Manual Deployment:**
   - Go to Render dashboard
   - Click "Manual Deploy" → "Deploy latest commit"

---

## 📊 Monitoring Your App

In Render Dashboard you can:
- View **Logs** (real-time application output)
- Check **Metrics** (CPU, memory usage)
- See **Events** (deployment history)
- Monitor **Health** (uptime status)

---

## 💰 Free Tier Limitations

Render Free Tier includes:
- ✅ 750 hours/month of runtime
- ✅ Automatic HTTPS
- ✅ Custom domains
- ❌ Sleeps after 15 min inactivity (cold starts take 30s)
- ❌ No persistent disk (data loss on restart)
- ❌ Limited bandwidth

---

## 🎯 Next Steps

1. **Test Your Deployment**
   - Visit your Render URL
   - Test all features
   - Check logs for errors

2. **Share Your Project**
   - Share the Render URL with others
   - Add it to your GitHub README
   - Include in your portfolio

3. **Monitor Performance**
   - Check logs regularly
   - Monitor for errors
   - Track usage patterns

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **GitHub Issues:** Create an issue in your repository

---

Good luck with your deployment! 🚀
