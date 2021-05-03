FROM lambci/lambda:build-python3.8

WORKDIR /code

COPY . /code/

RUN mkdir -p /asset && \
	python -m pip install --upgrade pip && \
	pip install mangum uvicorn fastapi[all] requests>=2.19.1 pystac==0.5.6 jsonschema==3.2.0 click==7.1.2 -t /asset

RUN pip install /code -t /asset

RUN cp /code/cdk-deployment/lambda/lambda.py /asset/lambda.py

CMD ["echo", "hello world"]