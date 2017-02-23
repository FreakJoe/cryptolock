import unittest
import os

from cryptolock.Database import Database
from config import TEST_DB_NAME, DATA_PATH

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Create a fresh test database
        if os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))):
            os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

        self.db = Database(TEST_DB_NAME)

    @classmethod
    def tearDownClass(self):
        self.db.close()
        os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

    def test_init(self):
        self.assertTrue(os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))))

    def test_add_document(self):
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
        self.db.add_document(('test_document_5', 'test_content_5'))
        self.assertTrue(self.db.update_document(('test_document_5', 'new_test_content_5')))
        self.assertEqual(self.db.get_document_content('test_document_5'), 'new_test_content_5')

    def test_get_document_content(self):
        self.db.add_document(('test_document_6', 'test_content_6'))
        self.assertEqual(self.db.get_document_content('test_document_6'), 'test_content_6')
