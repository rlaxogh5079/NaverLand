# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class NaverLandCrawlerItem(Item):
    
    _0atclNo = Field() # 건물 고유 번호

    _1company = Field() # 건물 건설사 이름

    _2place = Field() # 건물 위치
    
    _3price = Field() # 건물 가격 (예: 전세 9억, 전세 17억 등등)

    _4pyeong = Field() # 건물 평수
    
    _5fac = Field() # 건물 주변 편의시설 정보
