FROM python:3.10.2-slim-buster

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python crawler/CORTARNOS.py