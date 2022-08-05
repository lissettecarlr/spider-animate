import Search
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,QTime,QUrl,Qt
from PyQt5.QtGui import QIcon,QDesktopServices,QPixmap,QCursor
import queue
from gui import Ui_MainWindow
import sys
from loguru import logger
import time
import  sqlite3
import utils
import threading
import syncDb

class wincore (QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(wincore,self).__init__()
        self.setupUi(self)
        self.closeFlag = False
        self.init()
        
    def init(self):
        self.version = "v0.1.5"
        #保存当前季度所有搜索目标
        self.targets = []
        self.dbName = ""
        self.basePath = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.statusBar=QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('久远~~~',5000) 
        self.setWindowTitle('爬取工具 ' + self.version)
        # logger.add("./log/webPrint.log",format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}",rotation="500 MB",encoding='utf-8',filter="",level="INFO")

        #绑定事件
        self.pushButton.clicked.connect(self.buttonStart)

        #禁止窗口大小改变
        self.setFixedSize(self.width(), self.height())
        try:
            self.setWindowIcon(QIcon(self.basePath + '/assets/logo.png'))
        except:
            pass

        #右键菜单
        self.textBrowser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textBrowser.customContextMenuRequested.connect(self.showMenu)

        self.contextMenu = QMenu(self)
        self.clearBrowser = self.contextMenu.addAction('清空显示')
        self.clearBrowser.triggered.connect(self.Event)

        self.comboBox_2.currentIndexChanged.connect(self.combox2Change_event)

        #菜单
        self.action.triggered.connect(self.shwoAnimationUpdate)
        self.action_2.triggered.connect(self.readme)
        self.action_3.triggered.connect(self.spiderAll)
        self.action_4.triggered.connect(self.spidertoday)
        self.action_5.triggered.connect(self.updateDb)
        
        #读取配置
        self.readAnimation("七月番")

        # 消息队列
        self.msgQueue = queue.Queue()

        # 网络状态
        self.netStatus = False
        self.netTask = None

        #搜索
        self.searchTask = None

        #定时更新软件状态 使用qt定时器
        self.uiTimer = QTimer(self)
        self.uiTimer.timeout.connect(self.updateStatus)

        #UI更新定时器
        self.uiTimer.start(2000)

    def readAnimation(self,quarter):
        self.targets = []

        if(quarter == "七月番"):
            self.dbName = "search202207"
        elif(quarter == "四月番"):
            self.dbName = "search202204"
        else:
            print("未知：" + quarter)
            return

        res = utils.selectTable(self.dbName)
        for row in res:
            self.targets.append({"name":row["name"],"key":row["key"]})
            self.comboBox.addItem(row["name"])

    def combox2Change_event(self):
        quarter = self.comboBox_2.currentText()
        self.comboBox.clear()
        self.readAnimation(quarter)

    #更新UI
    def updateStatus(self):
        while(self.msgQueue.empty() == False):
            txt = self.msgQueue.get()
            self.textBrowser.append(txt)
            self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    def searchOverCallback(self):
        self.pushButton.setEnabled(True)
        self.showMessage("结束爬取")

    #启动各个子线程执行功能
    def buttonStart(self):
        self.pushButton.setEnabled(False)
        self.showMessage("开始爬取")
        # keyword = self.lineEdit.text()
        index = self.comboBox.currentIndex()
        #keyword = self.targets[index]["name"] + self.targets[index]["key"]
        keyword = self.targets[index]
        if(keyword["name"] == ""):
            self.showMessage("缺失查询关键字")
            self.pushButton.setEnabled(True)
            return

        self.searchTask = Search.searchTask(keyword,self.searchOverCallback,self.showMessage)
        self.searchTask.start()
  
    #关闭子线程执行功能
    def buttonStop(self):
        self.pushButton.setEnabled(True)
        self.showMessage("结束")

    def closeEvent(self,event):
        self.uiTimer.stop()
        self.searchTask.close()
 
    def showMessage(self,txt,color="black"):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" => "
        if(color == "black"):
            txt = "<font color='black'>"+ t + txt +"<font>"
        elif(color == "red"):
            txt = "<font color='red'>"+ t + txt +"<font>"
        else:
            txt = t + txt
        self.msgQueue.put(txt)

    # 显示更新日期
    def shwoAnimationUpdate(self):
        res = utils.selectTable(self.dbName)
        self.showMessage("===============================")    
        for row in res:
            self.showMessage(row["name"] + "\t\t\t" + row["week"])
        self.showMessage("===============================")

    
    def readme(self):
        QDesktopServices.openUrl(QUrl("https://github.com/lissettecarlr/spider-animate"))

    # 通过数据库查询星期，然后轮询
    def spidertoday(self):
        res = utils.selectTablebyTodayWeek(self.dbName)
        targets = []
        for p in res:
            targets.append({"name":p["name"],"key":p["key"]})
        #print(targets)
        self.showMessage("开始爬取今日更新",color="red")
        t = threading.Thread(target=self.spiderAllThread,args=(targets,))
        t.start()

    # 爬取所有
    def spiderAll(self):
        #开个新线程执行，否则会卡住UI
        self.showMessage("开始当前季度全部爬取任务",color="red")
        t = threading.Thread(target=self.spiderAllThread,args=(self.targets,))
        t.start()
      
    def spiderAllThread(self,list):
        self.pushButton.setEnabled(False)
        for tar in list:
            self.searchTask = Search.searchTask(tar,self.searchOverCallback,self.showMessage)
            self.searchTask.start()
            self.searchTask.join()
        self.pushButton.setEnabled(True)    
        self.showMessage("批量爬取结束",color="red")

    # 右键菜单
    def showMenu(self,pos):
        self.contextMenu.exec_(QCursor.pos()) 
    def Event(self):
        if(self.sender().text() == "清空显示"):
            self.textBrowser.clear()
    def updateDb(self):
        syncDb.getAnimationDb()
        self.showMessage("更新番列表完成",color="red")

import os

def winOpen(sys):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app= QtWidgets.QApplication(sys.argv)

    # 配置
    try:
        base = os.path.dirname(os.path.realpath(sys.argv[0]))
        file = open(base + '/assets/qss/style.qss',"r", encoding="utf-8")
        qss = file.read().replace("$DataPath",".")
        app.setStyleSheet(qss)
    except:
        pass

    win = wincore()
    win.show()
    sys.exit(app.exec_())

        
if __name__ == "__main__":
    winOpen(sys)
