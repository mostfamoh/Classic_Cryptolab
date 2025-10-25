# 🔧 Fix Render Build Error

Your build failed. Here's how to fix it:

## Option 1: Simplify Build Command (Recommended)

1. Go to Render Dashboard → Your Backend Service
2. Click **"Settings"** (not Environment)
3. Find **"Build Command"**
4. Replace with this simpler command:

```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input
```

5. Click **"Save Changes"**
6. Click **"Manual Deploy"** → **"Deploy latest commit"**

This will:
- ✅ Install packages
- ✅ Run migrations
- ✅ Collect static files
- ❌ Skip test users for now (we'll add them manually)

---

## Option 2: Check What Failed

1. Go to your backend service in Render
2. Click on the failed deployment
3. Scroll through the **"Logs"** 
4. Look for the **red error message**
5. **Tell me what error you see** and I'll fix it

Common errors:
- `psycopg2` not found → Need to add it to requirements
- Permission denied on build.sh → Wrong line endings
- Module not found → Missing dependency

---

## After Deploy Succeeds:

### Create Test Users Manually:

1. Go to Backend Service → **"Shell"** tab
2. Run this single command:
```bash
python manage.py create_test_users
```

OR create one user manually:
```python
python manage.py shell
```
Then:
```python
from users.models import User
User.objects.create_user(username='student', email='student@test.com', password='student123', role='student')
exit()
```

---

## Quick Fix Now:

**Copy this exact Build Command for Render:**

```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input
```

Then redeploy!

Let me know what error you see in the logs if this doesn't work.
