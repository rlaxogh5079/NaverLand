FROM python:3.10.2-slim-buster

COPY . .

RUN pip install --upgrade pip
RUN pip install scrapy
RUN pip install pymysql

ENTRYPOINT ["/bin/sh","scrapy.sh"]