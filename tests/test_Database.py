import unittest
import os

from ..cryptolock.Database import Database
from ..config import TEST_DB_NAME, DATA_PATH

class TestDatabase(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))
		Database(TEST_DB_NAME)

	@classmethod
	def tearDownClass(self):
		os.remove(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME)))

	def test_init(self):
		self.assertTrue(os.path.exists(os.path.join(DATA_PATH, '{}.db'.format(TEST_DB_NAME))))