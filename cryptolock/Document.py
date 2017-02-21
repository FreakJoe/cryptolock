from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary

base = declarative_base()

class Document(base):
	__tablename__ = 'documents'
	id = Column(Integer, primary_key=True)
	document_name = Column(String)
	document_content = Column(LargeBinary)