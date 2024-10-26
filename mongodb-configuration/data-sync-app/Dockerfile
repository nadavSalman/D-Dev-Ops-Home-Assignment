# syntax=docker/dockerfile:1

# base python image for custom image
FROM python:3.9.13-slim-buster

# create working directory and install pip dependencies
WORKDIR /hello-py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy python project files from local to /hello-py image working directory
COPY . .


CMD ["python", "main.py"]