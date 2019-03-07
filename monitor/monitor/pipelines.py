# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Item
from scrapy.conf import settings
import pymongo

class MonitorPipeline(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbName = settings["MONGODB_DBNAME"]
        client = pymongo.MongoClient(host = host, port = port)
        tdb = client[dbName]
        self.post = tdb[settings["MONGODB_DOCNAME"]]
        self.query = tdb[settings["MONGODB_DOCNAME"]]

    def process_item(self, item, spider):
        news = dict(item)
        res = self.post.find_one({'news_url' : news["news_url"]})
        if not res:
            self.post.insert_one(news).inserted_id
        return item
