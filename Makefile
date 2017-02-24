pip_install:
	pip install -r requirements.txt

compile:
	pyinstaller run.py --clean --onefile --name=CryptoLock
	
test:
	nosetests -v
	
lint:
	pylint cryptolock --max-line-length=240
	
lint_tests:
	pylint tests --max-line-length=240