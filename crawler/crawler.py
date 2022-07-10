import requests
from crawler.headers import headers
from datetime import datetime

CON_URL = "https://new.land.naver.com/api/regions/complexes?cortarNo={}"
DETAIL_URL = "https://new.land.naver.com/api/complexes/overview/{}?complexNo={}"


def get_complexList(CORTARNO: str) -> list:
    request_url = CON_URL.format(CORTARNO)
    response = requests.get(request_url, headers=headers)
    complexList = response.json()["complexList"]
    return complexList


def get_details(complexList: list) -> list:
    detail_list = []
    for complex in complexList:
        complexNo = complex["complexNo"]
        request_url = DETAIL_URL.format(complexNo, complexNo)
        print(request_url)
        response = requests.get(request_url, headers=headers)
        details = response.json()
        detail_list.append(details)
    return detail_list


def get_items(details: list) -> list:
    items = []
    for detail in details:
        item = {}
        try:
            item["minArea"] = detail["minArea"]
            item["maxArea"] = detail["maxArea"]
            item["minLeasePriceByLetter"] = detail["minLeasePriceByLetter"]
            item["maxLeasePriceByLetter"] = detail["maxLeasePriceByLetter"]
        except:
            print("해당 집은 판매되고 있지 않습니다.")
            continue
        item["complexTypeName"] = detail["complexTypeName"]
        item["complexType"] = detail["complexType"]
        item["complexName"] = detail["complexName"]
        item["complexNo"] = detail["complexNo"]
        try:
            try:
                created_year, created_month, created_day = datetime.strptime(detail["useApproveYmd"], "%Y%m%d").strftime("%Y-%m-%d").split("-")
            except:
                created_year, created_month = datetime.strptime(detail["useApproveYmd"], "%Y%m").strftime("%Y-%m").split("-")
                created_day = None
        except:
            created_year = None
            created_month = None
            created_day = None
        item["created_year"] = created_year
        item["created_month"] = created_month
        item["created_day"] = created_day

        now = datetime.now()
        update_year = str(now.year)
        update_month = str(now.month)
        update_day = str(now.day)
        item["update_year"] = update_year
        item["update_month"] = update_month
        item["update_day"] = update_day

        item["latitude"] = detail["latitude"]
        item["longitude"] = detail["longitude"]

        items.append(item)

    return items

