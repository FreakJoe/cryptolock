clean:
	if test -e "data/tests"; then \
		rm -r "data/tests"; \
	fi

test:
	nosetests -v