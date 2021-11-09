# syntax=docker/dockerfile:1
FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml /OnlineCompilerPython/ /templates/

RUN pip install poetry

RUN poetry install
