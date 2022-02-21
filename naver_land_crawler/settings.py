BOT_NAME = 'naver_land_crawler'

SPIDER_MODULES = ['naver_land_crawler.spiders']
NEWSPIDER_MODULE = 'naver_land_crawler.spiders'

ROBOTSTXT_OBEY = False
LOG_FILE = "spider.log"

RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

TELNETCONSOLE_ENABLED=False

DOWNLOAD_DELAY = 0.2

COOKIES_ENABLED = False
COOKIES_DEBUG = False

CONCURRENT_REQUESTS = 1000

ITEM_PIPELINES = {
   'naver_land_crawler.pipelines.NaverLandCrawlerPipeline': 300,
}
