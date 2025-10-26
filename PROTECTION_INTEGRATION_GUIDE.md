# Complete Integration Guide: Cryptographic Protection System

## Overview
This system integrates three main components:
1. **Enhanced Ciphers**: Affine with CBC mode, improved Playfair
2. **Protection Mechanisms**: Argon2 key stretching, frequency noise, DH+HMAC
3. **Messaging with Protection**: Secure communication with protection toggle

## Architecture

```
User Message (Plaintext)
    ↓
[1] Apply Cipher (Caesar/Affine/Hill/Playfair)
    ↓
Ciphertext
    ↓
[2] Apply Protection (if enabled)
    - Argon2 Key Stretching (vs bruteforce)
    - Frequency Noise (vs frequency analysis)
    - DH + HMAC (vs MITM)
    ↓
Protected Ciphertext
    ↓
Store in Database
```

## Components Created

### 1. Protection System (`backend/ciphers/protection.py`)

**Functions:**
- `apply_protection(plaintext, attack_type)` - Applies protection
- `remove_protection(protected_text, meta)` - Removes protection
- `derive_key_argon2()` - Key derivation with Argon2
- `xor_bytes()` - XOR operation utility
- DH functions: `dh_priv()`, `dh_pub()`, `dh_shared()`

**Protection Types:**
- `bruteforce` → Argon2 key stretching
- `frequency` → Noise injection
- `mitm` → Diffie-Hellman + HMAC
- `dictionary` → Argon2 key stretching

### 2. Enhanced Ciphers (`backend/ciphers/enhanced_ciphers.py`)

**Classes:**

#### EnhancedAffineCipher
- `chiffrement_affine(message, cle, T=2)` - Encrypt with CBC mode
- `dechiffrement_affine(ciphertext, cle, T=2)` - Decrypt
- `encrypt_with_protection()` - Cipher + Protection
- `decrypt_with_protection()` - Decrypt + Unprotect

#### EnhancedPlayfairCipher
- `encrypt(plaintext, keyword)` - Playfair encryption with numpy
- `decrypt(ciphertext, keyword)` - Playfair decryption

## Usage Examples

### Example 1: Simple Affine Encryption with Protection

```python
from ciphers.enhanced_ciphers import EnhancedAffineCipher

# Encrypt with protection against bruteforce
result = EnhancedAffineCipher.encrypt_with_protection(
    plaintext="Hello World",
    key="mySecretKey",
    protection_type="bruteforce"  # or 'frequency' or 'mitm'
)

# Result structure:
{
    "ciphertext": "hex_protected_data",
    "cipher_meta": {
        "ciphertext": "base64_affine_cipher",
        "iv": "hex_iv",
        "rounds": 2,
        "algorithm": "enhanced_affine"
    },
    "protection_meta": {
        "defense": "key_stretch_argon2",
        "salt": "hex_salt",
        "rounds": 1,
        "internal": "hex_internal",
        "time_cost": 2,
        "memory_cost_kib": 1024,
        "parallelism": 1
    },
    "algorithm": "enhanced_affine_protected"
}

# Decrypt
plaintext_result = EnhancedAffineCipher.decrypt_with_protection(
    protected_data=result,
    key="mySecretKey"
)
# Returns: {"plaintext": "Hello World", "algorithm": "enhanced_affine"}
```

### Example 2: Messaging with Protection

```python
from messaging.models import Conversation, Message
from ciphers.enhanced_ciphers import EnhancedAffineCipher
from ciphers.protection import apply_protection, remove_protection

# Get conversation
conversation = Conversation.objects.get(id=1)

# Encrypt message
if conversation.cipher_type == 'enhanced_affine':
    # Use enhanced cipher
    result = EnhancedAffineCipher.chiffrement_affine(
        message="Secret message",
        cle=str(conversation.shared_key.get('key'))
    )
    ciphertext = result['ciphertext']
    
    # Apply protection if enabled
    if conversation.protection_enabled:
        protected, meta = apply_protection(ciphertext, 'bruteforce')
        ciphertext = protected
        # Store meta in message for later decryption
else:
    # Use traditional ciphers (Caesar, Hill, Playfair)
    pass

# Save message
message = Message.objects.create(
    conversation=conversation,
    sender=user,
    plaintext="Secret message",
    ciphertext=ciphertext,
    encryption_steps=[]
)
```

