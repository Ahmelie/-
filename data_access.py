# -*- coding:utf-8 -*-
import pymysql
import socket

class data_access:#数据访问层
    sqlcon=pymysql.connect(host='localhost',port=3306,user='root',password='aimeili19991020@',db='pro1', charset='utf8')
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def __init__(self):
        data_access.server.bind(('localhost',6999)) #绑定端口
        data_access.server.listen(5) #开始监听
        while True:
            conn,addr = data_access.server.accept() #等待链接
            print(data_access,conn,addr)
            if True:
                try:
                    data = conn.recv(1024)  #接收数据
                    print('recive:',data.decode()) #打印数据
                    msg=self.call_sql(data.decode())
                    conn.send(msg.encode()) #发送数据
                except ConnectionResetError as e:
                    print('关闭了正在占线的链接！')
                    break
            conn.close()
    def call_sql(self,msg):
        cursor = data_access.sqlcon.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.callproc(msg)
        data = cursor.fetchall()
        cursor.close()
        #data_access.sqlcon.commit()
        str=''
        for temp in range(len(data)):
            temp2=list(data[temp].values())
            str=str+temp2[0]+' '
        print(str)
        return str
a=data_access()
a.sqlcon.close()
