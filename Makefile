compile:
	pyinstaller run.py --clean --onefile --name=CryptoLock
	
test:
	nosetests -v