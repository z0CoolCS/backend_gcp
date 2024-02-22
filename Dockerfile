FROM python:3.10.6-buster

WORKDIR /app

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn app:app --host 0.0.0.0 --port $PORT