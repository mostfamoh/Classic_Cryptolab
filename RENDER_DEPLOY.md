# 🚀 Quick Deploy to Render - Step by Step

## ✅ Step 1: Push to GitHub

1. **Go to GitHub** (https://github.com) and login
2. **Create a new repository**:
   - Click the "+" icon → "New repository"
   - Name: `classic-cryptolab` (or any name you want)
   - Make it **Public**
   - **DO NOT** initialize with README (we already have one)
   - Click "Create repository"

3. **Copy the repository URL** you'll see something like:
   ```
   https://github.com/YOUR_USERNAME/classic-cryptolab.git
   ```

4. **Run these commands in PowerShell** (replace YOUR_USERNAME):
   ```powershell
   cd "C:\Users\j\OneDrive\Desktop\ssad\classic-cryptolab"
   git remote add origin https://github.com/YOUR_USERNAME/classic-cryptolab.git
   git branch -M main
   git push -u origin main
   ```

   If asked for credentials:
   - Username: your GitHub username
   - Password: use a Personal Access Token (not your password)
   
   **Create Token**: GitHub → Settings → Developer settings → Personal access tokens → Generate new token → Select "repo" scope

---

## 🎨 Step 2: Deploy Frontend to Render

1. **Go to Render** (https://render.com) and sign up/login with GitHub

2. **Create Static Site**:
   - Click "New +" → "Static Site"
   - Connect your GitHub repository: `classic-cryptolab`
   - Click "Connect"

3. **Configure Static Site**:
   ```
   Name: cryptolab-frontend
   Branch: main
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

4. **Add Environment Variable**:
   - Click "Advanced"
   - Add: `VITE_API_URL` = `https://cryptolab-backend.onrender.com/api`
   - (We'll update this after backend is deployed)

5. **Click "Create Static Site"**
   - Wait 2-3 minutes for deployment
   - You'll get a URL like: `https://cryptolab-frontend.onrender.com`

---

## 🔧 Step 3: Deploy Backend to Render

1. **Create Web Service**:
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Select your `classic-cryptolab` repository

2. **Configure Web Service**:
   ```
   Name: cryptolab-backend
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   Start Command: gunicorn cryptolab.wsgi:application
   Instance Type: Free
   ```

3. **Add Environment Variables**:
   Click "Environment" and add these:
   
   ```
   SECRET_KEY = django-insecure-CHANGE-THIS-TO-RANDOM-STRING
   DEBUG = False
   ALLOWED_HOSTS = .onrender.com
   CORS_ALLOWED_ORIGINS = https://cryptolab-frontend.onrender.com
   PYTHON_VERSION = 3.11.9
   ```

   **Generate SECRET_KEY**: Use this online generator:
   https://djecrety.ir/
   
   Or run in Python:
   ```python
   import secrets
   print(secrets.token_urlsafe(50))
   ```

4. **Add PostgreSQL Database**:
   - In the same screen, scroll down to "Databases"
   - Click "Create Database" → "PostgreSQL"
   - Name: `cryptolab_db`
   - Render will automatically set `DATABASE_URL` environment variable

5. **Click "Create Web Service"**
   - Wait 5-10 minutes for first deployment
   - Backend will be at: `https://cryptolab-backend.onrender.com`

---

## 🔄 Step 4: Update Frontend Environment

1. **Go back to Frontend service** in Render
2. **Update Environment Variable**:
   - `VITE_API_URL` = `https://cryptolab-backend.onrender.com/api`
3. **Trigger Redeploy**:
   - Click "Manual Deploy" → "Deploy latest commit"

---

## 🔒 Step 5: Update Backend CORS

1. **Go to Backend service** in Render
2. **Update Environment Variable**:
   - `CORS_ALLOWED_ORIGINS` = `https://cryptolab-frontend.onrender.com`
3. **Save changes** (will auto-redeploy)

---

## ✅ Step 6: Create Test Users

1. **Go to Backend service** in Render
2. **Click "Shell" tab** (or "Console")
3. **Run these commands**:
   ```bash
   python manage.py shell
   ```
   Then in the Python shell:
   ```python
   from users.models import User
   User.objects.create_user(username='student', email='student@test.com', password='student123', role='student')
   User.objects.create_user(username='instructor', email='instructor@test.com', password='instructor123', role='instructor')
   exit()
   ```

---

## 🎉 Step 7: Test Your Live App!

1. **Visit your frontend URL**: `https://cryptolab-frontend.onrender.com`
2. **Register a new account** or login with:
   - Username: `student` | Password: `student123`
3. **Test features**:
   - ✅ Try ciphers (Caesar, Affine, Hill, Playfair)
   - ✅ Send encrypted messages
   - ✅ Perform MITM attacks
   - ✅ View encryption steps

---

## 📝 Your URLs

After deployment:
- **Frontend**: `https://cryptolab-frontend.onrender.com`
- **Backend**: `https://cryptolab-backend.onrender.com`
- **Backend API**: `https://cryptolab-backend.onrender.com/api/`
- **Admin Panel**: `https://cryptolab-backend.onrender.com/admin/`

---

## 🐛 Troubleshooting

### Backend shows "Application failed to respond"
- Check Render logs: Backend service → Logs tab
- Verify all environment variables are set
- Make sure `DATABASE_URL` exists (added automatically with PostgreSQL)
- Check `requirements.txt` has all dependencies

### Frontend can't connect to backend
- Verify `VITE_API_URL` in frontend environment variables
- Check CORS settings in backend (`CORS_ALLOWED_ORIGINS`)
- Open browser console (F12) for specific errors

### Database errors
- Go to Backend service → Shell
- Run: `python manage.py migrate`
- Check PostgreSQL database is created and connected

### Free tier limitations
- Backend spins down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for hobby projects)

---

## 🎓 Next Steps (Optional)

### Add Custom Domain
1. Render Dashboard → Your Service → Settings → Custom Domains
2. Add your domain (e.g., `cryptolab.yourdomain.com`)
3. Update DNS records as instructed
4. Free SSL certificate automatically provisioned

### Enable Admin Panel
1. Create superuser in Render Shell:
   ```bash
   python manage.py createsuperuser
   ```
2. Visit: `https://cryptolab-backend.onrender.com/admin/`

### Monitor Usage
- Render Dashboard shows bandwidth, requests, and uptime
- Free tier: 100 GB bandwidth/month, 750 hours/month

---

**🎊 Congratulations! Your Classic CryptoLab is now LIVE on the internet!**

Share your app:
- Frontend: `https://cryptolab-frontend.onrender.com`
- Show friends, add to portfolio, use for teaching!

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/
- Check Render logs for specific errors
