FROM nvidia/cuda:12.0.0-cudnn8-devel-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev

RUN adduser --disabled-password --gecos '' celery_user
WORKDIR /celery

COPY requirements.txt .
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install gevent
COPY . .
USER celery_user

CMD ["celery", "-A", "tasks", "worker","--loglevel=info","-c","5","-P","gevent"]