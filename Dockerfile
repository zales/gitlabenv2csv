FROM python:3

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY gitlabenv2csv.py .

CMD [ "python", "./gitlabenv2csv.py" ]
