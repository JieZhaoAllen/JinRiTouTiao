# -*- coding: utf-8 -*-
import time
import redis
import pymysql
import json
from urllib.parse import quote

def put_redis(data, name):
    """
    任务放入Reis中
    :param datas:放入的数据
    :param name:Redis Key名称
    :return:打印redis中的数量
    """
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_PARAMS['db'], encoding=REDIS_PARAMS['encoding'])
    data = json.dumps(data)
    result = r.lpush(name, data)
    print("Redis Add {0} Task Success".format(result))


def get_system_time_stamp():
    """
    获取系统当天的时间
    :return:
    """
    system_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # 转换成时间数组
    timeArray = time.strptime(system_time, "%Y-%m-%d")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return int(timestamp)


def get_parent_url(keyword):
    skurl_list = []
    db = pymysql.connect('192.168.0.12', 'root', 'inter3i.com', 'crawler', charset='utf8')
    # 创建游标
    cursor = db.cursor()
    # sql查询zjd表中数据
    sql = "select * from crawl_task WHERE project_name = '{0}'".format(keyword)

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()

        for row in results:
            skurl_dict = {}
            skurl_dict['keyword'] = row[1]
            skurl_dict['column'] = row[2]
            skurl_dict['customer_name'] = row[3]
            skurl_list.append(skurl_dict)
    except:
        print("Error: unable to fetch data")
        # 关闭数据库连接
    db.close()
    return skurl_list

def get_child_url(data):
    redis_key = 'TouTiao_GetParentUrl:start_urls'
    '''
    创建父URL列表
    :param keyword:
    :return:
    '''
    keyword = quote(data['keyword'])
    data.pop('keyword')
    for counts in range(0, 220, 20):
        url = 'https://www.toutiao.com/search_content/?offset=' + str(
            counts) + '&format=json&keyword=' + keyword + '&autoload=true&count=20&cur_tab=1&from=search_tab'
        print(url)
        data['url'] = url
        put_redis(data, redis_key)
        print('d')



if __name__ == '__main__':
    COLUMN1 = '今日头条'
    REDIS_HOST = '192.168.0.24'
    REDIS_PORT = '6379'
    REDIS_PARAMS = {
        "db": 2,
        "password": None,
        "encoding": 'utf-8',
    }

    keyword_list_boya = get_parent_url('博雅舆情')
    for data in keyword_list_boya:
        data['column1'] = COLUMN1
        get_child_url(data)
        print('d')









