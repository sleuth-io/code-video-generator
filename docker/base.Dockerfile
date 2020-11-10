FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update \
    && apt -y install git wget unzip build-essential libcairo2-dev ffmpeg

# Workaround until this is released: https://github.com/ManimCommunity/manim/issues/632
RUN pip uninstall pangocairocffi cairocffi \
    && pip install --no-binary :all: -U pangocairocffi --no-cache
