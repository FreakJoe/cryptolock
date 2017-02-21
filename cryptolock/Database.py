from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, LargeBinary

class Database():
	def __init__(self):
		self.engine = create_engine('sqlite:///contents.db')

		from .File import base
		base.metadata.create_all(self.engine)

		self.session = sessionmaker(bind=self.engine)()