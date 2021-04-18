# Источник https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113
# вакансии удаленной работы.
# Задача: Обойти с точки входа все вакансии и собрать след данные:
# 1. название вакансии
# 2. оклад (строкой от до или просто сумма)
# 3. Описание вакансии
# 4. ключевые навыки - в виде списка названий
# 5. ссылка на автора вакансии
# Перейти на страницу автора вакансии,
# собрать данные:
# 1. Название
# 2. сайт ссылка (если есть)
# 3. сферы деятельности (списком)
# 4. Описание
# Обойти и собрать все вакансии данного автора.
import scrapy
from ..loaders import HhVacancyLoader, HhAuthorLoader


class HhSpider(scrapy.Spider):
    vac_counter = 0
    auth_counter = 0
    page_counter = 0
    name = 'hh'
    allowed_domains = ['spb.hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']
    selectors = {
        'vacancy': '//a[@data-qa="vacancy-serp__vacancy-title"]/@href',
        'pagination': '//div[@data-qa="pager-block"]//a[@data-qa="pager-next"]/@href',
        'author': '//a[@data-qa="vacancy-company-name"]/@href',
        'author_vacancies': '//a[@data-qa="employer-page__employer-vacancies-link"]/@href'
    }
    _xpath_vacancy_query_regular = {
        'title': '//h1[@data-qa="vacancy-title"]/text()',
        'salary': '//p[contains(@class, "vacancy-salary")]/span[@data-qa="bloko-header-2"]/text()',
        'description': '//div[@data-qa="vacancy-description"]//text()',
        'skills': '//span[@data-qa="bloko-tag__text"]//text()',
        'author': '//a[@data-qa="vacancy-company-name"]/@href',
    }
    _xpath_author_query = {
        'name': '//div[@class="bloko-column bloko-column_xs-4 bloko-column_s-8'
                ' bloko-column_m-9 bloko-column_l-11"]//span[@class="company-header-title-name"]/text()',
        'web_site': '//a[@class="g-user-content"]//@href',
        'activity': '//div[contains(text(), "Сферы деятельности")]/../p/text()',
        'description': '//div[@class="g-user-content"]//text()',
    }
    _xpath_author_query_premium = {
        'name': '//h3[@class="b-subtitle b-employerpage-vacancies-title"]//text()',
    }

    def _get_follow(self, response, selector, callback, **kwargs):
        for link_selector in response.xpath(selector).extract():
            yield response.follow(
                link_selector,
                callback=callback
            )

    def parse(self, response, **kwargs):
        yield from self._get_follow(
            response,
            self.selectors['vacancy'],
            self.vacancy_parse
        )
        yield from self._get_follow(
            response,
            self.selectors['pagination'],
            self.page_parse
        )

    def page_parse(self, response, **kwargs):
        self.page_counter += 1
        print(f'##{self.page_counter}## pages parsed.')
        yield from self._get_follow(
            response,
            self.selectors['pagination'],
            self.parse
        )

    def vacancy_parse(self, response):
        loader = HhVacancyLoader(response=response)
        loader.add_value('vacancy', response.url)
        loader.add_value('source', 'vacancy')
        for key, selector in self._xpath_vacancy_query_regular.items():
            if len(response.xpath(selector)) > 0:
                loader.add_xpath(key, selector)
            else:
                loader.add_value(key, '-----not_defined-----')

        yield loader.load_item()
        self.vac_counter += 1
        print(f'-={self.vac_counter}=- vacancies parsed.')

        yield from self._get_follow(
            response,
            self.selectors['author'],
            callback=self.author_parse
        )

    def author_parse(self, response):
        loader = HhAuthorLoader(response=response)
        loader.add_value('profile', response.url)
        loader.add_value('source', 'author')
        if len(response.xpath(self._xpath_author_query['name'])) > 0:

            for key, selector in self._xpath_author_query.items():
                if len(response.xpath(selector)) > 0:
                    loader.add_xpath(key, selector)
                else:
                    loader.add_value(key, '-----not_defined-----')
        else:

            for key, selector in self._xpath_author_query_premium.items():
                if len(response.xpath(selector)) > 0:
                    loader.add_xpath(key, selector)
                    loader.add_value('web_site', 'try to use vacancies or author URL')
                    loader.add_value('activity', 'try to use vacancies or author URL')
                    loader.add_value('description', 'try to use vacancies or author URL')
                else:
                    loader.add_value(key, '-----not_defined-----')

        yield loader.load_item()
        self.auth_counter += 1
        print(f'++{self.auth_counter}++ authors parsed.')
        yield from self._get_follow(
            response,
            self.selectors['author_vacancies'],
            self.parse
        )
