# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NvshenspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NvshenItem(scrapy.Item):
    _id = scrapy.Field()
    detail_url = scrapy.Field()
    cover_url = scrapy.Field()
    title = scrapy.Field()

    tags = scrapy.Field()
    describe = scrapy.Field()
    album_count = scrapy.Field()
    album_photos = scrapy.Field()
    create_date = scrapy.Field()
    views = scrapy.Field()
    pass
