# 基于TF-IDF算法的关键词抽取

import jieba
import jieba.analyse

sentence = '房屋工程、市政工程、装修装饰工程、消防工程、土石方工程、公路工程、水利水电工程、机电安装工程、地基与基础工程、幕墙工程、钢结构工程、楼宇智能化工程的设计与施工。'

keywords = jieba.analyse.extract_tags(sentence, topK=20, withWeight=True, allowPOS=('n','vn','ns'))

# print(type(keywords))
# <class 'list'>

for item in keywords:
    print(item[0],item[1])

import jieba.posseg as pseg
words = pseg.cut(" 改造面积3.09万平方米，改造棚户区797户，建设住宅、道路、园林绿化、消防、室外照明及配套设施等")
for word, flag in words:
    print('%s, %s' % (word, flag))