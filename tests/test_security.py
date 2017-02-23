import unittest
import random
import string

from cryptolock.security import ensure_key_validity, encrypt, decrypt

def random_string(length, pool=4):
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
	def test_encrypt_decrypt(self):
		"""Test a random string of length 100 containing all typical characters
		with a random key of length 16 containing alphanumeric characters
		to ensure the string is recovered after encryption and decryption"""
		for i in range(10):
			test_string = random_string(100)
			test_key = random_string(16, 2)
			self.assertEqual(decrypt(encrypt(test_string, test_key), test_key), test_string)

	def test_encrypt(self):
		self.assertFalse(encrypt('tooshort', 'somekey'))
		self.assertFalse(encrypt('definitelynottooshortthough', 'tooooooooooooooooooooooooolong'))
		self.assertFalse(encrypt('definitelynottooshortthough', ['not', 'really', 'a', 'key']))

	def test_decrypt(self):
		self.assertFalse(decrypt('tooshort', 'somekey'))
		self.assertFalse(decrypt('definitelynottooshortthough', 'tooooooooooooooooooooooooolong'))
		self.assertFalse(decrypt('definitelynottooshortthough', ['not', 'really', 'a', 'key']))

	def test_ensure_key_validity(self):
		self.assertEqual(ensure_key_validity('123456789'), '0000000123456789')

		self.assertFalse(ensure_key_validity('123456789123456789'))
		self.assertFalse(ensure_key_validity(12345678))
		self.assertFalse(ensure_key_validity(['12345678']))