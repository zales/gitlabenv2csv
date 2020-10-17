FROM python:3-alpine

LABEL maintainer="o.zalesky@gmail.com"

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
    gcc \
    g++

COPY gitlabenv2csv ./gitlabenv2csv
COPY setup.py .
COPY README.md .

RUN python3 setup.py sdist bdist_wheel && \
    pip3 install dist/gitlabenv2csv-*.tar.gz

ENTRYPOINT [ "gitlabenv2csv" ]
