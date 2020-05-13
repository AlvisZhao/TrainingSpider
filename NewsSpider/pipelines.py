# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import happybase
import hashlib
#导入thrift的python模块
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
#导入生成的Hbase模块
from hbase import THBaseService
from hbase.ttypes import *

# class NewsspiderPipeline(object):
#     def process_item(self, item, spider):
#         print("已接收到数据，正在存储......")
#         myPath = "E:\LearnLife\Python\Spider\Report"
#         if not os.path.exists(myPath):
#             os.mkdir(myPath)
#         for i in range(len(item['title'])):
#             fileNamePath = myPath + os.path.sep + item['title'][i] + ".txt"
#             for it in item:
#                 with open(fileNamePath, 'a+', encoding='utf-8')as f:
#                     if len(item[it]) == 0:
#                         f.write("不详" + "\n")
#                     else:
#                         f.write(str(item[it][i]) + "\n")
#                         print("写入成功")
#         return item

class NewsHBasePipeline(object):

    def __init__(self):
        # 创建Socket连接，到niit110:9090
        self.transport = TSocket.TSocket("niit01", 9090)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = THBaseService.Client(self.protocol)

    def putData(self, rowkey, data):
        # 打开端口进行通讯
        self.transport.open()
        # put操作
        table = b'ns01:t6'
        v1 = TColumnValue(b'f1', b'date', data[0])
        v2 = TColumnValue(b'f1', b'time', data[1])
        v3 = TColumnValue(b'f1', b'author', data[2])
        v4 = TColumnValue(b'f1', b'source', data[3])
        v5 = TColumnValue(b'f1', b'content', data[4])
        vals = [v1, v2, v3, v4, v5]
        put = TPut(rowkey, vals)
        self.client.put(table, put)
        print("存储okkkk!!")
        self.transport.close()

    def process_item(self, item, spider):
        for i in range(len(item['title'])):
            for it in item:
                title = (item['title'][i].encode('utf-8'))
                print(len(item[it]))
                print(title)
                date = item['date'][i].encode('utf-8')
                time = item['time'][i].encode('utf-8')
                author = item['author'][i].encode('utf-8')
                source = item['source'][i].encode('utf-8')
                content = item['content'][i].encode('utf-8')
                data = [date, time, author, source, content]
                self.putData(title, data)
        return item


