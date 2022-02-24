cd ~/NaverLand

CORTARNO=$(<~/NaverLand/naver_land_crawler/spiders/CORTARNO.txt)

docker run -d --name naver_land_crawler$CORTARNO --link mysqlserver naver_land_crawler

scrapy crawl RegionSpider

scrapy crawl NaverLandSpider