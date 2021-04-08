# Источник https://magnit.ru/promo/?geo=moskva
# Необходимо собрать структуры товаров по акции и сохранить их в MongoDB
#
# пример структуры и типы обязательно хранить поля даты как объекты datetime
# {
#     "url": str,
#     "promo_name": str,
#     "product_name": str,
#     "old_price": float,
#     "new_price": float,
#     "image_url": str,
#     "date_from": "DATETIME",
#     "date_to": "DATETIME",
# }


import requests
from urllib.parse import urljoin
import bs4
import pymongo
import time


class MagnitParse:
    headers = {'User-Agent': 'Chuck Norris'}

    def __init__(self, start_url, db_client):
        self.start_url = start_url
        db = db_client["gb_data_mining_29_03_21"]
        self.collection = db["magnit"]

    def _get_response(self, url, *args, **kwargs):
        while True:
            response = requests.get(url, *args, **kwargs, headers=self.headers)
            if response.status_code in (200, 301, 304):
                return response
            time.sleep(1)

    def _get_soup(self, url, *args, **kwargs):
        return bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, "lxml")

    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)

    def get_price(self, tag, _class) -> dict:
        try:
            float('.'.join(tag.find('div', {'class': _class}).text.split()))
        except Exception:
            return {'price': 'None'}
        return {'price': float('.'.join(tag.find('div', {'class': _class}).text.split()))}

    @property
    def _template(self):
        return {
            "product_name": lambda tag: tag.find("div", attrs={"class": "card-sale__title"}).text,
            "url": lambda tag: urljoin(self.start_url, tag.attrs.get("href", "")),
            "promo_name": lambda tag: tag.find("div", attrs={"class": "card-sale__name"}).text,
            "old_price": lambda tag: self.get_price(tag, 'label__price label__price_old')['price'],
            "new_price": lambda tag: self.get_price(tag, 'label__price label__price_new')['price'],
            "image_url": lambda tag: urljoin(self.start_url, tag.find('img').attrs.get('data-src')),
            "date_from": lambda tag: self.get_date(
                tag.find('div', attrs={'class': 'card-sale__date'}).text.replace('с ', '').replace('\n', '').split(
                    'до '))['from'],
            "date_to": lambda tag: self.get_date(
                tag.find('div', attrs={'class': 'card-sale__date'}).text.replace('с ', '').replace('\n', '').split(
                    'до '))['to']
        }

    def _parse(self, url):
        soup = self._get_soup(url)
        catalog_main = soup.find("div", attrs={"class": "сatalogue__main"})
        product_tags = catalog_main.find_all("a", recursive=False)
        for product_tag in product_tags:
            product = {}
            for key, funk in self._template.items():
                try:
                    product_tag.find("div", attrs={"class": "card-sale__title"}).text
                except AttributeError:
                    continue
                product[key] = funk(product_tag)
            print(product)
            yield product

    def _save(self, data):
        if len(data) > 0:
            self.collection.insert_one(data)

    def get_date(self, date: list) -> dict:
        month = {'янв': '01', 'фев': '02', 'мар': '03', 'апр': '04', 'мая': '05', 'июн': '06', 'июл': '07', 'авг': '08',
                 'сен': '09', 'окт': '10', 'ноя': '11', 'дек': '12'}
        num_from = ''
        num_to = ''
        if len(date) < 2:
            date = date[0].replace('Только ', '').split()
            for mon in month.keys():
                if mon in date[1]:
                    num_to = num_from = month[mon]
            date_from = f'2021-{num_from}-{date[0]} 12:00:00'
            date_to = f'2021-{num_to}-{date[0]} 12:00:00'
            return {'from': date_from, 'to': date_to}

        for mon in month.keys():
            if mon in date[0].split()[1]:
                num_from = month[mon]
            if mon in date[1].split()[1]:
                num_to = month[mon]
        date_from = f'2021-{num_from}-{date[0].split()[0]} 12:00:00'
        date_to = f'2021-{num_to}-{date[1].split()[0]} 12:00:00'
        return {'from': date_from, 'to': date_to}


if __name__ == "__main__":
    _url = "https://magnit.ru/promo/?geo=moskva"
    _db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = MagnitParse(_url, _db_client)
    parser.run()
