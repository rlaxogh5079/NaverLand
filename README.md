## Scrapy -> Naver Land

네이버 부동산 정보를 Scrapy와 Docker를 활용하여 MySQL에 저장하는 코드입니다. (작업환경 : WSL - Ubuntu)

### 기본 설정

```
$ cd ~

$ git clone https://github.com/rlaxogh5079/NaverLand


pipelines.py 파일에서 11번째 줄에 password = 에 mysql 유저 비밀번호를 입력하시고,

docker-compose.yml 파일에서 34번째 줄에 MYSQL_ROOT_PASSWORD: 에 설정하실 비밀번호를 입력합니다.

```

### Docker 실행

```
Docker를 실행하기 위해서는 아래코드를 작성합니다.

$ cd ~/NaverLand

$ sudo docker-compose up -d --build

위 코드를 입력하여 Scrapy 코드를 Docker로 실행시킵니다.

$ docker exec -it mysqlserver mysql -u root -p 

위 코드를 입력하여 Docker의 MySQL에 접근할 수 있습니다.



spider.py파일에 있는 CORTARNO에 크롤링을 원하는 지역의 고유번호를 적으세요.(기본값 : 1168000000)

https://new.land.naver.com/api/regions/list?cortarNo=0000000000

각 지역의 고유번호를 알기 위해서는 위 사이트로 들어가 cortarNo를 계속 바꿔가며 확인하실 수 있습니다.

```
