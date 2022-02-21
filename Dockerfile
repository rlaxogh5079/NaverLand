FROM ubuntu:20.04

FROM python:3.9.7

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ENTRYPOINT ["dockerize", "-wait", "tcp://mysqlserver:3306", "-timeout", "20s"]
COPY requirements.txt ./
COPY . .

RUN pip install --upgrade pip
RUN pip install scrapy
RUN pip install pymysql

EXPOSE 3306