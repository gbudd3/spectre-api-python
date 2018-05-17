
test:
	pip install .
	pytest -v tests
	
doctest:
	python3 -m doctest src/spectreapi/*.py

lint:
	pylint src/spectreapi/*.py

distribution:
	rm -f dist/*
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*
	
