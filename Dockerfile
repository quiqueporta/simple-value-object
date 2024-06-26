FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONPATH="/app"

COPY ./requirements-test.txt /

RUN pip install --upgrade pip
RUN pip install -r /requirements-test.txt

COPY . /app
