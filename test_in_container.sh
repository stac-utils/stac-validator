#!/bin/sh

set -e

VALIDATOR_IMG_NAME=sparkgeo/stac-validator
VALIDATOR_TESTER_NAME=stac-validator-test

docker build -t $VALIDATOR_IMG_NAME .
docker run --rm --name $VALIDATOR_TESTER_NAME -d -v `pwd`/tests:/tests $VALIDATOR_IMG_NAME tail -f /dev/null
docker exec $VALIDATOR_TESTER_NAME pip install pytest coverage
docker exec $VALIDATOR_TESTER_NAME coverage run -m pytest tests
EXIT_CODE=$?
docker exec $VALIDATOR_TESTER_NAME coverage report
docker stop $VALIDATOR_TESTER_NAME

exit $EXIT_CODE