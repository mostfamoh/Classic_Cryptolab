# Classic CryptoLab - New Features Summary

## ✅ Completed Features

### 1. **3×3 Hill Cipher Support** ✓
- **Location**: `backend/ciphers/crypto_algorithms.py`
- **Changes**:
  - Updated `HillCipher` class to support both 2×2 and 3×3 matrices
  - Enhanced matrix inversion algorithm to handle 3×3 cofactor calculations
  - Modified encryption/decryption to work with variable block sizes (2 or 3 characters)
  
- **Usage Example**:
```python
# 3×3 Matrix key
key_matrix = [
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15]
]

# Encrypt
result = HillCipher.encrypt("HELLO", key_matrix, show_steps=True)
# Returns: {"ciphertext": "...", "steps": [...]}
```

---

### 2. **Step-by-Step Encryption/Decryption** ✓
- **Location**: `backend/ciphers/crypto_algorithms.py` (all cipher classes)
- **Changes**:
  - Added `show_steps` parameter to all cipher encrypt/decrypt methods
  - Methods now return dict with `ciphertext`/`plaintext` and optional `steps` array
  - Each cipher shows detailed transformation steps for educational purposes

- **Supported Ciphers**:
  1. **Caesar Cipher**: Shows character-by-character shifts
  2. **Affine Cipher**: Shows modular arithmetic calculations
  3. **Hill Cipher (2×2 & 3×3)**: Shows matrix multiplications per block
  4. **Playfair Cipher**: Shows digraph transformations and matrix lookups

- **API Usage**:
```javascript
POST /api/ciphers/operate/
{
  "cipher_type": "hill",
  "operation": "encrypt",
  "text": "HELLO",
  "key": {"matrix": [[3,3],[2,5]]},
  "show_steps": true  // NEW parameter
}

Response:
{
  "result": "URMUP",
  "steps": [
    "1. Key Matrix (2x2):\n[[3 3]\n [2 5]]",
    "2. Plaintext: HELLO",
    "3. Convert to numbers: [7, 4, 11, 11, 14]",
    "Block 1:",
    "  Plaintext block: [7, 4] = 'HE'",
    "  Matrix multiplication:\n[[3 3]\n [2 5]] × [[7]\n [4]]",
    "  = [[33]\n [34]]",
    "  Mod 26: [7, 8]",
    "  Ciphertext block: 'HI'",
    ...
  ]
}
```

---

### 3. **Secure Messaging System** ✓
- **Location**: `backend/messaging/` (new Django app)
- **Models**:
  1. **Conversation**: Represents secure channel between two users
     - Fields: `user_a`, `user_b`, `cipher_type`, `shared_key`, `is_intercepted`
     - Tracks which cipher and key are being used
  
  2. **Message**: Individual encrypted message in conversation
     - Fields: `conversation`, `sender`, `plaintext`, `ciphertext`, `encryption_steps`, `was_intercepted`
     - Stores both plaintext (for education) and ciphertext
  
  3. **InterceptedMessage**: Record of MITM attack
     - Fields: `original_message`, `attacker`, `attacker_key`, `decrypted_plaintext`, `modified_plaintext`, `attack_steps`, `success`

- **API Endpoints**:
```
POST   /api/messaging/conversations/              - Create conversation
GET    /api/messaging/conversations/              - List user's conversations
GET    /api/messaging/conversations/{id}/         - Get conversation details
GET    /api/messaging/conversations/{id}/messages/ - List messages
POST   /api/messaging/messages/send/              - Send encrypted message
POST   /api/messaging/mitm/attack/                - Perform MITM attack
GET    /api/messaging/mitm/interceptions/         - View all interceptions
```

- **Example: Alice sends message to Bob**:
```javascript
// 1. Create conversation
POST /api/messaging/conversations/
{
  "user_b_id": 2,  // Bob
  "cipher_type": "hill",
  "shared_key": {"matrix": [[3,3],[2,5]]}
}

// 2. Send encrypted message
POST /api/messaging/messages/send/
{
  "conversation_id": 1,
  "plaintext": "MEET AT NOON",
  "show_steps": true
}

Response:
{
  "id": 1,
  "sender": {...},
  "plaintext": "MEET AT NOON",
  "ciphertext": "URMUPQXYZ...",
  "encryption_steps": [...],
  "was_intercepted": false
}
```

---

### 4. **Man-in-the-Middle Attack Simulation** ✓
- **Location**: `backend/messaging/views.py` - `MITMAttackView`
- **Features**:
  - Eve can intercept any message in the system
  - Attempts to decrypt with attacker's guessed key
  - Compares decrypted text with original to check success
  - Optionally modifies message and re-encrypts with actual key
  - Records full attack process with steps

- **Attack Flow**:
```
1. Eve intercepts Alice→Bob message
2. Eve tries to decrypt with guessed key
3. System checks if decryption matches original
4. If Eve knows the key:
   - She can modify the message
   - System re-encrypts modified message with real key
   - Bob receives modified message (MITM successful!)
5. All attack attempts are logged for analysis
```

- **Example: Eve attacks message**:
```javascript
POST /api/messaging/mitm/attack/
{
  "message_id": 1,
  "attacker_key": {"matrix": [[3,3],[2,5]]},  // Eve's guessed key
  "modified_plaintext": "MEET AT MIDNIGHT",   // Modified message
  "show_steps": true
}

Response:
{
  "id": 1,
  "original_message": {...},
  "attacker": {"username": "eve"},
  "decrypted_plaintext": "MEET AT NOON",
  "modified_plaintext": "MEET AT MIDNIGHT",
  "modified_ciphertext": "URMUPQABCD...",
  "success": true,  // Eve guessed correct key!
  "attack_steps": [
    "=== MAN-IN-THE-MIDDLE ATTACK ===",
    "Intercepted message from alice",
    "Ciphertext: URMUPQXYZ...",
    "Attacker's key: {...}",
    "Actual shared key: {...}",
    "=== DECRYPTION ATTEMPT ===",
    ...,
    "=== RESULT ===",
    "Decrypted: MEET AT NOON",
    "Original: MEET AT NOON",
    "Success: true",
    "=== RE-ENCRYPTION (with actual key) ===",
    "Modified message: MEET AT MIDNIGHT",
    ...
  ]
}
```

