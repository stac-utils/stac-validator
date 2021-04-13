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
	cd lambda-libraries && \
	docker build -f "Dockerfile" -t lambdalayer:latest .
	docker run -d -it --name lambdalayer lambdalayer:latest
	docker cp lambdalayer:libraries.zip ./validator-cdk/lambda
	docker stop lambdalayer
	docker rm lambdalayer
	docker rmi lambdalayer

add-val:
	cp -r stac_validator validator-cdk/lambda

build-cdk:
	make build-libraries
	make add-val

deploy-cdk:
	cd validator-cdk && \
	cdk deploy