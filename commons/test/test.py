# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/7'

import time
import re
import datetime

'''
    邮箱验证码失效原理：取出数据库时间正则，和时间处理转换为时间戳相减大于15min=900,验证码失效
'''
# 时间戳
# current_time = time.time()
# print(current_time)
# 格式化的时间
# localtime = time.asctime( time.localtime(time.time()) )
# print(localtime)
# 格式化成2016-03-20 11:45:39形式
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# 格式化成Sat Mar 28 22:24:24 2016形式
# print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
b = "2018-12-21 19:32:35.790931"
c = "2018-12-21 19:32:37.790931"


def time_produce(str):
    origin_datetime = re.search('(.*[.])', str).group(1)
    datetime = re.sub(r'[.]', '', origin_datetime)
    return datetime


# b = time_produce(b)
# c = time_produce(c)
# print(b)
# print(c)

# now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# now_time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# # print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))
now_time3 = datetime.datetime.now()
#
# # 转换为时间戳
# time1 = time.mktime(time.strptime(b, "%Y-%m-%d %H:%M:%S"))
# time2 = time.mktime(time.strptime(c, "%Y-%m-%d %H:%M:%S"))
# print(time2 - time1)


def calculate_delta_time(date_time):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
    now_time_strip = time.mktime(time.strptime(now_time, "%Y-%m-%d %H:%M:%S"))
    datetime_strip = time.mktime(time.strptime(date_time, "%Y-%m-%d %H:%M:%S"))
    delta_timestrip = now_time_strip - datetime_strip
    return delta_timestrip

print(calculate_delta_time(now_time3))
