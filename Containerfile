FROM python:3

WORKDIR /app

COPY main.py /app/
COPY keys /app/keys/
COPY config.ini /app/config.ini

ENTRYPOINT ["python", "main.py"]
