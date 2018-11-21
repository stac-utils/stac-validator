build_lambda:
	pip install . -t stac_validator_lambda
	chmod 755 stac_validator_lambda
	cd stac_validator_lambda;  zip -r ../stac_validator_lambda.zip *
