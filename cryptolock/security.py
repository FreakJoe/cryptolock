from Crypto.Cipher import AES
from Crypto import Random

def encrypt(message, key):
	"""AES-encrypts a message using the provided key"""

	if not ensure_message_validity(message):
		return False

	key = ensure_key_validity(key)
	if not key:
		return False

	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CFB, iv)
	message_encrypted = iv + cipher.encrypt(message)

	return message_encrypted

def decrypt(message, key):
	"""Decrypts an AES-encrypted message using the provided key"""

	if not ensure_message_validity(message):
		return False

	key = ensure_key_validity(key)
	if not key:
		return False

	# Retrieve the iv stored in the first AES.block_size places of the string
	iv = message[0:AES.block_size]
	# and the actual message stored in the remaining part of the string
	message = message[AES.block_size:]
	cipher = AES.new(key, AES.MODE_CFB, iv)
	message_decrypted = cipher.decrypt(message)

	return message_decrypted

def ensure_key_validity(key):
	# Ensure the key is a string
	if not isinstance(key, str):
		return False

	# Ensure byte-length is multiple of 16
	if len(key) < 16:
		key = key.zfill(16)

	elif len(key) > 16:
		return False

	return key

def ensure_message_validity(message):
	# Ensure the message is a string
	if not isinstance(message, str):
		return False

	# Ensure the message is longer than AES.block_size as it has to contain an iv of that length
	if not len(message) > AES.block_size:
		return False

	return True