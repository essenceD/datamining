# Источник https://www.avito.ru/krasnodar/kvartiry/prodam
#
# задача обойти пагинацию и подразделы квартир в продаже.
#
# Собрать данные:
# URL
# Title
# Цена
# Адрес (если доступен)
# Параметры квартиры (блок под фото)
# Ссылку на автора
#
# Дополнительно но не обязательно вытащить телефон автора
import scrapy
from ..loaders import AdsLoader


class AvitoaptsSpider(scrapy.Spider):
    name = 'AvitoApts'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/krasnodar/kvartiry/prodam']
    selector_xpath = {
        'pagination': '//div[contains(@class, "pagination-hidden-")]//@href',
        'apts': '//div[contains(@class, "iva-item-content-")]//div[contains(@class, "iva-item-titleStep-")]//a/@href',
        'vip_apts': '//div[contains(@class, "items-vip-")]//div[contains(@class, "iva-item-titleStep-")]/a/@href',

    }
    apt_selector_xpath = {
        'title': '//h1[contains(@class, "title-info-title")]//text()',
        'price': '//div[@class="item-price"]//span[contains(@class, "price-value-string")]'
                 '//span[@class="js-item-price"]/@content',
        'address': '//div[@itemprop="address"]//text()',
        'description': '//div[@class="item-view-block"]//text()',
        'author': '//div[contains(@class, "item-view-seller-info")]//'
                  'div[contains(@data-marker, "seller-info/name")]//@href'
    }

    def _get_follow(self, response, selector, callback, **kwargs):
        for link_selector in response.xpath(selector).extract():
            yield response.follow(link_selector, callback=callback)

    def parse(self, response, **kwargs):
        yield from self._get_follow(response, self.selector_xpath['apts'], self.apt_parse)
        yield from self._get_follow(response, self.selector_xpath['vip_apts'], self.apt_parse)
        yield from self._get_follow(response, self.selector_xpath['pagination'], self.page_parse)

    def page_parse(self, response, **kwargs):
        yield from self._get_follow(response, self.selector_xpath['pagination'], self.parse)

    def apt_parse(self, response, **kwargs):
        loader = AdsLoader(response=response)
        loader.add_value('url', response.url)
        for key, selector in self.apt_selector_xpath.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()
        yield from self._get_follow(response, self.selector_xpath['pagination'], self.parse)
