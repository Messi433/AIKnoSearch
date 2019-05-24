# _*_ encoding:utf-8 _*_
from django.db import models


# Create your models here


# 用户热搜词汇model
class TopUserPhrase(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"词汇名称")
    detail = models.CharField(max_length=20, verbose_name=u"词汇描述", default=u"软件开发术语")
    img_url = models.CharField(max_length=50, verbose_name=u"图片路径")

    class Meta:
        db_table = 'phrase_top_user'
        verbose_name = '用户热搜词汇'
        verbose_name_plural = verbose_name


''' 
    软件开发体系词汇
    一个词汇对象对应一个父类型，一个根类型，一个别名
'''


# 开发体系model
class DevelopmentSystem(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"词汇名称")
    alias = models.CharField(max_length=50, verbose_name=u"词汇别名", null=True)
    detail = models.CharField(max_length=70, verbose_name=u"词汇描述", default=u"软件开发术语")
    father_type = models.CharField(max_length=50, verbose_name=u"父词汇类型", null=True)
    root_type = models.CharField(max_length=50, verbose_name=u"根词汇类型", null=False)
    img_url = models.CharField(max_length=100, verbose_name=u"图片路径")
    system = models.CharField(choices=(
        ("ai", u'人工智能'), ("bigdata", u'大数据'), ("couldcompute", u'云计算'), ("blockchain", u'区块链'),
        ("database", u'数据库'), ("operation", u'运维/系统/服务器'), ("development", u'软件开发')), max_length=30,
        verbose_name=u'从属体系')

    class Meta:
        db_table = 'phrase_development_system'
        verbose_name = '开发体系词汇'
        verbose_name_plural = verbose_name


'''开发体系的子model'''


# 开发体系的开发工具model
class DevelopmentTools(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"词汇名称")
    alias = models.CharField(max_length=50, verbose_name=u"词汇别名", null=True)
    detail = models.CharField(max_length=70, verbose_name=u"词汇描述", default=u"软件开发术语")
    father_type = models.CharField(max_length=50, verbose_name=u"父词汇类型", null=True)
    root_type = models.CharField(max_length=50, verbose_name=u"根词汇类型", null=False)
    img_url = models.CharField(max_length=100, verbose_name=u"图片路径")
    system = models.CharField(choices=(
        ("ai", u'人工智能'), ("bigdata", u'大数据'), ("couldcompute", u'云计算'), ("blockchain", u'区块链'),
        ("database", u'数据库'), ("operation", u'运维/系统/服务器'), ("development", u'软件开发')), max_length=30,
        verbose_name=u'从属体系')

    class Meta:
        db_table = 'phrase_development_tools'
        verbose_name = '开发工具'
        verbose_name_plural = verbose_name


# 开发体系的开发框架或库model
class FrameworkAndLib(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"词汇名称")
    alias = models.CharField(max_length=50, verbose_name=u"词汇别名", null=True)
    detail = models.CharField(max_length=70, verbose_name=u"词汇描述", default=u"软件开发术语")
    father_type = models.CharField(max_length=50, verbose_name=u"父词汇类型", null=True)
    root_type = models.CharField(max_length=50, verbose_name=u"根词汇类型", null=False)
    img_url = models.CharField(max_length=100, verbose_name=u"图片路径")
    system = models.CharField(choices=(
        ("ai", u'人工智能'), ("bigdata", u'大数据'), ("couldcompute", u'云计算'), ("blockchain", u'区块链'),
        ("database", u'数据库'), ("operation", u'运维/系统/服务器'), ("development", u'软件开发')), max_length=30,
        verbose_name=u'从属体系')

    class Meta:
        db_table = 'phrase_framework_and_lib'
        verbose_name = '框架和库'
        verbose_name_plural = verbose_name


# 开发体系的编程语言model
class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"词汇名称")
    alias = models.CharField(max_length=50, verbose_name=u"词汇别名", null=True)
    detail = models.CharField(max_length=70, verbose_name=u"词汇描述", default=u"软件开发术语")
    father_type = models.CharField(max_length=50, verbose_name=u"父词汇类型", null=True)
    root_type = models.CharField(max_length=50, verbose_name=u"根词汇类型", null=False)
    img_url = models.CharField(max_length=100, verbose_name=u"图片路径")
    system = models.CharField(choices=(
        ("ai", u'人工智能'), ("bigdata", u'大数据'), ("couldcompute", u'云计算'), ("blockchain", u'区块链'),
        ("database", u'数据库'), ("operation", u'运维/系统/服务器'), ("development", u'软件开发')), max_length=30,
        verbose_name=u'从属体系')

    class Meta:
        db_table = 'phrase_language'
        verbose_name = '编程语言'
        verbose_name_plural = verbose_name


'''所有体系的全局model'''


# 对应词汇体系的相关网站
class WebSite(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"词汇名称")
    alias = models.CharField(max_length=50, verbose_name=u"词汇别名", null=True)
    detail = models.CharField(max_length=70, verbose_name=u"词汇描述", default=u"软件开发术语")
    father_type = models.CharField(max_length=50, verbose_name=u"父词汇类型", null=True)
    root_type = models.CharField(max_length=50, verbose_name=u"根词汇类型", null=False)
    img_url = models.CharField(max_length=100, verbose_name=u"图片路径")
    system = models.CharField(choices=(
        ("ai", u'人工智能'), ("bigdata", u'大数据'), ("couldcompute", u'云计算'), ("blockchain", u'区块链'),
        ("database", u'数据库'), ("operation", u'运维/系统/服务器'), ("development", u'软件开发')), max_length=30,
        verbose_name=u'从属体系')

    class Meta:
        db_table = 'phrase_website'
        verbose_name = '相关网站'
        verbose_name_plural = verbose_name
