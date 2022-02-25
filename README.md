## Scrapy -> Naver Land

네이버 부동산 정보를 Scrapy와 Docker를 활용하여 MySQL에 저장하는 코드입니다. (작업환경 : WSL - Ubuntu)

### 기본 설정

```
$ cd ~

$ git clone https://github.com/rlaxogh5079/NaverLand

$ cd ~/NaverLand

$ mkdir data

$ sudo cp -r /var/lib/mysql ~/NaverLand/data

pipelines.py 파일에서 11번째 줄에 password = 에 mysql Root Password를 입력합니다.

scrapy.sh파일 3번째 줄에 크롤링을 원하는 지역의 고유번호를 적으세요.(기본값 : 1168000000)

https://new.land.naver.com/api/regions/list?cortarNo=0000000000

각 지역의 고유번호를 알기 위해서는 위 사이트로 들어가 cortarNo를 계속 바꿔가며 확인하실 수 있습니다.
```

### Docker 실행

```
$ docker run --name mysqlserver -e LC_ALL=C.UTF-8 -e TZ=Asia/Seoul -v ~/NaverLand/data/mysql:/var/lib/mysql -d -p 3306:3306 mysql:8.0.28

우선 위 코드를 작성하여 mysql을 실행시킵니다.

$ docker exec -it mysqlserver mysql -u root -p
Enter password:

실행 되었다면, 위 코드를 입력하고 기존 MySQL의 비밀번호를 입력해 mysql에 진입합니다.

mysql> create user 계정ID@'%' identified by '계정비밀번호' ;

mysql> grant all privileges on *.* to 계정ID@'%' with grant option;

mysql> flush privileges;

위 코드를 작성한 후 생성한 ID를 pipelines.py파일 10번째 줄에 user=''에 적습니다.

Docker를 실행하기 위해서는 아래코드를 작성합니다.

$ cd ~/NaverLand

$ sudo docker build -t naver_land_crawler .

그 후 CodeRunner를 설치받고 버튼을 클릭해 scrapy.sh파일을 실행시켜 주시면 됩니다.

scrapy.sh 파일 5번째 줄에 docker run 명령어에서 --ip 프록시ip 를 넣는다면 ip를 우회하여 크롤링이 가능합니다.

예) docker run --ip 1.1.1.1 -d --name naver_land_crawler$CORTARNO --link mysqlserver naver_land_crawler
```