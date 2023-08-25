FROM python:3

WORKDIR /app

COPY main.py /app/
RUN mkdir /app/keys

ENTRYPOINT ["python", "main.py"]
