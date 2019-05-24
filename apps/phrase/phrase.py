# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/20'

import re

from django.db.models import Q
import jieba

from .models import *
from commons.commons import get_users_keywords,get_random_objs


class TopUserPhrasePipeline:
    # 用户热点词汇
    def update_users_keywords(self):
        # 获取用户热点关键词
        keywords = get_users_keywords()
        # 验证关键词是否是词汇术语
        for keyword in keywords:
            # 词汇model列表
            model_list = [DevelopmentSystem, WebSite, DevelopmentTools, FrameworkAndLib, Language]
            # 遍历所有phrase_model
            for model in model_list:
                # 查询关键词是否是phrase_model中的词汇
                model_obj = self.query_top_phrase(model, keyword)
                if model_obj:
                    self.db_operate(model_obj)

    def query_top_phrase(self, model, keyword):
        try:
            model_obj = model.objects.get(Q(name=keyword) | Q(alias=keyword))
            return model_obj
        except Exception as e:
            return None

    # 数据表更新或插入操作
    def db_operate(self, model_obj):
        name = model_obj.name
        detail = model_obj.detail
        img_url = model_obj.img_url
        try:
            # 查询该词汇是否在top_user_phrase数据表中
            top_phrase_obj = TopUserPhrase.objects.get(name=name)
        except Exception as e:
            top_phrase_obj = None
        # 如果查询到相应记录则更新,没有查到则插入记录
        if top_phrase_obj:
            top_phrase_obj.name = name
            top_phrase_obj.detail = detail
            top_phrase_obj.img_url = img_url
            top_phrase_obj.save()
        else:
            top_phrase_obj = TopUserPhrase()
            top_phrase_obj.name = name
            top_phrase_obj.detail = detail
            top_phrase_obj.img_url = img_url
            top_phrase_obj.save()


class PhrasePipeline:
    # 词汇验证
    def process_phrase(self, keyword):
        # 词汇model列表
        model_list = [DevelopmentSystem, WebSite, DevelopmentTools, FrameworkAndLib, Language]
        # 查询关键词是否存在某个词汇数据表
        for model in model_list:
            query_obj, sub_root_objs_dict = self.query_keyword(keyword=keyword, model=model)
            if query_obj:
                # 词汇所属model
                phrase_model = model
                # 返回相应类型的查询词汇
                phrase_dicts = self.return_phrase(query_obj, sub_root_objs_dict, phrase_model)
                return phrase_dicts

    # 从查询model关键词以及子model root_type关键词
    '''
    bug若关键词带有前缀如Ruby faker若在前面的体系查询不到该关键词，
    则截取Ruby查询Ruby返回Ruby的体系，而该关键词体系在后面
    '''

    def query_keyword(self, keyword, model):
        # 查询并返回该model对应数据表的数据对象
        try:
            query_obj = model.objects.get(Q(name=keyword) | Q(alias=keyword))
            if query_obj:
                sub_root_objs_dict = self.query_root_type(model, query_obj)
                return query_obj, sub_root_objs_dict
        # 原始关键词查询为空抛异常
        except Exception as e:
            # 截取关键词的字母
            letter_keyword = self.split_letter(keyword=keyword)
            try:
                query_obj = model.objects.get(Q(name=letter_keyword) | Q(alias=letter_keyword))
                if query_obj:
                    sub_root_objs_dict = self.query_root_type(model, query_obj)
                    return query_obj, sub_root_objs_dict
            # 字母关键词查询为空抛异常
            except Exception as e:
                # 截取关键词汉字
                character_keyword = self.split_character(keyword=keyword)
                # 汉字分词器分词
                if character_keyword == '':
                    return None, None
                else:
                    characters = list(jieba.cut(character_keyword))
                    # 循环分词列表,若查询到关键词则return
                    for index, character in enumerate(characters):
                        try:
                            query_obj = model.objects.get(Q(name=character) | Q(alias=character))
                            if query_obj:
                                sub_root_objs_dict = self.query_root_type(model, query_obj)
                                return query_obj, sub_root_objs_dict
                        # 汉字关键词查询为空抛异常
                        except Exception as e:
                            # 循环到汉字分词的最后一个元素仍未查出,bug截取所有空格查询,或者让名词有空格
                            if index == len(characters) - 1:
                                print("侧边栏关键词查询为空")
                                return None, None

    # 查询子model root_type关键词
    def query_root_type(self, model, query_obj):
        # 如果model是开发体系父model
        if model == DevelopmentSystem:
            # 查询子表中是否对应根类词汇
            root_phrase = query_obj.root_type
            # 对应开发工具数据表对象list
            tool_root_objs = DevelopmentTools.objects.filter(root_type__icontains=root_phrase)
            # 对应开发框架或库数据表对象list
            lib_root_objs = FrameworkAndLib.objects.filter(root_type__icontains=root_phrase)
            # 查询的对象为空
            if tool_root_objs.count() == 0 | lib_root_objs.count() == 0:
                return None
            else:
                return locals()
        else:
            return None
        # elif model == DataBaseSystem:
        # bug
        #     pass

    # 提取关键词英文字母
    def split_letter(self, keyword):
        # 只匹配第一个英文字符串,若无英文字母则返回相应关键词
        try:
            re_keyword = re.match(r'.*?([A-Za-z]*[A-Za-z]).*', keyword).group(1)
        except Exception as e:
            re_keyword = keyword
        return re_keyword

    # 提取关键词汉字
    def split_character(self, keyword):
        try:
            re_keyword = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", keyword)
        except Exception as e:
            re_keyword = keyword
        return re_keyword

    '''
        侧边栏返回的词汇集合:
        词汇对应model的father_type、root_type词汇集合，
        如果有对应字model，也返回子model的root_type词汇集合
        相关网站model对应体系的root_type词汇集合
    '''

    def return_phrase(self, query_obj, sub_root_objs_dict, model):
        # 返回词条的dict的列表
        phrase_dicts = []
        # 词汇对象的相应字段值
        phrase_system = query_obj.system
        phrase_father_type = query_obj.father_type
        # 对应model数据表的父类根类词汇集
        phrase_father_dict, phrase_root_dict = self.process_term_phrase(model, query_obj)
        if phrase_father_type:
            # 添加到dict列表
            phrase_dicts.append(phrase_father_dict)
            phrase_dicts.append(phrase_root_dict)
        else:
            phrase_dicts.append(phrase_root_dict)
        # 若子model对象存在
        if sub_root_objs_dict:
            # 对应子model数据表的根类词汇集
            # 若词汇体系是development
            if phrase_system == 'development':
                # db对象
                tool_root_objs = get_random_objs(sub_root_objs_dict["tool_root_objs"], 12)
                lib_root_objs = get_random_objs(sub_root_objs_dict["lib_root_objs"], 12)
                tool_root_objs_type = tool_root_objs[0].root_type
                lib_root_objs_type = lib_root_objs[0].root_type
                tool_root_objs_dict = PhraseObjFormat().return_dicts(tool_root_objs, tool_root_objs_type)
                lib_root_objs_dict = PhraseObjFormat().return_dicts(lib_root_objs, lib_root_objs_type)
                # 添加到dict列表
                phrase_dicts.append(tool_root_objs_dict)
                phrase_dicts.append(lib_root_objs_dict)
            # 若词汇体系是database
            elif phrase_system == 'database':
                # bug
                pass
        # 相关网站根类词汇集合
        if model == WebSite:
            pass
        else:
            website_objs = get_random_objs(WebSite.objects.filter(system=phrase_system), 12)
            website_root_type = website_objs[0].root_type
            website_root_dict = PhraseObjFormat().return_dicts(website_objs, website_root_type)
            # 添加到dict列表
            phrase_dicts.append(website_root_dict)
        # 其他人还搜词条从验证词汇获得
        # 取该表前16条数据对象
        others_search_objs = TopUserPhrase.objects.all()[:16]
        if others_search_objs.count() == 0:
            pass
        else:
            others_search_dict = PhraseObjFormat().return_dicts(others_search_objs, "其他人还搜")
            # 添加到dict列表
            phrase_dicts.append(others_search_dict)
        return phrase_dicts

    # 处理父类词汇,根类词汇
    def process_term_phrase(self, model, model_obj):
        # 判断父类词汇对象是否存在,因为词汇体系中只允许父类词汇对象可以为空
        # 与该词汇同父类的词汇
        father_type = model_obj.father_type
        root_type = model_obj.root_type
        if father_type:
            # father_type词汇集合,词汇图片集合,词汇说明集合
            father_type_objs = get_random_objs(model.objects.filter(father_type=father_type), 12)
            father_dict = PhraseObjFormat().return_dicts(objs=father_type_objs, title=father_type)
        else:
            father_dict = None
        # 与该词汇同根类的词汇
        # root_type词汇集合,词汇图片集合,词汇说明集合
        root_type_objs = get_random_objs(model.objects.filter(root_type=root_type), 12)
        root_dict = PhraseObjFormat().return_dicts(objs=root_type_objs, title=root_type)
        return father_dict, root_dict


