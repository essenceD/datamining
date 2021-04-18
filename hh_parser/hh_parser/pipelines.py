# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class HhParserPipeline:
    def process_item(self, item, spider):
        return item


class HhParserMongoPipeline:
    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client['hh_data']

    def process_item(self, item, spider):
        source = ''.join(item.pop('source'))
        print(source)
        self.db[source].insert_one(item)
        return item
