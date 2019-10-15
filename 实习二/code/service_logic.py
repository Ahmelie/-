# -*- coding:utf-8 -*-
import socket     

class service_logic:#业务逻辑层
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def __init__(self):
        service_logic.server.bind(('localhost',1222)) 
        service_logic.server.listen(5) 
        while True:
            conn,addr = service_logic.server.accept() 
            print("service_logic",conn,addr)
            if True:
                try:
                    data = conn.recv(1024)  #接收数据
                    print('recive:',data.decode()) #打印接收到的数据
                    msg=self.send_data_acc(data)
                    conn.send(msg.encode()) #然后再发送数据
                except ConnectionResetError as e:
                    print('关闭了正在占线的链接！')
                    break
            conn.close()
        
    def send_data_acc(self,msg):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#新建链接
        client.connect(('localhost',6999))
        if True:
            client.send(msg)  
            data = client.recv(1024) 
            print('recv:',data.decode())
        client.close() #关闭链接
        return data.decode()
a=service_logic()
