upload:
	python3 -m build --sdist
	python3 -m build --wheel

	twine upload --verbose dist/*

test:
	twine upload --repository testpypi dist/*