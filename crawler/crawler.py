import requests
from CORTARNOS import CORTARNOS

CON_URL = "https://m.land.naver.com/cluster/ajax/articleList?rletTpCd=APT&tradTpCd=all&z=9&cortarNo={}&page={}"

def get_item():
    for CORTARNO in CORTARNOS:
        page = 1
        while True:
            request_url = CON_URL.format(CORTARNO, page)
