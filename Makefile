install:
	pip install .

install-edit:
	pip install --editable .  

code-check:
	pre-commit install
	pre-commit autoupdate
	pre-commit run --all-files

test:
	pytest --verbose
