# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/17'

from datetime import datetime

from elasticsearch import Elasticsearch

from search.models import BlogType, CourseType
from commons.utils import clean_data

# 创建es连接
es_server = Elasticsearch(hosts=['127.0.0.1'])


# 使用es DSL语言执行查询
def search(s_type, keyword, current_page):
    if s_type == "blog":
        start_time = datetime.now()  # 查询开始时间
        resp_blog = es_server.search(
            index="blog_index",
            body={
                "query": {
                    "multi_match": {
                        "query": keyword,
                        "fields": ["title", "content"],
                        "fuzziness": 1
                    }
                },
                "from": (current_page - 1) * 10,  # "from": 0 从第一条数据开始,每一页返回记录为10
                "size": 10,

                "highlight": {
                    "pre_tags": ["<span class='highlight'>"],
                    "post_tags": ["</span>"],
                    "fields": {
                        "title": {},
                        "content": {},
                    }
                }
            }
        )

        end_time = datetime.now()  # 查询结束时间
        query_time = (end_time - start_time).total_seconds()  # 计算查询返回记录的时间

        total_numbers = resp_blog['hits']['total']  # 返回的总记录数

        # 页码数计算 每10条记录作为1页
        # 最后一页的记录数整除10，总数/10,反之/10加1
        if (current_page % 10) > 0:
            page_numbers = int((total_numbers / 10) + 1)
        else:
            page_numbers = int(total_numbers / 10)

        # 抽取从索引中搜索的数据
        hit_list = []
        for hit in resp_blog['hits']['hits']:
            hit_dict = {}
            if 'title' in hit['highlight']:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]
            '''高亮出现排版bug，因为多加了一个标签导致排版有问题'''
            # if 'content' in hit['highlight']:
            #     # hit_dict["content"] = "".join(hit["highlight"]["content"])[:100]  # content内容太多截断200
            #     # hit_dict["content"] = clean_data("".join(hit["highlight"]["content"])[:100])
            # else:
            hit_dict["content"] = clean_data(hit["_source"]["content"][:150])
            hit_dict["post_date"] = hit["_source"]["post_date"]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]
            hit_dict["index"] = hit["_index"]
            hit_list.append(hit_dict)

        return hit_list, total_numbers, page_numbers, query_time
    elif s_type == 'course':
        start_time = datetime.now()  # 查询开始时间
        # 查询course
        resp_course = es_server.search(
            index="course_index",
            body={
                "query": {
                    "multi_match": {
                        "query": keyword,
                        "fields": ["sub_title", "content"],  # 搜索sub_title,content
                        "fuzziness": 1
                    }
                },
                "from": (current_page - 1) * 10,  # "from": 0 从第一条数据开始,每一页返回记录为10
                "size": 10,

                "highlight": {
                    "pre_tags": ["<span class='highlight'>"],
                    "post_tags": ["</span>"],
                    "fields": {
                        "sub_title": {},
                        "content": {},
                    }
                }
            }
        )
        end_time = datetime.now()  # 查询结束时间
        query_time = (end_time - start_time).total_seconds()  # 计算查询返回记录的时间

        total_numbers = resp_course['hits']['total']  # 返回的总记录数
        '''页码数计算'''
        '''最后一页的记录数整除10，总数/10,反之/10加1'''
        if (current_page % 10) > 0:
            page_numbers = int((total_numbers / 10) + 1)
        else:
            page_numbers = int(total_numbers / 10)

        '''抽取从索引中搜索的数据'''
        hit_list = []
        for hit in resp_course['hits']['hits']:
            hit_dict = {}
            # 关键字高亮
            if 'sub_title' in hit['highlight']:
                hit_dict["sub_title"] = "".join(hit["highlight"]["sub_title"])[:70]
            else:
                hit_dict["sub_title"] = hit["_source"]["sub_title"][:70]
            hit_dict["content"] = clean_data(hit["_source"]["content"][:150])
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]
            hit_dict["index"] = hit["_index"]
            hit_list.append(hit_dict)

        return hit_list, total_numbers, page_numbers, query_time
    elif s_type == 'graph':
        # 预留功能接口
        pass
    else:
        print("搜索异常，请输入正确的type")


# 关键词预搜索
def pre_search(keyword_type, keyword):
    if keyword_type == 1:
        resp_blog = es_server.search(
            index="blog_index",
            body={
                "query": {
                    "multi_match": {
                        "query": keyword,
                        "fields": ["title", "content"],
                        "fuzziness": 1
                    }
                },
                "from": 0,  # 返回前2条数据
                "size": 2,
            }
        )
        # 抽取从索引中搜索的数据
        hit_list = []
        for hit in resp_blog['hits']['hits']:
            hit_dict = {}
            hit_dict["title"] = hit["_source"]["title"]
            hit_dict["content"] = clean_data("".join(hit["_source"]["content"])[:100])
            hit_dict["post_date"] = hit["_source"]["post_date"]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]
            hit_dict["index"] = hit["_index"]
            hit_list.append(hit_dict)

        return hit_list
    elif keyword_type == 2:
        # 查询course
        resp_course = es_server.search(
            index="course_index",
            body={
                "query": {
                    "multi_match": {
                        "query": keyword,
                        "fields": ["sub_title"],  # 搜索sub_title有的内容
                        "fuzziness": 1
                    }
                },
                "from": 0,  # 返回前2条数据
                "size": 2,

            }
        )
        # 抽取搜索的数据
        hit_list = []
        for hit in resp_course['hits']['hits']:
            hit_dict = {}
            hit_dict["sub_title"] = hit["_source"]["sub_title"]
            hit_dict["content"] = clean_data("".join(hit["_source"]["content"])[:100])
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]
            hit_dict["index"] = hit["_index"]
            hit_list.append(hit_dict)

        return hit_list
    elif keyword_type == 3:
        pass
    else:
        print("预搜索异常")
