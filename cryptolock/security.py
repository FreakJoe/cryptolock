def encrypt(message, key):
	return message + key

def decrypt(message, key):
	return message[0:len(message) - len(key)]

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