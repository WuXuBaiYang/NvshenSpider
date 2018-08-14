# -*- coding: utf-8 -*-
import re
import os
import scrapy
from hashlib import md5
from pymongo import MongoClient


class DownloadspiderSpider(scrapy.Spider):
    name = 'DownloadSpider'
    allowed_domains = ['t1.onvshen.com']
    start_urls = ['http://t1.onvshen.com/']
    dir_path = "/Volumes/移动城堡/spider_data/nvshen_data"  # 根据运行环境进行修改
    file_pattern = r"/|\.|\\"

    print("正在初始化数据库")
    client = MongoClient("127.0.0.1", 27017)
    collection = client.python_spider.nvshen_spider

    def start_requests(self):
        for item in self.collection.find({"album_photos": {"$exists": True}}):
            _path = "%s/%s[%dP]" % (self.dir_path, re.sub(self.file_pattern, "", item["title"]), item["album_count"])
            if not os.path.exists(_path):
                os.mkdir(_path)
            for url in item["album_photos"]:
                _file_path = "%s/%s%s" % (
                    _path, md5(url[:url.rindex(".")].encode("utf-8")).hexdigest(), url[url.rindex("."):])
                if not os.path.exists(_file_path):
                    yield scrapy.Request(url, dont_filter=True, flags=[_file_path])

    def parse(self, response):
        _file_path = response.flags[0]
        with open(_file_path, "wb") as f:
            f.write(response.body)
            print("文件已写入", _file_path)
