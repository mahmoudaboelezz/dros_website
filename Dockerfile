FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && apt-get install build-essential
RUN pip install -r requirements.txt
COPY . /app

CMD python /app/website/manage.py runserver 0.0.0.0:8080