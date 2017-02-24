"""Tests the SecureDatabase module"""

import unittest
import os

from cryptolock.SecureDatabase import SecureDatabase
from cryptolock.exceptions import CryptoInvalidKeyException
from cryptolock.utility import random_string
from config import TEST_DB_NAME, DATA_PATH

class TestSecureDatabase(unittest.TestCase):
    """Tests the SecureDatabase module"""

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
        """Tests the SecureDatabase initialization"""

        self.assertTrue(os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))))

    def test_add_document(self):
        """Tests the add_document method"""

        name = 'test_document_1'
        message = random_string(100)
        key = random_string(16, 2)

        self.assertTrue(self.sdb.add_document((name, message), key))
        self.assertEqual(self.sdb.get_document_content(name, key), message)

        # Invalid input
        self.assertFalse(self.sdb.add_document((name, 5), key))
        self.assertFalse(self.sdb.add_document((name, message, 5), key))
        self.assertFalse(self.sdb.add_document((name, 5), 644))

        with self.assertRaises(CryptoInvalidKeyException):
            self.assertFalse(self.sdb.add_document((name, message), ['th', 'br']))

    def test_update_document(self):
        """Tests the update_document method"""

        name = 'test_document_2'
        message = random_string(100)
        new_message = random_string(100)
        key = random_string(16, 2)

        self.sdb.add_document((name, message), key)
        self.assertTrue(self.sdb.update_document((name, new_message), key))
        self.assertEqual(self.sdb.get_document_content(name, key), new_message)

    def test_get_document_content(self):
        """Tests the get_document_content method"""

        name = 'test_document_3'
        message = random_string(100)
        key = random_string(16, 2)

        self.sdb.add_document((name, message), key)
        self.assertEqual(self.sdb.get_document_content(name, key), message)