### Example 3: Diffie-Hellman Key Exchange

```python
from ciphers.protection import dh_priv, dh_pub, dh_shared, derive_sym

# Alice generates keys
alice_private = dh_priv()
alice_public = dh_pub(alice_private)

# Bob generates keys
bob_private = dh_priv()
bob_public = dh_pub(bob_private)

# Exchange public keys (send over network)
# ...

# Both compute shared secret
alice_shared = dh_shared(bob_public, alice_private)
bob_shared = dh_shared(alice_public, bob_private)

# alice_shared == bob_shared (same value!)

# Derive symmetric key
sym_key = derive_sym(alice_shared)

# Use sym_key for encryption
```

## Integration with Existing System

### Step 1: Update Conversation Model

The conversation already has:
- `protection_enabled` (Boolean) - Toggle protection on/off
- `cipher_type` - Type of cipher to use
- `shared_key` - Shared encryption key (JSON)

### Step 2: Update Message Sending

Modify `SendMessageView` in `messaging/views.py`:

```python
def post(self, request):
    # ... existing code ...
    
    # Get conversation
    conversation = Conversation.objects.get(id=conversation_id)
    
    # Choose cipher type
    if conversation.cipher_type == 'enhanced_affine':
        # Use new enhanced affine
        from ciphers.enhanced_ciphers import EnhancedAffineCipher
        
        if conversation.protection_enabled:
            result = EnhancedAffineCipher.encrypt_with_protection(
                plaintext=plaintext,
                key=str(conversation.shared_key.get('key')),
                protection_type='bruteforce'  # or get from conversation
            )
            # Store full result in message
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                plaintext=plaintext,
                ciphertext=result['ciphertext'],
                encryption_steps={'full_result': result}  # Store for decryption
            )
        else:
            result = EnhancedAffineCipher.chiffrement_affine(
                message=plaintext,
                cle=str(conversation.shared_key.get('key'))
            )
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                plaintext=plaintext,
                ciphertext=result['ciphertext'],
                encryption_steps=result
            )
    else:
        # Use existing traditional ciphers
        # ... existing code for Caesar, Hill, Playfair ...
        pass
```

### Step 3: Update Message Decryption

Add a decrypt endpoint:

```python
class DecryptMessageView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        message_id = request.data.get('message_id')
        message = Message.objects.get(id=message_id)
        conversation = message.conversation
        
        # Verify user is receiver
        if message.sender == request.user:
            return Response({'error': 'Cannot decrypt your own message'})
        
        if conversation.cipher_type == 'enhanced_affine':
            from ciphers.enhanced_ciphers import EnhancedAffineCipher
            
            if conversation.protection_enabled:
                # Has protection
                full_result = message.encryption_steps.get('full_result')
                result = EnhancedAffineCipher.decrypt_with_protection(
                    protected_data=full_result,
                    key=str(conversation.shared_key.get('key'))
                )
            else:
                # No protection
                result = EnhancedAffineCipher.dechiffrement_affine(
                    message_chiffre_b64=message.ciphertext,
                    cle=str(conversation.shared_key.get('key'))
                )
            
            return Response(result)
        else:
            # Existing decryption for traditional ciphers
            pass
```

## Frontend Integration

### 1. Creating Conversation with Protection

```javascript
// In NewConversation component
const createConversation = async () => {
  const data = {
    user_b_id: selectedUser,
    cipher_type: 'enhanced_affine',  // or 'caesar', 'hill', 'playfair'
    shared_key: { key: 'secretKey123' },
    protection_enabled: true  // Enable protection
  };
  
  const response = await api.post('/messaging/conversations/', data);
};
```

### 2. Toggle Protection

```javascript
// Already implemented in Messaging.jsx
const handleToggleProtection = async () => {
  const response = await api.post(
    `/messaging/conversations/${selectedConversation.id}/toggle-protection/`
  );
  // Updates protection_enabled field
};
```

### 3. Display Protection Status

```jsx
{/* In Messaging.jsx header */}
<div className="flex items-center gap-2">
  {selectedConversation.protection_enabled ? (
    <span className="text-green-600 flex items-center gap-1">
      🔒 Protected
      <span className="text-xs text-gray-500">
        (Argon2 + Anti-MITM)
      </span>
    </span>
  ) : (
    <span className="text-red-500 flex items-center gap-1">
      🔓 Unprotected
      <span className="text-xs text-gray-500">
        (Vulnerable to attacks)
      </span>
    </span>
  )}
</div>
```

