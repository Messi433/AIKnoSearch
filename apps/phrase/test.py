# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/19'
import jieba
import random


def obj_name():
    character_keyword = "软件前端开发哈哈笑1234xxxl"
    characters = list(jieba.cut(character_keyword))
    for index, i in enumerate(characters):
        if index == len(characters)-1:
            print(index)
            print('last_item  '+i)
    # real_test_raw = ['第一段文字','这是第二段','第三段文字']
    # real_documents = [(jieba.cut(item_text,cut_all=False)) for item_text in real_test_raw]
    # real_documents = [list(jieba.cut(item_text, cut_all=False)) for item_text in real_test_raw]
    # real_documents = list(jieba.cut(character_keyword, cut_all=False))
    # for i in real_documents:
    #     i = i
    #     print(i)
def random_list_print():
    nums=[1,2,3,4,5,6,7,8,9,10]
    random_list = random.sample(nums,10)

    print(len(nums))

random_list_print()



