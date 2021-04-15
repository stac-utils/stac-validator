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

build-libraries:
	cd cdk-deployment/lambda-libraries && \
	docker build -f "Dockerfile" -t lambdalayer:latest .
	docker run -d -it --name lambdalayer lambdalayer:latest
	docker cp lambdalayer:libraries.zip ./cdk-deployment/lambda
	docker stop lambdalayer
	docker rm lambdalayer
	docker rmi lambdalayer

add-val:
	cp -r stac_validator cdk-deployment/lambda

build-cdk:
	make build-libraries
	make add-val

deploy-cdk:
	cd cdk-deployment && \
	cdk deploy

cdk-pipeline:
	make build-cdk
	cd cdk-deployment && \
	pip install -r requirements.txt && \
	cdk deploy

build-container:
	docker build -t stac_val .

run-container:
	docker container run -it stac_val /bin/bash