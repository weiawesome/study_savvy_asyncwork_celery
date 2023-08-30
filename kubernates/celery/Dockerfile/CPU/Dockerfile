FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev

RUN adduser --disabled-password --gecos '' celery_user
WORKDIR /celery

COPY ../../requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gevent torch torchaudio

RUN apt-get update && apt-get install -y ffmpeg

COPY ../.. .

USER celery_user

CMD ["celery", "-A", "tasks", "worker","--loglevel=info","-c","5","-P","gevent"]