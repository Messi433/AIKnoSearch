# _*_ encoding:utf-8 _*_
import json
import re

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q, Max
from elasticsearch import Elasticsearch
import redis

from search.models import BlogType, CourseType
from search.commons import search
from users.models import UserKeyWord, UserHistory
from commons.commons import get_topn_zip, set_topn
from phrase.phrase import TopUserPhrasePipeline, PhrasePipeline

'''创建es连接'''
server = Elasticsearch(hosts=['127.0.0.1'])
'''创建redis连接'''
r = redis.StrictRedis(host='localhost', password="k753951", decode_responses=True)


# 搜索
class Search(View):
    # 插入关键词以及最新的分数形成用户历史记录,执行搜索才可以进行插入set历史记录
    def set_history(self, keywords, user):
        '''
            定义key_name
            先判断缓存是否存在用户的相关key,存在则直接插入用户当前搜索的关键词，不存在则把用户搜索记录表返回到redis缓存,再执行关键词插入
            向key插入keyword并加入最新的score值,以表明这是用户最新的查询记录,每插入一次总score++.
        '''
        if user:
            # 用户名，用户搜索记录和最大分数值key_name
            username = user.username
            user_history = username + "_history"
            user_history_score = username + "_history_score"
            #
            if r.exists(user_history) & r.exists(user_history_score):
                '''缓存存在'''
                if keywords:
                    # 历史关键词总分数,每插入一个关键词,总分数加1
                    max_score = r.get(user_history_score)
                    # 有序集合方式插入当前总分数和数据,
                    r.zadd(user_history, max_score, keywords)
                    # 总分数加1
                    r.incr(user_history_score)
                else:
                    print('用户输入关键字为空！')
            else:
                '''用户数据表数据同步到redis缓存'''
                # 取出对应用户的搜索记录对象
                user_mysql_histories = UserHistory.objects.filter(user=user).order_by("history_score")
                '''数据库存在用户搜索记录,而缓存为空'''
                if user_mysql_histories:
                    # 返回搜索记录表到redis缓存
                    # 取出最大分数值max_score
                    max_score = user_mysql_histories.aggregate(history_score=Max("history_score"))["history_score"] + 1
                    # 用户搜索记录同步到redis缓存
                    for i in user_mysql_histories:
                        r.zadd(user_history, i.history_score, i.keyword)
                    # 插入max_score到redis缓存中
                    r.set(user_history_score, max_score)
                    # 插入关键词
                    if keywords:
                        max_score = r.get(user_history_score)
                        # 有序集合方式插入当前总分数和数据,
                        r.zadd(user_history, max_score, keywords)
                        # 总分数++
                        r.incr(user_history_score)
                    else:
                        print('用户输入关键字为空！')
                else:
                    '''数据库为空,缓存为空'''
                    if keywords:
                        # max_score初始化为1
                        max_score = 1
                        r.set(user_history_score, max_score)
                        # 有序集合方式插入当前总分数和数据,
                        r.zadd(user_history, max_score, keywords)
                        # 总分数加1
                        r.incr(user_history_score)
                    else:
                        print('用户输入关键字为空!')
        else:
            print('用户对象为空值')

    # 返回缓存中的关键词记录并排序
    def get_history(self, user):
        # 逆序排列，分数最高的最历史记录优先显示(即最新的历史记录)
        username = user.username
        user_history = username + "_history"
        user_history_score = username + "_history_score"
        # 返回所有历史记录
        histories = r.zrevrangebyscore(user_history, "+inf", "-inf")
        # 返回分数前五高的历史记录
        # histories = r.zrevrangebyscore(user_history, "+inf", "-inf", start=0, num=5)
        # 返回最大的分数值
        max_score = int(r.get(user_history_score))
        # 每个关键词的相应分数值
        history_score_list = []
        for histroy in histories:
            history_score_list.append(int(r.zscore(user_history, histroy)))
        history_zip = zip(histories, history_score_list)
        return history_zip

    def get(self, request):
        # 从前端获取用户关键字
        keywords_raw = request.GET.get("q", "")
        # 去除特殊字符
        keywords_raw = re.sub(r',|;|<|>', '', keywords_raw)
        # 截取左右空格
        keywords = keywords_raw.strip()
        # 获取用户搜索类型
        s_type = request.GET.get("s_type", "")
        if s_type == "blog" or s_type == "course":
            if request.user.is_authenticated:
                user = request.user
                # 向redis缓存插入用户搜索的关键词形成搜索记录
                self.set_history(keywords, user)
                # 从缓存中取出搜索记录
                history_zip = self.get_history(user)
                # 更新搜索记录到数据库
                for history, history_score in history_zip:
                    # 如果用户和其搜索的关键词存在,更新关键词，搜索类型对应对象的score值，否则插入新的数据
                    try:
                        user_history = UserHistory.objects.get(Q(user=user) & Q(keyword=history))
                    except Exception as e:
                        user_history = None

                    if user_history:
                        # 更新数据
                        user_history.user = user
                        user_history.keyword = history
                        user_history.history_score = history_score
                        user_history.save()
                    else:
                        # 插入数据
                        user_history = UserHistory()
                        user_history.user = user
                        user_history.keyword = history
                        user_history.history_score = history_score
                        user_history.save()
                # 从数据库中取出前10条历史记录
                history_objects = UserHistory.objects.filter(user=user).order_by("-history_score")[:10]
                histories = []
                for i in history_objects:
                    histories.append(i.keyword)
                # 向数据库中插入搜索类型和关键词
                if s_type == 'blog':
                    keyword_type = 1
                    try:
                        user_keywords = UserKeyWord.objects.get(user=user, keyword=keywords, keyword_type=keyword_type)
                    except Exception as e:
                        user_keywords = None
                    if user_keywords:
                        user_keywords.user = user
                        user_keywords.keyword = keywords
                        user_keywords.keyword_type = keyword_type
                        # 存在的关键词score ++
                        user_keywords.score = user_keywords.score + 1
                        user_keywords.save()
                    else:
                        user_keywords = UserKeyWord()
                        user_keywords.user = user
                        user_keywords.keyword = keywords
                        user_keywords.keyword_type = keyword_type
                        user_keywords.save()
                elif s_type == 'course':
                    keyword_type = 2
                    try:
                        user_keywords = UserKeyWord.objects.get(user=user, keyword=keywords, keyword_type=keyword_type)
                    except Exception as e:
                        user_keywords = None
                    if user_keywords:
                        user_keywords.user = user
                        user_keywords.keyword = keywords
                        user_keywords.keyword_type = keyword_type
                        # 同对象的score ++
                        user_keywords.score = user_keywords.score + 1
                        user_keywords.save()
                    else:
                        user_keywords = UserKeyWord()
                        user_keywords.user = user
                        user_keywords.keyword = keywords
                        user_keywords.keyword_type = keyword_type
                        user_keywords.save()
                elif s_type == 'graph':
                    pass
            else:
                histories = None
            # 向缓存中插入所有用户关键词形成搜索热点
            set_topn(keywords)
            # 从缓存中取出搜索热点
            topn_zip = get_topn_zip()
            # 获取当前页数
            current_page = request.GET.get("p", "1")
            try:
                current_page = int(current_page)
            except:
                current_page = 1

            # 调用search()返回相关数据
            hit_list, total_numbers, page_numbers, query_time = search(s_type, keywords, current_page)
            # 取出关键词词汇体系数据
            phrase_dicts = PhrasePipeline().process_phrase(keyword=keywords)

            # 更新用户搜索热点数据库
            TopUserPhrasePipeline().update_users_keywords()

            return render(request, 'main.html',
                          {"hit_list": hit_list, "keywords": keywords, "keywords_raw": keywords_raw,
                           "histories": histories, "current_page": current_page, "total_numbers": total_numbers,
                           "page_numbers": page_numbers, "query_time": query_time, "topn_zip": topn_zip,
                           "s_type": s_type, "phrase_dicts": phrase_dicts})
        else:
            return HttpResponse("搜索异常，请输入正确的搜索类型")


