import requests
from headers import headers

CON_URL = "https://new.land.naver.com/api/regions/complexes?cortarNo={}"
DETAIL_URL = "https://new.land.naver.com/api/complexes/overview/{}?complexNo={}"


def get_complexList(CORTARNO: str) -> list:
    request_url = CON_URL.format(CORTARNO)
    response = requests.get(request_url, headers=headers)
    complexList = response.json()["complexList"]
    return complexList


def get_details(complexList: list) -> list:
    for complex in complexList:
        complexNo = complex["complexNo"]
        request_url = DETAIL_URL.format(complexNo, complexNo)
        response = requests.get(request_url, headers=headers)
        details = response.json()
        yield details


def get_items(details: dict) -> dict:
    print(details[0])
