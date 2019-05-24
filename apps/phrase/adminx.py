# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/11/28'

import xadmin

from .models import *

'''model注册xadmin'''


# 软件开发体系Admin
class DevelopmentSystemAdmin(object):
    list_display = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 显示列
    search_fields = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 搜索字段
    list_filter = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 过滤字段


class LanguageAdmin(object):
    list_display = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 显示列
    search_fields = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 搜索字段
    list_filter = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 过滤字段


class DevelopmentToolsAdmin(object):
    list_display = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 显示列
    search_fields = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 搜索字段
    list_filter = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 过滤字段


class FrameworkAndLibAdmin(object):
    list_display = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 显示列
    search_fields = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 搜索字段
    list_filter = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']


# 数据库体系Admin

# 相关网站Admin
class WebSiteAdmin(object):
    list_display = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 显示列
    search_fields = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 搜索字段
    list_filter = ['name', 'alias', 'detail', 'father_type', 'root_type', 'img_url', 'system']  # 过滤字段


# 用户热点词汇Admin
class TopUserPhraseAdmin(object):
    list_display = ['name', 'detail', 'img_url']  # 显示列
    search_fields = ['name', 'detail', 'img_url']  # 搜索字段
    list_filter = ['name', 'detail', 'img_url']  # 过滤字段


# 软件开发体系
xadmin.site.register(DevelopmentSystem, DevelopmentSystemAdmin)
xadmin.site.register(Language, LanguageAdmin)
xadmin.site.register(DevelopmentTools, DevelopmentToolsAdmin)
xadmin.site.register(FrameworkAndLib, FrameworkAndLibAdmin)
# 数据库体系

# 相关网站
xadmin.site.register(WebSite, WebSiteAdmin)
# 用户热点词汇
xadmin.site.register(TopUserPhrase, TopUserPhraseAdmin)
