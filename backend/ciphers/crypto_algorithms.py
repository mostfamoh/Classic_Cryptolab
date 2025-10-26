"""
Classical cipher implementations for CryptoLab.
"""
import string
import numpy as np
from typing import Tuple, List


class CaesarCipher:
    """Caesar Cipher implementation."""
    
    @staticmethod
    def encrypt(plaintext: str, key: int, show_steps: bool = False) -> dict:
        """Encrypt text using Caesar cipher."""
        result = []
        shift = key % 26
        steps = []
        
        if show_steps:
            steps.append(f"1. Plaintext: {plaintext}")
            steps.append(f"2. Shift key: {key} (normalized to {shift})")
            steps.append(f"3. Encryption formula: E(x) = (x + {shift}) mod 26")
            steps.append("\n4. Character-by-character encryption:")
        
        for i, char in enumerate(plaintext):
            if char.isupper():
                old_pos = ord(char) - 65
                new_pos = (old_pos + shift) % 26
                new_char = chr(new_pos + 65)
                if show_steps:
                    steps.append(f"   '{char}' (pos {old_pos}) → ({old_pos} + {shift}) mod 26 = {new_pos} → '{new_char}'")
                result.append(new_char)
            elif char.islower():
                old_pos = ord(char) - 97
                new_pos = (old_pos + shift) % 26
                new_char = chr(new_pos + 97)
                if show_steps:
                    steps.append(f"   '{char}' (pos {old_pos}) → ({old_pos} + {shift}) mod 26 = {new_pos} → '{new_char}'")
                result.append(new_char)
            else:
                result.append(char)
                if show_steps:
                    steps.append(f"   '{char}' → '{char}' (unchanged)")
        
        ciphertext = ''.join(result)
        
        if show_steps:
            steps.append(f"\n5. Final ciphertext: {ciphertext}")
            return {"ciphertext": ciphertext, "steps": steps}
        else:
            return {"ciphertext": ciphertext}
    
    @staticmethod
    def decrypt(ciphertext: str, key: int, show_steps: bool = False) -> dict:
        """Decrypt text using Caesar cipher."""
        if show_steps:
            result = CaesarCipher.encrypt(ciphertext, -key, show_steps=True)
            result["plaintext"] = result.pop("ciphertext")
            result["steps"][0] = f"1. Ciphertext: {ciphertext}"
            result["steps"][2] = f"3. Decryption formula: D(x) = (x - {key}) mod 26"
            result["steps"][-1] = f"\n5. Final plaintext: {result['plaintext']}"
            return result
        else:
            result = CaesarCipher.encrypt(ciphertext, -key, show_steps=False)
            return {"plaintext": result["ciphertext"]}
    
    @staticmethod
    def get_info():
        """Get cipher information."""
        return {
            "name": "Caesar Cipher",
            "description": "A substitution cipher that shifts each letter by a fixed number of positions.",
            "key_type": "integer (0-25)",
            "weaknesses": [
                "Only 26 possible keys - easily brute forced",
                "Vulnerable to frequency analysis",
                "Preserves word patterns and lengths"
            ],
            "protection": [
                "Use more complex ciphers like Vigenère",
                "Combine with transposition",
                "Use modern encryption algorithms"
            ]
        }


