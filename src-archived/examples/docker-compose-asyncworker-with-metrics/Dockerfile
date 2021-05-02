FROM python:3.8-alpine

WORKDIR /app
COPY metrics.py /app

RUN apk add --virtual .deps gcc g++ make openssl-dev libxml2 libffi-dev \
  && pip install async-worker

CMD ["python", "./metrics.py"]
