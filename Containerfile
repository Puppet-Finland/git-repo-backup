FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY main.py /app/
RUN mkdir /app/keys

ENTRYPOINT ["python", "main.py"]
