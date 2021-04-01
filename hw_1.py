# Источник: https://5ka.ru/special_offers/
#
# Задача организовать сбор данных,
# необходимо иметь метод сохранения данных в .json файлы
#
# результат: Данные скачиваются с источника,
# при вызове метода/функции сохранения в файл скачанные данные сохраняются в Json вайлы,
# для каждой категории товаров должен быть создан отдельный файл и содержать
# товары исключительно соответсвующие данной категории.
#
# пример структуры данных для файла:
# нейминг ключей можно делать отличным от примера
#
# {
# "name": "имя категории",
# "code": "Код соответсвующий категории (используется в запросах)",
# "products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
# }

import json
from pathlib import Path
import requests as rq


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


url_cats = 'https://5ka.ru/api/v2/categories/'
url_prods = 'https://5ka.ru/api/v2/special_offers/'

header = {'User-Agent': 'Jason Statham'}

response_cats = rq.get(url=url_cats)

data_cats = json.loads(response_cats.text)

result = []
for category in data_cats:
    params = {
        "store": None,
        "records_per_page": None,
        "page": None,
        "categories": category['parent_group_code'],
        "ordering": None,
        "price_promo__gte": None,
        "price_promo__lte": None,
        "search": None
    }
    response_prods = rq.get(url=url_prods, params=params, headers=header)
    data_prods = json.loads(response_prods.content)
    result.append({'name': category['parent_group_name'], 'code': category['parent_group_code'],
                   'products': data_prods['results']})

path = get_save_path('categories')

for sample in result:
    prod_path = path.joinpath(f"{sample['name']}.json")
    prod_path.write_text(json.dumps(sample, ensure_ascii=False), encoding='utf-8')
