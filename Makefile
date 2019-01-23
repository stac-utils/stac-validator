build_lambda:
	cp -a stac_validator stac_validator_lambda/
	pip install -r stac_validator_lambda/lambda_requirements.txt -t stac_validator_lambda
	chmod 755 stac_validator_lambda
	cd stac_validator_lambda;  zip -r ../stac_validator_lambda.zip *
