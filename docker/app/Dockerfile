FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3.10 python3.10-dev python3-pip \
    ffmpeg libsm6 libxext6

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src/ /app/

RUN mkdir -p /app/media

CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "wsgi:app"]
