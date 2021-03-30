install:
	pre-commit install
	pip install .

code-check:
	pre-commit run --all-files

test:
	pytest --mypy --cov --cov-report=html --verbose
