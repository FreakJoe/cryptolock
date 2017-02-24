"""Defines exceptions specific to this project"""

class CryptoBaseException(Exception):
    """Base exception to be inherited by other exceptions"""

    def __init__(self, value):
        """Set the exception's message and cause"""

        self.value = value

    def __str__(self):
        """Return a string representation of the exception"""

        return repr(self.value)

class CryptoInvalidKeyException(Exception):
    """Exception raised when an invalid key is supplied for encryption or decryption"""

    pass

class CryptoInvalidMessageException(Exception):
    """Exception raised when an invalid message is supplied for decryption"""

    pass

class CryptoFalseKeyException(Exception):
    """Exception raised when a false key is supplied for decryption"""

    pass

class BinaryFileException(Exception):
    """Exception raised when a false key is supplied for decryption"""

    pass

class InvalidFileException(Exception):
    """Exception raised when an invalid file is supplied for adding or reading"""

    pass

class DocumentNotFoundException(Exception):
    """Exception raised when an a document that is supposed to be read doesn't exist"""

    pass
