
test:
	python3 -m doctest  spectre.py
	python3 -m unittest unittest_spectre.py
	
verbosetest:
	python3 -m doctest  -v spectre.py

lint:
	pylint spectre.py
	
