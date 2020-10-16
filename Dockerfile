FROM python:3-slim

LABEL maintainer="o.zalesky@gmail.com"

WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY gitlabenv2csv.py .

ENTRYPOINT [ "python", "./gitlabenv2csv.py" ]
