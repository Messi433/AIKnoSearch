# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
'''所有用户的关键词搜索点击数排行'''


class UsersTopnKeyword(models.Model):
    keyword = models.CharField(max_length=50, verbose_name=u"词汇名称")
    score = models.IntegerField(default=1, verbose_name=u'关键词搜索次数')

    class Meta:
        db_table = 'users_topn_keyword'
        verbose_name = '所有用户关键词搜索数排行'
        verbose_name_plural = verbose_name


'''用户信息'''


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=100, verbose_name='昵称')
    # 用户头像图片,未设置则设置默认头像
    image = models.ImageField(upload_to=u'images/users/%Y/%m', default='images/users/default.png', max_length=100)

    class Meta:
        db_table = 'users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


'''邮箱验证'''


class EmailVerification(models.Model):
    code = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    type = models.CharField(choices=(("register", u'注册'), ("modify", "修改密码"), ("update", "更新邮箱账号")), max_length=10)  # 请求类型
    time = models.DateTimeField(default=datetime.now)  # 发送请求时间
    # 验证码激活状态
    status = models.IntegerField(choices=((0,u'验证码未激活'),(1,u'验证码已激活')),default=0)
    class Meta:
        verbose_name = '邮箱验证'
        verbose_name_plural = verbose_name


'''用户关键词信息'''


class UserKeyWord(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100, verbose_name=u"关键词")
    score = models.IntegerField(default=1, verbose_name=u'关键词搜索分数值')
    keyword_type = models.IntegerField(choices=((1, 'blog'), (2, 'course'), (3, 'graph')), default=1,
                                       verbose_name=u"搜索类型")
    join_time = models.DateTimeField(default=datetime.now, verbose_name=u"搜索时间")

    class Meta:
        verbose_name = '用户关键词信息'
        verbose_name_plural = verbose_name


'''用户关键词搜索记录'''


class UserHistory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100, verbose_name=u"关键词")
    history_score = models.IntegerField(default=1, verbose_name=u'关键词权值')
    join_time = models.DateTimeField(default=datetime.now, verbose_name=u"搜索时间")

    class Meta:
        verbose_name = '用户关键词搜索记录'
        verbose_name_plural = verbose_name
