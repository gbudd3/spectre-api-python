
test:
	python3 -m doctest  src/spectre/spectre.py
	python3 -m unittest tests/unittest_spectre.py
	
verbosetest:
	python3 -m doctest  -v spectre.py
	python3 -m unittest -v unittest_spectre.py

lint:
	pylint src/spectre/spectre.py

distribution:
	python3 setup.py sdist bdist_wheel
	
