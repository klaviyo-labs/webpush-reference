FROM python:3.9.4-slim
 
WORKDIR /

ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app
