from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Join
from urllib.parse import urljoin


def clear_title(title):
    return title.replace('\xa0', '').replace('\n ', '')


def clear_price(price):
    return float(price)


def clear_description(description):
    return description.replace('\n ', '').replace('\xa0', '')


def clear_address(address):
    return address.replace('\n ', '')


def clear_author(author):
    if 'https://www.avito.ru' not in author:
        return urljoin('https://www.avito.ru', author)
    return author


class AdsLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()

    title_in = MapCompose(clear_title)
    title_out = Join()

    price_in = MapCompose(clear_price)
    price_out = TakeFirst()

    description_in = MapCompose(clear_description)
    description_out = Join(' ')

    address_in = MapCompose(clear_address)
    address_out = Join()

    author_in = MapCompose(clear_author)
    author_out = TakeFirst()
