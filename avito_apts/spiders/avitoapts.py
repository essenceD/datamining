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
    allowed_domains = ['avito.ru/krasnodar/kvartiry/prodam']
    start_urls = ['https://www.avito.ru/krasnodar/kvartiry/prodam']
    selector_xpath = {
        'pagination': '//div[contains(@class, "pagination-hidden-")]//@href',
        'apts': '//div[contains(@class, "iva-item-content-")]//div[contains(@class, "iva-item-titleStep-")]//a/@href',
        'vip_apts': '//div[contains(@class, "items-vip-")]//div[contains(@class, "iva-item-titleStep-")]/a/@href',

    }
    apt_selector_xpath = {
        'url': '',
        'title': '',
        'price': '',
        'address': '',
        'description': '',
        'author': ''
    }

    def _get_follow(self, response, selector, callback, **kwargs):
        for link_selector in response.xpath(selector).extract():
            yield response.follow(
                link_selector,
                callback=callback
            )

    def parse(self, response, **kwargs):
        print(1)
        yield from self._get_follow(response, self.selector_xpath['apts'], self.apt_parse)
        # yield from self._get_follow(response, self.selector_xpath['vip_apts'], self.apt_parse)
        yield from self._get_follow(response, self.selector_xpath['pagination'], self.page_parse)

    def page_parse(self, response, **kwargs):
        yield from self._get_follow(response, self.selector_xpath['pagination'], self.parse)

    def apt_parse(self, response, **kwargs):
        print(response.status)
        loader = AdsLoader()
        print(2)
        for key, selector in self.apt_selector_xpath.items():
            loader.add_xpath(key, selector)
        print(3)
        # yield from self._get_follow(response, )
