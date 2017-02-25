"""Provides an entry point for the application"""

from cryptolock.SecureDatabase import SecureDatabase
from cryptolock.commands import add, read
from cryptolock.exceptions import InvalidFileException, BinaryFileException, DocumentNotFoundException, CryptoFalseKeyException, CryptoInvalidKeyException, CryptoInvalidMessageException

def main():
    """Entry point for the application"""

    secure_database = SecureDatabase()
    commands = {
        1: ('Lock a file into the database.', add),
        2: ('Read a file from the database.', read)
    }

    print('Welcome to CryptoLock.')
    print('For instructions please check out https://github.com/FreakJoe/cryptolockpy.\n\n')
    for command in sorted(commands.items(), key=lambda t: t[0]):
        output = '{} - {}'.format(command[0], command[1][0])
        print(output)

    command = raw_input('\nPlease choose one of the following options by inputting the number in front:\n')

    # Try to call the function the user chose
    try:
        commands[int(command)][1](secure_database)

    except (KeyError, ValueError, InvalidFileException, BinaryFileException, DocumentNotFoundException, CryptoFalseKeyException, CryptoInvalidKeyException, CryptoInvalidMessageException) as ex:
        if type(ex).__name__ in [KeyError.__name__, ValueError.__name__]:
            print('Your choice was invalid.')

        elif type(ex).__name__ == InvalidFileException.__name__:
            print('The document or document name you\'ve specified is invalid.')

        elif type(ex).__name__ == BinaryFileException.__name__:
            print('The document you\'ve tried to save is a binary file. Please use only plain-text files.')

        elif type(ex).__name__ == DocumentNotFoundException.__name__:
            print('The document you\'ve tried to read was not found.')

        elif type(ex).__name__ == CryptoFalseKeyException.__name__:
            print('The password you\'ve specified was incorrect.')

        elif type(ex).__name__ == CryptoInvalidKeyException.__name__:
            print('The password you\'ve specified was invalid.')

        elif type(ex).__name__ == CryptoInvalidMessageException.__name__:
            print('The message you\'ve tried to read from or write to the database was invalid.')

        else:
            print('An unspecified error has occured. Please contact the developer on github.')
