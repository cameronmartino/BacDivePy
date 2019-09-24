.PHONY: test

test:
	nosetests -v bacdive --with-coverage --cover-package=bacdive
