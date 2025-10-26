"""
Enhanced cipher implementations with protection mechanisms.
"""

import random
import base64
import numpy as np
from typing import Dict, Tuple
from .protection import apply_protection, remove_protection


class EnhancedAffineCipher:
    """
    Affine cipher with CBC-like mode and IV for enhanced security.
    Works with full byte range (0-255) instead of just alphabet.
    """
    
    @staticmethod
    def chiffrement_affine(message: str, cle: str, T=2) -> Dict:
        """
        Encrypt message using enhanced affine cipher with CBC mode.
        
        Args:
            message: Plain text to encrypt
            cle: Secret key (string)
            T: Number of rounds (default: 2)
            
        Returns:
            dict with 'ciphertext' (base64) and encryption metadata
        """
        # Convert message to bytes
        message_octets = message.encode("utf-8")
        
        # Generate random IV (1 byte)
        iv = bytes([random.randint(0, 255)])
        
        # Generate parameters from key
        random.seed(cle)
        a_list = []
        b_list = []
        for i in range(T):
            a = random.choice([x for x in range(1, 256, 2)])  # odd numbers (coprime with 256)
            b = random.randint(0, 255)
            a_list.append(a)
            b_list.append(b)
        
        def affine(x, a, b):
            return (a * x + b) % 256
        
        # Encrypt with CBC mode
        message_chiffre = bytearray()
        prev = iv[0]
        
        for oct in message_octets:
            val = oct ^ prev  # XOR with previous ciphertext (CBC)
            for i in range(T):  # Apply T rounds
                val = affine(val, a_list[i], b_list[i])
            message_chiffre.append(val)
            prev = val
        
        # Return IV + ciphertext in base64
        full = iv + bytes(message_chiffre)
        ciphertext_b64 = base64.b64encode(full).decode("utf-8")
        
        return {
            "ciphertext": ciphertext_b64,
            "iv": iv.hex(),
            "rounds": T,
            "algorithm": "enhanced_affine"
        }
    
    @staticmethod
    def dechiffrement_affine(message_chiffre_b64: str, cle: str, T=2) -> Dict:
        """
        Decrypt message encrypted with enhanced affine cipher.
        
        Args:
            message_chiffre_b64: Base64 encoded ciphertext
            cle: Secret key (same as encryption)
            T: Number of rounds (must match encryption)
            
        Returns:
            dict with 'plaintext' and decryption metadata
        """
        # Decode from base64
        full = base64.b64decode(message_chiffre_b64)
        
        # Extract IV and ciphertext
        iv = full[0:1]
        ciphertext = full[1:]
        
        # Regenerate same parameters from key
        random.seed(cle)
        a_list = []
        b_list = []
        for i in range(T):
            a = random.choice([x for x in range(1, 256, 2)])
            b = random.randint(0, 255)
            a_list.append(a)
            b_list.append(b)
        
        def affine_inv(y, a, b):
            # Find modular inverse of a (mod 256)
            for i in range(1, 256):
                if (a * i) % 256 == 1:
                    a_inv = i
                    break
            return (a_inv * (y - b)) % 256
        
        # Decrypt with CBC mode
        textclair_octets = bytearray()
        prev = iv[0]
        
        for val in ciphertext:
            tmp = val
            # Reverse the rounds
            for i in reversed(range(T)):
                tmp = affine_inv(tmp, a_list[i], b_list[i])
            octet_clair = tmp ^ prev  # XOR with previous ciphertext
            textclair_octets.append(octet_clair)
            prev = val
        
        plaintext = textclair_octets.decode("utf-8", errors="ignore")
        
        return {
            "plaintext": plaintext,
            "algorithm": "enhanced_affine"
        }
    
    @staticmethod
    def encrypt_with_protection(plaintext: str, key: str, protection_type: str = 'bruteforce') -> Dict:
        """
        Encrypt with affine cipher and apply protection.
        
        Args:
            plaintext: Text to encrypt
            key: Encryption key
            protection_type: Type of attack to protect against
            
        Returns:
            dict with ciphertext and all metadata
        """
        # First encrypt with affine
        cipher_result = EnhancedAffineCipher.chiffrement_affine(plaintext, key)
        
        # Then apply protection
        protected_text, protection_meta = apply_protection(
            cipher_result['ciphertext'],
            protection_type
        )
        
        return {
            "ciphertext": protected_text,
            "cipher_meta": cipher_result,
            "protection_meta": protection_meta,
            "algorithm": "enhanced_affine_protected"
        }
    
    @staticmethod
    def decrypt_with_protection(protected_data: Dict, key: str) -> Dict:
        """
        Remove protection and decrypt affine cipher.
        
        Args:
            protected_data: Data from encrypt_with_protection
            key: Decryption key
            
        Returns:
            dict with plaintext
        """
        # Remove protection first
        cipher_text = remove_protection(
            protected_data['ciphertext'],
            protected_data['protection_meta']
        )
        
        # Then decrypt affine
        result = EnhancedAffineCipher.dechiffrement_affine(cipher_text, key)
        
        return result


