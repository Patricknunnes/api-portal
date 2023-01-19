FROM python:3

WORKDIR /app
COPY . .

RUN pip install "fastapi[all]" --no-cache-dir
RUN pip install "python-jose[cryptography]" --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8080
