from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, LargeBinary
from Crypto.Cipher import AES
from Crypto import Random
from threading import Thread
import os
import sys
import signal
from time import sleep

engine = create_engine('sqlite:///contents.db')
base = declarative_base()

class File(base):
	__tablename__ = 'files'
	id = Column(Integer, primary_key=True)
	file_name = Column(String)
	file_content = Column(LargeBinary)

base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

def add_file(name, key):
	if len(key) != 16:
		print('Key needs to be 16 bytes')
		return

	file_content = open(name).read()
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CFB, iv)
	file_content_c = iv + cipher.encrypt(file_content)

	file_db = session.query(File).filter(File.file_name == name).first()
	if not file_db:
		new_file = File()
		new_file.file_name = name
		new_file.file_content = file_content_c
		session.add(new_file)
		session.commit()

	else:
		file_db.file_content = file_content_c
		session.commit()

def kill_file():
	global file_name
	if file_name:
		sleep(30)
		os.remove(file_name)
		file_name = None

def read_file(name, key):
	global file_name
	file_name = name
	file_db = session.query(File).filter(File.file_name == name).first()
	file_content = file_db.file_content
	iv = file_content[0:16]
	file_content = file_content[16:]

	cipher = AES.new(key, AES.MODE_CFB, iv)
	file_content_d = cipher.decrypt(file_content)

	print('file will be restored for 30 seconds')
	open(name, 'w').write(file_content_d)
	t = Thread(target=kill_file)
	t.start()

if sys.argv[1] == 'add':
	# python lock.py add file.txt THISISA16BYTEKEY THISISA16BYTEKEY
	if sys.argv[3] != sys.argv[4]:
		print('Make sure you confirm your key by typing it twice')

	add_file(sys.argv[2], sys.argv[3])

if sys.argv[1] == 'read':
	# python lock.py read file.txt THISISA16BYTEKEY
	read_file(sys.argv[2], sys.argv[3])