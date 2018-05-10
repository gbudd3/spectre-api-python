
test:
	pip install .
	pytest -v tests
	
doctest:
	python3 -m doctest  src/spectreapi/spectre.py

lint:
	pylint src/spectre/spectre.py

distribution:
	rm -f dist/*
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*
	
