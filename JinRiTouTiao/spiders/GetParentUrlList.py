# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from ..items import JinritoutiaoItem
from scrapy.loader import ItemLoader
from selenium import webdriver

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class GetParentUrlSpider(RedisSpider):

    name = "TouTiao_GetParentUrl"
    # allowed_domains = ["www.toutiao.com"]
    # start_urls = []

    # def __init__(self):
    # 设置不加载图片
    #     chrome_opt = webdriver.ChromeOptions()
    #     prefs = {"profile.managed_default_content_sttings.images": 2}
    #     chrome_opt.add_experimental_option("prefs", prefs)
    #     driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_opt)
    #     self.driver = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
    #     super(GetParentUrlSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)

    #个性化设置setting中的配置
    custom_settings = {
        "COOKIES_ENABLED": True
    }
    def spider_closed(self, spider):
        print("spider closed")
        self.driver.close()

    def make_requests_from_url(self, data):
        data = json.loads(data)
        url = data['url']
        return Request(url, dont_filter=True, meta=data, callback=self.parse_list)


    def parse_list(self, response):
        data_json = response.body
        data_json = data_json.decode()
        data_json = json.loads(data_json)

        datas = data_json['data']
        for data in datas:
            try:
                data['media_creator_id']
            except KeyError:
                continue



            """
            #普通装载item的方法
            screen_name = data['source']
            created_at = data['datetime']
            post_title = data['title']
            comments_count = data['comments_count']
            page_url = data['article_url']

            item = JinritoutiaoItem()

            item['screen_name'] = screen_name
            item['created_at'] = created_at
            item['post_title'] = post_title
            item['comments_count'] = comments_count
            item['page_url'] = page_url
            item['column'] = response.meta['column']
            item['column1'] = response.meta['column1']
            """


            #通过ItemLoader加载Item
            itemLoader = ItemLoader(item=JinritoutiaoItem(), response=response)
            # itemLoader.add_xpath("")
            # itemLoader.add_css("")
            itemLoader.add_value("screen_name", data['source'])
            itemLoader.add_value("created_at", data['datetime'])
            itemLoader.add_value("post_title", data['title'])
            itemLoader.add_value("comments_count", data['comments_count'])
            itemLoader.add_value("page_url", data['article_url'])
            itemLoader.add_value("column", response.meta['column'])
            itemLoader.add_value("column1", response.meta['column1'])
            item = itemLoader.load_item()
            yield item


