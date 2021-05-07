FROM python:3.6

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "--bind", ":8000","wsgi:app"]
