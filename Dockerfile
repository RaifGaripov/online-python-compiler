# syntax=docker/dockerfile:1
FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN pip install poetry

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml ./

RUN poetry install
