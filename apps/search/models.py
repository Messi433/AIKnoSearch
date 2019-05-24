from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text,Index,Integer
from elasticsearch_dsl.analysis import CustomAnalyzer

from elasticsearch_dsl import connections

'''创建连接'''
connections.create_connection(hosts=['127.0.0.1:9200'], timeout=20)

#重写方法否则报错
class CustomAnalyzer(CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer =CustomAnalyzer("ik_smart",filter=["lowercase"])

'''索引初始化'''
class BlogType(Document):
    suggest =  Completion(analyzer=ik_analyzer)

    title = Text(analyzer="ik_max_word")
    post_date = Date()
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")

    class Index:
        name = 'blog_index'
        settings = {
            "number_of_shards": 5,
            "number_of_replicas":1
        }

class CourseType(Document):
    suggest =  Completion(analyzer=ik_analyzer)

    sub_title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    content = Text(analyzer="ik_smart")

    class Index:
        name = 'course_index'
        settings = {
            "number_of_shards": 5,
            "number_of_replicas":1
        }
if __name__ == "__main__":
    BlogType.init()
    CourseType.init()