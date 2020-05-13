#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests
import os
import base64
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np


#导入thrift的python模块
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
#导入编译生成的hbase 模块
from myThrift.hbase import THBaseService
from myThrift.hbase.ttypes import *

def get(url):
    #创建Socket连接，到s201:9090
    transport = TSocket.TSocket('192.168.43.155', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = THBaseService.Client(protocol)
    #打开传输端口
    transport.open()
    #对url进行base64编码，形成bytes,作为rowkey
    urlBase64Bytes = url.encode("utf-8")
    #get
    table = b'ns01:t6'
    rowkey=urlBase64Bytes
    # v1 = TColumn(b"f1",b'date')
    # v2 = TColumn(b"f1",b'time')
    # v3 = TColumn(b"f1",b'author')
    # v4 = TColumn(b"f1",b'source')
    # v5 = TColumn(b"f1",b'content')
    # cols = [v1,v2,v3,v4,v5]

    v1 = TColumn(b"f1",b'content')
    cols = [v1]

    get = TGet(rowkey,cols)
    res = client.get(table,get)
   # print(bytes.decode(res.columnValues[0].qualifier))
    #print(bytes.decode(res.columnValues[0].family))
   # print(res.columnValues[0].timestamp)
    print(bytes.decode(res.columnValues[0].value))

    Hdata= res.columnValues[0].value
    words = jieba.lcut(Hdata) #用jieba库的精确模式将txt装换成列表的格式
    print("分词：")
    print(words)

    transport.close()
    print("Get data okokok")
    return Hdata

def scan_data(num):
    #创建Socket连接，到s201:9090
    transport = TSocket.TSocket('192.168.43.155', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = THBaseService.Client(protocol)
    #打开传输端口
    transport.open()
    table = b'ns01:t6'
    v1 = TColumn(b"f1",b'date')
    v2 = TColumn(b"f1",b'time')
    v3 = TColumn(b"f1",b'author')
    v4 = TColumn(b"f1",b'source')
    v5 = TColumn(b"f1",b'content')
    cols = [v1,v2,v3,v4,v5]
    scan = TScan(columns=cols)
    r = client.getScannerResults(table,scan,num)

    #打开停用词表
    f_stop=open("stopwords.txt",encoding="utf8")
    #读取
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()#关闭资源
    #将停用词格式化，用\n分开，返回一个列表
    f_stop_seg_list=f_stop_text.split("\n")
    mywordList=[]
   # mywordList.append(news)将Hbase数据加到mywordList
   #  i=0
    for x in r:
        # i=i+1
        print("============")
        # print( i )
        print(bytes.decode(x.columnValues[0].qualifier))
        print(bytes.decode(x.columnValues[0].family))
        print(x.columnValues[0].timestamp)
        print(bytes.decode(x.columnValues[0].value))
        print(bytes.decode(x.columnValues[1].value))
        print(bytes.decode(x.columnValues[2].value))
        print(bytes.decode(x.columnValues[3].value))
        print(bytes.decode(x.columnValues[4].value))

        news=bytes.decode(x.columnValues[1].value)
        print("刚读出的新闻：")
        print(news)
        #进行分词
        seg_list=jieba.cut(news,cut_all=False)

        #将一个generator的内容用/连接
        listStr='/'.join(seg_list)
        print(listStr)
         #对默认模式分词的进行遍历，去除停用词
        for myword in listStr.split('/'):
            #去除停用词
            if not(myword.split()) in f_stop_seg_list and len(myword.strip())>1:
                mywordList.append(myword)
        #return ' '.join(mywordList)

    #    #1 words = jieba.lcut(news)#对每条新闻进行分词
    #
    #     print("分词后的新闻：")
    #     print(words)
    #     mywordList.append(words)

    print("下面是Hbase读出来的数据 进行stop分词后 即MywordList：")
    print(mywordList)

    return mywordList


    transport.close()
    print("Scan data is okokok")

import jieba
from collections import Counter
def WCSort(jbtxt):
    seg_list = jbtxt
    c = Counter()
   # print(jbtxt)
    for x in seg_list:
        if len(x)>1 and x != '\r\n':
            c[x] += 1
    #print('常用词频度统计结果')
    print("文本分析结果：")
    for (k,v) in c.most_common(100):
        print('%s%s %s  %d' % ('  '*(5-len(k)), k, '*'*int(v/2), v))

    return  seg_list

def wordCloud_make(hdata_txt,num):
   # test_str = "".join(hdata_txt)#list转str
    hdata_str=' '.join(hdata_txt)
    print(hdata_txt)
    print(hdata_str)

    w = WordCloud(
        background_color="white", #设置背景为白色，默认为黑色

        width=700,              #设置图片的宽度
        height=500,              #设置图片的高度
        margin=10,               #设置图片的边缘

        max_font_size=100,        random_state=30,
        font_path='‪C:\Windows\Fonts\SIMYOU.TTF')   #中文处理，用系统自带的字体)
    w.generate(hdata_str)
    #w.to_file('novelWordcloud.png')
    #开始画图
    plt.imshow(w)
    #为云图去掉坐标轴
    plt.axis("off")
    #画云图，显示
    plt.imshow(w)
    #保存云图
    #w.to_file('WordCloud\'+ num + '.png)

    w.to_file("%d.png"%(num))
    print("plt is okk")


if __name__ == '__main__':

    #hdata=get(url)
    num=0
    while num<100:
        num+=50

        hdata=scan_data(num)#读取Hbase数据 进行分词返回list
        jbtxt=WCSort(hdata)#对分完词的词统计排序 做排名
        wordCloud_make(hdata,num)#词云制作
        print("对%d条新闻分析结束"%(num))

