import unittest
import os

from cryptolock.SecureDatabase import SecureDatabase
from cryptolock.security import encrypt, decrypt
from config import TEST_DB_NAME, DATA_PATH

class TestSecureDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Create a fresh test database
        if os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))):
            os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

        self.sdb = SecureDatabase(TEST_DB_NAME)

    @classmethod
    def tearDownClass(self):
        self.sdb.close()
        os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

    def test_init(self):
        self.assertTrue(os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))))

    def test_add_document(self):
        name = 'test_document_1'
        message = 'Test message 12345!'
        key = 'test_key_12345'
        
        self.assertTrue(self.sdb.add_document((name, message), key))
        self.assertEqual(self.sdb.get_document_content(name, key), message)

        # Invalid input
        self.assertFalse(self.sdb.add_document((name, 5), key))
        self.assertFalse(self.sdb.add_document((name, 5), 644))
        self.assertFalse(self.sdb.add_document((name, 5), ['th', 'br']))
        self.assertFalse(self.sdb.add_document((name, message, 5), key))

    def test_update_document(self):
        name = 'test_document_2'
        message = 'Test message 54321!'
        new_message = 'Test message 135813!'
        key = 'test_key_54321'

        self.sdb.add_document((name, message), key)
        self.assertTrue(self.sdb.update_document((name, new_message), key))
        self.assertEqual(self.sdb.get_document_content(name, key), new_message)

    def test_get_document_content(self):
        name = 'test_document_3'
        message = 'Test message 12345!'
        key = 'test_key_54321'

        self.sdb.add_document((name, message), key)
        self.assertEqual(self.sdb.get_document_content(name, key), message)