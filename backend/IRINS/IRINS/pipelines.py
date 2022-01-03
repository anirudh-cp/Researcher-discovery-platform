# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
from bson import json_util

class IrinsPipeline:
    client = None
    db = None
    collection = None

    def __init__(self):
        self.client = MongoClient('mongodb+srv://python:pythonpass@datacluster.8ohor.mongodb.net/RDP_DB?retryWrites=true&w=majority')
        self.db = self.client.get_database('RDP_DB')
        self.collection = self.db.irins

    def process_item(self, item, spider):
        self.collection.insert_one(item)
        item['_id'] = str(item['_id'])
        return item
