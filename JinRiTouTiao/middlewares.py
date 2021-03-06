# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from fake_useragent import UserAgent
from .tools.crawl_xici_ip import GetIP
import redis


class JinritoutiaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JSPageMiddleware(object):

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
        super(JSPageMiddleware, self).__init__()

    def process_request(self, request, spider):
        if spider.name == "TouTiao_GetParentUrl":
            self.driver.get(request.url)
            html = self.driver.page_source
            import time
            time.sleep(3)
            self.driver.close()
            print("访问{0}".format(request.url))
            return HtmlResponse(url=request.url, body=html, encoding="utf-8", request=request)


class RandomUserAgentMiddlwareOne(object):
    """
    随机切换User-Agent
    """
    def __init__(self, crawler):
        super(RandomUserAgentMiddlwareOne, self).__init__()
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        request.headers.setdefault(b'User-Agent', self.ua.random)


class RandomUserAgentMiddlwareTwo(object):
    """
    可配置的随机切换User-Agent, 并增加代理
    """
    def __init__(self, crawler):
        super(RandomUserAgentMiddlwareTwo, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        """
        get_ua采用闭包(函数中定义函数)
        :param request:
        :param spider:
        :return:
        """
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault(b'User-Agent', get_ua())



class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        get_ip = GetIP()
        request.meta["proxy"] = get_ip.get_random_ip()


# class ProxyMiddleware(object):
#     redisclient = redis.Redis(REDIS_PROXY_HOST, REDIS_PROXY_PORT)
#     DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)
#
#     def process_request(self, request, spider):
#         """
#         将request设置为使用代理
#         """
#         try:
#             self.redisclient = redis.Redis(REDIS_PROXY_HOST, REDIS_PROXY_PORT)
#             proxy = self.redisclient.srandmember(REDIS_PROXY_KEY)
#             proxyjson = json.loads(proxy)
#             ip = proxyjson["proxy"]
#             print ip
#             request.meta['proxy'] = "https://%s" % ip
#         except Exception, ee:
#             print '------------------------------', ee