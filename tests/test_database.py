"""Tests the Database module"""

import unittest
import os

from cryptolock.Database import Database
from config import TEST_DB_NAME, DATA_PATH

class TestDatabase(unittest.TestCase):
    """Tests the Database module"""

    @classmethod
    def setUpClass(cls):
        """Creates a fresh test database"""

        # Create a fresh test database
        if os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))):
            os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

        cls.db = Database(TEST_DB_NAME)

    @classmethod
    def tearDownClass(cls):
        """"Closes the database connection and deletes the test database file"""

        cls.db.close()
        os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

    def test_init(self):
        """Tests the SecureDatabase initialization"""

        self.assertTrue(os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))))

    def test_add_document(self):
        """Tests the add_document method"""

        # Accept tuples
        self.assertTrue(self.db.add_document(('test_document_1', 'test_content_1')))
        # Accept lists
        self.assertTrue(self.db.add_document(['test_document_2', 'test_content_2']))
        # Accept only two-length-input: name and content
        self.assertFalse(self.db.add_document(('test_document_3', 'test_content_3', 'test')))
        # Accept only strings in the iterable
        self.assertFalse(self.db.add_document((4, ['bla'])))
        # Accept updating of values
        self.assertTrue(self.db.add_document(('test_document_1', 'new_test_content_1')))
        self.assertEqual(self.db.get_document_content('test_document_1'), 'new_test_content_1')

    def test_update_document(self):
        """Tests the update_document method"""

        self.db.add_document(('test_document_5', 'test_content_5'))
        self.assertTrue(self.db.update_document(('test_document_5', 'new_test_content_5')))
        self.assertEqual(self.db.get_document_content('test_document_5'), 'new_test_content_5')

    def test_get_document_content(self):
        """Tests the get_document_content method"""

        self.db.add_document(('test_document_6', 'test_content_6'))
        self.assertEqual(self.db.get_document_content('test_document_6'), 'test_content_6')
