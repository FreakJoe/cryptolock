"""Provides the functionality for various commands chosen in the CLI"""

import os

from binaryornot.check import is_binary

from cryptolock.exceptions import InvalidFileException, BinaryFileException
from cryptolock.security import ensure_key_validity

def add(sdb, document=None, key=None):
    """Locks a document into the database"""

    if not document:
        # Input document
        pass

    if not isinstance(document, str):
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
        # Input key
        pass

    key = ensure_key_validity(key)
    return sdb.add_document((document_name, document_content), key)

def read(sdb, document_name=None, key=None):
    """Reads a document from the database"""

    if not document_name:
        # Input document
        pass

    if not isinstance(document_name, str):
        raise TypeError

    if not key:
        # Input key
        pass

    key = ensure_key_validity(key)
    return sdb.get_document_content(document_name, key)
