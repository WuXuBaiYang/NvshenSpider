# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from pymongo.errors import PyMongoError

print("正在初始化数据库")
client = MongoClient("127.0.0.1", 27017)
collection = client.python_spider.nvshen_spider


class NvshenspiderPipeline(object):
    def process_item(self, item, spider):
        if "tags" not in item.keys():
            if len(item.keys()) == 2:
                collection.update({"detail_url": item["detail_url"]}, {"$addToSet": {
                    "album_photos": {"$each": item["album_photos"]}}}, upsert=True)
                print("图片增加", item["detail_url"])
            else:
                try:
                    collection.insert_one(item)
                    print("数据已插入", item["detail_url"])
                except PyMongoError as e:
                    print("数据已存在", item["detail_url"])
        elif "album_photos" in item.keys():
            collection.update({"detail_url": item["detail_url"]}, {"$set": item}, upsert=True)
            print("详情页数据已更新", item["detail_url"])
        else:
            print("-------------------------数据格式错误-------------------------", item)
