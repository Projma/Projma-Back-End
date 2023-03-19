# Pull base image
FROM python:3.10.2-slim-bullseye

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install --fix-missing build-essential libpq-dev python3-dev
# RUN apt-get -y install build-essential libssl-dev libpq-dev libffi-dev python3-dev

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .