# 🔐 Classic CryptoLab

A comprehensive educational web application for teaching and learning classical encryption algorithms. Built with Django REST Framework and React.

## 🎯 Features

### For Students
- **Authentication**: Secure registration and login with JWT
- **Cipher Operations**: Encrypt and decrypt using Caesar, Affine, Hill (2x2), and Playfair ciphers
- **Cryptanalysis**: Run attacks including brute force, frequency analysis, and known-plaintext
- **Exercises**: Complete instructor-assigned exercises with automatic grading
- **History Tracking**: View your encryption/decryption history
- **Dashboard**: Track progress and scores

### For Instructors
- **Exercise Management**: Create, edit, and delete exercises
- **Student Monitoring**: View all student activities and submissions
- **Dashboard**: Overview of student performance and engagement
- **Grading**: Automatic and manual grading options

### Cipher Implementations
1. **Caesar Cipher** - Simple shift cipher
2. **Affine Cipher** - Linear transformation cipher
3. **Hill Cipher** - Matrix-based polygraphic cipher (2x2)
4. **Playfair Cipher** - Digraph substitution cipher

### Attack Simulations
1. **Caesar Brute Force** - Try all 26 possible shifts
2. **Frequency Analysis** - Compare letter frequencies with English
3. **Hill Known-Plaintext** - Recover Hill cipher key from known pairs

## 🛠️ Technology Stack

### Backend
- **Django 5.0** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database (or SQLite for development)
- **JWT** - Authentication via SimpleJWT
- **NumPy** - Matrix operations for Hill cipher

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **TailwindCSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide React** - Icons

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (optional, SQLite works for development)

### Backend Setup

1. **Clone the repository**
```powershell
cd classic-cryptolab\backend
```

2. **Create virtual environment**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment**
```powershell
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```powershell
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```powershell
python manage.py createsuperuser
```

7. **Run development server**
```powershell
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**
```powershell
cd ..\frontend
```

2. **Install dependencies**
```powershell
npm install
```

3. **Configure environment**
```powershell
cp .env.example .env
# Edit .env if needed (default: http://localhost:8000/api)
```

4. **Run development server**
```powershell
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 🚀 Usage

### First Time Setup

1. **Start Backend**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

2. **Start Frontend** (in a new terminal)
```powershell
cd frontend
npm run dev
```

3. **Access the Application**
   - Open browser to `http://localhost:5173`
   - Register a new account (choose Student or Instructor role)
   - Start exploring!

### Quick Start Guide

#### As a Student:
1. **Register/Login** with role "Student"
2. **Try Ciphers**: Go to Ciphers page, select a cipher, enter text and key
3. **Run Attacks**: Go to Attacks page, enter ciphertext to analyze
4. **Complete Exercises**: View and submit answers to instructor exercises
5. **Track Progress**: Check your dashboard for statistics

#### As an Instructor:
1. **Register/Login** with role "Instructor"
2. **Create Exercises**: Use the Instructor Dashboard to create exercises
3. **Monitor Students**: View student activities and submissions
4. **Grade Submissions**: Review and manually grade if needed

## 📚 API Documentation

### Authentication Endpoints
```
POST /api/auth/register/          - Register new user
POST /api/auth/login/             - Login and get tokens
POST /api/auth/logout/            - Logout (blacklist token)
POST /api/auth/token/refresh/     - Refresh access token
GET  /api/auth/profile/           - Get user profile
PATCH /api/auth/profile/          - Update profile
POST /api/auth/change-password/   - Change password
GET  /api/auth/students/          - List students (instructors only)
```

### Cipher Endpoints
```
POST /api/ciphers/operate/        - Encrypt/decrypt
GET  /api/ciphers/info/           - Get cipher info
GET  /api/ciphers/info/all/       - Get all cipher info
GET  /api/ciphers/keys/           - List saved keys
POST /api/ciphers/keys/           - Create key
GET  /api/ciphers/history/        - View history
```

