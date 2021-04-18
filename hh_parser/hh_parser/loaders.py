from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Join
from urllib.parse import urljoin


def clear_salary(salary):
    if not salary:
        return 'not defined'
    return salary.replace('\xa0', '')


def clear_description(description):
    if not description:
        return 'not defined'
    return description.replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '')


def clear_author(author):
    if not author:
        return 'not defined'
    return urljoin('https://spb.hh.ru', ''.join(author))


def clear_author_description(description):
    if not description:
        return 'not defined'
    return description.replace('\xa0', ' ').replace('\r\n', '').replace('\u200b', '')


def clear_author_name(name):
    if not name:
        return 'not defined'
    return name.replace('\xa0', ' ').replace('Вакансии компании ', '').strip()


class HhVacancyLoader(ItemLoader):
    default_item_class = dict

    vacancy_out = TakeFirst()

    title_out = TakeFirst()

    skills_out = Join(', ')

    salary_in = MapCompose(clear_salary)
    salary_out = Join()

    description_in = MapCompose(clear_description)
    description_out = Join()

    author_in = MapCompose(clear_author)
    author_out = TakeFirst()


class HhAuthorLoader(ItemLoader):
    default_item_class = dict

    profile_out = TakeFirst()

    name_in = MapCompose(clear_author_name)
    name_out = Join()

    web_site_out = TakeFirst()

    activity_out = Join()

    description_in = MapCompose(clear_author_description)
    description_out = Join()
