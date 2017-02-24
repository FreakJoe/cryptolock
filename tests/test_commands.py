"""Tests the commands module"""

import unittest
import os

from cryptolock.commands import add, read
from cryptolock.exceptions import BinaryFileException
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

    def test_add(self):
        """Test the add function"""

        for test_file in self.test_files:
            if not test_file[1]:
                with self.assertRaises(BinaryFileException):
                    add(test_file[0])

            else:
                add(test_file[0])

    def test_read(self):
        """Test the read function"""

        for test_file in self.test_files:
            if test_file[1]:
                add(test_file[0])

                f = open(test_file[0], 'r')
                self.assertEqual(read(test_file[1]), f.read())
