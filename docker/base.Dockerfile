FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update \
    && apt -y install git wget unzip build-essential libcairo2-dev ffmpeg libsndfile1
