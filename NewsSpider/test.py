from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase import THBaseService
from hbase.ttypes import *
if __name__ == '__main__':
    # thrift默认端口是9090
    host = '192.168.118.134'
    port = 9090
    socket = TSocket.TSocket(host, port)
    socket.setTimeout(5000)

    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = THBaseService.Client(protocol)

    socket.open()
    # #put操作
    table = b'test:t1'
    row = b'row1'
    v1 = TColumnValue(b'f1', b'id', b'101')
    v2 = TColumnValue(b'f1', b'name', b'tomas')
    v3 = TColumnValue(b'f1', b'age', b'12')
    vals = [v1, v2, v3]
    put = TPut(row, vals)
    client.put(table, put)
    print("okkkk!!")
    socket.close()