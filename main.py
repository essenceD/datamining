from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import pymongo

from my_parser.spiders.autoyoula import AutoyoulaSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule('my_parser.settings')
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(AutoyoulaSpider)
    crawler_proc.start()
