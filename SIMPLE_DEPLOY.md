# 🚀 Easy Render Deployment - Step by Step

## 📋 What You Need:
1. GitHub account ✅ (You already have your code at: https://github.com/mostfamoh/Classic_Cryptolab)
2. Render account (Free - sign up below)

---

## STEP 1️⃣: Deploy Backend (5 minutes)

### A. Create Render Account
1. Go to: **https://render.com**
2. Click **"Get Started"**
3. **Sign up with GitHub** (easiest option)
4. Authorize Render to access your repositories

### B. Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Build and deploy from a Git repository"** → **"Next"**
3. Find and click **"Connect"** next to: `mostfamoh/Classic_Cryptolab`
4. If you don't see it, click **"Configure account"** → Select repositories

### C. Configure Your Backend
Fill in these settings:

**Basic Settings:**
```
Name: cryptolab-backend
Region: Oregon (USA) or closest to you
Branch: main
Root Directory: backend
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command: 
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py create_test_users

Start Command:
gunicorn cryptolab.wsgi:application

Instance Type: Free
```

### D. Add Environment Variables
Scroll down to **"Environment Variables"** and click **"Add Environment Variable"** for each:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `django-prod-secret-8k2n4m6p9q3r5t7v9w2x4y6z8a1b3c5d7e9f` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `PYTHON_VERSION` | `3.11.9` |

**Don't add CORS yet - we'll do that after frontend**

### E. Add PostgreSQL Database
1. Scroll down to **"Add Database"**
2. Click **"Add Database"** button
3. Select **"PostgreSQL"**
4. A new database will be created and `DATABASE_URL` will be added automatically
5. Click **"Create Web Service"**

⏳ **Wait 5-10 minutes** - Render will:
- Install dependencies
- Create database
- Run migrations
- **Automatically create test users!**
- Start the server

Your backend URL will be something like:
```
https://cryptolab-backend.onrender.com
```

**📝 Copy this URL - you'll need it for the frontend!**

---

## STEP 2️⃣: Deploy Frontend (2 minutes)

### A. Create Static Site
1. In Render dashboard, click **"New +"** → **"Static Site"**
2. Select your repository: `mostfamoh/Classic_Cryptolab`
3. Click **"Connect"**

### B. Configure Frontend
Fill in these settings:

```
Name: cryptolab-frontend
Branch: main
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

### C. Add Environment Variable
Click **"Advanced"** → **"Add Environment Variable"**

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://cryptolab-backend.onrender.com/api` |

**⚠️ IMPORTANT:** Replace with YOUR actual backend URL from Step 1!

Click **"Create Static Site"**

⏳ **Wait 2-3 minutes**

Your frontend URL will be something like:
```
https://cryptolab-frontend.onrender.com
```

---

## STEP 3️⃣: Update Backend CORS (1 minute)

1. Go back to your **Backend service** in Render
2. Click **"Environment"** in the left menu
3. Click **"Add Environment Variable"**
4. Add:

| Key | Value |
|-----|-------|
| `CORS_ALLOWED_ORIGINS` | `https://cryptolab-frontend.onrender.com` |

**⚠️ IMPORTANT:** Use YOUR actual frontend URL from Step 2!

5. Your backend will automatically redeploy (takes 2-3 minutes)

---

## 🎉 DONE! Test Your Live App

### Your Live URLs:
- **Frontend**: `https://cryptolab-frontend.onrender.com` (your actual URL)
- **Backend API**: `https://cryptolab-backend.onrender.com/api/`
- **Admin Panel**: `https://cryptolab-backend.onrender.com/admin/`

### Test Accounts (Already Created!):
- **Student**: username: `student` | password: `student123`
- **Instructor**: username: `instructor` | password: `instructor123`
- **Admin**: username: `admin` | password: `admin123`

### Test the App:
1. ✅ Open your frontend URL
2. ✅ Login with student account
3. ✅ Try Caesar cipher
4. ✅ Send an encrypted message to instructor
5. ✅ Perform a MITM attack
6. ✅ View decryption steps

---

## 🐛 Troubleshooting

### Backend "Application failed to respond"
1. Go to Backend service → **"Logs"** tab
2. Look for errors in red
3. Most common: Database not connected (wait 1-2 more minutes)

### Frontend can't connect to backend
1. Check Backend **"Logs"** for CORS errors
2. Verify `VITE_API_URL` has `/api` at the end
3. Verify `CORS_ALLOWED_ORIGINS` matches your frontend URL exactly
4. Make sure backend is running (green dot)

### Free Tier Sleep Mode
- Free tier apps sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- You have 750 hours/month free (enough for learning!)

### Can't see test users?
Backend logs should show:
```
✅ Created student user (username: student, password: student123)
✅ Created instructor user (username: instructor, password: instructor123)
✅ Created admin superuser (username: admin, password: admin123)
```

If not, go to Backend → **Shell** tab and run:
```bash
python manage.py create_test_users
```

---

## 📱 Share Your App!

Your app is now live on the internet! Share it:
- Add to your portfolio
- Share with friends: `https://cryptolab-frontend.onrender.com`
- Use for teaching cryptography
- Add to your resume/CV

---

## 🎓 What's Next? (Optional)

### Monitor Your App
- Render Dashboard shows: uptime, requests, bandwidth
- Free tier: 100 GB bandwidth/month

### Add Custom Domain
- Render Settings → Custom Domains
- Point your domain DNS to Render
- Free SSL certificate included!

### Access Admin Panel
- Visit: `https://cryptolab-backend.onrender.com/admin/`
- Login with: `admin` / `admin123`
- Manage users, view data, etc.

---

**🎊 Congratulations! Your Classic CryptoLab is LIVE!** 🔐

Questions? Check the Render logs or let me know!
