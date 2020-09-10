FROM python:3.7
WORKDIR /stac_validator
COPY ./stac_validator .
RUN python stac_validator.py https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json --version v1.0.0-beta.2