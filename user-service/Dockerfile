FROM python:3.8-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install gcc -y &&\
    apt-get clean

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install -r ./requirements.txt

COPY ./app /app