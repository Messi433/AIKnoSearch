# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/11/28'

import xadmin
from xadmin import views

from .models import *

'''xadmin配置'''


class BaseSetting(object):
    enable_themes = True  # 主题设置开启
    use_bootswatch = True


class GlobalSetting(object):
    site_title = 'AIKno后台管理系统'  # 后台标题设置
    site_footer = 'AIKnoSearch'  # 页脚设置
    menu_style = 'accordion'  # app下的表折叠


'''model注册xadmin'''


class EmailVerificationAdmin(object):
    list_display = ['code', 'email', 'type', 'time','status']  # 显示列
    search_fields = ['code', 'email', 'type', 'time','status']  # 搜索字段
    list_filter = ['code', 'email', 'type', 'time','status']  # 过滤字段


class UserKeywordAdmin(object):
    list_display = ['user', 'keyword', 'score', 'keyword_type', 'join_time']  # 显示列
    search_fields = ['user', 'keyword', 'score', 'keyword_type', 'join_time']  # 搜索字段
    list_filter = ['user', 'keyword', 'score', 'keyword_type', 'join_time']  # 过滤字段


class UserHistoryAdmin(object):
    list_display = ['user', 'keyword', 'history_score', 'join_time']  # 显示列
    search_fields = ['user', 'keyword', 'history_score', 'join_time']  # 搜索字段
    list_filter = ['user', 'keyword', 'history_score', 'join_time']


class UsersTopnKeywordAdmin(object):
    list_display = ['keyword', 'score']  # 显示列
    search_fields = ['keyword', 'score']  # 搜索字段
    list_filter = ['keyword', 'score']  # 过滤字段


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(EmailVerification, EmailVerificationAdmin)
xadmin.site.register(UserKeyWord, UserKeywordAdmin)
xadmin.site.register(UserHistory, UserHistoryAdmin)
xadmin.site.register(UsersTopnKeyword, UsersTopnKeywordAdmin)
