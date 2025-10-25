# 🚀 Quick Start Guide - Classic CryptoLab

## Step-by-Step Setup (Windows PowerShell)

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```powershell
cd classic-cryptolab
.\setup.ps1
```

This will:
- Check Python and Node.js installations
- Create virtual environment
- Install all dependencies
- Create .env files
- Run database migrations

### Option 2: Manual Setup

#### Backend Setup

```powershell
# Navigate to backend directory
cd classic-cryptolab\backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create environment file
Copy-Item .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

#### Frontend Setup

In a **new terminal**:

```powershell
# Navigate to frontend directory
cd classic-cryptolab\frontend

# Install dependencies
npm install

# Create environment file
Copy-Item .env.example .env

# Run development server
npm run dev
```

## 🎯 First Time Usage

### 1. Access the Application

Open your browser and go to: `http://localhost:5173`

### 2. Create Your Account

**For Students:**
- Click "Sign up"
- Choose username, email, password
- Select role: **Student**
- Click "Sign Up"

**For Instructors:**
- Click "Sign up"
- Choose username, email, password
- Select role: **Instructor**
- Click "Sign Up"

### 3. Explore Features

#### As a Student:

**Try Caesar Cipher:**
1. Go to **Ciphers** page
2. Select "Caesar" cipher
3. Enter text: `HELLO WORLD`
4. Set shift: `3`
5. Click "Encrypt"
6. Result: `KHOOR ZRUOG`

**Run a Brute Force Attack:**
1. Go to **Attacks** page
2. Select "Caesar Brute Force"
3. Enter ciphertext: `KHOOR ZRUOG`
4. Click "Run Attack"
5. See all 26 possible decryptions ranked by likelihood

**Complete an Exercise:**
1. Go to **Exercises** page
2. Click on an exercise
3. Try to decrypt the ciphertext
4. Submit your answer
5. Get automatic feedback

#### As an Instructor:

**Create an Exercise:**
1. Go to **Instructor** dashboard
2. Click "Create Exercise"
3. Fill in:
   - Title: "Caesar Cipher Practice"
   - Description: "Decrypt this message encrypted with Caesar cipher"
   - Cipher type: Caesar
   - Ciphertext: `KHOOR ZRUOG`
   - Correct answer: `HELLO WORLD`
   - Points: 10
4. Click "Create"

**Monitor Students:**
1. Go to **Instructor** dashboard
2. View recent submissions
3. See student statistics
4. Review activity logs

## 📚 Example Workflows

### Workflow 1: Learning Caesar Cipher

1. **Read about Caesar Cipher** (Ciphers page → Info panel)
2. **Encrypt a message**: "MEET AT DAWN" with shift 5
3. **Decrypt it back**: Use same shift to verify
4. **Try an attack**: Use brute force to break it
5. **Complete exercise**: Apply your knowledge

### Workflow 2: Exploring Affine Cipher

1. **Go to Ciphers page**
2. **Select Affine cipher**
3. **Set keys**: a=5 (must be coprime with 26), b=8
4. **Encrypt**: "SECRET MESSAGE"
5. **Note the weakness**: Read info panel
6. **Try frequency analysis**: Copy result to Attacks page

### Workflow 3: Hill Cipher Known-Plaintext Attack

1. **Encrypt with Hill cipher**:
   - Text: "HELP"
   - Matrix: [[6, 24], [1, 13]]
   - Note the ciphertext
2. **Go to Attacks page**
3. **Select "Hill Known-Plaintext"**
4. **Enter plaintext**: "HELP"
5. **Enter ciphertext**: (your result)
6. **See recovered key matrix**

## 🔧 Troubleshooting

### Backend won't start

**Error: `ModuleNotFoundError: No module named 'django'`**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Error: `django.db.utils.OperationalError`**
```powershell
# Database issue - run migrations
python manage.py migrate
```

### Frontend won't start

**Error: `Cannot find module`**
```powershell
# Reinstall dependencies
Remove-Item node_modules -Recurse -Force
npm install
```

**Error: `EADDRINUSE: address already in use`**
```powershell
# Port 5173 is in use - kill the process or use different port
npm run dev -- --port 3000
```

### Login Issues

**Error: "No active account found with the given credentials"**
- Double-check username and password
- Remember: usernames are case-sensitive
- Make sure you registered successfully

**Error: "Token is invalid or expired"**
- Clear browser localStorage
- Login again
- Check backend is running

### CORS Errors

**Error: "blocked by CORS policy"**
1. Check `backend/.env`:
   ```
   CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
   ```
2. Restart backend server

## 🔐 Security Notes

### For Development:
- Default SECRET_KEY is insecure - change in production
- DEBUG=True shows detailed errors - disable in production
- SQLite is fine for testing - use PostgreSQL in production

### For Production:
- Set strong SECRET_KEY
- Set DEBUG=False
- Use PostgreSQL database
- Enable HTTPS
- Set proper ALLOWED_HOSTS
- Use environment variables for secrets

## 📦 Database Management

### Reset Database (Development)

```powershell
# Stop servers
# Delete database
Remove-Item db.sqlite3

# Recreate
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

### Backup Database

```powershell
# Export data
python manage.py dumpdata > backup.json

# Import data
python manage.py loaddata backup.json
```

## 🎓 Educational Tips

### For Students:
1. Start with Caesar cipher (easiest)
2. Try different keys and see patterns
3. Use attacks to understand weaknesses
4. Complete exercises to test knowledge
5. Track your progress on dashboard

### For Instructors:
1. Create exercises with increasing difficulty
2. Start with Caesar, move to Affine, then Hill/Playfair
3. Monitor student progress regularly
4. Provide hints for difficult exercises
5. Use activity logs to identify struggling students

## 🌟 Best Practices

### Key Management:
- **Caesar**: Use shift 3-13 for moderate security
- **Affine**: Ensure 'a' is coprime with 26 (1,3,5,7,9,11,15,17,19,21,23,25)
- **Hill**: Use invertible matrices only
- **Playfair**: Use memorable keywords without repeated letters

### Text Preparation:
- Remove special characters for better results
- Use uppercase for consistency
- Keep messages relatively short for learning
- Include common words for frequency analysis

## 📞 Getting Help

### Resources:
- **README.md**: Full documentation
- **API Documentation**: In README under "API Documentation"
- **Cipher Theory**: Info panels in Ciphers page
- **Attack Methods**: Attack guide in Attacks page

### Common Questions:

**Q: How do I know if my cipher is secure?**
A: None of these classical ciphers are secure by modern standards. They're for education only.

**Q: Why can't I break my Playfair cipher?**
A: Playfair is more resistant to frequency analysis. Try known-plaintext attack instead.

**Q: What if I forget my password?**
A: Currently no password reset. Contact admin or create new account.

**Q: Can I use this for real encryption?**
A: NO! These are classical ciphers for education only. Use modern encryption (AES, RSA) for real security.

---

**Ready to start? Run the setup script and begin your cryptography journey! 🚀**
