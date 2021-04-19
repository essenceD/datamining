from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avito_apts.spiders.avitoapts import AvitoaptsSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule('avito_apts.settings')
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(AvitoaptsSpider)
    crawler_proc.start()
