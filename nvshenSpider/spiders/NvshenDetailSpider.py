# -*- coding: utf-8 -*-
import re
import scrapy
from pymongo import MongoClient
from bs4 import BeautifulSoup as Soup
from nvshenSpider.items import NvshenItem
from urllib.parse import urljoin, urlsplit

print("正在初始化数据库")
client = MongoClient("127.0.0.1", 27017)
collection = client.python_spider.nvshen_spider


class NvshendetailspiderSpider(scrapy.Spider):
    name = 'NvshenDetailSpider'
    base_url = "https://www.nvshens.com/"
    allowed_domains = ['nvshens.com']

    def start_requests(self):
        for item in collection.find({"album_photos": {"$exists": False}}):
            yield scrapy.Request(item["detail_url"], dont_filter=True)

    def parse(self, response):
        soup = Soup(response.body, "lxml")
        web_path = urlsplit(response.url)[2]
        item = NvshenItem()
        if web_path.endswith(".html"):  # 详情页分页图片解析
            item["detail_url"] = response.url[:response.url.rindex("/") + 1]
            photos = []
            for i in soup.find("div", class_="gallery_wrapper").find_all("img"):
                photos.append(i.get("src"))
            item["album_photos"] = photos
        else:  # 详情页信息解析
            item["detail_url"] = response.url
            tags = []
            for a in soup.find("div", class_="album_tags").find_all("a"):
                href = a.get("href")
                tags.append({
                    "name": a.text,
                    "url": href if href.startswith("http") else urljoin(self.base_url, href)
                })
            item["tags"] = tags
            item["describe"] = soup.find("div", class_="albumInfo").text
            info = soup.find("div", id="dinfo", class_="albumInfo").text
            item["create_date"] = re.search('\d{4}/\d{1,2}/\d{1,2}', info).group().strip()
            item["album_count"] = int(re.search('\d{1,3}', info).group().strip())
            item["views"] = re.search(' \d{1,6} ', info).group().strip()
            photos = []
            for i in soup.find("div", class_="gallery_wrapper").find_all("img"):
                photos.append(i.get("src"))
            item["album_photos"] = photos
        yield item  # 数据存储
        # 获取详情页的图片分页
        pages_tag = soup.find("div", id="pages").find_all("a", class_="a1")
        next_page_url = urljoin(self.base_url, pages_tag[len(pages_tag) - 1].get("href"))
        if next_page_url.endswith(".html"):
            yield scrapy.Request(next_page_url)  # 请求分页
