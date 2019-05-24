# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/12'

from django.urls import path

from users.views import *

app_name ="users"

urlpatterns = [
    # path(r'login/', UserLogin.as_view(), name='login'),
    # path(r'logout/', UserLogout.as_view(), name='logout'),
    # path(r'register/', Register.as_view(), name='register'),
    # # ?P提取一个变量作为参数,code是变量, .*是过滤规则(正则表达式)
    # path(r'activate/(?P<activate_code>.*)/$', UserActivation.as_view(), name='activation'),
    # path(r'reset/', ResetPassword.as_view(), name='reset'),
    # path(r'verify/', EmailVeriCode.as_view(), name='verify'),
    # # path(r'verify/(?P<veri_email>.*)/$', EmailVeriCode.as_view(), name='verify'),
]