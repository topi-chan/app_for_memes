FROM python:3.10.5-bullseye

ENV PYTHONBUFFERED=1

RUN apt-get update && apt-get install -y gcc python-dev
RUN apt-get install -y libpq-dev postgresql-client
RUN apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz


COPY requirements.txt .
COPY . ./app/

WORKDIR app

RUN pip install -U pip
RUN pip install -r ./requirements.txt

EXPOSE 5000
