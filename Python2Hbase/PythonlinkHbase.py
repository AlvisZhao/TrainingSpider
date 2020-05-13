# -*- encoding=utf-8 -*-
#导入os模块
import os


#导入thrift的python模块
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


#导入编译生成的hbase 模块
from myThrift.hbase import THBaseService
from myThrift.hbase.ttypes import *


#创建Socket连接，到s201:9090
transport = TSocket.TSocket('192.168.24.130', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = THBaseService.Client(protocol)


#打开传输端口
transport.open()


# #put操作
# table = b'ns01:t4'
# row = b'row1'
# v1 = TColumnValue(b'f1', b'id', b'101')
# v2 = TColumnValue(b'f1', b'name', b'tomas')
# v3 = TColumnValue(b'f1', b'age', b'12')
# vals = [v1, v2, v3]
# put = TPut(row, vals)
# client.put(table, put)
# print("okkkk!!")
# transport.close()

#get
table = b'ns01:t4'
rowkey=b"row1"
col_id = TColumn(b"f1",b"id")
col_name = TColumn(b"f1",b"name")
col_age = TColumn(b"f1",b"age")

cols = [col_id,col_name,col_age]
get = TGet(rowkey,cols)
res = client.get(table,get)
print(bytes.decode(res.columnValues[0].qualifier))
print(bytes.decode(res.columnValues[0].family))
print(res.columnValues[0].timestamp)
print(bytes.decode(res.columnValues[0].value))


#delete
# table = b'ns1:t1'
# rowkey = b"row1"
# col_id = TColumn(b"f1", b"id")
# col_name = TColumn(b"f1", b"name")
# col_age = TColumn(b"f1", b"age")
# cols = [col_id, col_name]
#
# #构造删除对象
# delete = TDelete(rowkey,cols)
# res = client.deleteSingle(table, delete)
# transport.close()
# print("ok")


# table = b'ns1:calllogs'
# startRow = b'00,15778423030,20170208043827,0,17731088562,570'
# stopRow = b'17,15338595369,20170410132142,0,15732648446,512'
# dur = TColumn(b"f1", b"callDuration")
# time = TColumn(b"f1", b"callTime")
# caller = TColumn(b"f1", b"caller")
# callee = TColumn(b"f1", b"callee")
# cols = [dur, time,caller,callee]
#
# scan = TScan(startRow=startRow,stopRow=stopRow,columns=cols)
# r = client.getScannerResults(table,scan,100);
# for x in r:
#     print("============")
#     print(bytes.decode(x.columnValues[0].qualifier))
#     print(bytes.decode(x.columnValues[0].family))
#     print(x.columnValues[0].timestamp)
#     print(bytes.decoe(x.columnValues[0].value))