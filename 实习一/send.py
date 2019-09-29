import boto3
import tkinter
from tkinter import *           # 导入 Tkinter 库
root = Tk()                   
root.title("send")
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='MyQueue')
L1 = Label(root, text="输入消息：")
L1.place(x=8,y=10)
E1 = Entry(root,width=25)
E1.place(x=68,y=10)
text = Listbox(root,width=40,height=8) 
text.place(x=10,y=40)
def send():
    userInput=E1.get()
    response = queue.send_message(MessageBody=userInput)
    E1.delete(0, END)
    text.insert(tkinter.END, "你成功地发送了一条消息，id为：",response.get('MessageId'))
    text.see(tkinter.END)
    text.update()
B1 = tkinter.Button(root, text ="发送", command = send)
B1.place(x=258,y=5)
root.geometry('300x200+550+220')
root.mainloop()                 # 进入消息循环
