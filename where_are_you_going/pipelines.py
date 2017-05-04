# -*- coding: utf-8 -*-

import pymongo

class DatabasePipeline(object):
  collection_name = "alumnis"

  def __init__(self, mongo_uri, mongo_db):
    self.mongo_uri = mongo_uri
    self.mongo_db = mongo_db

  @classmethod
  def from_crawler(cls, crawler):
    return cls(
      mongo_uri=crawler.settings.get('MONGO_URI'),
      mongo_db=crawler.settings.get('MONGO_DATABASE', 'mom')
    )

  def open_spider(self, spider):
    self.client = pymongo.MongoClient(self.mongo_uri)
    self.db = self.client[self.mongo_db]

  def close_spider(self, spider):
    self.client.close()

  def process_item(self, item, spider):
    user = self.db[self.collection_name].find_one({'registry': item['registry']})

    if user:
      self.db[self.collection_name].update({
        'registry': item['registry']
      }, item)
      return item

    if not user:
      self.db[self.collection_name].insert_one(item)
      return item