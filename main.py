from ctypes.wintypes import tagRECT
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

class wincore (QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(wincore,self).__init__()
        self.setupUi(self)
        self.closeFlag = False
        self.init()
        
    def init(self):
        self.version = "v0.1.1"
        self.targets = []
        self.statusBar=QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('久远~~~',5000) 
        self.setWindowTitle('爬取工具 ' + self.version)
        # logger.add("./log/webPrint.log",format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}",rotation="500 MB",encoding='utf-8',filter="",level="INFO")

        #绑定事件
        self.pushButton.clicked.connect(self.buttonStart)

        #禁止窗口大小改变
        self.setFixedSize(self.width(), self.height())

        #右键菜单
        self.textBrowser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textBrowser.customContextMenuRequested.connect(self.showMenu)

        self.contextMenu = QMenu(self)
        self.clearBrowser = self.contextMenu.addAction('清空显示')
        self.clearBrowser.triggered.connect(self.Event)

        #读取配置
        conn=sqlite3.connect("Animation.db")
        cursor = conn.execute("SELECT * from search202207")
        #print("NAME\tKEY")
        for row in cursor:
            self.targets.append({"name":row[0],"key":row[1]})
            self.comboBox.addItem(row[0])
        conn.close()

        # print(self.targets)

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
        #print(keyword)
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

    def readme(self):
        QDesktopServices.openUrl(QUrl("https://www.baidu.com"))

    def closeEvent(self,event):
        self.uiTimer.stop()
        self.searchTask.close
 
    def showMessage(self,txt,color="black"):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" => "
        if(color == "black"):
            txt = "<font color='black'>"+ t + txt +"<font>"
        elif(color == "red"):
            txt = "<font color='red'>"+ t + txt +"<font>"
        else:
            txt = t + txt
        self.msgQueue.put(txt)

    # 右键菜单
    def showMenu(self,pos):
        self.contextMenu.exec_(QCursor.pos()) 
    def Event(self):
        if(self.sender().text() == "清空显示"):
            self.textBrowser.clear()

def winOpen(sys):
    app= QtWidgets.QApplication(sys.argv)
    win = wincore()
    win.show()
    sys.exit(app.exec_())

        
if __name__ == "__main__":
    winOpen(sys)
