#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests
import os
import base64


#导入thrift的python模块
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
#导入编译生成的hbase 模块
from myThrift.hbase import THBaseService
from myThrift.hbase.ttypes import *

#response =requests.get('http://duanziwang.com/')
#data = response.text
#result = re.findall('<a href="http://duanziwang.com/.*?.html">(.*?)</a>',data)

def get_page(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0(Windows NT 10.0;Win64; x64) APPleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
        response = requests.get(url, timeout=10)
        data = response.text
        result = re.findall('<a href="http://duanziwang.com/.*?.html">(.*?)</a>',data)
        #result = re.findall('<a href="http://duanziwang.com/category/.*?">(.*?)</a>',data)
        #result = re.findall('<a href="http://duanziwang.com/tag/.*?">(.*?)</a>',data)
        return  result
    except:
        return ""
    #/html/body/section/div/div/main
    #//*[@id="1844"]/div[2]
    #//*[@id="1847"]/div[1]/h1/a
    #//*[@id="1845"]/div[1]/h1/a
    #//*[@id="1847"]/div[2]/p/text()
    #//*[@id="1843"]/footer/div/a[2]
def out_write(result):
    with open('areduanzi4.txt','a',encoding='utf-8')as fw:
        for i in result:
            fw.write('\n'+i)
            fw.flush()

def put(url,result):
    #创建Socket连接，到s201:9090
    transport = TSocket.TSocket('192.168.43.155', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = THBaseService.Client(protocol)
    #打开传输端口
    transport.open()
    #对url进行base64编码，形成bytes,作为rowkey
    urlBase64Bytes = url.encode("utf-8")

    #put操作
    table = b'ns01:t4'
    rowkey = urlBase64Bytes

    for i in result:
        #v1 = TColumnValue(rb'f1', b'duanzi',i)
        print(i)
        print("-"*30)
        bytes = i.encode('utf-8')
        tcls = TColumnValue(b'f1', b'content', bytes)
        vals = [tcls]
        put = TPut(rowkey, vals)
        client.put(table, put)
    print("okkkk!!")
    transport.close()


def get(url,d,m):
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
    table = b'ns01:t4'
    rowkey=urlBase64Bytes
    col_id = TColumn(b"f1",b'content')
    cols = [col_id]
    get = TGet(rowkey,cols)
    res = client.get(table,get)
    print(bytes.decode(res.columnValues[0].qualifier))
    print(bytes.decode(res.columnValues[0].family))
    print(res.columnValues[0].timestamp)
    print(bytes.decode(res.columnValues[0].value))
    transport.close()
    print("Get data okokok")

def scan():
    #创建Socket连接，到s201:9090
    transport = TSocket.TSocket('192.168.43.155', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = THBaseService.Client(protocol)
    #打开传输端口
    transport.open()

    # scan 全表扫描操作
    table = b'ns01:t4'

    # startRow = b'34,13520401111,20180114152647,0,13269364444,406'
    # stopRow = b'90,15032295555,20180922165903,0,15778421111,298'
    # dur = TColumn(b"f1", b"callDuration")
    # time = TColumn(b"f1", b"callTime")
    # caller = TColumn(b"f1", b"caller")
    # callee = TColumn(b"f1", b"callee")
    # cols = [dur, time,caller,callee]
    #caller = TColumn(b"f1", b"name")

    callee = TColumn(b"f1", b'content')
    cols = [callee]

    scan = TScan(columns=cols,startRow="1".encode(),stopRow="10".encode(),maxVersions=10)
    r = client.getScannerResults(table,scan,10);
    print(len(r))
    for x in r:
        print("============")
        print(bytes.decode(x.columnValues[0].qualifier))
        #print(bytes.decode(x.columnValues[0].family))
      #  print(x.columnValues[0].timestamp)
        print(bytes.decode(x.columnValues[0].value))

        print(x.columnValues[0].value)

    transport.close()
    print("Scan data okokok")


def out_print(data):
    for i in data:
        print(i)

if __name__ == '__main__':
    url = "http://duanziwang.com/"
    #u =get_page(url) #爬取网页
    #out_write(u)#写到文档
   # put(url,u)


#    get(url)
   # out_print(u)#打印到屏幕
    scan()
