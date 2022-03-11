FROM python:3.8-slim-buster
WORKDIR /code
COPY . /code/

RUN pip install . && \
    stac-validator --help

ENTRYPOINT ["stac-validator"]
