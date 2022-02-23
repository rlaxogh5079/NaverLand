FROM python:3.9.7

COPY requirements.txt ./
COPY . .

RUN pip install --upgrade pip
RUN pip install scrapy
RUN pip install pymysql
ENTRYPOINT ["/bin/sh","scrapy.sh"]