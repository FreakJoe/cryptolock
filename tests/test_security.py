import unittest

from cryptolock.security import ensure_key_validity, encrypt, decrypt

class TestSecurity(unittest.TestCase):
	def test_encrypt(self):
		pass
		
	def test_decrypt(self):
		pass

	def test_ensure_key_validity(self):
		self.assertEqual(ensure_key_validity('123456789'), '0000000123456789')

		self.assertFalse(ensure_key_validity('123456789123456789'))
		self.assertFalse(ensure_key_validity(12345678))
		self.assertFalse(ensure_key_validity(['12345678']))