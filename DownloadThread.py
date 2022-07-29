
from threading import Thread
import os
import utils


class DownloadThread(Thread):
    """ 下载的线程 """
    def __init__(self, downloadInfo, sem,savePath):
        super().__init__()
        self.downloadInfo = downloadInfo
        self.name = downloadInfo["title"] + ".torrent" 
        self.sem = sem
        self.savePath = savePath
        self.seedFiles = []
        # 获取下载目录下的所有文件
        for _, _, files in os.walk(self.savePath):  
            self.seedFiles = files
            #print("当前目录下的文件有:{}".format( self.seedFiles))

    def run(self):
        if self.name in self.seedFiles:
            print("已有{}文件,直接返回".format(self.name))
        else:
            print("下载文件: {}".format(self.downloadInfo["title"]))
            self.download(self.downloadInfo["downloadUrl"], self.name)

        # 解开信号锁
        self.sem.release()

    def download(self, downloadURL, name):
        """ 进行下载请求 """
        response = utils.requestsPost(downloadURL)
        data = response.content
        print(self.savePath +'\\'+name)
        try:
            with open(self.savePath +'\\'+name,"wb") as f:
                f.write(data)
            print("下载完成: {}".format(name))
        except:
            print("下载失败: {}".format(name))
