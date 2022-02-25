cd ~/NaverLand

export CORTARNO=1168000000

docker run -d --name naver_land_crawler$CORTARNO --link mysqlserver naver_land_crawler

scrapy crawl RegionSpider

scrapy crawl NaverLandSpider



