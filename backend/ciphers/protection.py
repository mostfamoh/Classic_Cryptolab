"""
Protection mechanisms against various cryptographic attacks.
Implements key stretching (Argon2), frequency noise, and Diffie-Hellman with HMAC.
"""

import os
import random
import hashlib
import hmac
from typing import Tuple, Dict

try:
    from argon2.low_level import hash_secret_raw, Type
except ImportError:
    # Fallback to PBKDF2 if Argon2 is not available
    hash_secret_raw = None
    Type = None


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR operation between data and key (key is repeated if shorter)"""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def derive_key_argon2(passphrase: str, salt: bytes,
                      time_cost: int = 2,
                      memory_cost_kib: int = 65536,  # 64 MB
                      parallelism: int = 2,
                      hash_len: int = 32) -> bytes:
    """Derive a key using Argon2id"""
    if hash_secret_raw is None:
        # Fallback to PBKDF2 if Argon2 is not available
        import hashlib
        return hashlib.pbkdf2_hmac('sha256', passphrase.encode('utf-8'), salt, 100000, hash_len)
    
    return hash_secret_raw(
        secret=passphrase.encode('utf-8'),
        salt=salt,
        time_cost=time_cost,
        memory_cost=memory_cost_kib,
        parallelism=parallelism,
        hash_len=hash_len,
        type=Type.ID
    )


def key_stretch_wrap_argon2(plain: str,
                           rounds: int = 1,
                           time_cost: int = 2,
                           memory_cost_kib: int = 1024,  # 1 MB for demo
                           parallelism: int = 1) -> Tuple[str, Dict]:
    """Apply key stretching protection using Argon2"""
    salt = os.urandom(12)
    internal = os.urandom(8).hex()
    data = plain.encode('utf-8')
    
    for r in range(rounds):
        key = derive_key_argon2(
            internal + f":{r}", 
            salt,
            time_cost=time_cost,
            memory_cost_kib=memory_cost_kib,
            parallelism=parallelism,
            hash_len=32
        )
        data = xor_bytes(data, key)
    
    meta = {
        'defense': 'key_stretch_argon2',
        'salt': salt.hex(),
        'rounds': rounds,
        'internal': internal,
        'time_cost': time_cost,
        'memory_cost_kib': memory_cost_kib,
        'parallelism': parallelism
    }
    return data.hex(), meta


def unwrap_key_stretch_argon2(cipher_hex: str, meta: Dict) -> str:
    """Remove key stretching protection"""
    data = bytes.fromhex(cipher_hex)
    salt = bytes.fromhex(meta['salt'])
    internal = meta['internal']
    
    for r in reversed(range(meta['rounds'])):
        key = derive_key_argon2(
            internal + f":{r}", 
            salt,
            time_cost=meta['time_cost'],
            memory_cost_kib=meta['memory_cost_kib'],
            parallelism=meta['parallelism'],
            hash_len=32
        )
        data = xor_bytes(data, key)
    
    return data.decode('utf-8')


def frequency_wrap(plain: str, ratio: float = 0.25) -> Tuple[str, Dict]:
    """Add noise to defeat frequency analysis"""
    rng = random.Random()
    out = bytearray()
    noise_pos = []
    
    for b in plain.encode('utf-8'):
        out.append(b)
        if rng.random() < ratio:
            noise_pos.append(len(out))
            out.append(rng.choice(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    
    return out.hex(), {'defense': 'noise', 'noise_pos': noise_pos}


def unwrap_frequency(cipher_hex: str, meta: Dict) -> str:
    """Remove frequency noise"""
    data = bytearray(bytes.fromhex(cipher_hex))
    pos = set(meta.get('noise_pos', []))
    cleaned = bytearray(b for i, b in enumerate(data) if i not in pos)
    return cleaned.decode('utf-8')


# Diffie-Hellman parameters (small for demo, use larger in production)
DH_P = 2357
DH_G = 2


def dh_priv():
    """Generate private DH key"""
    return random.randint(2, DH_P - 2)


def dh_pub(x):
    """Generate public DH key"""
    return pow(DH_G, x, DH_P)


def dh_shared(pub, priv):
    """Calculate shared DH secret"""
    return pow(pub, priv, DH_P)


def derive_sym(shared_int: int) -> bytes:
    """Derive symmetric key from DH shared secret"""
    return hashlib.sha256(str(shared_int).encode()).digest()


def mitm_wrap(plain: str) -> Tuple[str, Dict]:
    """Protect against MITM using DH + XOR + HMAC"""
    a = dh_priv()
    A = dh_pub(a)
    b = dh_priv()
    B = dh_pub(b)
    shared = dh_shared(B, a)
    sym = derive_sym(shared)
    ct = xor_bytes(plain.encode('utf-8'), sym)
    tag = hmac.new(sym, ct, hashlib.sha256).hexdigest()
    
    return ct.hex(), {
        'defense': 'dh_xor_hmac',
        'shared': shared,
        'hmac': tag,
        'A_pub': A,
        'B_pub': B
    }


def unwrap_mitm(cipher_hex: str, meta: Dict) -> str:
    """Remove MITM protection"""
    sym = derive_sym(meta['shared'])
    ct = bytes.fromhex(cipher_hex)
    
    # Verify HMAC
    if not hmac.compare_digest(
        hmac.new(sym, ct, hashlib.sha256).hexdigest(), 
        meta.get('hmac', '')
    ):
        raise ValueError("HMAC verification failed - possible tampering!")
    
    return xor_bytes(ct, sym).decode('utf-8')


# Mapping from attack type to protection method
ATTACK_TO_DEFENSE = {
    'bruteforce': 'key_stretch_argon2',
    'frequency': 'noise',
    'mitm': 'dh_xor_hmac',
    'dictionary': 'key_stretch_argon2'  # Same as bruteforce
}

ENCRYPT_METHODS = {
    'key_stretch_argon2': key_stretch_wrap_argon2,
    'noise': frequency_wrap,
    'dh_xor_hmac': mitm_wrap
}

DECRYPT_METHODS = {
    'key_stretch_argon2': unwrap_key_stretch_argon2,
    'noise': unwrap_frequency,
    'dh_xor_hmac': unwrap_mitm
}


def apply_protection(plaintext: str, attack_type: str = 'bruteforce') -> Tuple[str, Dict]:
    """
    Apply protection based on attack type.
    Returns (protected_text, metadata)
    """
    defense = ATTACK_TO_DEFENSE.get(attack_type, 'key_stretch_argon2')
    
    # Use lighter parameters for demo
    if defense == 'key_stretch_argon2':
        return ENCRYPT_METHODS[defense](
            plaintext,
            rounds=1,
            time_cost=2,
            memory_cost_kib=1024,
            parallelism=1
        )
    else:
        return ENCRYPT_METHODS[defense](plaintext)


def remove_protection(protected_text: str, meta: Dict) -> str:
    """
    Remove protection based on metadata.
    Returns original plaintext
    """
    defense = meta.get('defense')
    if defense not in DECRYPT_METHODS:
        raise ValueError(f"Unknown defense method: {defense}")
    
    return DECRYPT_METHODS[defense](protected_text, meta)
