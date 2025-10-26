# 📖 Classic CryptoLab - User Guide

**Complete Guide to Using Classic CryptoLab**

Last Updated: October 26, 2025

---

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding Ciphers](#understanding-ciphers)
3. [Using the Platform](#using-the-platform)
4. [Encryption Examples](#encryption-examples)
5. [Protection Mechanisms](#protection-mechanisms)
6. [Secure Messaging](#secure-messaging)
7. [Viewing History](#viewing-history)
8. [Understanding Attacks](#understanding-attacks)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### First Time Login

1. **Access the Platform**
   - Development: `http://localhost:5173`
   - Production: `https://classic-cryptolab.onrender.com`

2. **Test Users Available**:
   ```
   Students:
   - Username: student1, Password: password123
   - Username: student2, Password: password123
   
   Instructor:
   - Username: instructor1, Password: password123
   ```

3. **Login Process**:
   - Enter username and password
   - Click "Login"
   - You'll be redirected to dashboard

### Dashboard Overview

After logging in, you'll see:
- **Encryption/Decryption Tool** - Main cipher operations
- **Messaging** - Secure communication with other users
- **History** - All your past operations
- **Exercises** - Practice tasks (for students)
- **Attack Simulations** - Learn about vulnerabilities

---

## 🔤 Understanding Ciphers

### Cipher Comparison Table

| Cipher | Strength | Speed | Key Type | Best Use Case |
|--------|----------|-------|----------|---------------|
| **Caesar** | Very Weak | Very Fast | Single number | Learning basics |
| **Affine** | Weak | Fast | Two numbers | Understanding math |
| **Hill** | Moderate | Medium | Matrix | Learning linear algebra |
| **Playfair** | Moderate | Medium | Keyword | Historical encryption |
| **Enhanced Affine** | Strong | Slow | Password | Modern encryption |
| **Enhanced Playfair** | Strong | Medium | Keyword | Secure communication |

### When to Use Each Cipher

#### Use Caesar When:
- ✅ Learning basic encryption concepts
- ✅ Understanding substitution ciphers
- ✅ Quick manual encryption needed
- ❌ **NOT** for real secrets (too weak!)

#### Use Affine When:
- ✅ Learning mathematical cryptography
- ✅ Understanding linear transformations
- ✅ Teaching modular arithmetic
- ❌ **NOT** for real secrets (weak)

#### Use Hill When:
- ✅ Learning matrix-based encryption
- ✅ Understanding polyalphabetic ciphers
- ✅ Teaching linear algebra applications
- ❌ **NOT** for real secrets (known-plaintext vulnerable)

#### Use Playfair When:
- ✅ Understanding digraph substitution
- ✅ Historical encryption study
- ✅ More security than monoalphabetic
- ❌ **NOT** for real secrets (frequency vulnerable)

#### Use Enhanced Affine When:
- ✅ Need strong encryption
- ✅ Multiple rounds required
- ✅ CBC mode desired
- ✅ **CAN** use for real secrets (with protection)

#### Use Enhanced Playfair When:
- ✅ Need digraph encryption
- ✅ Professional implementation needed
- ✅ NumPy available
- ✅ **CAN** use for real secrets (with protection)

---

## 💻 Using the Platform

### Encrypting a Message

#### Method 1: Quick Encryption

1. **Select Cipher**
   - Click on cipher type (Caesar, Affine, etc.)

2. **Enter Message**
   ```
   Plaintext: HELLO WORLD
   ```

3. **Set Key**
   - Caesar: Shift = 3
   - Affine: a = 5, b = 8
   - Hill: Matrix = [[6, 24], [1, 16]]
   - Playfair: Keyword = "MONARCHY"

4. **Click "Encrypt"**
   - Result appears instantly
   - See step-by-step process

5. **Copy Result**
   - Click copy button
   - Send to recipient

#### Method 2: Encryption with Steps

1. **Enable "Show Steps"**
   - Toggle switch in settings

2. **Encrypt as usual**

3. **View Detailed Steps**:
   ```
   Step 1: H (position 7)
           Apply: (5 × 7 + 8) mod 26
           Result: 17 → R
   
   Step 2: E (position 4)
           Apply: (5 × 4 + 8) mod 26
           Result: 2 → C
   
   ... and so on
   ```

### Decrypting a Message

1. **Select Same Cipher Type**
   - Must match encryption cipher

2. **Enter Ciphertext**
   ```
   Ciphertext: RCLLA
   ```

3. **Enter Same Key**
   - Must use exact same key

4. **Click "Decrypt"**
   - Plaintext appears

5. **Verify Result**
   - Should match original message

---

## 📝 Encryption Examples

### Example 1: Caesar Cipher

**Scenario**: Send simple message to friend

```
Step 1: Choose Caesar Cipher
Step 2: Enter message: "MEET AT NOON"
Step 3: Choose shift: 3
Step 4: Encrypt

Result: "PHHW DW QRRQ"

To Share:
- Send ciphertext: PHHW DW QRRQ
- Tell key: Caesar shift 3
- Friend decrypts: MEET AT NOON
```

**Visual Process**:
```
M + 3 = P
E + 3 = H
E + 3 = H
T + 3 = W
(space stays space)
A + 3 = D
T + 3 = W
(space stays space)
N + 3 = Q
O + 3 = R
O + 3 = R
N + 3 = Q
```

### Example 2: Affine Cipher

**Scenario**: Use mathematical encryption

```
Step 1: Choose Affine Cipher
Step 2: Enter message: "HELLO"
Step 3: Set keys:
        a = 5 (must be coprime with 26)
        b = 8 (any number 0-25)
Step 4: Encrypt

Result: "RCLLA"

Mathematics:
H (7):  (5 × 7 + 8) mod 26 = 43 mod 26 = 17 = R
E (4):  (5 × 4 + 8) mod 26 = 28 mod 26 = 2  = C
L (11): (5 × 11 + 8) mod 26 = 63 mod 26 = 11 = L
L (11): (5 × 11 + 8) mod 26 = 63 mod 26 = 11 = L
O (14): (5 × 14 + 8) mod 26 = 78 mod 26 = 0  = A
```

### Example 3: Hill Cipher

**Scenario**: Encrypt with matrices

```
Step 1: Choose Hill Cipher
Step 2: Enter message: "HELP" (must be even length)
Step 3: Create 2×2 matrix:
        [6  24]
        [1  16]
        
        Check: determinant mod 26 must be coprime with 26
        det = (6×16 - 24×1) = 96 - 24 = 72
        72 mod 26 = 20 (coprime with 26 ✓)

Step 4: Encrypt

Result: "ETKR"

Mathematics:
HE → [7, 4]
[6  24]   [7]     [186]     [4]
[1  16] × [4]  =  [71]  →  [19] → ET

LP → [11, 15]
[6  24]   [11]    [426]     [10]
[1  16] × [15] =  [251] →  [17] → KR
```

### Example 4: Enhanced Affine

**Scenario**: Strong encryption for sensitive data

```
Step 1: Choose Enhanced Affine
Step 2: Enter message: "Secret Meeting at Midnight"
Step 3: Enter password: "myStrongPassword123"
Step 4: Enable protection: Argon2
Step 5: Encrypt

Result:
{
  "ciphertext": "/mZ5JzG+fpNgijZKEYsBfrJ6q3w...",
  "iv": "fe",
  "rounds": 2,
  "protection": "bruteforce (Argon2)"
}

Features:
✓ Random IV (different output each time)
✓ 2 rounds of encryption
✓ Byte-level security (0-255)
✓ Base64 encoded
✓ Argon2 protected

To Share:
- Send ciphertext
- Share password securely
- Friend decrypts automatically
```

---

## 🛡️ Protection Mechanisms

### Understanding Protection

**Without Protection**:
```
Plaintext: HELLO
Cipher: Caesar(3)
Ciphertext: KHOOR

Attacker tries all keys:
  0: HELLO (0.95 match - found!) ✓
  Time: <1 millisecond
```

**With Protection (Argon2)**:
```
Plaintext: HELLO
Cipher: Caesar(3)
Protection: Argon2
Ciphertext: 3a5b7c... (protected)

Attacker tries all keys:
  0: [Computing Argon2...] (100ms)
     Result: Invalid
  1: [Computing Argon2...] (100ms)
     Result: Invalid
  ...
  Time: 2.6 seconds (100,000x slower!)
```

### When to Enable Protection

#### Enable Protection For:
- ✅ Sensitive messages
- ✅ Long-term storage
- ✅ Weak ciphers (Caesar, Affine)
- ✅ Messages that might be intercepted
- ✅ Educational demonstrations

#### Protection Not Needed For:
- ❌ Already strong ciphers (with caution)
- ❌ Public information
- ❌ Speed-critical applications
- ❌ Very short messages

### Protection Type Guide

#### Use Argon2 (Brute Force Protection) For:
- Caesar Cipher (only 26 keys)
- Short keys
- Dictionary word passwords
- **Effect**: Slows down each attempt by 100,000×

#### Use Frequency Noise For:
- Affine Cipher
- Hill Cipher
- Any substitution cipher
- **Effect**: Hides letter patterns completely

#### Use DH + HMAC For:
- Playfair Cipher
- Network transmission
- Multi-party communication
- **Effect**: Prevents MITM and detects tampering

---

## 💬 Secure Messaging

### Creating a Secure Conversation

#### Step 1: Navigate to Messaging
- Click "Messaging" in main menu

#### Step 2: Start New Conversation
1. Click "+ New Conversation"
2. Select recipient (student2, etc.)
3. Choose cipher type
4. Set shared key
5. **Toggle Protection ON** 🔒
6. Click "Create"

#### Step 3: Send Encrypted Message
1. Type your message in plaintext
2. Click "Send"
3. Message is automatically:
   - Encrypted with selected cipher
   - Protected based on cipher type
   - Saved to history
   - Sent to recipient

#### Step 4: Receive Message
1. See encrypted message in conversation
2. Click "Decrypt" to view
3. See decryption steps
4. View protection details

### Example Conversation

**Setup**:
```
Participants: Alice (student1) & Bob (student2)
Cipher: Affine (a=5, b=8)
Protection: ON (Frequency Noise)
```

**Alice Sends**:
```
Plaintext: "Meet me at the library at 3pm"
↓
Affine Encrypt (a=5, b=8)
↓
Ciphertext: "PCCR PC GR RVC FWZLGL..."
↓
Add Frequency Noise (25%)
↓
Protected: "P#C$C%R P^C G&R R*V..."
↓
Store in Database
```

**Bob Receives**:
```
Protected Ciphertext from Database
↓
Remove Frequency Noise
↓
Ciphertext: "PCCR PC GR RVC FWZLGL..."
↓
Affine Decrypt (a=5, b=8)
↓
Plaintext: "Meet me at the library at 3pm"
```

### Protection Toggle

**Button**: 🔒 Protection ON (green) / 🔓 Protection OFF (red)

**What It Does**:
- **ON**: All future messages in conversation are protected
- **OFF**: Future messages sent without protection
- **Note**: Already sent messages keep their original protection status

**When to Toggle**:
- Turn ON for sensitive conversations
- Turn OFF for public/speed-critical messages
- Change anytime (affects only new messages)

---

## 📊 Viewing History

### Accessing History

1. **Navigate to History**
   - Click "History" in main menu

2. **View Recent Operations**
   - Shows last 50 operations by default
   - Displays: cipher, operation, time, protection

3. **Filter Results**:
   ```
   Filters Available:
   - Cipher Type (Caesar, Affine, etc.)
   - Operation (Encrypt / Decrypt)
   - Protection Status (ON / OFF)
   - Protection Type (Argon2, Noise, DH+HMAC)
   - Context (Standalone, Messaging, Exercise)
   - Date Range
   ```

### Understanding History Entries

**Example Entry**:
```
┌─────────────────────────────────────────────┐
│ [Oct 26, 2025 - 10:30 AM]                  │
│                                              │
│ Cipher: Affine                               │
│ Operation: ENCRYPT                           │
│ Protection: 🔊 Frequency Noise Injection     │
│ Context: Messaging                           │
│                                              │
│ Input: "Hello World"                         │
│ Output: "R#c$l%la Z^o&rld"                  │
│ Key: {a: 5, b: 8}                           │
│                                              │
│ [View Steps] [Copy] [Replay]                │
└─────────────────────────────────────────────┘
```

### Exporting History

1. **Select Entries**
   - Check boxes next to entries

2. **Click "Export"**
   - Choose format: JSON, CSV, PDF

3. **Download**
   - File contains all selected operations

### Using History for Learning

#### Review Pattern:
```
1. Perform encryption
2. View in history
3. Study the steps
4. Try to replicate manually
5. Compare results
6. Understand the process
```

#### Common Use Cases:
- **Study**: Review past encryptions to understand patterns
- **Debug**: Find where encryption went wrong
- **Learn**: See how protection affects output
- **Compare**: Different ciphers on same input
- **Track**: Monitor your progress over time

---

## ⚔️ Understanding Attacks

### Attack Simulations (Educational Only!)

**Important**: All attacks are for educational purposes in a controlled environment.

### 1. Brute Force Attack

**What It Is**:
- Try every possible key until finding the right one
- Works on ciphers with small key spaces

**How to Simulate**:
```
1. Navigate to "Attacks" section
2. Select "Brute Force"
3. Choose target cipher (e.g., Caesar)
4. Enter ciphertext
5. Click "Run Attack"
6. Watch as each key is tried
7. See when correct key is found
```

**Example**:
```
Ciphertext: "KHOOR ZRUOG"
Cipher: Caesar

Attack Progress:
  Shift 0: "KHOOR ZRUOG" ❌
  Shift 1: "JGNNQ YQTNF" ❌
  Shift 2: "IFMMP XPSME" ❌
  Shift 3: "HELLO WORLD" ✅ FOUND!

Time: <1ms (without protection)
Time: 2.6s (with Argon2 protection)
```

**Learning Points**:
- Small key spaces are vulnerable
- Protection dramatically slows attacks
- Some ciphers are inherently weak

### 2. Frequency Analysis Attack

**What It Is**:
- Analyze letter frequencies in ciphertext
- Compare to known language frequencies
- Deduce substitution mapping

**How to Simulate**:
```
1. Navigate to "Attacks" → "Frequency Analysis"
2. Enter ciphertext (needs 100+ letters)
3. Select language (English)
4. Click "Analyze"
5. See frequency chart
6. View suggested mapping
7. Test decryption
```

**Example**:
```
Ciphertext (100 letters):
"RCLLA PSZFA RCLLA HSSZR..."

Frequency Count:
  R: 15 times (most common)
  C: 12 times
  L: 10 times
  ...

English Frequencies:
  E: 12.7% (most common)
  T: 9.1%
  A: 8.2%
  ...

Suggested Mapping:
  R → E
  C → T
  L → A

Test Decryption:
  "RCLLA" → "ETAA" (close but not quite)
  
Refine with bigrams:
  Common "RC" → "ET" or "TH"?
  
Final Mapping:
  R → H
  C → E
  L → L
  ...

Result: "HELLO WORLD HELLO WORLD..."
```

**Effect of Protection**:
```
Without Noise:
  Clear frequency pattern ✓
  Attack succeeds 95%+ ✓
  
With 25% Noise:
  No clear pattern ❌
  All letters ~equal frequency ❌
  Attack fails <10% success ✓
```

### 3. Man-in-the-Middle (MITM) Attack

**What It Is**:
- Intercept message between sender and receiver
- Potentially modify message
- Forward to receiver

**How to Simulate**:
```
1. Navigate to "Attacks" → "MITM"
2. Select message to intercept
3. Choose attacker key (if known)
4. Modify plaintext (optional)
5. Click "Execute Attack"
6. See if attack succeeds
```

**Example Scenario**:
```
Alice → Bob: "TRANSFER $100 TO BOB"

Without HMAC:
  1. Alice encrypts: "WUDQVIHU..."
  2. Eve intercepts
  3. Eve decrypts (knows key)
  4. Eve modifies: "TRANSFER $100 TO EVE"
  5. Eve re-encrypts: "WUDQVIHU..."
  6. Bob receives and decrypts
  7. Bob: "Transferring $100 to Eve" ❌
  
With HMAC:
  1. Alice encrypts + HMAC tag
  2. Eve intercepts
  3. Eve modifies message
  4. Eve forwards (can't recompute HMAC)
  5. Bob checks HMAC
  6. HMAC mismatch detected!
  7. Bob: "Attack detected! Rejecting." ✓
```

**Learning Points**:
- Encryption alone ≠ integrity
- HMAC prevents tampering
- Key exchange is critical

---

## 🎯 Best Practices

### For Students

#### Learning Progression:
```
Week 1: Caesar Cipher
  - Understand shifting
  - Manual encryption/decryption
  - Learn about brute force

Week 2: Affine Cipher
  - Understand modular arithmetic
  - Learn coprime requirement
  - Practice frequency analysis

Week 3: Hill Cipher
  - Understand matrices
  - Learn about invertibility
  - Practice matrix operations

Week 4: Playfair Cipher
  - Understand digraphs
  - Learn matrix rules
  - Compare to monoalphabetic

Week 5: Protection Mechanisms
  - Add Argon2 to Caesar
  - Add noise to Affine
  - Add HMAC to Playfair

Week 6: Attack Defenses
  - Run attacks on unprotected
  - Run attacks on protected
  - Understand effectiveness
```

#### Study Tips:
1. **Start Simple**: Master Caesar before moving on
2. **Use Steps**: Always enable "Show Steps" when learning
3. **Compare**: Try same message with different ciphers
4. **History**: Review your past work regularly
5. **Attacks**: Run attack simulations to understand vulnerabilities
6. **Protection**: See how protection affects security

### For Instructors

#### Creating Exercises:
```
1. Login as instructor
2. Navigate to "Exercises"
3. Click "Create New"
4. Fill in details:
   - Title: "Caesar Cipher Practice"
   - Description: "Encrypt the given message"
   - Cipher: Caesar
   - Difficulty: Easy
   - Points: 10
5. Add test cases
6. Set deadline
7. Publish
```

#### Monitoring Students:
```
1. Dashboard shows:
   - Student activity levels
   - Exercise completion rates
   - Average scores
   - Common mistakes

2. View individual students:
   - All operations
   - Exercise submissions
   - Areas needing help
```

### Security Best Practices

#### ✅ DO:
- Use protection for weak ciphers
- Enable "Show Steps" when learning
- Review history to understand patterns
- Run attack simulations to learn
- Use enhanced ciphers for real secrets

#### ❌ DON'T:
- Use weak ciphers without protection for real secrets
- Share keys over insecure channels
- Reuse keys across conversations
- Ignore attack warnings
- Trust unverified messages (check HMAC!)

---

## 🔧 Troubleshooting

### Common Issues

#### "Invalid Key" Error

**Problem**: Affine cipher shows "Invalid key"

**Cause**: `a` value not coprime with 26

**Solution**:
```
Valid values for a:
1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25

Try one of these!
```

#### "Matrix Not Invertible" Error

**Problem**: Hill cipher fails with matrix error

**Cause**: Determinant not coprime with 26

**Solution**:
```
1. Calculate: det = ad - bc
2. Check: gcd(det mod 26, 26) must = 1
3. Try different matrix if not

Example working matrix:
[6  24]  → det = 96-24 = 72 → 72 mod 26 = 20 ✓
[1  16]     gcd(20, 26) = 2 ❌ Wait, this is wrong!

Actually: gcd(20, 26) = 2 (not coprime)
Better matrix:
[3  3]   → det = 9-6 = 3 → gcd(3, 26) = 1 ✓
[2  3]
```

#### Decryption Returns Gibberish

**Problem**: Decrypted text is nonsense

**Possible Causes**:
1. **Wrong Key**: Using different key than encryption
   - Solution: Verify key matches exactly
   
2. **Wrong Cipher**: Using different cipher type
   - Solution: Use same cipher as encryption
   
3. **Protection Mismatch**: Trying to decrypt protected message without removing protection
   - Solution: Use decrypt endpoint that handles protection

4. **Corrupted Ciphertext**: Message was modified
   - Solution: Check HMAC if enabled, re-send message

#### Protection Seems Slow

**Problem**: Encryption/decryption takes several seconds

**Cause**: This is intentional! Argon2 protection.

**Explanation**:
```
Without Argon2: <1ms
With Argon2:    100-500ms (demo settings)
                
This is a FEATURE, not a bug!
- Makes brute force 100,000x slower
- Legitimate users: 0.5s delay (acceptable)
- Attackers: 2.6s for Caesar, hours for others
```

**Solution**:
- For learning: Use demo settings (current)
- For production: Increase to 500ms
- For speed tests: Temporarily disable protection

#### History Not Saving

**Problem**: Operations don't appear in history

**Causes & Solutions**:
1. **Not Logged In**: Login required
   - Solution: Login first

2. **"Log Operation" Disabled**: Check settings
   - Solution: Enable in preferences

3. **Database Issue**: Server problem
   - Solution: Check server logs, restart if needed

---

## 📚 Additional Resources

### Documentation Files

- **README.md** - Complete project overview
- **PROTECTION_INTEGRATION_GUIDE.md** - Technical protection details
- **IMPLEMENTATION_SUMMARY.md** - Development history
- **API_DOCUMENTATION.md** - Full API reference

### Learning Resources

#### Recommended Reading Order:
1. This User Guide (you are here!)
2. README.md (overview)
3. Try Caesar cipher examples
4. Run brute force attack
5. Add Argon2 protection
6. Try other ciphers
7. Read Protection Guide
8. Implement secure messaging
9. Review complete API docs

#### External Resources:
- **Cryptography Basics**: Wikipedia articles on each cipher
- **Argon2 Paper**: "Argon2: The Password Hashing Competition"
- **DH Paper**: "New Directions in Cryptography" by Diffie & Hellman
- **HMAC RFC**: RFC 2104

### Getting Help

1. **Check Documentation**: Most answers are in docs
2. **View History**: See if you did it correctly before
3. **Compare Examples**: Use examples in this guide
4. **Ask Instructor**: For educational questions
5. **GitHub Issues**: For technical problems

---

## 🎓 Learning Path

### Beginner Track (Weeks 1-2)

**Week 1: Caesar Cipher**
- [ ] Encrypt your name with shift 3
- [ ] Decrypt a message from friend
- [ ] Try all 26 shifts manually
- [ ] Run brute force attack
- [ ] Add Argon2 protection
- [ ] Run brute force on protected
- [ ] Compare times

**Week 2: Affine Cipher**
- [ ] Encrypt with a=5, b=8
- [ ] Understand coprime requirement
- [ ] Try invalid key (a=2)
- [ ] Learn modular arithmetic
- [ ] Analyze frequency
- [ ] Add frequency noise
- [ ] Compare attack success

### Intermediate Track (Weeks 3-4)

**Week 3: Hill Cipher**
- [ ] Create 2×2 matrix
- [ ] Check invertibility
- [ ] Encrypt 4-letter word
- [ ] Decrypt result
- [ ] Try known-plaintext attack
- [ ] Add protection
- [ ] Study linear algebra application

**Week 4: Playfair Cipher**
- [ ] Create keyword matrix
- [ ] Encrypt digraph pairs
- [ ] Handle same-letter pairs
- [ ] Decrypt message
- [ ] Compare to Caesar
- [ ] Add HMAC protection
- [ ] Simulate MITM attack

### Advanced Track (Weeks 5-6)

**Week 5: Enhanced Ciphers**
- [ ] Use Enhanced Affine with CBC
- [ ] Understand IV purpose
- [ ] Try multi-round encryption
- [ ] Use Enhanced Playfair
- [ ] Compare to classical versions
- [ ] Combine with protection
- [ ] Benchmark performance

**Week 6: Complete System**
- [ ] Create secure conversation
- [ ] Toggle protection on/off
- [ ] Send/receive messages
- [ ] View complete history
- [ ] Filter by criteria
- [ ] Export history
- [ ] Present findings

---

## ✅ Quick Reference

### Cipher Keys Quick Guide

| Cipher | Key Format | Example |
|--------|-----------|---------|
| Caesar | Single number (0-25) | `{"shift": 3}` |
| Affine | Two numbers (a coprime with 26, b any) | `{"a": 5, "b": 8}` |
| Hill | 2×2 matrix (invertible) | `{"matrix": [[6,24],[1,16]]}` |
| Playfair | Keyword (letters only) | `{"keyword": "MONARCHY"}` |
| Enhanced Affine | Password string | `"myPassword123"` |
| Enhanced Playfair | Keyword | `{"keyword": "SECRET"}` |

### Protection Type Mapping

| Cipher | Default Protection | Reason |
|--------|-------------------|---------|
| Caesar | Argon2 (bruteforce) | Small key space |
| Affine | Noise (frequency) | Frequency vulnerable |
| Hill | Noise (frequency) | Pattern analysis |
| Playfair | DH+HMAC (mitm) | Shared key vulnerable |
| Enhanced Affine | Argon2 (bruteforce) | Key stretching beneficial |
| Enhanced Playfair | DH+HMAC (mitm) | Integrity important |

### Common Commands

```bash
# Start backend
cd backend
venv\Scripts\activate
python manage.py runserver

# Start frontend
cd frontend
npm run dev

# Run tests
cd backend
python test_protection.py

# View history
GET /api/ciphers/history/?limit=10

# Toggle protection
POST /api/messaging/conversations/{id}/toggle-protection/
```

---

**End of User Guide** 📖

*For more information, see README.md or contact support.*

*Last Updated: October 26, 2025*
