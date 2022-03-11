help:			## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:		## Install using pip
	pip install .

install-edit:		## Install using pip in edit mode
	pip install --editable .["test"]

code-check:		## Check and format code using pre-commit
	pre-commit install
	pre-commit autoupdate
	pre-commit run --all-files

test:			## Run the tests
	pytest --verbose
	pytest --mypy stac-validator

build-docker:		## Build a Docker container
	docker build -t stac-validator .

build-tox:		## Test stac_validator on multiple Python versions
	docker build -f tox/Dockerfile-tox -t stac_tox .

run:			## Run the Docker Container and enter into bash
	docker run -it --entrypoint /bin/bash stac-validator
