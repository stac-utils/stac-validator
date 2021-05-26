FROM lambci/lambda:build-python3.8

WORKDIR /code

COPY . /code/

RUN mkdir -p /asset && \
	python -m pip install --upgrade pip && \
	pip install stac-validator mangum uvicorn fastapi[all] -t /asset --no-binary pydantic

# RUN pip install -e /code -t /asset
RUN ls
RUN cp /code/lambda.py /asset/

CMD ["lambda.handler"]