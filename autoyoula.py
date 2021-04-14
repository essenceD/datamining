# Источник https://auto.youla.ru/ +
# Обойти все марки авто и зайти на странички объявлений +
# Собрать след стуркутру и сохранить в БД Монго +
# Название объявления +
# Список фото объявления (ссылки) +
# Список характеристик +
# Описание объявления +
# ссылка на автора объявления -
# дополнительно попробуйте вытащить телефона -


import scrapy
import pymongo


class AutoyoulaSpider(scrapy.Spider):
    db = pymongo.MongoClient('mongodb://localhost:27017')['youla_cars']
    collection = db['youla']
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['http://auto.youla.ru/']
    _css_selectors = {
        'brands': 'div.ColumnItemList_column__5gjdt a.blackLink',
        'pagination': 'div.Paginator_block__2XAPy a.Paginator_button__u1e7D',
        'car': 'article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu'
    }

    @staticmethod
    def _get_or_follow(response, selector_css, callback, **kwargs):
        for link_selector in response.css(selector_css):
            yield response.follow(link_selector.attrib.get('href'), callback=callback)

    def parse(self, response, **kwargs):
        yield from self._get_or_follow(response, self._css_selectors['brands'], callback=self.brand_parse)
        # for link_selector in response.css(self._css_selectors['brands']):
        #     yield response.follow(link_selector.attrib.get('href'), callback=self.brand_parse)

    def brand_parse(self, response):
        yield from self._get_or_follow(response, self._css_selectors['pagination'], self.brand_parse)
        yield from self._get_or_follow(response, self._css_selectors['car'], self.car_parse)
        # for link_selector in response.css(self._css_selectors['pagination']):
        #     yield response.follow(link_selector.attrib.get('href'), callback=self.brand_parse)

    def _save(self, data):
        if len(data) > 0:
            self.collection.insert_one(data)

    def car_parse(self, response):
        data = {
            'title': response.css('.AdvertCard_advertTitle__1S1Ak::text').extract_first(),
            'url': response.url,
            'description': response.css('.AdvertCard_descriptionInner__KnuRi::text').extract_first(),
            'specs': {
                'year': response.css(
                    'div.AdvertCard_specs__2FEHc div.AdvertSpecs_data__xK2Qx a.blackLink::text').extract_first(),
                'mileage': response.css('div.AdvertCard_specs__2FEHc '
                                        'div.AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[0],
                'body': response.css(
                    'div.AdvertCard_specs__2FEHc div.AdvertSpecs_data__xK2Qx a.blackLink::text').extract()[1],
                'transmission': response.css('div.AdvertCard_specs__2FEHc div.'
                                             'AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[1],
                'engine': response.css('div.AdvertCard_specs__2FEHc div.'
                                       'AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[2],
                'steering': response.css('div.AdvertCard_specs__2FEHc div.'
                                         'AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[3],
                'color': response.css('div.AdvertCard_specs__2FEHc div.'
                                      'AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[4],
                'drive': response.css('div.AdvertCard_specs__2FEHc div.'
                                      'AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[5],
                'power': response.css('div.AdvertCard_specs__2FEHc div.'
                                      'AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[6],
                'customs': response.css('div.AdvertCard_specs__2FEHc div.'
                                        'AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[7],
                'owners': response.css('div.AdvertCard_specs__2FEHc div.'
                                       'AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()[8]
            },
            'photos': response.css('figure.PhotoGallery_photo__36e_r img::attr(src)').extract(),
            'author': ''
        }

        # print(1)
        self._save(data)