### Attack Endpoints
```
POST /api/attacks/caesar-brute-force/     - Caesar brute force
POST /api/attacks/frequency-analysis/     - Frequency analysis
POST /api/attacks/hill-known-plaintext/   - Hill known-plaintext
GET  /api/attacks/recommendations/        - Get attack recommendations
GET  /api/attacks/logs/                   - View attack logs
```

### Exercise Endpoints
```
GET  /api/exercises/                      - List exercises
POST /api/exercises/                      - Create exercise (instructors)
GET  /api/exercises/{id}/                 - Get exercise detail
PATCH /api/exercises/{id}/                - Update exercise
DELETE /api/exercises/{id}/               - Delete exercise
GET  /api/exercises/submissions/          - List submissions
POST /api/exercises/submissions/          - Submit exercise
GET  /api/exercises/student-stats/        - Student statistics
GET  /api/exercises/instructor-dashboard/ - Instructor dashboard
GET  /api/exercises/activity-logs/        - Activity logs
```

## 🔒 Security Features

- **JWT Authentication** with access and refresh tokens
- **Password Hashing** using Django's default (PBKDF2)
- **CORS Protection** with configurable origins
- **SQL Injection Protection** via Django ORM
- **XSS Protection** via React's built-in escaping
- **CSRF Protection** for cookie-based operations
- **Role-Based Access Control** for instructor features

## 🎨 Project Structure

```
classic-cryptolab/
├── backend/
│   ├── cryptolab/              # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                  # User authentication app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── ciphers/                # Cipher operations app
│   │   ├── models.py
│   │   ├── crypto_algorithms.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── attacks/                # Cryptanalysis app
│   │   ├── models.py
│   │   ├── attack_algorithms.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── exercises/              # Exercise management app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/         # Reusable components
    │   │   ├── Layout.jsx
    │   │   └── ProtectedRoute.jsx
    │   ├── contexts/           # React contexts
    │   │   └── AuthContext.jsx
    │   ├── pages/              # Page components
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   ├── Dashboard.jsx
    │   │   ├── Ciphers.jsx
    │   │   ├── Attacks.jsx
    │   │   ├── Exercises.jsx
    │   │   └── InstructorDashboard.jsx
    │   ├── services/           # API services
    │   │   └── api.js
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## 🌐 Deployment

### Backend (Render.com)

1. **Create `render.yaml`**:
```yaml
services:
  - type: web
    name: cryptolab-api
    env: python
    buildCommand: "pip install -r requirements.txt; python manage.py collectstatic --noinput; python manage.py migrate"
    startCommand: "gunicorn cryptolab.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: cryptolab-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False

databases:
  - name: cryptolab-db
    databaseName: cryptolab
    user: cryptolab
```

2. **Push to GitHub and connect to Render**

### Frontend (Netlify)

1. **Build command**: `npm run build`
2. **Publish directory**: `dist`
3. **Environment variables**: Set `VITE_API_URL` to your backend URL

## 📖 Learning Resources

### Cipher Theory
- **Caesar Cipher**: Named after Julius Caesar, shifts each letter by a fixed number
- **Affine Cipher**: Uses modular arithmetic with formula E(x) = (ax + b) mod 26
- **Hill Cipher**: Uses matrix multiplication for encryption
- **Playfair Cipher**: Uses a 5×5 grid of letters based on a keyword

### Attack Methods
- **Brute Force**: Try all possible keys
- **Frequency Analysis**: Exploit letter frequency patterns
- **Known-Plaintext**: Use known plaintext-ciphertext pairs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is for educational purposes.

## 👥 Authors

Built for cryptography education and learning.

## 🐛 Known Issues

- Hill cipher only supports 2x2 matrices (3x3 and larger not yet implemented)
- Frequency analysis works best with longer texts
- Playfair treats I and J as the same letter

## 🔮 Future Enhancements

- [ ] More cipher types (Vigenère, Columnar Transposition)
- [ ] Larger Hill cipher matrices (3x3, 4x4)
- [ ] Real-time collaboration features
- [ ] Mobile-responsive improvements
- [ ] Export/import exercises
- [ ] Detailed analytics for instructors
- [ ] Gamification with badges and leaderboards

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Happy Cryptography Learning! 🔐**
