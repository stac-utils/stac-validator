install:
	pip install .

code-check:
	pre-commit install
	pre-commit update
	pre-commit run --all-files

test:
	pytest --mypy --cov --cov-report=html --verbose
