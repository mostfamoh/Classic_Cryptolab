"""
Cryptanalysis attack implementations.
"""
from collections import Counter
from typing import List, Dict, Tuple
import numpy as np
from ciphers.crypto_algorithms import CaesarCipher, HillCipher


# English letter frequency (%)
ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}


class CaesarBruteForce:
    """Brute force attack on Caesar cipher."""
    
    @staticmethod
    def attack(ciphertext: str) -> List[Dict]:
        """Try all possible Caesar shifts."""
        results = []
        
        for shift in range(26):
            decrypted = CaesarCipher.decrypt(ciphertext, shift)
            score = CaesarBruteForce._score_text(decrypted)
            results.append({
                'shift': shift,
                'decrypted_text': decrypted,
                'score': score
            })
        
        # Sort by score (higher is better)
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    @staticmethod
    def _score_text(text: str) -> float:
        """Score text based on English letter frequency."""
        text = text.upper()
        total_letters = sum(1 for c in text if c.isalpha())
        
        if total_letters == 0:
            return 0
        
        score = 0
        counter = Counter(c for c in text if c.isalpha())
        
        for letter, count in counter.items():
            text_freq = (count / total_letters) * 100
            expected_freq = ENGLISH_FREQ.get(letter, 0)
            # Lower difference is better
            score -= abs(text_freq - expected_freq)
        
        return score


class FrequencyAnalysis:
    """Frequency analysis attack."""
    
    @staticmethod
    def analyze(text: str) -> Dict:
        """Perform frequency analysis on text."""
        text = text.upper()
        letters = [c for c in text if c.isalpha()]
        total = len(letters)
        
        if total == 0:
            return {
                'letter_frequencies': {},
                'most_common': [],
                'total_letters': 0,
                'english_comparison': {}
            }
        
        # Count frequencies
        counter = Counter(letters)
        frequencies = {letter: (count / total) * 100 for letter, count in counter.items()}
        
        # Get most common
        most_common = counter.most_common(10)
        
        # Compare with English
        english_comparison = {}
        for letter in frequencies:
            diff = abs(frequencies[letter] - ENGLISH_FREQ.get(letter, 0))
            english_comparison[letter] = {
                'text_freq': round(frequencies[letter], 2),
                'english_freq': ENGLISH_FREQ.get(letter, 0),
                'difference': round(diff, 2)
            }
        
        return {
            'letter_frequencies': {k: round(v, 2) for k, v in frequencies.items()},
            'most_common': [{'letter': letter, 'count': count, 'frequency': round((count/total)*100, 2)} 
                           for letter, count in most_common],
            'total_letters': total,
            'english_comparison': english_comparison,
            'chi_squared': FrequencyAnalysis._chi_squared(frequencies)
        }
    
    @staticmethod
    def _chi_squared(observed_freq: Dict[str, float]) -> float:
        """Calculate chi-squared statistic."""
        chi_sq = 0
        for letter in ENGLISH_FREQ:
            observed = observed_freq.get(letter, 0)
            expected = ENGLISH_FREQ[letter]
            if expected > 0:
                chi_sq += ((observed - expected) ** 2) / expected
        return round(chi_sq, 2)


class HillKnownPlaintextAttack:
    """Known-plaintext attack on Hill cipher (2x2)."""
    
    @staticmethod
    def attack(plaintext: str, ciphertext: str) -> Dict:
        """
        Attempt to recover Hill cipher key from known plaintext-ciphertext pairs.
        Requires at least 4 characters (2 pairs for 2x2 matrix).
        """
        # Clean text
        plaintext = ''.join(c.upper() for c in plaintext if c.isalpha())
        ciphertext = ''.join(c.upper() for c in ciphertext if c.isalpha())
        
        if len(plaintext) < 4 or len(ciphertext) < 4:
            return {
                'success': False,
                'error': 'Need at least 4 characters of plaintext and ciphertext'
            }
        
        if len(plaintext) != len(ciphertext):
            return {
                'success': False,
                'error': 'Plaintext and ciphertext must be same length'
            }
        
        try:
            # Convert to numbers
            plain_nums = [ord(c) - 65 for c in plaintext[:4]]
            cipher_nums = [ord(c) - 65 for c in ciphertext[:4]]
            
            # Create plaintext matrix P (2x2)
            P = np.array([[plain_nums[0], plain_nums[2]], 
                         [plain_nums[1], plain_nums[3]]])
            
            # Create ciphertext matrix C (2x2)
            C = np.array([[cipher_nums[0], cipher_nums[2]], 
                         [cipher_nums[1], cipher_nums[3]]])
            
            # Calculate P inverse mod 26
            P_inv = HillCipher._matrix_mod_inv(P, 26)
            
            # Key K = C * P^(-1) mod 26
            K = np.dot(C, P_inv) % 26
            
            # Verify the key by encrypting plaintext
            verification = HillCipher.encrypt(plaintext, K.tolist())
            
            success = verification == ciphertext
            
            return {
                'success': success,
                'recovered_key': K.tolist(),
                'verification': {
                    'original_ciphertext': ciphertext,
                    'encrypted_with_key': verification,
                    'match': success
                }
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Attack failed: {str(e)}'
            }