class AffineCipher:
    """Affine Cipher implementation."""
    
    @staticmethod
    def _gcd(a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def _mod_inverse(a: int, m: int) -> int:
        """Calculate modular multiplicative inverse."""
        if AffineCipher._gcd(a, m) != 1:
            raise ValueError(f"No modular inverse exists for {a} and {m}")
        
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1
    
    @staticmethod
    def encrypt(plaintext: str, key_a: int, key_b: int, show_steps: bool = False) -> dict:
        """Encrypt text using Affine cipher."""
        if AffineCipher._gcd(key_a, 26) != 1:
            raise ValueError(f"Key 'a' ({key_a}) must be coprime with 26")
        
        steps = []
        if show_steps:
            steps.append(f"1. Plaintext: {plaintext}")
            steps.append(f"2. Key: a={key_a}, b={key_b}")
            steps.append(f"3. Encryption formula: E(x) = ({key_a}x + {key_b}) mod 26")
            steps.append("\n4. Character-by-character encryption:")
        
        result = []
        for char in plaintext:
            if char.isupper():
                x = ord(char) - 65
                encrypted = (key_a * x + key_b) % 26
                new_char = chr(encrypted + 65)
                if show_steps:
                    steps.append(f"   '{char}' (x={x}) → ({key_a}×{x} + {key_b}) mod 26 = {encrypted} → '{new_char}'")
                result.append(new_char)
            elif char.islower():
                x = ord(char) - 97
                encrypted = (key_a * x + key_b) % 26
                new_char = chr(encrypted + 97)
                if show_steps:
                    steps.append(f"   '{char}' (x={x}) → ({key_a}×{x} + {key_b}) mod 26 = {encrypted} → '{new_char}'")
                result.append(new_char)
            else:
                result.append(char)
                if show_steps:
                    steps.append(f"   '{char}' → '{char}' (unchanged)")
        
        ciphertext = ''.join(result)
        
        if show_steps:
            steps.append(f"\n5. Final ciphertext: {ciphertext}")
            return {"ciphertext": ciphertext, "steps": steps}
        else:
            return {"ciphertext": ciphertext}
    
    @staticmethod
    def decrypt(ciphertext: str, key_a: int, key_b: int, show_steps: bool = False) -> dict:
        """Decrypt text using Affine cipher."""
        if AffineCipher._gcd(key_a, 26) != 1:
            raise ValueError(f"Key 'a' ({key_a}) must be coprime with 26")
        
        a_inv = AffineCipher._mod_inverse(key_a, 26)
        
        steps = []
        if show_steps:
            steps.append(f"1. Ciphertext: {ciphertext}")
            steps.append(f"2. Key: a={key_a}, b={key_b}")
            steps.append(f"3. Calculate a^(-1) mod 26: {a_inv}")
            steps.append(f"4. Decryption formula: D(y) = {a_inv}(y - {key_b}) mod 26")
            steps.append("\n5. Character-by-character decryption:")
        
        result = []
        
        for char in ciphertext:
            if char.isupper():
                y = ord(char) - 65
                decrypted = (a_inv * (y - key_b)) % 26
                new_char = chr(decrypted + 65)
                if show_steps:
                    steps.append(f"   '{char}' (y={y}) → {a_inv}×({y} - {key_b}) mod 26 = {decrypted} → '{new_char}'")
                result.append(new_char)
            elif char.islower():
                y = ord(char) - 97
                decrypted = (a_inv * (y - key_b)) % 26
                new_char = chr(decrypted + 97)
                if show_steps:
                    steps.append(f"   '{char}' (y={y}) → {a_inv}×({y} - {key_b}) mod 26 = {decrypted} → '{new_char}'")
                result.append(new_char)
            else:
                result.append(char)
                if show_steps:
                    steps.append(f"   '{char}' → '{char}' (unchanged)")
        
        plaintext = ''.join(result)
        
        if show_steps:
            steps.append(f"\n6. Final plaintext: {plaintext}")
            return {"plaintext": plaintext, "steps": steps}
        else:
            return {"plaintext": plaintext}
    
    @staticmethod
    def get_info():
        """Get cipher information."""
        return {
            "name": "Affine Cipher",
            "description": "A substitution cipher using the formula E(x) = (ax + b) mod 26",
            "key_type": "two integers: 'a' (coprime with 26) and 'b' (0-25)",
            "weaknesses": [
                "Limited keyspace (312 valid keys)",
                "Vulnerable to frequency analysis",
                "Known-plaintext attack with 2 character pairs"
            ],
            "protection": [
                "Use polyalphabetic ciphers",
                "Increase alphabet size",
                "Use modern cryptographic algorithms"
            ]
        }


class HillCipher:
    """Hill Cipher implementation (2x2 or 3x3 matrix)."""
    
    @staticmethod
    def generate_matrix_from_key(key: str, size: int = 2) -> Tuple[np.ndarray, List[str]]:
        """
        Generate a Hill cipher matrix from a text key.
        
        Args:
            key: Text key (e.g., "HILL", "CRYPTO")
            size: Matrix size (2 or 3)
        
        Returns:
            Tuple of (matrix, steps for display)
        """
        steps = []
        steps.append(f"=== Generating {size}x{size} Matrix from Key ===")
        steps.append(f"1. Key text: '{key}'")
        
        # Convert key to uppercase and remove non-letters
        key = ''.join(c.upper() for c in key if c.isalpha())
        steps.append(f"2. Cleaned key: '{key}'")
        
        # Convert to numbers
        numbers = [ord(c) - 65 for c in key]
        steps.append(f"3. Convert to numbers (A=0, B=1, ...): {numbers}")
        
        # Need size*size numbers for matrix
        needed = size * size
        
        # Pad or trim to exact size
        if len(numbers) < needed:
            # Pad with sequential numbers starting from last number + 1
            last_num = numbers[-1] if numbers else 0
            for i in range(len(numbers), needed):
                numbers.append((last_num + i + 1) % 26)
            steps.append(f"4. Padded to {needed} numbers: {numbers}")
        elif len(numbers) > needed:
            numbers = numbers[:needed]
            steps.append(f"4. Trimmed to {needed} numbers: {numbers}")
        else:
            steps.append(f"4. Already have {needed} numbers")
        
        # Create matrix
        matrix = np.array(numbers).reshape(size, size)
        steps.append(f"5. Form {size}x{size} matrix:\n{matrix}")
        
        # Check if matrix is invertible
        det = int(np.round(np.linalg.det(matrix)))
        det_mod = det % 26
        steps.append(f"6. Calculate determinant: {det} (mod 26 = {det_mod})")
        
        # Check if determinant is coprime with 26
        import math
        gcd = math.gcd(det_mod, 26)
        steps.append(f"7. Check gcd({det_mod}, 26) = {gcd}")
        
        if gcd != 1:
            steps.append(f"⚠️ Matrix not invertible! gcd ≠ 1")
            steps.append(f"8. Adjusting matrix to make it invertible...")
            
            # Try adjusting diagonal elements
            for adjustment in range(1, 26):
                test_matrix = matrix.copy()
                test_matrix[0, 0] = (matrix[0, 0] + adjustment) % 26
                test_det = int(np.round(np.linalg.det(test_matrix)))
                test_det_mod = test_det % 26
                test_gcd = math.gcd(test_det_mod, 26)
                
                if test_gcd == 1:
                    matrix = test_matrix
                    det_mod = test_det_mod
                    steps.append(f"   Adjusted matrix[0,0] by +{adjustment}")
                    steps.append(f"   New matrix:\n{matrix}")
                    steps.append(f"   New determinant: {test_det} (mod 26 = {det_mod})")
                    steps.append(f"   gcd({det_mod}, 26) = {test_gcd} ✓")
                    break
        else:
            steps.append(f"✓ Matrix is invertible!")
        
        return matrix, steps
    
    @staticmethod
    def _matrix_mod_inv(matrix: np.ndarray, modulus: int) -> np.ndarray:
        """Calculate modular inverse of a matrix."""
        size = matrix.shape[0]
        det = int(np.round(np.linalg.det(matrix)))
        det = det % modulus
        
        # Find modular inverse of determinant
        det_inv = None
        for i in range(1, modulus):
            if (det * i) % modulus == 1:
                det_inv = i
                break
        
        if det_inv is None:
            raise ValueError("Matrix is not invertible in modular arithmetic")
        
        # Calculate adjugate matrix
        if size == 2:
            adj = np.array([[matrix[1, 1], -matrix[0, 1]], 
                            [-matrix[1, 0], matrix[0, 0]]])
        elif size == 3:
            # Calculate cofactor matrix
            cofactors = np.zeros((3, 3))
            for i in range(3):
                for j in range(3):
                    minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                    cofactors[i, j] = ((-1) ** (i + j)) * np.linalg.det(minor)
            adj = cofactors.T
        else:
            raise ValueError(f"Unsupported matrix size: {size}x{size}")
        
        # Calculate inverse
        inv = (det_inv * adj) % modulus
        return inv.astype(int)
    
    @staticmethod
    def _text_to_numbers(text: str) -> List[int]:
        """Convert text to list of numbers."""
        return [ord(char.upper()) - 65 for char in text if char.isalpha()]
    
    @staticmethod
    def _numbers_to_text(numbers: List[int]) -> str:
        """Convert list of numbers to text."""
        return ''.join(chr(num % 26 + 65) for num in numbers)
    
    @staticmethod
    def encrypt(plaintext: str, key_matrix, show_steps: bool = False) -> dict:
        """
        Encrypt text using Hill cipher with 2x2 or 3x3 matrix.
        
        Args:
            plaintext: Text to encrypt
            key_matrix: Either a List[List[int]] matrix or a string key
            show_steps: Whether to show encryption steps
        
        Returns:
            Dictionary with ciphertext and optional steps
        """
        steps = []
        
        # Check if key_matrix is a string (text key)
        if isinstance(key_matrix, str):
            if show_steps:
                steps.append("=== Step 1: Generate Matrix from Text Key ===")
            
            # Determine size based on key length
            key_len = len([c for c in key_matrix if c.isalpha()])
            size = 2 if key_len <= 4 else 3
            
            # Generate matrix from key
            key, matrix_steps = HillCipher.generate_matrix_from_key(key_matrix, size)
            
            if show_steps:
                steps.extend(matrix_steps)
                steps.append("\n=== Step 2: Encryption Process ===")
        else:
            # key_matrix is already a matrix
            key = np.array(key_matrix)
        
        size = key.shape[0]
        
        if key.shape[0] != key.shape[1] or size not in [2, 3]:
            raise ValueError(f"Key matrix must be 2x2 or 3x3, got {key.shape}")
        
        # Convert to numbers
        numbers = HillCipher._text_to_numbers(plaintext)
        original_length = len(numbers)
        
        # Pad if necessary
        while len(numbers) % size != 0:
            numbers.append(23)  # Add 'X'
        
        if show_steps:
            if not isinstance(key_matrix, str):
                steps.append(f"1. Key Matrix ({size}x{size}):\n{key}")
            steps.append(f"2. Plaintext: {plaintext}")
            steps.append(f"3. Convert to numbers (A=0, B=1, ...): {numbers}")
            if len(numbers) > original_length:
                steps.append(f"4. Padded with 'X' (23) to multiple of {size}: {numbers}")
        
        # Encrypt in blocks
        encrypted = []
        block_num = 1
        for i in range(0, len(numbers), size):
            block = np.array([[numbers[i + j]] for j in range(size)])
            result = np.dot(key, block) % 26
            encrypted_block = [int(result[j, 0]) for j in range(size)]
            encrypted.extend(encrypted_block)
            
            if show_steps:
                steps.append(f"\nBlock {block_num}:")
                steps.append(f"  Plaintext block: {[numbers[i + j] for j in range(size)]} = '{HillCipher._numbers_to_text([numbers[i + j] for j in range(size)])}'")
                steps.append(f"  Matrix multiplication:\n{key} × {block.T}\n  = {result.T}")
                steps.append(f"  Mod 26: {encrypted_block}")
                steps.append(f"  Ciphertext block: '{HillCipher._numbers_to_text(encrypted_block)}'")
                block_num += 1
        
        ciphertext = HillCipher._numbers_to_text(encrypted)
        
        if show_steps:
            steps.append(f"\nFinal ciphertext: {ciphertext}")
            return {"ciphertext": ciphertext, "steps": steps}
        else:
            return {"ciphertext": ciphertext}
    
    @staticmethod
    def decrypt(ciphertext: str, key_matrix, show_steps: bool = False) -> dict:
        """
        Decrypt text using Hill cipher.
        
        Args:
            ciphertext: Text to decrypt
            key_matrix: Either a List[List[int]] matrix or a string key
            show_steps: Whether to show decryption steps
        
        Returns:
            Dictionary with plaintext and optional steps
        """
        steps = []
        
        # Check if key_matrix is a string (text key)
        if isinstance(key_matrix, str):
            if show_steps:
                steps.append("=== Step 1: Generate Matrix from Text Key ===")
            
            # Determine size based on key length
            key_len = len([c for c in key_matrix if c.isalpha()])
            size = 2 if key_len <= 4 else 3
            
            # Generate matrix from key
            key, matrix_steps = HillCipher.generate_matrix_from_key(key_matrix, size)
            
            if show_steps:
                steps.extend(matrix_steps)
                steps.append("\n=== Step 2: Calculate Inverse Matrix ===")
        else:
            # key_matrix is already a matrix
            key = np.array(key_matrix)
        
        size = key.shape[0]
        
        if key.shape[0] != key.shape[1] or size not in [2, 3]:
            raise ValueError(f"Key matrix must be 2x2 or 3x3, got {key.shape}")
        
        # Get inverse key
        try:
            key_inv = HillCipher._matrix_mod_inv(key, 26)
        except ValueError as e:
            raise ValueError(f"Cannot decrypt: {str(e)}")
        
        if show_steps:
            if not isinstance(key_matrix, str):
                steps.append(f"1. Key Matrix ({size}x{size}):\n{key}")
            steps.append(f"Inverse Key Matrix:\n{key_inv}")
            
            # Show how inverse was calculated
            det = int(np.round(np.linalg.det(key)))
            det_mod = det % 26
            steps.append(f"Determinant: {det} (mod 26 = {det_mod})")
            
            # Find determinant inverse
            det_inv = None
            for i in range(1, 26):
                if (det_mod * i) % 26 == 1:
                    det_inv = i
                    break
            steps.append(f"Determinant inverse: {det_inv}")
            steps.append(f"Verification: ({det_mod} × {det_inv}) mod 26 = {(det_mod * det_inv) % 26}")
            
            steps.append(f"\n=== Step 3: Decryption Process ===")
            steps.append(f"Ciphertext: {ciphertext}")
        
        # Convert to numbers
        numbers = HillCipher._text_to_numbers(ciphertext)
        
        if show_steps:
            steps.append(f"Convert to numbers: {numbers}")
        
        # Decrypt in blocks
        decrypted = []
        block_num = 1
        for i in range(0, len(numbers), size):
            block = np.array([[numbers[i + j]] for j in range(size)])
            result = np.dot(key_inv, block) % 26
            decrypted_block = [int(result[j, 0]) for j in range(size)]
            decrypted.extend(decrypted_block)
            
            if show_steps:
                steps.append(f"\nBlock {block_num}:")
                steps.append(f"  Ciphertext block: {[numbers[i + j] for j in range(size)]} = '{HillCipher._numbers_to_text([numbers[i + j] for j in range(size)])}'")
                steps.append(f"  Matrix multiplication:\n{key_inv} × {block.T}\n  = {result.T}")
                steps.append(f"  Mod 26: {decrypted_block}")
                steps.append(f"  Plaintext block: '{HillCipher._numbers_to_text(decrypted_block)}'")
                block_num += 1
        
        plaintext = HillCipher._numbers_to_text(decrypted)
        
        if show_steps:
            steps.append(f"\nFinal plaintext: {plaintext}")
            return {"plaintext": plaintext, "steps": steps}
        else:
            return {"plaintext": plaintext}
    
    @staticmethod
    def get_info():
        """Get cipher information."""
        return {
            "name": "Hill Cipher (2x2 or 3x3)",
            "description": "A polygraphic substitution cipher using linear algebra and matrix multiplication",
            "key_type": "2x2 or 3x3 invertible matrix (modulo 26)",
            "weaknesses": [
                "Vulnerable to known-plaintext attack",
                "Matrix must be invertible (determinant coprime with 26)",
                "Requires exact multiple of block size",
                "Linear algebraic structure can be exploited"
            ],
            "protection": [
                "Use larger matrices (4x4, 5x5)",
                "Combine with transposition",
                "Use modern block ciphers like AES"
            ]
        }


class PlayfairCipher:
    """Playfair Cipher implementation."""
    
    @staticmethod
    def _create_matrix(key: str) -> Tuple[List[List[str]], dict]:
        """Create Playfair 5x5 matrix from key."""
        # Remove duplicates and create key string
        key = key.upper().replace('J', 'I')
        seen = set()
        key_chars = []
        
        for char in key:
            if char.isalpha() and char not in seen:
                seen.add(char)
                key_chars.append(char)
        
        # Add remaining letters
        for char in string.ascii_uppercase:
            if char != 'J' and char not in seen:
                key_chars.append(char)
        
        # Create 5x5 matrix
        matrix = [key_chars[i:i+5] for i in range(0, 25, 5)]
        
        # Create position dictionary
        positions = {}
        for i, row in enumerate(matrix):
            for j, char in enumerate(row):
                positions[char] = (i, j)
        
        return matrix, positions
    
    @staticmethod
    def _prepare_text(text: str) -> str:
        """Prepare text for Playfair encryption."""
        text = text.upper().replace('J', 'I')
        text = ''.join(char for char in text if char.isalpha())
        
        # Insert X between double letters
        prepared = []
        i = 0
        while i < len(text):
            prepared.append(text[i])
            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    prepared.append('X')
                else:
                    prepared.append(text[i + 1])
                    i += 1
            i += 1
        
        # Add padding if odd length
        if len(prepared) % 2 != 0:
            prepared.append('X')
        
        return ''.join(prepared)
    
    @staticmethod
    def encrypt(plaintext: str, key: str, show_steps: bool = False) -> dict:
        """Encrypt text using Playfair cipher."""
        matrix, positions = PlayfairCipher._create_matrix(key)
        text = PlayfairCipher._prepare_text(plaintext)
        
        steps = []
        if show_steps:
            steps.append(f"1. Key: {key}")
            steps.append(f"2. Playfair matrix:")
            for row in matrix:
                steps.append(f"   {' '.join(row)}")
            steps.append(f"\n3. Prepared text: {text}")
            steps.append("\n4. Digraph encryption:")
        
        result = []
        for i in range(0, len(text), 2):
            char1, char2 = text[i], text[i + 1]
            row1, col1 = positions[char1]
            row2, col2 = positions[char2]
            
            if row1 == row2:  # Same row
                enc1 = matrix[row1][(col1 + 1) % 5]
                enc2 = matrix[row2][(col2 + 1) % 5]
                if show_steps:
                    steps.append(f"   {char1}{char2} (same row) → {enc1}{enc2}")
                result.append(enc1)
                result.append(enc2)
            elif col1 == col2:  # Same column
                enc1 = matrix[(row1 + 1) % 5][col1]
                enc2 = matrix[(row2 + 1) % 5][col2]
                if show_steps:
                    steps.append(f"   {char1}{char2} (same column) → {enc1}{enc2}")
                result.append(enc1)
                result.append(enc2)
            else:  # Rectangle
                enc1 = matrix[row1][col2]
                enc2 = matrix[row2][col1]
                if show_steps:
                    steps.append(f"   {char1}{char2} (rectangle) → {enc1}{enc2}")
                result.append(enc1)
                result.append(enc2)
        
        ciphertext = ''.join(result)
        
        if show_steps:
            steps.append(f"\n5. Final ciphertext: {ciphertext}")
            return {"ciphertext": ciphertext, "steps": steps}
        else:
            return {"ciphertext": ciphertext}
    
    @staticmethod
    def decrypt(ciphertext: str, key: str, show_steps: bool = False) -> dict:
        """Decrypt text using Playfair cipher."""
        matrix, positions = PlayfairCipher._create_matrix(key)
        text = ciphertext.upper().replace('J', 'I')
        text = ''.join(char for char in text if char.isalpha())
        
        steps = []
        if show_steps:
            steps.append(f"1. Key: {key}")
            steps.append(f"2. Playfair matrix:")
            for row in matrix:
                steps.append(f"   {' '.join(row)}")
            steps.append(f"\n3. Ciphertext: {text}")
            steps.append("\n4. Digraph decryption:")
        
        result = []
        for i in range(0, len(text), 2):
            char1, char2 = text[i], text[i + 1]
            row1, col1 = positions[char1]
            row2, col2 = positions[char2]
            
            if row1 == row2:  # Same row
                dec1 = matrix[row1][(col1 - 1) % 5]
                dec2 = matrix[row2][(col2 - 1) % 5]
                if show_steps:
                    steps.append(f"   {char1}{char2} (same row) → {dec1}{dec2}")
                result.append(dec1)
                result.append(dec2)
            elif col1 == col2:  # Same column
                dec1 = matrix[(row1 - 1) % 5][col1]
                dec2 = matrix[(row2 - 1) % 5][col2]
                if show_steps:
                    steps.append(f"   {char1}{char2} (same column) → {dec1}{dec2}")
                result.append(dec1)
                result.append(dec2)
            else:  # Rectangle
                dec1 = matrix[row1][col2]
                dec2 = matrix[row2][col1]
                if show_steps:
                    steps.append(f"   {char1}{char2} (rectangle) → {dec1}{dec2}")
                result.append(dec1)
                result.append(dec2)
        
        plaintext = ''.join(result)
        
        if show_steps:
            steps.append(f"\n5. Final plaintext: {plaintext}")
            return {"plaintext": plaintext, "steps": steps}
        else:
            return {"plaintext": plaintext}
    
    @staticmethod
    def get_info():
        """Get cipher information."""
        return {
            "name": "Playfair Cipher",
            "description": "A digraph substitution cipher using a 5x5 matrix",
            "key_type": "keyword or phrase",
            "weaknesses": [
                "Frequency analysis on digraphs",
                "Known-plaintext attack possible",
                "I and J are treated as same letter"
            ],
            "protection": [
                "Use larger matrices (6x6 with full alphabet)",
                "Use modern encryption",
                "Combine with other techniques"
            ]
        }
