FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    gcc
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

RUN apt-get install scrot -y
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app
COPY . .
RUN POETRY_VIRTUALENVS_CREATE=false /root/.local/bin/poetry install