# -*- coding:utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import numpy as np
import matplotlib
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import socket       # 导入 socket 模块

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

year = ['1999','2000','2001','2002','2003','2004',
       '2005','2006','2007','2008','2009','2010',
       '2011','2012','2013','2014','2015','2016']


#画布控件继承自 matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg 类
class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.str=[]
        self.type=''
        fig = plt.figure(1)#创建画布,设置宽高，每英寸像素点数
        self.axes = fig.add_subplot(111)#
        FigureCanvasQTAgg.__init__(self, fig)#调用基类的初始化函数
        #self.setParent(parent)
        #FigureCanvasQTAgg.updateGeometry(self)
    def replot(self):
        self.axes.cla()#清除已绘的图形-
        self.axes.plot(year, self.str, 'go-', label=self.type)
        self.axes.set_title(self.type+"-折线图")
        self.axes.legend()  #生成默认图例
        self.draw()
    def rebar(self):
        self.axes.cla()#清除已绘的图形
        self.axes.bar(x=year, height=self.str, width=0.4, label=self.type, color='green') 
        for x, y in enumerate(self.str):
            self.axes.text(x, y - 400, '%s' % y, ha='center', va='bottom')
        self.axes.set_title(self.type+"-条形图")
        self.axes.legend()  #生成默认图例
        self.draw()
    def repie(self):
        self.axes.cla()#清除已绘的图形
        self.axes.pie(x=self.str,
                labels=year,
                autopct='%1.1f%%',
                explode=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                shadow=True)
        self.axes.set_title(self.type+"-饼状图")
        self.axes.legend()  #生成默认图例
        self.draw()
    def choose(self,i):
        msg=''
        if i==1:
            msg='getprice'
            self.type='均价'
        elif i==2:
            msg='getperatio'
            self.type='市盈率'
        elif i==3:
            msg='getturnover'
            self.type="转手率"
        self.send_ser_log(msg)
    def send_ser_log(self,msg):
        self.str=[]#更新
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #新建连接
        client.connect(('localhost',1222)) 
        
        client.send(msg.encode('utf-8')) 
        data = client.recv(1024) 
        print('recv:',data.decode()) 
        y=data.decode().split();
        for temp in range(len(y)):
            self.str.append(float(y[temp]))
        print('str:',self.str)
        #self.client.close() #关闭这个链接
        client.close()
        
class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #创建 matplotlib画布控件
        self.myfigure = Canvas(self)
        layout = QtWidgets.QFormLayout()

        self.button1 = QtWidgets.QPushButton("折线图")
        self.button1.setFixedWidth(100)
        self.button1.clicked.connect(lambda : self.myfigure.replot())
        
        self.button2 = QtWidgets.QPushButton("条形图")
        self.button2.setFixedWidth(100)
        self.button2.clicked.connect(lambda : self.myfigure.rebar())
        
        self.button3 = QtWidgets.QPushButton("饼状图")
        self.button3.setFixedWidth(100)
        self.button3.clicked.connect(lambda : self.myfigure.repie())
        
        self.button4 = QtWidgets.QPushButton("均价")
        self.button4.setFixedWidth(100)
        self.button4.clicked.connect(lambda : self.myfigure.choose(1))
        
        self.button5 = QtWidgets.QPushButton("市盈率")
        self.button5.setFixedWidth(100)
        self.button5.clicked.connect(lambda : self.myfigure.choose(2))
        
        self.button6 = QtWidgets.QPushButton("转手率")
        self.button6.setFixedWidth(100)
        self.button6.clicked.connect(lambda : self.myfigure.choose(3))

        layout.addWidget(self.button4)#添加到布局
        layout.addWidget(self.button5)
        layout.addWidget(self.button6)
        
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        
        layout.addWidget(self.myfigure)#添加到布局
        
        self.setLayout(layout)
        self.resize(800,800)
        self.setWindowTitle("浦发银行股市分析系统")
       

qApp = QtWidgets.QApplication(sys.argv)
ui = Widget()
ui.show()
sys.exit(qApp.exec_())
