# syntax=docker/dockerfile:1

# FROM python:3.8-slim-buster
FROM ufoym/deepo:pytorch-py36-cpu

# WORKDIR /

# COPY requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "test.py"]