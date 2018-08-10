# -*- coding: utf-8 -*-
import scrapy
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as Soup
from nvshenSpider.items import NvshenItem


class NvshenspiderSpider(scrapy.Spider):
    name = 'NvshenSpider'
    base_url = "https://www.nvshens.com/"
    allowed_domains = ['nvshens.com']

    def start_requests(self):
        response = requests.get("https://www.nvshens.com/gallery/", proxies={"https": "https://127.0.0.1:1087"})
        if response.status_code == 200:
            soup = Soup(response.content, "lxml")
            for a in soup.find("div", class_="box_entry").find_all("a"):
                page_url = urljoin(self.base_url, a.get("href"))
                yield scrapy.Request(page_url, dont_filter=True)
        else:
            print("分类解析失败", response.status_code)

    def parse(self, response):
        soup = Soup(response.body, "lxml")
        for a in soup.find("div", class_="listdiv").find_all("a", class_="galleryli_link"):
            detail_url = urljoin(self.base_url, a.get("href"))
            item = NvshenItem()
            item["detail_url"] = detail_url
            item["cover_url"] = a.img.get("data-original")
            item["title"] = a.img.get("title")
            yield item  # 数据存储
        pages_tag = soup.find("div", class_="pagesYY").find_all("a")
        next_page = pages_tag[len(pages_tag) - 1]
        if next_page.get("class") is None:
            yield scrapy.Request(urljoin(self.base_url, next_page.get("href")))  # 请求分页
