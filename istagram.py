# Источник instgram
# Задача авторизованным пользователем обойти список произвольных тегов,
# Сохранить структуру Item олицетворяющую сам Tag (только информация о теге)
# Сохранить структуру данных поста, Включая обход пагинации. (каждый пост как отдельный item, словарь внутри node)
# Все структуры должны иметь след вид
# date_parse (datetime) время когда произошло создание структуры
# data - данные полученные от инстаграм
# Скачать изображения всех постов и сохранить на диск
import scrapy
import json
from urllib.parse import urlencode


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com', 'i.instagram.com']
    start_urls = ['https://www.instagram.com/']
    _login_url = '/accounts/login/ajax/'
    _tags_path = '/explore/tags/'
    _pagination_path = 'https://i.instagram.com/api/v1/tags/'

    def __init__(self, login, password, tags, *args, **kwargs):
        self.login = login
        self.password = password
        self.tags = tags
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        try:
            js_data = self.js_extract(response)
            yield scrapy.FormRequest(
                response.urljoin(self._login_url),
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.password
                },
                headers={'x-csrftoken': js_data['config']['csrf_token']}
            )
            print(1)
        except AttributeError:
            if response.json()['authenticated']:
                print('authenticated confirmed')
                for tag in self.tags:
                    yield response.follow(f'{self._tags_path}{tag}/', callback=self.tag_page_parse)

    def tag_page_parse(self, response):
        try:
            parse_data = self.get_parse_data(response)
            # id_ = urlencode(parse_data['next_max_id'])
            yield scrapy.FormRequest(
                f'{self._pagination_path}{parse_data["name"]}/sections/',
                method='POST',
                callback=self.tag_page_parse,
                formdata={
                    'include_persistent': '0',
                    'max_id': parse_data['next_max_id'][:-2] + '%3D%3D',
                    'page': f'{parse_data["next_page"] + 1}',
                    'surface': 'grid',
                    'tab': 'recent'
                },
                headers={
                    'x-csrftoken': parse_data['x-csrftoken'],
                    'x-ig-app-id': parse_data['id'],
                    ':authority': 'i.instagram.com',
                    ':path': '/api/v1/tags/travel/sections/',
                    ':scheme': 'https',
                    'x-ig-www-claim': 'hmac.AR3zA1yi3bm0HrLF0bP6OeMpmzYBqwyZABbMyOAb2MP94NS7',
                    'x-instagram-ajax': '822bad258fea'

                }
            )
        except KeyError:
            print('pagination')
            # self.parse(response)

    def tag_parse(self, response):
        print('tag_parse')

    def get_parse_data(self, response):
        js_data = self.js_extract(response)
        print('get_parse_data')
        return {
            'next_max_id': js_data['entry_data']['TagPage'][0]['data']['recent']['next_max_id'],
            'id': js_data['entry_data']['TagPage'][0]['data']['id'],
            'name': js_data['entry_data']['TagPage'][0]['data']['name'],
            'followers': js_data['entry_data']['TagPage'][0]['data']['media_count'],
            'profile_picture_url': js_data['entry_data']['TagPage'][0]['data']['profile_pic_url'],
            'next_page': js_data['entry_data']['TagPage'][0]['data']['recent']['next_page'],
            'x-csrftoken': js_data['config']['csrf_token']
        }

    def js_extract(self, response):
        script = response.xpath(
            '//body//script[contains(text(), "window._sharedData = ")]//text()'
        ).extract_first()
        return json.loads(script.replace('window._sharedData = ', '')[:-1])


