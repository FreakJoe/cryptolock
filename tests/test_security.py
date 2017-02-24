"""Tests the security module"""

import unittest

from cryptolock.security import ensure_key_validity, encrypt, decrypt
from cryptolock.exceptions import CryptoInvalidKeyException, CryptoInvalidMessageException, CryptoFalseKeyException
from cryptolock.utility import random_string

class TestSecurity(unittest.TestCase):
    """Tests the security module"""

    def test_encrypt_decrypt(self):
        """Tests a random string of length 100 containing all typical characters
        with a random key of length 16 containing alphanumeric characters
        to ensure the string is recovered after encryption and decryption"""

        for _ in range(10):
            test_string = random_string(100)
            test_key = random_string(16, 2)
            false_test_key = random_string(16, 2)

            # Ensure proper encryption and decryption
            self.assertEqual(decrypt(encrypt(test_string, test_key), test_key), test_string)
            # Ensure hmac verification
            with self.assertRaises(CryptoFalseKeyException):
                decrypt(encrypt(test_string, test_key), false_test_key)

    def test_encrypt(self):
        """Tests the encrypt method"""

        test_string = random_string(100)

        with self.assertRaises(CryptoInvalidKeyException):
            encrypt(test_string, 'tooooooooooooooooooooooooolong')

        with self.assertRaises(CryptoInvalidKeyException):
            encrypt(test_string, ['not', 'really', 'a', 'key'])

    def test_decrypt(self):
        """Tests the decrypt method"""

        test_string = random_string(100)

        with self.assertRaises(CryptoInvalidMessageException):
            decrypt('tooshort', 'somekey')

        with self.assertRaises(CryptoInvalidKeyException):
            decrypt(test_string, 'tooooooooooooooooooooooooolong')

        with self.assertRaises(CryptoInvalidKeyException):
            decrypt(test_string, ['not', 'really', 'a', 'key'])

    def test_ensure_key_validity(self):
        """Tests the ensure_key_validity method"""

        self.assertEqual(ensure_key_validity('123456789'), '0000000123456789')
        with self.assertRaises(CryptoInvalidKeyException):
            ensure_key_validity('123456789123456789')

        with self.assertRaises(CryptoInvalidKeyException):
            ensure_key_validity(12345678)

        with self.assertRaises(CryptoInvalidKeyException):
            ensure_key_validity(['12345678'])
