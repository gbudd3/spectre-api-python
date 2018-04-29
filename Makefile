
test:
	python3 -m doctest  spectre.py
	
verbosetest:
	python3 -m doctest  -v spectre.py

lint:
	pylint spectre.py
	
