import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, LargeBinary

from .Document import Document
from ..config import DATA_PATH, DB_NAME

class Database():
	def __init__(self, db_name=DB_NAME):
		"""Initialize the database file and create all tables"""

		# Ensure the data directory exists
		if not os.path.exists(DATA_PATH):
			os.makedirs(DATA_PATH)

		self.engine = create_engine('sqlite:///{}.db'.format(os.path.join(DATA_PATH, db_name)))

		from .Document import base
		base.metadata.create_all(self.engine)

		self.session = sessionmaker(bind=self.engine)()

	def add_document(self, document):
		"""Stores a document of format (document_name, document_content) in the database. 
		If the document is new,	a database entry is added, otherwise the existing entry is updated."""

		# Ensure the document is supplied as a list or tuple of two strings: document name and document content
		if (not isinstance(document, tuple) and not isinstance(document, list)) or not len(document) == 2 or not isinstance(document[0], str) or not isinstance(document[1], str):
			return False

		document_name = document[0]
		document_content = document[1]
		document_in_db = self.session.query(Document).filter(Document.document_name == document_name).first()
		# If the document doesn't already exist
		if not document_in_db:
			# Add entry to the database
			new_document = Document()
			new_document.document_name = document_name
			new_document.document_content = document_content
			self.session.add(new_document)
			self.session.commit()

		# If the document does already exist
		else:
			# Update instead of adding new entry
			return self.update_document(document)

		return True

	def update_document(self, document):
		"""Updates an existing document in the database"""

		# Ensure the document is supplied as a list or tuple of two strings: document name and document content
		if (not isinstance(document, tuple) and not isinstance(document, list)) or not len(document) == 2 or not isinstance(document[0], str) or not isinstance(document[1], str):
			return False

		document_name = document[0]
		document_content = document[1]
		document_in_db = session.query(Document).filter(Document.document_name == document_name).first()
		if document_in_db:
			document_in_db.file_content = document_content
			self.session.commit()

		else:
			return False

		return True

	def get_document_content(self, document_name):
		"""Fetches a document's content from the database"""

		# Ensure the document name supplied is a string
		if not isinstance(document_name, str):
			return False

		document_in_db = session.query(Document).filter(Document.document_name == document_name).first()
		if not document_in_db:
			return False

		return document_in_db.document_content