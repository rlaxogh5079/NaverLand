from __future__ import unicode_literals
from naver_land_crawler.spiders.spider import CORTARNO
import pymysql
from datetime import datetime


class NaverLandCrawlerPipeline:

    def __init__(self):
        self.db = pymysql.connect(host="mysqlserver",
                                  user='',  # 유저 이름
                                  password='',  # 유저 비밀번호
                                  charset='utf8',
                                  port=3306)  # 데이터 베이스에 host,user,password를 활용하여 접근

        self.cursor = self.db.cursor()  # 데이터 베이스 커서 설정

        self.create_DB()  # 데이터 베이스 생성

        self.create_main_TABLE()  # distance 테이블 생성

        self.create_location_TABLE()  # location 테이블 생성

        self.create_price_TABLE()  # price 테이블 생성

    def create_DB(self):  # 데이터 베이스를 생성하는 함수

        try:

            self.cursor.execute(f'''
                CREATE DATABASE NAVERHOUSES{CORTARNO}
            ''')  # 데이터 베이스가 존재하지 않는다면 생성

        except:

            pass  # 존재한다면 패스

        self.cursor.execute(f'''
            USE NAVERHOUSES{CORTARNO}
        ''')  # HOUSEDB를 사용

    def create_main_TABLE(self):  # main 테이블을 생성하는 함수

        try:

            self.cursor.execute(f'''
                CREATE TABLE distance(
                `index` bigint UNSIGNED NOT NULL,
                `bus_dis` smallint UNSIGNED DEFAULT NULL,
                `train_dis` smallint UNSIGNED DEFAULT NULL,
                `conv_dis` smallint UNSIGNED DEFAULT NULL,
                `mart_dis` smallint UNSIGNED DEFAULT NULL,
                `laundry_dis` smallint UNSIGNED DEFAULT NULL,
            )''')  # 테이블이 존재하지 않는다면 테이블 생성

        except pymysql.err.OperationalError:  # 테이블이 존재한다면 패스

            pass

    def create_sub_TABLE(self):  # sub 테이블을 생성하는 함수

        try:

            self.cursor.execute(f'''
                CREATE TABLE sub(
                `atclNo` bigint UNSIGNED NOT NULL,
                `location` varchar(10) NOT NULL,
                `location_detail` varchar(20) NOT NULL
            )''')  # 테이블이 존재하지 않는다면 테이블 생성

        except pymysql.err.OperationalError:  # 테이블이 존재한다면 패스

            pass

    def create_월세_TABLE(self):  # 월세 테이블 생성하는 함수try:

        try:

            self.cursor.execute(f'''
                CREATE TABLE 월세(
                `atclNo` bigint UNSIGNED NOT NULL,
                `sort` varchar(4) NOT NULL,
                `deposit` smallint NOT NULL,
                `month_rent` smallint NOT NULL,
            )''')  # 테이블이 존재하지 않는다면 테이블 생성

        except pymysql.err.OperationalError:  # 테이블이 존재한다면 패스

            pass

    def create_전세_TABLE(self):

        try:

            self.cursor.execute(f'''
                `atclNo` bigint UNSIGNED NOT NULL,
                `sort` varchar(4) NOT NULL,
                `deposit` smallint NOT NULL
            ''')

        except:

            pass

    def create_매매_TABLE(self):

        try:

            self.cursor.execute(f'''
                `atclNo` bigint UNSIGNED NOT NULL,
                `sort` varchar(4) NOT NULL,
                `price` smallint NOT NULL
            ''')

        except:

            pass

    def process_item(self, item, spider):

        inserted_at = str(datetime.today())[:10]

        atclNo = item['_0atclNo']

        index = atclNo+inserted_at

        dong = item['_1place'][2]

        location = item['_1place'][:1]

        location_detail = dong + item['_1place'][3]

        sort = item['_2price'][0]

        deposit = item['_2price'][1]

        month_rent = item['_2price'][2]

        self.cursor.execute(f'''
            SELECT * FROM  {dong} WHERE index = {index}
            ''')  # index 값이 존재하는지 조회

        result = self.cursor.fetchone()  # SELECT 헀던 값을 return SELECT 값이 없으면 None을 Return

        if result == None:  # 데이터가 존재하지않는다면

            self.cursor.execute(f'''
            INSERT INTO main(index, 
                                bus_dis, 
                                train_dis, 
                                conv_dis, 
                                mart_dis, 
                                laundry_dis)
            values ({index}, 
                    {item['_4fac'][0]}, 
                    {item['_4fac'][1]}, 
                    {item['_4fac'][2]}, 
                    {item['_4fac'][3]}, 
                    {item['_4fac'][4]})''')  # 테이블에 데이터를 추가

            self.cursor.excute(f'''
                INSERT INTO sub(atclNo,
                                    sort,
                                    location,
                                    location_detail)
                values ({atclNo},
                        {sort},
                        {location},
                        {location_detail})
            ''')

            self.cursor.execute(f'''
            INSERT INTO 월세(atclNo,
                             sort,
                            deposit,
                            month_rent)
            values ({atclNo},
                    {sort},
                    {deposit},
                    {month_rent})
            ''')

            self.cursor.execute(f'''
            INSERT INTO 전세(atclNo,
                             sort,
                             deposit)
            values ({atclNo},
                    {sort},
                    {deposit})
            ''')

            self.cursor.execute(f'''
            INSERT INTO 매매(atclNo,
                             sort,
                            price)
            values ({atclNo},
                    {sort},
                    {deposit})
            ''')

            self.db.commit()  # SQL 정보 업데이트

        else:  # 존재한다면

            print('data already exist')  # 데이터가 이미 존재한다 출력