class EnhancedPlayfairCipher:
    """
    Playfair cipher using numpy for matrix operations.
    """
    
    @staticmethod
    def encrypt(plaintext: str, keyword: str, show_steps: bool = False) -> Dict:
        """
        Encrypt using Playfair cipher.
        
        Args:
            plaintext: Text to encrypt
            keyword: Keyword for matrix generation
            show_steps: Whether to show encryption steps
            
        Returns:
            dict with ciphertext and optional steps
        """
        steps = []
        
        if show_steps:
            steps.append(f"1. Keyword: {keyword}")
            steps.append(f"2. Plaintext: {plaintext}")
        
        # Build 5x5 matrix
        final_keyword = ""
        for letter in keyword.lower():
            if letter not in final_keyword and letter.isalpha():
                final_keyword += letter
        
        matrix = [letter for letter in final_keyword]
        alphabet = [chr(i) for i in range(97, 123)]
        for letter in alphabet:
            if letter == 'j':
                continue
            elif letter not in matrix:
                matrix.append(letter)
        
        matrix = np.array(matrix).reshape(5, 5)
        
        if show_steps:
            steps.append(f"3. Matrix:\n{matrix}")
        
        # Prepare plaintext
        plaintext = plaintext.replace(" ", "").lower()
        plaintext_pair = []
        i = 0
        while i < len(plaintext):
            if i == len(plaintext) - 1:
                plaintext_pair.append(plaintext[i] + 'x')
                i += 1
            elif plaintext[i] == plaintext[i + 1]:
                plaintext_pair.append(plaintext[i] + "x")
                i += 1
            else:
                plaintext_pair.append(plaintext[i] + plaintext[i + 1])
                i += 2
        
        if show_steps:
            steps.append(f"4. Digraphs: {plaintext_pair}")
        
        # Encrypt
        textchiffre = ""
        for pair in plaintext_pair:
            pair_handled = False
            
            # Same row
            for row in range(5):
                row_current = matrix[row, :]
                if pair[0] in row_current and pair[1] in row_current:
                    first_letter = list(row_current).index(pair[0])
                    second_letter = list(row_current).index(pair[1])
                    textchiffre += matrix[row, (first_letter + 1) % 5]
                    textchiffre += matrix[row, (second_letter + 1) % 5]
                    pair_handled = True
                    break
            
            if pair_handled:
                continue
            
            # Same column
            for col in range(5):
                column_current = matrix[:, col]
                if pair[0] in column_current and pair[1] in column_current:
                    first_letter = list(column_current).index(pair[0])
                    second_letter = list(column_current).index(pair[1])
                    textchiffre += matrix[(first_letter + 1) % 5, col]
                    textchiffre += matrix[(second_letter + 1) % 5, col]
                    pair_handled = True
                    break
            
            if pair_handled:
                continue
            
            # Rectangle
            first_letter_cor = np.where(matrix == pair[0])
            second_letter_cor = np.where(matrix == pair[1])
            textchiffre += matrix[first_letter_cor[0][0], second_letter_cor[1][0]]
            textchiffre += matrix[second_letter_cor[0][0], first_letter_cor[1][0]]
        
        if show_steps:
            steps.append(f"5. Ciphertext: {textchiffre}")
            return {"ciphertext": textchiffre, "steps": steps}
        
        return {"ciphertext": textchiffre}
    
    @staticmethod
    def decrypt(ciphertext: str, keyword: str, show_steps: bool = False) -> Dict:
        """
        Decrypt using Playfair cipher.
        
        Args:
            ciphertext: Text to decrypt
            keyword: Keyword for matrix generation
            show_steps: Whether to show decryption steps
            
        Returns:
            dict with plaintext and optional steps
        """
        steps = []
        
        if show_steps:
            steps.append(f"1. Keyword: {keyword}")
            steps.append(f"2. Ciphertext: {ciphertext}")
        
        # Build matrix (same as encryption)
        final_keyword = ""
        for letter in keyword.lower():
            if letter not in final_keyword and letter.isalpha():
                final_keyword += letter
        
        matrix = [letter for letter in final_keyword]
        alphabet = [chr(i) for i in range(97, 123)]
        for letter in alphabet:
            if letter == 'j':
                continue
            elif letter not in matrix:
                matrix.append(letter)
        
        matrix = np.array(matrix).reshape(5, 5)
        
        # Prepare pairs
        ciphertext = ciphertext.replace(" ", "").lower()
        ciphertext_pair = []
        i = 0
        while i < len(ciphertext) - 1:
            ciphertext_pair.append(ciphertext[i] + ciphertext[i + 1])
            i += 2
        
        # Decrypt
        textclair = ""
        for pair in ciphertext_pair:
            pair_handled = False
            
            # Same row (subtract 1 instead of add)
            for row in range(5):
                row_current = matrix[row, :]
                if pair[0] in row_current and pair[1] in row_current:
                    first_letter = list(row_current).index(pair[0])
                    second_letter = list(row_current).index(pair[1])
                    textclair += matrix[row, (first_letter + 4) % 5]  # -1 mod 5 = +4 mod 5
                    textclair += matrix[row, (second_letter + 4) % 5]
                    pair_handled = True
                    break
            
            if pair_handled:
                continue
            
            # Same column (subtract 1 instead of add)
            for col in range(5):
                column_current = matrix[:, col]
                if pair[0] in column_current and pair[1] in column_current:
                    first_letter = list(column_current).index(pair[0])
                    second_letter = list(column_current).index(pair[1])
                    textclair += matrix[(first_letter + 4) % 5, col]
                    textclair += matrix[(second_letter + 4) % 5, col]
                    pair_handled = True
                    break
            
            if pair_handled:
                continue
            
            # Rectangle (same as encryption)
            first_letter_cor = np.where(matrix == pair[0])
            second_letter_cor = np.where(matrix == pair[1])
            textclair += matrix[first_letter_cor[0][0], second_letter_cor[1][0]]
            textclair += matrix[second_letter_cor[0][0], first_letter_cor[1][0]]
        
        # Remove padding
        text = ""
        i = 0
        while i < len(textclair):
            if i > 0 and i < len(textclair) - 1 and textclair[i] == 'x' and textclair[i - 1] == textclair[i + 1]:
                i += 1
            elif i == len(textclair) - 1 and textclair[i] == 'x':
                i += 1
            else:
                text += textclair[i]
                i += 1
        
        if show_steps:
            steps.append(f"3. Plaintext: {text}")
            return {"plaintext": text, "steps": steps}
        
        return {"plaintext": text}
