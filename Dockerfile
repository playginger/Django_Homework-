FROM python:3

WORKDIR /well

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
