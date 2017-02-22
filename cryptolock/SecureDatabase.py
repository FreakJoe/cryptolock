from cryptolock.Database import Database
from cryptolock.security import encrypt, decrypt, ensure_key_validity
from config import DB_NAME

class SecureDatabase():
	def __init__(self, db_name=DB_NAME):
		"""Initializes database object that will be used to store secure data"""

		self.db = Database(db_name)

	def close(self):
		"""Closes the session"""

		return self.db.close()

	def add_document(self, document, key):
		"""Encrypts a document's content and passes it on to be saved in the database"""

		# Ensure the document is supplied as a list or tuple of two strings: document name and document content
		if (not isinstance(document, tuple) and not isinstance(document, list)) or not len(document) == 2 or not isinstance(document[0], str) or not isinstance(document[1], str):
			return False

		# Ensure key validity
		key = ensure_key_validity(key)
		if not key:
			return False

		document_name = document[0]
		document_content = document[1]
		encrypted_document_content = encrypt(document_content, key)

		return self.db.add_document((document_name, encrypted_document_content))

	def update_document(self, document, key):
		"""Updates an existing document in the database"""

		# Ensure the document is supplied as a list or tuple of two strings: document name and document content
		if (not isinstance(document, tuple) and not isinstance(document, list)) or not len(document) == 2 or not isinstance(document[0], str) or not isinstance(document[1], str):
			return False

		# Ensure key validity
		key = ensure_key_validity(key)
		if not key:
			return False

		document_name = document[0]
		document_content = document[1]
		encrypted_document_content = encrypt(document_content, key)

		return self.db.update_document((document_name, encrypted_document_content))


	def get_document_content(self, document_name, key):
		"""Fetches a document's content from the database"""

		# Ensure key validity
		key = ensure_key_validity(key)
		if not key:
			return False

		document_content = self.db.get_document_content(document_name)
		if not document_content:
			return False

		return decrypt(document_content, key)