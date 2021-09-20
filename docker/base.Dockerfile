FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update \
    && apt -y install git wget unzip build-essential libcairo2-dev ffmpeg libsndfile1 libpango1.0-dev
