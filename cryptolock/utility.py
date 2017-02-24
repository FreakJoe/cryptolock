"""Provides utility functions"""

import random
import string

def random_string(length, pool=4):
    """Generates a random string of length length
    containing a variety of characters as specified by pool"""

    char_pool = string.letters
    if pool >= 2:
        char_pool += string.digits

    if pool >= 3:
        char_pool += string.punctuation

    if pool >= 4:
        char_pool += string.whitespace

    random_string_return = ''.join([random.choice(char_pool) for _ in range(length)])
    return random_string_return