class AttackRecommendations:
    """Provide attack recommendations based on cipher type."""
    
    @staticmethod
    def get_recommendations(cipher_type: str) -> Dict:
        """Get attack strategies for a cipher type."""
        recommendations = {
            'caesar': {
                'attacks': [
                    {
                        'name': 'Brute Force',
                        'difficulty': 'Easy',
                        'description': 'Try all 26 possible shifts',
                        'time_complexity': 'O(n)',
                        'requirements': 'Only ciphertext needed'
                    },
                    {
                        'name': 'Frequency Analysis',
                        'difficulty': 'Easy',
                        'description': 'Compare letter frequencies with English',
                        'time_complexity': 'O(n)',
                        'requirements': 'Ciphertext of reasonable length'
                    }
                ],
                'protection': [
                    'Use longer keys (Vigenère)',
                    'Use polyalphabetic substitution',
                    'Use modern encryption'
                ]
            },
            'affine': {
                'attacks': [
                    {
                        'name': 'Brute Force',
                        'difficulty': 'Easy',
                        'description': 'Try all 312 valid key pairs',
                        'time_complexity': 'O(n)',
                        'requirements': 'Only ciphertext needed'
                    },
                    {
                        'name': 'Frequency Analysis',
                        'difficulty': 'Medium',
                        'description': 'Use frequency to narrow down keys',
                        'time_complexity': 'O(n)',
                        'requirements': 'Ciphertext of reasonable length'
                    },
                    {
                        'name': 'Known Plaintext (2 chars)',
                        'difficulty': 'Easy',
                        'description': 'Solve linear equations with 2 known pairs',
                        'time_complexity': 'O(1)',
                        'requirements': '2 plaintext-ciphertext pairs'
                    }
                ],
                'protection': [
                    'Use larger alphabet',
                    'Use polyalphabetic substitution',
                    'Combine with transposition'
                ]
            },
            'hill': {
                'attacks': [
                    {
                        'name': 'Known Plaintext',
                        'difficulty': 'Medium',
                        'description': 'Recover key matrix from known pairs',
                        'time_complexity': 'O(n³)',
                        'requirements': '4 plaintext-ciphertext pairs for 2x2'
                    },
                    {
                        'name': 'Frequency Analysis (limited)',
                        'difficulty': 'Hard',
                        'description': 'Works on digraphs, not single letters',
                        'time_complexity': 'O(n²)',
                        'requirements': 'Large amount of ciphertext'
                    }
                ],
                'protection': [
                    'Use larger matrices (3x3, 4x4)',
                    'Change keys frequently',
                    'Combine with other ciphers'
                ]
            },
            'playfair': {
                'attacks': [
                    {
                        'name': 'Frequency Analysis (digraphs)',
                        'difficulty': 'Hard',
                        'description': 'Analyze digraph frequencies',
                        'time_complexity': 'O(n²)',
                        'requirements': 'Large amount of ciphertext'
                    },
                    {
                        'name': 'Known Plaintext',
                        'difficulty': 'Medium',
                        'description': 'Reconstruct matrix from known pairs',
                        'time_complexity': 'O(n²)',
                        'requirements': 'Several plaintext-ciphertext pairs'
                    }
                ],
                'protection': [
                    'Use 6x6 matrix (full alphabet)',
                    'Change keys frequently',
                    'Use modern encryption'
                ]
            }
        }
        
        return recommendations.get(cipher_type, {})
