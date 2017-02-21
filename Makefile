clean:
	if test -e "data/tests"; then \
		rm -r "data/tests"; \
	fi

compile:
	pyinstaller run.py --clean --onefile --name=CryptoLock
	
test:
	nosetests -v