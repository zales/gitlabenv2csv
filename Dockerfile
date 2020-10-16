FROM python:3-slim

WORKDIR /code

RUN apt-get update && apt-get install -y gcc g++

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY gitlabenv2csv.py .

ENTRYPOINT [ "python", "./gitlabenv2csv.py" ]
