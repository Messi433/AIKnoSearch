# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/17'

import random
import datetime
import time

import redis

from users.models import *

# 创建redis连接
r = redis.StrictRedis(host='localhost', password="k753951", decode_responses=True)


# 存储所有的关键词形成热门搜索
def set_topn(keyword):
    if keyword == '':
        print('用户输入关键字为空！')
    else:
        if r.exists("topn"):
            # 将用户输入的关键字做为key，每执行一次key的score++，实现关键字加1操作
            r.zincrby("topn", keyword)
            # 缓存记录数
            topn_num = r.zcard("topn")
            # redis緩存中的数据量是100的倍数,则将redis缓存数据同步到数据库
            if topn_num % 100 == 0:
                # 从缓存中取出topn的成员数,以score值升序排列
                topn_keywords = r.zrange("topn", 0, -1)
                # topn的成员分数值list
                scores = []
                # 从缓存中取出topn成员数的分数值score升序排列
                for topn_keyword in topn_keywords:
                    # 添加分数值由高到低
                    scores.append(int(r.zscore('topn', topn_keyword)))
                # 压缩topn和score
                topn_zip = zip(topn_keywords, scores)
                for topn_keyword, score in topn_zip:
                    # 同步到数据库
                    try:
                        topn_keyword_obj = UsersTopnKeyword.objects.get(keyword=topn_keyword)
                        topn_keyword_obj.keyword = topn_keyword
                        topn_keyword_obj.score = score
                        topn_keyword_obj.save()
                    except Exception as e:
                        topn_keyword_obj = UsersTopnKeyword()
                        topn_keyword_obj.keyword = topn_keyword
                        topn_keyword_obj.score = score
                        topn_keyword_obj.save()


# 返回所有插入过的关键词及分数的zip(Search View)
def get_topn_zip():
    # 返回top10关键词
    topn = r.zrevrangebyscore("topn", "+inf", "-inf", start=0, num=10)
    # 返回top10分数值
    score_list = []
    for topi in topn:
        score_list.append(int(r.zscore('topn', topi)))
    # 压缩topn和score
    topn_zip = zip(topn, score_list)
    return topn_zip


# 所有用户的关键词搜索数topn(Front View)
def get_topn():
    # 若redis中不存在topn
    if r.exists("topn"):
        # 从redis缓存中取出搜索数score前10的关键词
        top_ten = r.zrevrangebyscore("topn", "+inf", "-inf", start=0, num=10)
        return top_ten
    else:
        # 同步数据库数据到redis缓存
        topn = UsersTopnKeyword.objects.all().order_by("-score")
        for topi in topn:
            keyword = topi.keyword
            score = topi.score
            r.zadd("topn", score, keyword)
        top_ten = r.zrevrangebyscore("topn", "+inf", "-inf", start=0, num=10)
        return top_ten


# 删除相关redis缓存
def delete_redis_key(username):
    user_history = username + "_history"
    user_history_score = username + "_history_score"
    r.delete(user_history)
    r.delete(user_history_score)


# 从数据库中随机取出5条用户关键词
def get_keywords(user):
    objs = list(UserKeyWord.objects.filter(user=user))
    if len(objs) > 5:
        random_objs = get_random_objs(objs, 5)
        keywords = []
        keyword_types = []
        for i in random_objs:
            keywords.append(i.keyword)
            keyword_types.append(i.keyword_type)
        return keywords, keyword_types
    else:
        keywords = []
        keyword_types = []
        for i in objs:
            keywords.append(i.keyword)
            keyword_types.append(i.keyword_type)
        return keywords, keyword_types


# 抽取随机对象
def get_random_objs(objs, rule):
    objs = list(objs)
    # 如果对象list多于12个元素
    if len(objs) > rule:
        # 随机从对象list抽取12个
        random_objs = random.sample(objs, rule)
        return random_objs
    else:
        return objs


# 从数据库中取出前10条历史记录
def get_history(user):
    history_objects = UserHistory.objects.filter(user=user).order_by("-history_score")[:10]
    histories = []
    for i in history_objects:
        histories.append(i.keyword)
    return histories


# 预搜索数据处理
def process_hits(multiple_hits):
    dict_list = []
    for hits in multiple_hits:
        for hit_dict in hits:
            dict_list.append(hit_dict)
    # 通过数据的score属性进行数据的降序排序
    dict_list.sort(key=lambda i: i["score"], reverse=True)
    dict_len = len(dict_list)
    if dict_len < 6:
        return_list = None
    else:
        # 返回给前端6条分数最高的数据
        return_list = dict_list[:6]

    return return_list


# 基于用户的热点搜索
def get_users_keywords():
    '''
    取所有用户的前三个热点词，存到一个list,再按照score降序排列,
    按照需求取一定数量的关键词,形成基于用户的搜索热点
    '''
    # 取出所有的用户对象
    users = UserProfile.objects.all()
    # 初始化一个存放所有用户热点keyword的空列表和空集合,空集合是keyword去重
    keyword_list = []
    keyword_set = set()
    # 遍历所有用户对象
    for user in users:
        # 从UserKeyWord表中取每个用户对应score前三的keyword对象作为热点keywords
        keyword_objects = UserKeyWord.objects.filter(user=user).order_by("-score")[:3]
        # 遍历每个用户取出的keyword对象
        for k in keyword_objects:
            keyword = k.keyword
            # 添加热点keyword到keyword_list
            keyword_list.append(keyword)
    # 遍历所有的热点keyword存入集合实现keyword去重
    for keyword in keyword_list:
        keyword_set.add(keyword)
    keywords = list(keyword_set)
    return keywords



