# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import time
import scrapy
from scrapy.loader.processors import MapCompose


def time_strip(timestamp):
    """
    时间戳转成新的时间格式(2016-05-05 20:28:54)
    :param timestamp:
    :return:
    """
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def data_time(dt):
    """
    时间转换成时间数组
    :param dt:
    :return:
    """
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    return timestamp


def format_time(time_str):
    if isinstance(time_str, int):
        return time_str



class JinritoutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    column = scrapy.Field()
    column1 = scrapy.Field()
    page_url = scrapy.Field()
    customer_name = scrapy.Field()
    screen_name = scrapy.Field()
    created_at = scrapy.Field(
        input_processor=MapCompose()
    )
    post_title = scrapy.Field(
        input_processor=MapCompose()
    )
    comments_count = scrapy.Field()