# 搜索建议
class SearchSuggest(View):
    # 获取用户传入的关键词和搜索类型
    def get(self, request):
        keywords = request.GET.get('s', '')  # 从get请求中获得关键词
        current_type = request.GET.get('s_type', '')  # 从get请求中获得搜索类型

        if current_type == 'blog':
            re_datas = []  # 返回的搜索建议不止一条
            if keywords:
                resp_blog = BlogType.search()  # 调用index的search()返回给s
                # 生成搜索建议
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                resp_blog = resp_blog.suggest("bole_suggest", keywords, completion={
                    "field": "suggest",
                    "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })

                suggestions_blog = resp_blog.execute()
                for suggest in suggestions_blog.suggest.bole_suggest[0].options[:10]:
                    source = suggest._source
                    re_datas.append(source['title'])
            return HttpResponse(json.dumps(re_datas), content_type="application/json")
        elif current_type == 'course':
            re_datas = []  # 返回的搜索建议不止一条
            if keywords:
                resp_course = CourseType.search()  # 调用index的search()返回给s
                # 生成搜索建议
                """fuzzy模糊搜索, fuzziness 编辑距离, prefix_length前面不变化的前缀长度"""
                resp_course = resp_course.suggest("course_suggest", keywords, completion={
                    "field": "suggest",
                    "fuzzy": {
                        "fuzziness": 1
                    },
                    "size": 5
                })
                suggestions_course = resp_course.execute()

                for suggest in suggestions_course.suggest.course_suggest[0].options[:10]:
                    source = suggest._source
                    re_datas.append(source['sub_title'])
            return HttpResponse(json.dumps(re_datas), content_type="application/json")
        # bug
        elif current_type == "graph":
            pass
