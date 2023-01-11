FROM python:3.9.7-alpine

RUN apk update
RUN apk add gcc python3-dev postgresql-dev musl-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY app.py app.py
COPY .env .env
COPY dictionary/ dictionary/

CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0"]