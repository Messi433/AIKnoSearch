# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/7'

import random
import string
import re

'''生成随机字符串'''


def return_random_str(type):
    if type == 'email':
        str = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 6))
        return str
    elif type == 'number':
        number = ''.join(random.sample('0123456789', 6))
        return number
    elif type == 'email_link':
        multi_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        return multi_str
    else:
        return 'error_code'


'''邮箱正则匹配'''


def email_match(str):
    # 传入待处理的字符串和规则
    str_match = re.match(r'.*(@.*).*', str).group(1)
    return str_match


'''常用邮箱登录入口匹配'''


def email_login_access(email):
    # 邮箱后缀匹配
    email_suffix = email_match(email)
    email_dicts = {'@gmail.com': 'https://accounts.google.com/signin ', '@qq.com': 'https://mail.qq.com/',
                   '@aliyun.com': 'https://mail.aliyun.com/', '@sina.com': 'https://mail.sina.com.cn/',
                   '@126.com': 'https://mail.126.com/ ', '@163.com': 'https://mail.163.com/',
                   '@tom.com': 'http://mail.tom.com/', '@outlook.com': 'https://login.live.com/',
                   '@yahoo.com': 'https://login.yahoo.com/'}
    for key in email_dicts.keys():
        if key == email_suffix:
            return email_dicts[key]


'''正则处理字符串'''
#截取字符串替换为空格
def sub_space(str,rule):
    sub_str = re.sub(rule,'',str)
    return sub_str

# 清理没用的字符
def clean_data(str):
    data = re.sub(r'\r|\n|\t|\xa0',"",str)
    return data

'''从list中随机选取num个独立的的元素'''
def select_from_list(list,num):
    return random.sample(list,num)



