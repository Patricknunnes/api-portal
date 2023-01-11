FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y libpq-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
