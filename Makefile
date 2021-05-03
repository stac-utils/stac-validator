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
	pytest --mypy stac_validator

build:			## Build a Docker container
	docker build -t stac_validator:2.0.0 .

build-tox:		## Test stac_validator on multiple Python versions
	docker build -f tox/Dockerfile-tox -t stac_tox .

run:			## Run the Docker Container and enter into bash
	docker run -it --entrypoint /bin/bash stac_validator:2.0.0
