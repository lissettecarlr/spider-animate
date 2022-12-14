
from ctypes import util
import os
import sys
import csv
import spiderTo36dm
import threading
import time
import random
import utils

class  searchTask(threading.Thread):
    def __init__(self,keyword,cb,print):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.overCb = cb
        self.uiPrint = print
        self.closeFlag = False

    def run(self):
        self.startSearch(self.keyword)
        self.overCb()

    def close(self):
        self.closeFlag = True

    def startSearch(self,keyword):
        # 对关键字进行搜索，得到各类信息
        keywordName = keyword["name"]
        searchKey = keywordName + " " + keyword["key"]
        (soup, htmlText) = searchAnimation(keyword = searchKey)
        if(soup == None):
            self.uiPrint("爬取失败")
            return

        # 该关键字搜索出的页码
        pageNum = getSearchPageNum(soup)
        self.uiPrint("关键字: " + searchKey + " 共有 " + str(pageNum) + " 页")
        if pageNum == None:
            self.uiPrint("搜索 :"+ searchKey+ " 没找到资源")
            return

        # 该关键字搜索出的数据总数
        resultCount = spiderTo36dm.getSearchTotalNum(soup)
        if resultCount == 0 or resultCount == None:
            self.uiPrint("该页没有资源.")
            return
        self.uiPrint("共搜索出资源：{}".format(resultCount))
    
        # 文件夹统一为一个
        seedFilePath = os.path.dirname(os.path.realpath(sys.argv[0])) 
        self.savePath = seedFilePath + "\\" + "result"
        self.csvFile = self.savePath + "\\" + keywordName + ".csv"
        self.htmlFile = self.savePath + "\\" + keywordName + ".html"
        # 判断文件夹是否存在,如果不存在就创建一个
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)


        if(os.path.exists(self.csvFile)):
            try:
                os.remove(self.csvFile)
                print("删除："+ self.csvFile)
            except:
                self.uiPrint("删除文件失败")
        else:
            pass

        if(os.path.exists(self.htmlFile)):
            try:
                os.remove(self.htmlFile)
                print("删除："+ self.htmlFile)
            except:
                self.uiPrint("删除文件失败")
        else:
            pass

        self.table = utils.createHtmlTable(keywordName)

        # 循环爬取每一页的数据
        for page in range(1, int(pageNum)+1):
            if(page != 1):
                (soup, htmlText) = searchAnimation(searchKey,page)  
            downInfo = self.searchAction(soup)
            self.uiPrint("第{}页 处理完成".format(page))
            self.saveResult(downInfo)
            if(self.closeFlag == True):
                return


    # 对搜索出来的页面进行操作
    def searchAction(self,soup):
        #获取本页数量
        pageListCount = getSearchOnePageListCount(soup)
        self.uiPrint("当前页面有 {} 个资源".format(pageListCount))

        # 获取所有资源子链接的url
        urlList = []
        for index in range(1, pageListCount+1):
            url = spiderTo36dm.getSearchUrl(soup,index)
            if(url != None):
                urlList.append(url)

        downloadInfos = []

        num = 1
        for url in urlList:
            if(self.closeFlag == True):
                return
            self.uiPrint("总共需要处理{}个资源，目前以进行{}个".format(len(urlList),num))
            num = num + 1
            downloadInfo = spiderTo36dm.getDownloadInfo(url)
            if downloadInfo == None:
                self.uiPrint("获取失败")
                continue

            # 多线程开始下载
            # self.startDownload(downloadInfo)

            # 将所有下载信息添加到列表中
            downloadInfos.append(downloadInfo)
            # 每次结束后随机延迟
            time.sleep(random.uniform(1.1,5.4)) 
        return downloadInfos

    # result应该具备title、downloadUrl、time、size四个属性
    def saveResult(self,result):
        if len(result) == 0 or result == None:
                return
        else:
            NewInfoCount = 0
            #其他方式保存
            for info in result:
                try:
                    with open (self.csvFile, "a+") as fp:
                        writer = csv.writer(fp)
                        writer.writerow((info["title"], info["downloadUrl"], info["magent"],info["time"], info["size"]))
                except IOError as error:
                    print(error)
                finally:
                    pass
                utils.appendHtmlTable(self.table,info["title"],info["magent"],info["size"])
                #如果由更新则存入数据库
                if(utils.selectAnimationInfo(info['title']) == False):
                    utils.insertAnimationInfo(info['title'],info['downloadUrl'],info['magent'],info['size'],info['time'])
                    NewInfoCount += 1
                else:
                    #print("已存在")
                    pass
            utils.saveHtmlTable(self.table,self.htmlFile)
            self.uiPrint("对比上次搜索，更新了{}个".format(NewInfoCount))
            
 
def getSearchPageNum(soup) -> int:
    return spiderTo36dm.getSearchPageNum(soup)
    
def searchAnimation(keyword , pageNum = None):
    return spiderTo36dm.searchAnimation(keyword, pageNum)
    
# 获取此页资源数量
def getSearchOnePageListCount(soup) -> int:
    return spiderTo36dm.getSearchOnePageListCount(soup)
 





  
