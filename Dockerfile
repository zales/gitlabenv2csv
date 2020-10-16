FROM python:3-alpine

LABEL maintainer="o.zalesky@gmail.com"

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
    gcc \
    g++

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY gitlabenv2csv.py .

ENTRYPOINT [ "python", "./gitlabenv2csv.py" ]
