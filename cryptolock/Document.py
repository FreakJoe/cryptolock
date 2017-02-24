"""Provides the Document model"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary

BASE = declarative_base()

class Document(BASE): # pylint: disable=too-few-public-methods
    """Document model"""

    __tablename__ = 'documents'
    document_id = Column(Integer, primary_key=True)
    document_name = Column(String)
    document_content = Column(LargeBinary)