---

## 🎯 How to Use

### Start the Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1  # Activate virtual environment
python manage.py runserver
```

### Run the Demo Script
```powershell
# In a new terminal (while server is running)
cd backend
python test_features.py
```

The demo script will:
1. Register test users (Alice, Bob, Eve)
2. Demonstrate 3×3 Hill cipher with steps
3. Show all ciphers with step-by-step encryption
4. Create secure conversation between Alice and Bob
5. Simulate MITM attack by Eve

---

## 📊 Database Schema

### New Tables
```sql
-- conversations table
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    user_a_id INTEGER REFERENCES users,
    user_b_id INTEGER REFERENCES users,
    cipher_type VARCHAR(20),
    shared_key JSON,
    is_intercepted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(user_a_id, user_b_id)
);

-- messages table
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations,
    sender_id INTEGER REFERENCES users,
    plaintext TEXT,
    ciphertext TEXT,
    encryption_steps JSON,
    timestamp TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    was_intercepted BOOLEAN DEFAULT FALSE
);

-- intercepted_messages table
CREATE TABLE intercepted_messages (
    id INTEGER PRIMARY KEY,
    original_message_id INTEGER REFERENCES messages,
    attacker_id INTEGER REFERENCES users,
    attacker_key JSON,
    decrypted_plaintext TEXT,
    modified_plaintext TEXT,
    modified_ciphertext TEXT,
    attack_steps JSON,
    timestamp TIMESTAMP,
    success BOOLEAN DEFAULT FALSE
);
```

---

## 🔧 Modified Files

### Backend
- ✅ `ciphers/crypto_algorithms.py` - Updated all cipher classes
- ✅ `ciphers/views.py` - Added show_steps support
- ✅ `ciphers/serializers.py` - Added show_steps field
- ✅ `messaging/models.py` - Created (new app)
- ✅ `messaging/views.py` - Created (new app)
- ✅ `messaging/serializers.py` - Created (new app)
- ✅ `messaging/urls.py` - Created (new app)
- ✅ `cryptolab/settings.py` - Added 'messaging' app
- ✅ `cryptolab/urls.py` - Added messaging routes
- ✅ `test_features.py` - Created demo script

### Database
- ✅ Applied migration: `messaging.0001_initial`

---

## 🎓 Educational Value

### For Students:
1. **Understand encryption step-by-step**: See exactly how each character is transformed
2. **Learn matrix cryptography**: Work with 3×3 Hill cipher matrices
3. **Practice secure communication**: Exchange encrypted messages with peers
4. **Recognize vulnerabilities**: See how MITM attacks work in practice

### For Instructors:
1. **Demonstrate attacks**: Show real MITM attack scenarios
2. **Compare cipher strengths**: Students can see which ciphers are vulnerable
3. **Monitor conversations**: Track which messages were intercepted
4. **Create exercises**: Use messaging system for hands-on assignments

---

## 🚀 Next Steps (Optional Frontend)

To complete the user interface, you would need to create React components for:

1. **Messaging Page** (`frontend/src/pages/Messaging.jsx`):
   - List conversations
   - Send/receive encrypted messages
   - View encryption steps for each message
   - Show which messages were intercepted

2. **MITM Attack Page** (`frontend/src/pages/MITMAttack.jsx`):
   - Select a message to intercept
   - Input attacker's guessed key
   - Optionally modify the message
   - View attack success/failure with steps

3. **Conversation View** Component:
   - Chat-like interface showing plaintext and ciphertext
   - Visual indicators for intercepted messages
   - Step-by-step encryption display

---

## 📝 API Testing Examples

### Using cURL:

```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'

# Test 3×3 Hill Cipher
curl -X POST http://127.0.0.1:8000/api/ciphers/operate/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cipher_type":"hill",
    "operation":"encrypt",
    "text":"HELLO",
    "key":{"matrix":[[6,24,1],[13,16,10],[20,17,15]]},
    "show_steps":true
  }'

# Create conversation
curl -X POST http://127.0.0.1:8000/api/messaging/conversations/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_b_id":2,
    "cipher_type":"caesar",
    "shared_key":{"shift":3}
  }'

# Send message
curl -X POST http://127.0.0.1:8000/api/messaging/messages/send/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id":1,
    "plaintext":"HELLO BOB",
    "show_steps":true
  }'

# MITM Attack
curl -X POST http://127.0.0.1:8000/api/messaging/mitm/attack/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id":1,
    "attacker_key":{"shift":3},
    "modified_plaintext":"HELLO EVE",
    "show_steps":true
  }'
```

---

## ✨ Summary

All requested features have been successfully implemented:

✅ **Hill cipher upgraded to 3×3** - Supports variable matrix sizes with proper inversion  
✅ **Step-by-step explanations** - All ciphers show detailed transformation steps  
✅ **Messaging system** - Users A and B can exchange encrypted messages  
✅ **MITM attack simulation** - Realistic man-in-the-middle attack demonstration  

The system is now a comprehensive educational platform for learning classical cryptography with hands-on secure messaging and attack simulations!
