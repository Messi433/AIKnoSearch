import time
import datetime

from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View
import redis

from users.models import *
from commons.commons import get_topn, delete_redis_key, get_keywords, get_history, process_hits
from search.commons import pre_search

from phrase.phrase import TopUserPhrasePipeline

# 创建redis连接
r = redis.StrictRedis(host='localhost', password="k753951", decode_responses=True)


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            histories = get_history(user=user)
            keywords, keyword_types = get_keywords(user=user)
            k_zip = zip(keywords, keyword_types)
            # 5个关键词所返回索引数据的list的list
            multiple_hits = []
            for keyword, keyword_type in k_zip:
                # 5条关键词*每个关键词从es中返回2条记录 = 10条记录
                hit_list = pre_search(keyword_type=keyword_type, keyword=keyword)
                multiple_hits.append(hit_list)
            data = process_hits(multiple_hits)
        else:
            histories = None
            data = None
        # 获得所有用户的关键词搜索数
        topn = get_topn()
        # 更新用户热搜关键词
        TopUserPhrasePipeline().update_users_keywords()
        # 清除数据库中邮箱验证信息

        return render(request, "index.html", {"histories": histories, "topn": topn, "data": data})


# 清空历史记录
class ClearHistory(View):
    def get(self, request):
        if request.user.is_authenticated:
            # 删除缓存历史记录
            username = request.user.username
            delete_redis_key(username)
            # 删除数据库中该user的搜索记录
            UserHistory.objects.filter(user=request.user).delete()
            return redirect(reverse('index'))
        else:
            pass

# bug
# 清除数据库中邮箱验证信息
