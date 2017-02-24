"""Tests the commands module"""

import unittest
import os

from cryptolock.SecureDatabase import SecureDatabase
from cryptolock.commands import add, read
from cryptolock.utility import random_string
from cryptolock.exceptions import BinaryFileException, InvalidFileException
from tests import data

class TestCommands(unittest.TestCase):
    """Tests the commands module"""

    @classmethod
    def setUpClass(cls):
        """Sets the location of the test files"""

        cls.test_file_location = os.path.dirname(os.path.abspath(data.__file__))
        cls.test_file_extensions = [('cfg', True), ('docx', False), ('png', False), ('txt', True)]
        cls.test_files = []
        for test_file_extension in cls.test_file_extensions:
            test_file = os.path.join(cls.test_file_location, 'test.{}'.format(test_file_extension[0]))
            cls.test_files.append((test_file, test_file_extension[1]))
        cls.sdb = SecureDatabase('test')

    def test_add(self):
        """Test the add function"""

        key = random_string(16, 2)
        with self.assertRaises(InvalidFileException):
            add(self.sdb, ('not', 'a', 'string'), key)

        with self.assertRaises(InvalidFileException):
            add(self.sdb, 'file_that_doesn\'t_exist', key)

        for test_file in self.test_files:
            if not test_file[1]:
                with self.assertRaises(BinaryFileException):
                    add(self.sdb, test_file[0], key)

            else:
                add(self.sdb, test_file[0], key)

    def test_read(self):
        """Test the read function"""

        key = random_string(16, 2)
        for test_file in self.test_files:
            if test_file[1]:
                add(self.sdb, test_file[0], key)

                with open(test_file[0], 'r') as f:
                    self.assertEqual(read(self.sdb, test_file[1], key), f.read())
