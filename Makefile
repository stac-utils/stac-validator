install:
	pip install .

code-check:
	pre-commit install
	pre-commit autoupdate
	pre-commit run --all-files

test:
	pytest --verbose
