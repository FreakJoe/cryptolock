from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary

base = declarative_base()

class File(base):
	__tablename__ = 'files'
	id = Column(Integer, primary_key=True)
	file_name = Column(String)
	file_content = Column(LargeBinary)