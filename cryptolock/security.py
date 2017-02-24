"""Provides security-related functionality"""

import hmac
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto import Random

from cryptolock.exceptions import CryptoInvalidKeyException, CryptoInvalidMessageException, CryptoFalseKeyException

def encrypt(message, key):
    """AES-encrypts a message using the provided key"""

    ensure_message_validity(message, False)
    key = ensure_key_validity(key)

    init_vector = Random.new().read(AES.block_size)
    hmac_digest = hmac.new(key, message, sha256).hexdigest()
    cipher = AES.new(key, AES.MODE_CFB, init_vector)
    message_encrypted = init_vector + cipher.encrypt(message) + hmac_digest

    return message_encrypted

def decrypt(message, key):
    """Decrypts an AES-encrypted message using the provided key"""

    ensure_message_validity(message)
    key = ensure_key_validity(key)

    # Retrieve the initialization vector stored in the first AES.block_size places of the string
    init_vector = message[0:AES.block_size]
    # Retrieve the hmac digest stored in the last sha256.digest_size * 2 characters of the string
    real_hmac_digest = message[int(len(message) - sha256().digest_size * 2):]
    # and the actual message stored in the remaining part of the string
    message = message[AES.block_size:int(len(message) - sha256().digest_size * 2)]

    cipher = AES.new(key, AES.MODE_CFB, init_vector)
    message_decrypted = cipher.decrypt(message)

    # Ensure the correct key is used to decrypt
    hmac_digest = hmac.new(key, message_decrypted, sha256).hexdigest()
    if not hmac.compare_digest(real_hmac_digest, hmac_digest):
        raise CryptoFalseKeyException

    return message_decrypted

def ensure_key_validity(key):
    """Ensure a key is valid to be used in encryption or decryption"""

    # Ensure the key is a string
    if not isinstance(key, str):
        raise CryptoInvalidKeyException

    # Ensure key length is multiple of 16
    if len(key) < 32:
        key = key.zfill(32)

    elif len(key) > 32 or len(key) == 0:
        raise CryptoInvalidKeyException

    return key

def ensure_message_validity(message, ensure_proper_length=True):
    """Ensure a message is valid to be decrypted"""

    # Ensure the message is a string
    if not isinstance(message, str):
        raise CryptoInvalidMessageException

    # Ensure the message is longer than AES.block_size as it has to contain an initialization vector of that length
    # and sha256.digest_size * 2 as it has to contain a hmac of that size
    if not len(message) > AES.block_size + sha256().digest_size * 2 and ensure_proper_length:
        raise CryptoInvalidMessageException

    return True