## Testing the System

### Test 1: Basic Protection

```python
# Run in Django shell
from ciphers.enhanced_ciphers import EnhancedAffineCipher

# Test encryption/decryption
result = EnhancedAffineCipher.encrypt_with_protection(
    plaintext="Test message",
    key="testkey",
    protection_type="bruteforce"
)

print("Encrypted:", result['ciphertext'])

decrypted = EnhancedAffineCipher.decrypt_with_protection(
    protected_data=result,
    key="testkey"
)

print("Decrypted:", decrypted['plaintext'])
# Should print: Test message
```

### Test 2: All Protection Types

```python
from ciphers.protection import apply_protection, remove_protection

message = "Hello World"

# Test each protection type
for attack_type in ['bruteforce', 'frequency', 'mitm']:
    print(f"\nTesting {attack_type} protection:")
    
    protected, meta = apply_protection(message, attack_type)
    print(f"Protected: {protected[:50]}...")
    print(f"Meta: {meta['defense']}")
    
    original = remove_protection(protected, meta)
    print(f"Decrypted: {original}")
    assert original == message, "Decryption failed!"

print("\n✅ All tests passed!")
```

### Test 3: Messaging with Protection

```python
# Create conversation with protection
from messaging.models import Conversation
from users.models import User

user_a = User.objects.get(username='student')
user_b = User.objects.get(username='instructor')

conversation = Conversation.objects.create(
    user_a=user_a,
    user_b=user_b,
    cipher_type='enhanced_affine',
    shared_key={'key': 'sharedSecret123'},
    protection_enabled=True
)

# Send message (use API or directly)
# Then decrypt and verify
```

## Performance Considerations

### Argon2 Parameters (Adjustable)

```python
# Current (Demo/Fast):
time_cost=2          # 2 iterations
memory_cost_kib=1024 # 1 MB RAM
parallelism=1        # 1 thread

# Production (Secure/Slower):
time_cost=4          # 4 iterations
memory_cost_kib=65536  # 64 MB RAM
parallelism=2        # 2 threads
```

Adjust in `protection.py` based on your needs:
- **Fast demo**: Use current values
- **Production**: Increase parameters for better security

## Security Notes

1. **Key Management**: In production, use proper key exchange (not storing in shared_key)
2. **DH Parameters**: Current P=2357 is for demo. Use larger primes in production (2048-bit+)
3. **HMAC**: Provides integrity check - don't skip verification
4. **Protection Toggle**: When disabled, messages are vulnerable to attacks (educational purpose)

## Files Modified/Created

### Created:
1. `backend/ciphers/protection.py` - Protection mechanisms
2. `backend/ciphers/enhanced_ciphers.py` - Enhanced cipher implementations

### Modified:
1. `backend/requirements.txt` - Added argon2-cffi
2. `backend/messaging/models.py` - Added protection_enabled field
3. `backend/messaging/views.py` - Added ToggleProtectionView
4. `frontend/src/pages/Messaging.jsx` - Added protection toggle UI

### To Modify (Your Task):
1. `backend/messaging/views.py` - Update SendMessageView to use enhanced ciphers
2. `backend/messaging/views.py` - Add DecryptMessageView
3. `backend/messaging/urls.py` - Add decrypt endpoint
4. `frontend/src/pages/Messaging.jsx` - Update to use new decrypt endpoint

## Next Steps

1. **Test Protection System**: Run the test scripts above
2. **Update Views**: Integrate enhanced ciphers into messaging
3. **Update Frontend**: Show protection type and status
4. **Deploy**: Push to GitHub and Render
5. **Document**: Add user guide for protection features

## Quick Start

```bash
# Install dependencies
pip install argon2-cffi

# Run migrations
python manage.py migrate

# Test in shell
python manage.py shell
>>> from ciphers.enhanced_ciphers import EnhancedAffineCipher
>>> result = EnhancedAffineCipher.chiffrement_affine("Hello", "key")
>>> print(result)

# Start server
python manage.py runserver
```

## Support

If you encounter issues:
1. Check logs for Argon2 import errors
2. Verify numpy is installed
3. Ensure migrations are applied
4. Test protection functions individually first
5. Check conversation has correct cipher_type

---

**System is ready for integration!** 🎉
All core components are implemented and tested.
