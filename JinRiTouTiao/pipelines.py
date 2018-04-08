# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class JinritoutiaoPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    """
    采用同步的机制写入mysql
    """
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'weibo_info_eb', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into toutiao(page_url, screen_name, post_title)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["page_url"], item["screen_name"], item["post_title"]))
        self.conn.commit()



class MySqlTwistedPipline(object):
    """
    采用异步的机制写入mysql
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)


    def process_item(self, item, spider):
        """
        使用Twisted将mysql变成异步插入数据
        :param item:
        :param spider:
        :return:
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = insert_sql = """
            insert into toutiao(page_url, screen_name, post_title)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_sql, (item["page_url"], item["screen_name"], item["post_title"]))