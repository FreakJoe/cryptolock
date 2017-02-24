"""Test the SecureDatabase module"""

import unittest
import os

from cryptolock.SecureDatabase import SecureDatabase
from cryptolock.security import encrypt, decrypt
from cryptolock.exceptions import CryptoInvalidKeyException, CryptoInvalidMessageException, CryptoFalseKeyException
from config import TEST_DB_NAME, DATA_PATH

class TestSecureDatabase(unittest.TestCase):
    """Test the SecureDatabase module"""

    @classmethod
    def setUpClass(cls):
        """Creates a fresh test database"""

        if os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))):
            os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

        cls.sdb = SecureDatabase(TEST_DB_NAME)

    @classmethod
    def tearDownClass(cls):
        """"Closes the database connection and deletes the test database file"""

        cls.sdb.close()
        os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

    def test_init(self):
        """Test the SecureDatabase initialization"""

        self.assertTrue(os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))))

    def test_add_document(self):
        """Test the add_document method"""

        name = 'test_document_1'
        message = 'Test message 12345!'
        key = 'test_key_12345'
        
        self.assertTrue(self.sdb.add_document((name, message), key))
        self.assertEqual(self.sdb.get_document_content(name, key), message)

        # Invalid input
        self.assertFalse(self.sdb.add_document((name, 5), key))
        self.assertFalse(self.sdb.add_document((name, message, 5), key))
        self.assertFalse(self.sdb.add_document((name, 5), 644))

        with self.assertRaises(CryptoInvalidKeyException):
            self.assertFalse(self.sdb.add_document((name, message), ['th', 'br']))

    def test_update_document(self):
        """Test the update_document method"""

        name = 'test_document_2'
        message = 'Test message 54321!'
        new_message = 'Test message 135813!'
        key = 'test_key_54321'

        self.sdb.add_document((name, message), key)
        self.assertTrue(self.sdb.update_document((name, new_message), key))
        self.assertEqual(self.sdb.get_document_content(name, key), new_message)

    def test_get_document_content(self):
        """Test the get_document_content method"""

        name = 'test_document_3'
        message = 'Test message 12345!'
        key = 'test_key_54321'

        self.sdb.add_document((name, message), key)
        self.assertEqual(self.sdb.get_document_content(name, key), message)
