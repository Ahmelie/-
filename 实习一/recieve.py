import boto3
import tkinter
from tkinter import *           # 导入 Tkinter 库
root = Tk()                   
root.title("recieve")
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='MyQueue')
L2 = Label(root, text="得到消息：")
L2.place(x=8,y=10)
text = Listbox(root,width=40,height=8) 
text.place(x=10,y=40)
def get():
    for message in queue.receive_messages():
        output=format(message.body)
        text.insert(tkinter.END, "你成功地收到了一条消息：",output)
        text.see(tkinter.END)
        text.update()
        message.delete()
B2 = tkinter.Button(root, text ="获取", command = get)
B2.place(x=258,y=5)
root.geometry('300x200+550+220')
root.mainloop()                 # 进入消息循环
