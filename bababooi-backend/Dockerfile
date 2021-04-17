FROM python:3.8.9-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy over deps
COPY Pipfile Pipfile

# install deps
RUN pip install pipenv && \
    pipenv install

COPY src src
COPY data data