"""
Test script for cryptographic protection system.
Run: python test_protection.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptolab.settings')
django.setup()

from ciphers.protection import apply_protection, remove_protection
from ciphers.enhanced_ciphers import EnhancedAffineCipher, EnhancedPlayfairCipher


def test_protection_mechanisms():
    """Test all protection types"""
    print("=" * 60)
    print("Testing Protection Mechanisms")
    print("=" * 60)
    
    test_message = "Hello, this is a secret message!"
    
    for attack_type in ['bruteforce', 'frequency', 'mitm']:
        print(f"\n🔒 Testing {attack_type.upper()} protection...")
        
        try:
            # Apply protection
            protected, meta = apply_protection(test_message, attack_type)
            print(f"   ✓ Protected: {protected[:40]}...")
            print(f"   ✓ Defense: {meta['defense']}")
            
            # Remove protection
            original = remove_protection(protected, meta)
            print(f"   ✓ Decrypted: {original}")
            
            # Verify
            assert original == test_message, "Decryption failed!"
            print(f"   ✅ {attack_type.upper()} test PASSED")
            
        except Exception as e:
            print(f"   ❌ {attack_type.upper()} test FAILED: {str(e)}")
            return False
    
    return True


def test_enhanced_affine():
    """Test enhanced affine cipher"""
    print("\n" + "=" * 60)
    print("Testing Enhanced Affine Cipher")
    print("=" * 60)
    
    test_message = "Hello World! 🔐"
    test_key = "mySecretKey123"
    
    try:
        # Test basic encryption/decryption
        print("\n📝 Testing basic encryption...")
        result = EnhancedAffineCipher.chiffrement_affine(test_message, test_key)
        print(f"   ✓ Ciphertext (base64): {result['ciphertext'][:40]}...")
        print(f"   ✓ IV: {result['iv']}")
        print(f"   ✓ Rounds: {result['rounds']}")
        
        print("\n🔓 Testing basic decryption...")
        decrypted = EnhancedAffineCipher.dechiffrement_affine(
            result['ciphertext'], 
            test_key
        )
        print(f"   ✓ Plaintext: {decrypted['plaintext']}")
        
        assert decrypted['plaintext'] == test_message, "Basic decryption failed!"
        print("   ✅ Basic affine test PASSED")
        
        # Test with protection
        print("\n🔐 Testing encryption with protection...")
        protected_result = EnhancedAffineCipher.encrypt_with_protection(
            test_message,
            test_key,
            protection_type='bruteforce'
        )
        print(f"   ✓ Protected ciphertext: {protected_result['ciphertext'][:40]}...")
        print(f"   ✓ Protection: {protected_result['protection_meta']['defense']}")
        
        print("\n🔓 Testing decryption with protection...")
        unprotected = EnhancedAffineCipher.decrypt_with_protection(
            protected_result,
            test_key
        )
        print(f"   ✓ Plaintext: {unprotected['plaintext']}")
        
        assert unprotected['plaintext'] == test_message, "Protected decryption failed!"
        print("   ✅ Protected affine test PASSED")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Affine test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_enhanced_playfair():
    """Test enhanced Playfair cipher"""
    print("\n" + "=" * 60)
    print("Testing Enhanced Playfair Cipher")
    print("=" * 60)
    
    test_message = "hello world"
    test_keyword = "playfair"
    
    try:
        print("\n📝 Testing Playfair encryption...")
        result = EnhancedPlayfairCipher.encrypt(test_message, test_keyword)
        print(f"   ✓ Ciphertext: {result['ciphertext']}")
        
        print("\n🔓 Testing Playfair decryption...")
        decrypted = EnhancedPlayfairCipher.decrypt(
            result['ciphertext'],
            test_keyword
        )
        print(f"   ✓ Plaintext: {decrypted['plaintext']}")
        
        # Note: Playfair may add padding, so we check if original is in decrypted
        assert test_message.replace(" ", "") in decrypted['plaintext'].replace(" ", ""), "Playfair decryption failed!"
        print("   ✅ Playfair test PASSED")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Playfair test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test full integration"""
    print("\n" + "=" * 60)
    print("Testing Full Integration")
    print("=" * 60)
    
    test_message = "This is a complete integration test!"
    test_key = "integrationKey"
    
    try:
        print("\n🔄 Testing: Message → Affine → Protection → Unprotection → Decrypt")
        
        # Step 1: Encrypt with affine
        cipher_result = EnhancedAffineCipher.chiffrement_affine(test_message, test_key)
        print(f"   ✓ Step 1: Affine encrypted")
        
        # Step 2: Apply protection
        protected, meta = apply_protection(cipher_result['ciphertext'], 'bruteforce')
        print(f"   ✓ Step 2: Protection applied ({meta['defense']})")
        
        # Step 3: Remove protection
        unprotected = remove_protection(protected, meta)
        print(f"   ✓ Step 3: Protection removed")
        
        # Step 4: Decrypt with affine
        final_result = EnhancedAffineCipher.dechiffrement_affine(unprotected, test_key)
        print(f"   ✓ Step 4: Affine decrypted")
        
        # Verify
        assert final_result['plaintext'] == test_message, "Integration test failed!"
        print(f"   ✓ Final plaintext: {final_result['plaintext']}")
        print("   ✅ Integration test PASSED")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Integration test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n🧪 Starting Cryptographic Protection System Tests\n")
    
    tests = [
        ("Protection Mechanisms", test_protection_mechanisms),
        ("Enhanced Affine Cipher", test_enhanced_affine),
        ("Enhanced Playfair Cipher", test_enhanced_playfair),
        ("Full Integration", test_integration)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
