
test:
	pip install .
	python3 -m doctest  src/spectreapi/spectre.py
	pytest -v tests
	
lint:
	pylint src/spectre/spectre.py

distribution:
	rm -f dist/*
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*
	
