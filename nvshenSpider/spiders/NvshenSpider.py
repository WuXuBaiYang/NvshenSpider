# -*- coding: utf-8 -*-
import re
import scrapy
import requests
from bs4 import BeautifulSoup as Soup
from nvshenSpider.items import NvshenItem
from urllib.parse import urljoin, urlsplit


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
        web_path = urlsplit(response.url)[2]
        if web_path.startswith("/gallery"):  # 解析列表页
            for a in soup.find("div", class_="listdiv").find_all("a", class_="galleryli_link"):
                item = NvshenItem()
                item["detail_url"] = urljoin(self.base_url, a.get("href"))
                item["cover_url"] = a.img.get("data-original")
                item["title"] = a.img.get("title")
                yield scrapy.Request(item["detail_url"])  # 请求详情页
                yield item  # 数据存储
            pages_tag = soup.find("div", class_="pagesYY").find_all("a")
            next_page = pages_tag[len(pages_tag) - 1]
            if next_page.get("class") is None:
                yield scrapy.Request(urljoin(self.base_url, next_page.get("href")))  # 请求分页
        elif web_path.startswith("/g"):  # 解析详情页
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
                item["album_count"] = re.search('\d{1,3}', info).group().strip()
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
        pass
