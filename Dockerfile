FROM python:3.6

WORKDIR /App

COPY requirements.txt /App
COPY api.py /App
COPY config.json /App

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["ls"]
CMD ["gunicorn", "--bind", ":5000","api:app"]

