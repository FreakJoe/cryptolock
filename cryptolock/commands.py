"""Provides the functionality for various commands chosen in the CLI"""

import webbrowser
import os
import tempfile
import time

from binaryornot.check import is_binary

from cryptolock.exceptions import InvalidFileException, BinaryFileException
from cryptolock.security import ensure_key_validity

def add(sdb, document=None, key=None):
    """Locks a document into the database"""

    if not document:
        document = raw_input('\nPlease enter the relative or absolute path to the text file you\'d like to save:\n')

    if not isinstance(document, str) or document == '':
        raise InvalidFileException

    if not os.path.exists(document):
        raise InvalidFileException

    if is_binary(document):
        raise BinaryFileException

    document_name = os.path.basename(document)
    document_content = None
    with open(document, 'r') as document_file:
        document_content = document_file.read()

    if not document_content:
        raise InvalidFileException

    if not key:
        key = raw_input('\nPlease enter the password you would like to use to protect the file:\n')

    key = ensure_key_validity(key)
    success = sdb.add_document((document_name, document_content), key)

    if success:
        print('The document was successfully added to the database.')

    else:
        print('An unspecified error has occured. Please contact the developer on github.')

    return success

def read(sdb, document_name=None, key=None):
    """Reads a document from the database"""

    if not document_name:
        document_name = raw_input('\nPlease enter the name of the text file you\'d like to view:\n')

    if not isinstance(document_name, str) or document_name == '':
        raise InvalidFileException

    if not key:
        key = raw_input('\nPlease enter the password you specified to protect the file:\n')

    key = ensure_key_validity(key)
    document_content = sdb.get_document_content(document_name, key)
    if not document_content:
        print('An unspecified error has occured. Please contact the developer on github.')
        return False

    temp_document_name = None
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_document:
        temp_document.write(document_content)
        webbrowser.open(temp_document.name)
        temp_document_name = temp_document.name
    
    # Wait for the temp file to be opened before removing it
    time.sleep(.1)
    os.remove(temp_document_name)

    return True
