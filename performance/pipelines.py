# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

'''
import json


class PerformancePipeline(object):

    def open_spider(self, spider):
        self.file = open('performance.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item
'''

class PerformancePipeline(object):

    collection_name = 'performance'

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        sheetname = settings['MONGODB_SHEETNAME']
        # 创建 MONGODB 数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        db = client[dbname]
        # 存放数据的数据库表名
        self.post = db[sheetname]

    def process_item(self, item, spider):
        # 直接将 item 转为 dict 后直接写入 mongodb
        # data = dict(item)
        # self.post.insert(data)
        # 遍历 item 类，解开 list 为 str 写入 mongodb
        for i in range(len(item['name'])):
            # 判断 name|date|place 是否存在 mongodb 中，如果不存在，就写入
            if (self.post.find_one({'name': item['name'][i]}) is None) or (self.post.find_one({'date': item['date'][i]}) is None) or (self.post.find_one({'place': item['place'][i]}) is None):
                self.post.insert({'name': item['name'][i], 'date': item['date'][i], 'place': item['place'][i]})
            # 如果已经存在，就 pass
            pass

        return item
