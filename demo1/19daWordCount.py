
#! python3
# -*- coding: utf-8 -*-
import os, codecs
import jieba
from collections import Counter
import docx
from docx import Document

def get_words(txt):
    seg_list = jieba.cut(txt)
    c = Counter()
    for x in seg_list:
        if len(x)>1 and x != '\r\n':
            c[x] += 1
    #print('常用词频度统计结果')
    print("十九大报告全文分析结果：")
    for (k,v) in c.most_common(10):
        print('%s %d'%(k,v))
        # print('%s%s %s  %d' % ('  '*(5-len(k)), k, '*'*int(v/3), v))

if __name__ == '__main__':
    with codecs.open('19da.txt', 'r', 'utf8') as f:
        txt = f.read()

    # document = Document('十九大报告全文.docx')
    # for paragraph in document.paragraphs:
    #     #print(paragraph.text)
    #     txt=paragraph.text
    get_words(txt)