FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache postgresql-libs \
    && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    && apk add --no-cache mariadb-dev \
    && apk add --no-cache bash \
    && python -m pip install -r requirements.txt --no-cache-dir \
    && apk --purge del .build-deps

EXPOSE 8080
