from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
import xadmin

from front.views import *
from search.views import SearchSuggest, Search
from users.views import *

urlpatterns = [
    # 第三方app相关urls
    path(r'xadmin/', xadmin.site.urls),
    path(r'captcha/', include('captcha.urls')),
    # 首页相关urls
    path(r'', IndexView.as_view(), name='index'),
    path(r'clear_history/', ClearHistory.as_view(), name='clear_history'),
    # 搜索相关urls
    path(r'suggest/', SearchSuggest.as_view(), name='suggest'),
    path(r'search/', Search.as_view(), name='search'),
    # 登录注册相关urls
    path(r'login/', UserLogin.as_view(), name='login'),
    path(r'logout/', UserLogout.as_view(), name='logout'),
    path(r'register/', Register.as_view(), name='register'),
    # ?P提取一个变量作为参数,code是变量, .*是过滤规则(正则表达式)，path()全匹配无法正则而url()可以
    url(r'^activate/(?P<activate_code>.*)/$', UserActivation.as_view(), name='activation'),
    path(r'reset/', ResetPassword.as_view(), name='reset'),
    path(r'verify/', EmailVeriCode.as_view(), name='verify'),

]

# 状态码错误跳转配置
handler500 = 'users.views.server_error'
# handler404 = 'users.views.page_not_found'
# handler403 = 'users.views.permission_denied'
