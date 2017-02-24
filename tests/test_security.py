"""Test the security module"""

import unittest
import random
import string

from cryptolock.security import ensure_key_validity, encrypt, decrypt
from cryptolock.exceptions import CryptoInvalidKeyException, CryptoInvalidMessageException, CryptoFalseKeyException

def random_string(length, pool=4):
    """Generate a random string of length length
    containing a variety of characters as specified by pool"""

    char_pool = string.letters
    if pool >= 2:
        char_pool += string.digits

    if pool >= 3:
        char_pool += string.punctuation

    if pool >= 4:
        char_pool += string.whitespace

    random_string = ''.join([random.choice(char_pool) for i in range(length)])
    return random_string

class TestSecurity(unittest.TestCase):
    """Test the security module"""

    def test_encrypt_decrypt(self):
        """Test a random string of length 100 containing all typical characters
        with a random key of length 16 containing alphanumeric characters
        to ensure the string is recovered after encryption and decryption"""

        for i in range(10):
            test_string = random_string(100)
            test_key = random_string(16, 2)
            false_test_key = random_string(16, 2)

            # Ensure proper encryption and decryption
            self.assertEqual(decrypt(encrypt(test_string, test_key), test_key), test_string)
            # Ensure hmac verification
            with self.assertRaises(CryptoFalseKeyException):
                self.assertFalse(decrypt(encrypt(test_string, test_key), false_test_key))

    def test_encrypt(self):
        """Test the encrypt method"""

        test_string = random_string(100)

        with self.assertRaises(CryptoInvalidKeyException):
            self.assertFalse(encrypt(test_string, 'tooooooooooooooooooooooooolong'))

        with self.assertRaises(CryptoInvalidKeyException):
            self.assertFalse(encrypt(test_string, ['not', 'really', 'a', 'key']))

    def test_decrypt(self):
        """Test the decrypt method"""

        test_string = random_string(100)

        with self.assertRaises(CryptoInvalidMessageException):
            self.assertFalse(decrypt('tooshort', 'somekey'))

        with self.assertRaises(CryptoInvalidKeyException):
            self.assertFalse(decrypt(test_string, 'tooooooooooooooooooooooooolong'))

        with self.assertRaises(CryptoInvalidKeyException):
            self.assertFalse(decrypt(test_string, ['not', 'really', 'a', 'key']))

    def test_ensure_key_validity(self):
        """Test the ensure_key_validity method"""

        self.assertEqual(ensure_key_validity('123456789'), '0000000123456789')

        self.assertFalse(ensure_key_validity('123456789123456789'))
        self.assertFalse(ensure_key_validity(12345678))
        self.assertFalse(ensure_key_validity(['12345678']))
