FROM python:3.7

COPY ./server /app
COPY ./schema /app/api/schema
COPY ./pylib/graph_ql/__init__.py /app/api/

WORKDIR /app

RUN pip install -r requirements.txt

CMD uvicorn api:app --host 0.0.0.0
