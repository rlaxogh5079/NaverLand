from __future__ import unicode_literals
from naver_land_crawler.spiders.spider import CORTARNO
import pymysql,csv
from datetime import datetime

class NaverLandCrawlerPipeline:

    def __init__(self):
        self.db=pymysql.connect(host="mysqlserver",
                        user='', # 유저 이름 
                        password='', # 유저 비밀번호
                        charset='utf8',
                        port=3306) # 데이터 베이스에 host,user,password를 활용하여 접근

        self.cursor=self.db.cursor() # 데이터 베이스 커서 설정

        self.create_DB() # 데이터 베이스 생성

        self.create_TABLE() # 테이블 생성

    def create_DB(self): # 데이터 베이스를 생성하는 함수

        try:

            self.cursor.execute(f'''
                CREATE DATABASE NAVERHOUSES{CORTARNO}
            ''') # 데이터 베이스가 존재하지 않는다면 생성

        except:

            pass # 존재한다면 패스

        self.cursor.execute(f'''
            USE NAVERHOUSES{CORTARNO}
        ''') # HOUSEDB를 사용


    def create_TABLE(self): # 테이블을 생성하는 함수

        REGION_LIST = csv.reader(open('region.csv','r'))

        for region in REGION_LIST:

            try:

                self.cursor.execute(f'''
                    CREATE TABLE {region[0]}(
                    `atclNo` bigint UNSIGNED NOT NULL,
                    `company` varchar(30) DEFAULT NULL,
                    `location_detail` varchar(20) NOT NULL,
                    `sort` varchar(4) NOT NULL,
                    `deposit` int UNSIGNED NOT NULL,
                    `month_rent` smallint UNSIGNED DEFAULT NULL, 
                    `pyeong` smallint UNSIGNED NOT NULL,
                    `bus_dis` smallint UNSIGNED DEFAULT NULL,
                    `train_dis` smallint UNSIGNED DEFAULT NULL,
                    `conv_dis` smallint UNSIGNED DEFAULT NULL,
                    `mart_dis` smallint UNSIGNED DEFAULT NULL,
                    `laundry_dis` smallint UNSIGNED DEFAULT NULL,
                    `inserted_at` timestamp NOT NULL
                )''') # 테이블이 존재하지 않는다면 테이블 생성 

            except pymysql.err.OperationalError: # 테이블이 존재한다면 패스

                pass

    def process_item(self,item,spider):

        dong = item['_2place'][2]

        detail_location = dong + item['_2place'][3]

        sort = item['_3price'][0]

        deposit = item['_3price'][1]

        month_rent = item['_3price'][2]

        self.cursor.execute(f'''
            SELECT * FROM  {dong} WHERE atclNo = %s and inserted_at = %s''',
            (item['_0atclNo'],str(datetime.today())[:10])) # _0atclNo를 가진 데이터를 데이터베이스에서 추출

        result = self.cursor.fetchone() # SELECT 헀던 값을 return SELECT 값이 없으면 None을 Return

        if result == None: # 데이터가 존재하지않는다면

            self.cursor.execute(f'''INSERT INTO {dong}
            (atclNo, company, location_detail, sort, deposit, month_rent, pyeong, bus_dis, train_dis, conv_dis, mart_dis, laundry_dis, inserted_at) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (item['_0atclNo'],
            item['_1company'],
            detail_location, 
            sort, 
            deposit,
            month_rent, 
            item['_4pyeong'],
            item['_5fac'][0], 
            item['_5fac'][1],
            item['_5fac'][2],
            item['_5fac'][3], 
            item['_5fac'][4],
            int(str(datetime.today())[:10].replace('-',''))
            )) # 테이블에 데이터를 추가
        
            self.db.commit() # SQL 정보 업데이트

        else: # 존재한다면

            print('data already exist') # 데이터가 이미 존재한다 출력