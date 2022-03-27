# syntax=docker/dockerfile:1

FROM python:3.9

ENV HOME /app

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

CMD /wait && uvicorn main:app --host 0.0.0.0 --port 8000 --reload