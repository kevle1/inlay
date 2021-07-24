FROM python:slim

ENV PYTHONDONTWRITEBYTECODE="1"
ENV PYTHONUNBUFFERED="1"

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r ./requirements.txt

COPY bot.py /app
COPY sites /app/sites
COPY util /app/util

CMD python3 bot.py
