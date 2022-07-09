from crawler.crawler import get_complexList, get_items, get_details
from crawler.CORTARNOS import CORTARNOS

for CORTARNO in CORTARNOS:
    complexList = get_complexList(CORTARNO)
    details = get_details(complexList)
    itmes = get_items(details)
