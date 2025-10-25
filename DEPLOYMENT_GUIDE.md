# 🚀 Classic CryptoLab - FREE Deployment Guide

This guide will help you deploy your application for FREE using Railway (Backend) and Vercel (Frontend).

---

## 📦 Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- Vercel account (sign up at https://vercel.com)

---

## 🔧 PART 1: Deploy Backend to Railway (FREE)

### Step 1: Prepare Your Code

1. Create a GitHub repository for your project
2. Push your code to GitHub:
```bash
cd C:\Users\j\OneDrive\Desktop\ssad\classic-cryptolab
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/classic-cryptolab.git
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `classic-cryptolab` repository
5. Railway will detect it's a Python app

### Step 3: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database" → "PostgreSQL"**
3. Railway will automatically create a database and set `DATABASE_URL` environment variable

### Step 4: Configure Environment Variables

In Railway, go to your backend service → **Variables** tab and add:

```
SECRET_KEY=your-random-secret-key-generate-one-here
DEBUG=False
ALLOWED_HOSTS=.railway.app,.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
```

**Generate SECRET_KEY**: Run this in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Step 5: Set Root Directory

1. In Railway, go to **Settings** → **Service**
2. Set **Root Directory** to `backend`
3. Click **"Save Config"**

### Step 6: Deploy!

Railway will automatically:
- Install dependencies from `requirements.txt`
- Run migrations
- Start the server with gunicorn

**Your backend URL**: `https://your-app-name.railway.app`

---

## 🎨 PART 2: Deploy Frontend to Vercel (FREE)

### Step 1: Create Environment File

Create `.env.production` in the `frontend` folder:

```
VITE_API_URL=https://your-backend-url.railway.app/api
```

Replace `your-backend-url` with your Railway URL from Part 1.

### Step 2: Update CORS in Backend

Go back to Railway → Your backend service → **Variables** and update:

```
CORS_ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://your-custom-domain.com
```

(You'll get the Vercel URL in the next steps)

### Step 3: Deploy to Vercel

1. Go to https://vercel.com
2. Click **"Add New..." → "Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add **Environment Variables**:
   ```
   VITE_API_URL=https://your-backend-url.railway.app/api
   ```
6. Click **"Deploy"**

**Your frontend URL**: `https://your-app-name.vercel.app`

### Step 4: Update Backend CORS Again

Now that you have your Vercel URL:
1. Go to Railway → Backend service → **Variables**
2. Update `CORS_ALLOWED_ORIGINS` with your actual Vercel URL
3. Redeploy backend (it will automatically redeploy)

---

## 🎯 ALTERNATIVE: Deploy BOTH to Render (All-in-One)

### Backend on Render

1. Go to https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `cryptolab-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn cryptolab.wsgi:application`
   - **Plan**: Free
5. Add environment variables (same as Railway)
6. Click **"Create Web Service"**

### Frontend on Render

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `cryptolab-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add environment variable:
   ```
   VITE_API_URL=https://cryptolab-backend.onrender.com/api
   ```
5. Click **"Create Static Site"**

---

## ✅ Verification Checklist

After deployment:

- [ ] Backend health check: `https://your-backend-url.railway.app/api/`
- [ ] Frontend loads: `https://your-frontend-url.vercel.app/`
- [ ] Can register a new account
- [ ] Can login
- [ ] Can use cipher tools
- [ ] Can send encrypted messages
- [ ] Can perform MITM attacks

---

## 🔒 Security Notes

1. **Never commit `.env` files** - They're in `.gitignore`
2. **Change SECRET_KEY** - Use a strong random key
3. **Use HTTPS** - Both platforms provide free SSL
4. **Set DEBUG=False** - Always in production
5. **Update ALLOWED_HOSTS** - Only allow your domains

---

## 📊 FREE Tier Limits

**Railway Free Tier:**
- $5 credit/month (enough for hobby projects)
- Automatically sleeps after inactivity
- 500 MB database storage
- 1 GB memory

**Vercel Free Tier:**
- 100 GB bandwidth/month
- Unlimited static sites
- Automatic SSL
- Global CDN

**Render Free Tier:**
- 750 hours/month
- Spins down after 15 min inactivity
- 100 GB bandwidth/month
- 512 MB memory

---

## 🐛 Troubleshooting

### Backend won't start
- Check Railway logs: Project → Service → Deployments → Logs
- Verify `requirements.txt` has all dependencies
- Check `DATABASE_URL` is set
- Verify `SECRET_KEY` is set

### Frontend can't connect to backend
- Check CORS settings in backend
- Verify `VITE_API_URL` in frontend environment variables
- Check backend URL is correct (include `/api`)
- Open browser console (F12) for errors

### Database errors
- Railway PostgreSQL takes 1-2 minutes to provision
- Run migrations manually in Railway shell if needed:
  ```bash
  python manage.py migrate
  ```

### Static files not loading
- Run `python manage.py collectstatic` in build command
- Check `STATIC_ROOT` and `STATICFILES_STORAGE` in settings
- Verify whitenoise is installed

---

## 🎓 Custom Domain (Optional)

### Add Custom Domain to Vercel (Free)
1. Vercel Dashboard → Your Project → Settings → Domains
2. Add your domain (e.g., `cryptolab.yourdomain.com`)
3. Update DNS records as instructed
4. Vercel automatically provisions SSL

### Add Custom Domain to Railway ($)
1. Railway → Your Service → Settings → Domains
2. Add custom domain (requires Railway Pro)
3. Update DNS records

---

## 📞 Need Help?

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/

---

**🎉 Your Classic CryptoLab is now live on the internet!**

Backend: `https://your-backend.railway.app`  
Frontend: `https://your-frontend.vercel.app`
