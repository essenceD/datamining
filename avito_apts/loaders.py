from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Join
from urllib.parse import urljoin


class AdsLoader(ItemLoader):
    default_item_class = dict()
