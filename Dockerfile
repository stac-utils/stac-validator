FROM python:3.8-buster
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt && \
    pip install . && \
    stac_validator --help
ENTRYPOINT ["stac_validator"]