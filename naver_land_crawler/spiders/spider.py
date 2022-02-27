import scrapy
import json
import os
from scrapy import Request
from naver_land_crawler.items import NaverLandCrawlerItem

HOMECOUNT = 20  # API에서 제공하는 한 페이지에 존재하는 집의 개수

item = NaverLandCrawlerItem()  # item 변수 선언

# 지역 고유 번호 (예시 : 서울특별시 강남구 -> 1168000000)
CORTARNO = int(os.environ['CORTARNO'])

ORIGIN_URL = 'https://m.land.naver.com'


class NaverLandSpider(scrapy.Spider):

    name = "NaverLandSpider"

    naver_land_url = f'{ORIGIN_URL}/cluster/ajax/articleList?rletTpCd=APT&tradTpCd=A1%3AB1%3AB2&z=9&cortarNo={CORTARNO}&page=1'

    def start_requests(self):  # crawling이 시작될때 가장먼저 호출하는 함수

        yield Request(url=self.naver_land_url, callback=self.get_url, dont_filter=True)

    def get_url(self, response):  # crawl 대상 url을 모두 구하는 함수

        body = json.loads(response.text)['body']

        # =을 기준으로 스플릿 했을때 제일 뒤에 있는 수, 즉 페이지 현재 페이지 수
        page = response.url.split('=')[-1]

        if page == '1':

            # CORTARNO 가 유요한 번호인지 체크하는 테스트 코드
            assert len(body) != 0, f"{CORTARNO} is Empty Region!"

            # API서버의 구조가 바뀌어 한 페이지에서 제공하는 집의 정보의 개수가 변동됨을 감지하는 테스트코드
            assert len(body) == HOMECOUNT, "API changed! check HOMECOUNT!!"

        token = response.url.split('=')  # '='를 기준으로 나눔

        # token[-1] 의 값은 '='기준으로 나눴을때 가장 뒤에있는 수, 즉 페이지 수
        token[-1] = str(int(page) + 1)

        # string상태에서 값을 변경하기 어려움, 따라서 list형식으로 변환한 후, list의 값을 바꾼후 string값으로 변환
        url = '='.join(token)

        if len(body) == HOMECOUNT:  # 만약 페이지가 꽉 찼다면 다음페이지가 존재함

            # crawl 대상에 추가 한후 다음 페이지를 또 추가하기 위해서 재귀함수 형식으로 작성
            yield Request(url=url, callback=self.get_url, dont_filter=True)

            # 전에 추가했던 crawl 대상을 get_article함수에 전달
            yield Request(url=url, callback=self.get_article, dont_filter=True)

    def get_article(self, response):  # atclNo을 추출하기 위한 함수

        body = json.loads(response.text)['body']

        for count in range(len(body)):  # 집의 개수만큼 count

            # atclNo를 url로 전달, 기본적인 정보를 얻기 위한 url
            yield Request(url=f"{ORIGIN_URL}/article/info/{body[count]['atclNo']}?newMobile", callback=self.get_information, dont_filter=True)

            # 경도와 위도를 url로 전달, fac요소를 추출하기 위한 url
            yield Request(url=f'{ORIGIN_URL}/mobile/api/mobile/articles/facilitiesTransInfo?lat={body[count]["lat"]}&lng={body[count]["lng"]}', callback=self.get_fac, dont_filter=True)

    def get_information(self, response):

        item['_0atclNo'] = int(response.url.split(
            '/')[-1][:-10])  # 해당 건물의 고유 번호를 url을 통해서 추출

        item['_1place'] = response.xpath('//*[@id="content"]').css('div > div').xpath(
            '//*[@class="detail_location"]/div[2]/em/text()')[0].extract().split(' ')  # 장소를 Xpath와 Css Selector를 통해 추출

        # 가격을 Xpath와 Css Selector를 통해 추출
        price = response.xpath(
            '//*[@id="detailMy--fixed"]').css('::text').getall()

        # 만원이라는 키워드가 추가적으로 따라옴, xpath와 css를 바꾸기 보다는 remove를 통해서 삭제하는편이 간편한거 같아 remvoe로 삭제해 줌
        price.remove('만원')

        sort = price[0]

        deposit = price[1]

        item['_2price'] = [sort]  # 월세, 전세, 매매 정보를 입력받음

        change_price = deposit.split(' ')  # 임의의 변수를 만들어 deposit 을 공백을 기준으로 나눔

        uk = change_price[0]

        # 수 단위(',')를 없애고 억 단위를 만 단위로 바꿈 (1억 -> 10000(만))
        uk = uk.replace(',', '').replace('억', '0000')

        try:

            man = change_price[1]

            man = man.replace(',', '')  # 수 단위(',')를 없앰

            deposit = int(uk) + int(man)  # 억단위였던 숫자와 천만원 단위였던 숫자를 더함

        except IndexError:

            deposit = int(uk)  # 천만원 단위가 존재하지 않는다면 억단위 숫자만 표시

        if sort == '월세':

            month_rent = int(price[2].replace('/', '').replace(',', ''))

            # 만약 sort가 월세라, 보증금(deposit), 집세(month_rent) 가 존재한다면, item['_3price']에 보증금, 집세 추가
            item['_2price'].append(deposit)

            item['_2price'].append(month_rent)  # month_rent에 존재하는 '/'를 제거함

        else:
            # 만약 sort가 월세가 아니라면 집의 가격만 존재, item[_3price]에 가격 추가
            item['_2price'].append(deposit)

            item['_2price'].append(None)  # 집세가 존재하지 않아 none을 추가

        item['_3pyeong'] = int(int(response.xpath('//*[@id="content"]/div/div[1]/div[1]/div/div[2]').css(
            'div > span::text').getall()[-1].split(' ')[-1][:-1])//3.305785)  # 면적을 Xpath와 Css Selector를 이용해 추출

        print(item)

        yield item

    def get_fac(self, response):

        # 주변 편의시설들의 정보를 json형식으로 불러옴
        nearFac = json.loads(response.text)['nearFacility']

        order_list = []

        for number in range(11):

            try:

                # number번째 종류의 편의시설이 존재한다면 order_list에 추가
                order_list.append(int(nearFac[number]['order'])-1)

            except IndexError:

                pass  # 존재하지 않는다면 pass

        # 버스정류장 지하철역 편의점 마트 세탁소 순서
        item['_4fac'] = [None, None, None, None, None]  # None값으로 초기화
        # 기본은 none으로 초기화
        for count in range(len(order_list)):

            fac_list = '버스정류장 지하철역 편의점 마트 세탁소'.split(
                ' ')  # 주변 편의시설들을 순서대로 리스트형식으로 생성

            # 만약 nearFac에서 labelName이 fac_list안에 있다면
            if nearFac[count]['complexView']['labelName'] in fac_list:

                item['_5fac'][fac_list.index(nearFac[count]['complexView']['labelName'])] = int(
                    nearFac[count]['closestDist'])  # 해당 labelName의 값을 closestDist로 변경
