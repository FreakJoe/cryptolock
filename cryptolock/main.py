"""Provides an entry point for the application"""

from cryptolock.SecureDatabase import SecureDatabase
from cryptolock.commands import add, read

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

    command = raw_input('\nPlease choose one of the following options by inputting the number in front: ')

    # Try to call the function the user chose
    try:
        commands[int(command)][1](secure_database)

    except (KeyError, ValueError):
        print('Your choice was invalid.')