# 词汇对象数据格式化
class PhraseObjFormat:
    # 将数据打包成dict并返回
    def return_dicts(self, objs, title):
        # 提取objs数据
        obj_list, obj_img_list, obj_detail_list = self.get_objects_data(objs)
        # 压缩并分割objs数据
        obj_zip_p, obj_zip_s = self.zip_list(obj_list, obj_img_list, obj_detail_list)
        # 打包数据成dict
        obj_dict = {"title": title, "zip_p": obj_zip_p, "zip_s": obj_zip_s}
        return obj_dict

    # 从数据表对象中提取出数据
    def get_objects_data(self, objs):
        names = []
        img_urls = []
        details = []
        for obj in objs:
            name = obj.name
            img_url = obj.img_url
            detail = obj.detail
            names.append(name)
            img_urls.append(img_url)
            details.append(detail)
        return names, img_urls, details

    # 压缩数据
    def zip_list(self, content_list, img_list, detail_list):
        # 分割list，前4个元素为一组,其余为一组
        contents_p, contents_s = self.deal_list(content_list)
        imgs_p, imgs_s = self.deal_list(img_list)
        details_p, details_s = self.deal_list(detail_list)
        # 压缩分割前后的list
        if len(contents_s) == 0 | len(imgs_s) == 0 | len(details_s) == 0:
            zip_p = zip(contents_p, imgs_p, details_p)
            zip_s = None
            return zip_p, zip_s
        else:
            zip_p = zip(contents_p, imgs_p, details_p)
            zip_s = zip(contents_s, imgs_s, details_s)
            return zip_p, zip_s
        # 返回处理的词汇列表

    def deal_list(self, list):
        # 返回分割list变量
        list_local = self.split_list(4, list)
        # 返回分割的list
        prefix = list_local["prefix"]
        suffix = list_local["suffix"]
        return prefix, suffix

    # 列表分割
    def split_list(self, index, list):
        last_index = len(list)
        # 返回list中第一个到第index个元素集合
        prefix = list[0:index]
        # 返回index到最后一个元素个元素集合
        suffix = list[index:last_index]
        return locals()
