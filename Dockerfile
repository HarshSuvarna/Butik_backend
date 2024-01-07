FROM python:3.8.10-slim

WORKDIR /app

COPY . /app


RUN pip install -r requirements.txt

WORKDIR /app/src

CMD uvicorn main:app --port=8080 --host=0.0.0.0