import os
import time
from loguru import logger
import random
import shutil
from utils import getNumInAnimateName,listSaveOrRead

from tools.htmlTable import htmlTable
from tools.sendEmail import SendEmail
from tools.vx import vxPost

from config.setting import recordUpdate,settinRead,settinInit
from defaultCfg import defaultConfig, projectPath
defaultConfig = defaultConfig()

#爬取36dm网站
import spiderTo36dm
def getSearchPageNum(soup) -> int:
    return spiderTo36dm.getSearchPageNum(soup)
    
def searchAnimation(keyword , pageNum = None):
    return spiderTo36dm.searchAnimation(keyword, pageNum)
    
# 获取此页资源数量
def getSearchOnePageListCount(soup) -> int:
    return spiderTo36dm.getSearchOnePageListCount(soup)

class spiderAnimate:
    def __init__(self):
        #搜索列表
        self.data = settinRead()
        self.searchList = self.data["animate"]

        self.resultPath = os.path.join(projectPath,"result")
        if(not os.path.exists(self.resultPath)):
            os.makedirs(self.resultPath)

        #配置文件
        settinInit()

    def task(self,sol):
        animateName = sol["name"]
        animateKey = sol["key"]

        # 每次还是全部集数都来来一遍，万一有更好的源呢
        searchKey = animateName + " " + animateKey
        (soup, htmlText) = searchAnimation(keyword = searchKey)
        if(soup == None):
            logger.warning("爬取失败")
            return

        # 该关键字搜索出的页码
        pageNum = getSearchPageNum(soup)
        logger.info("关键字：{}，共有：{} 页".format(searchKey,pageNum))
        if pageNum == None:
            logger.warning("搜索：{}，没有找到资源".format(searchKey))
            return

        # 该关键字搜索出的数据总数
        resultCount = spiderTo36dm.getSearchTotalNum(soup)
        if resultCount == 0 or resultCount == None:
            logger.warning("该页没有资源.")
            return
        logger.info("共搜索出资源：{}".format(resultCount)) 

        
        # 循环爬取每一页的数据
        self.result = []
        for page in range(1, int(pageNum)+1):
            if(page != 1):
                (soup, htmlText) = searchAnimation(searchKey,page)  

            downInfo = self.searchSolPage(soup)
            self.result +=downInfo
            logger.info("第{}页 处理完成".format(page))
            #self.saveResult(downInfo)
            #logger.info(self.result)
        #msg = self.saveResult(self.result,animateName,animateEpisode)
        msg = self.saveResult2(self.result,animateName)
        logger.info(msg)
        return msg
 

    # 对搜索出来的页面进行操作
    def searchSolPage(self,soup):
        #获取本页数量
        pageListCount = getSearchOnePageListCount(soup)
        logger.info("当前页面有 {} 个资源".format(pageListCount))
        # 获取所有资源子链接的url
        urlList = []
        for index in range(1, pageListCount+1):
            url = spiderTo36dm.getSearchUrl(soup,index)
            if(url != None):
                urlList.append(url)
        downloadInfos = []
        num = 1
        for url in urlList:
            logger.info("总共需要处理{}个资源，目前以进行{}个".format(len(urlList),num))
            num = num + 1
            downloadInfo = spiderTo36dm.getDownloadInfo(url)
            #{'title': '[Isekai Ojisan][10].mp4', 'downloadUrl': 'https://', 'magent': 'magnet:?', 'size': '369.6MB', 'time': '2022/12/19 23:22:17'}
            if downloadInfo == None:
                logger.info("获取失败")
                continue
            # 将所有下载信息添加到列表中
            downloadInfos.append(downloadInfo)
            # 每次结束后随机延迟
            time.sleep(random.uniform(1.1,5.4)) 
        return downloadInfos    

    #此函数是根据集数进行存储和发送
    def saveResult(self,downInfo,name,episodeHistory):
        if len(downInfo) == 0 or downInfo == None:
                return

        animatePath = os.path.join(self.resultPath,name)
        if not os.path.exists(animatePath):
            os.makedirs(animatePath)
        else:
            shutil.rmtree(animatePath)   
            os.makedirs(animatePath)

        newMsgList = []
        for sol in downInfo:
            title = sol['title']
            magent = sol['magent']
            size = sol["size"]
            stime = sol["time"]
            #logger.debug("title={}".format(title))
            episode = getNumInAnimateName(title)
            #logger.debug("episode={}".format(episode))
            if(episode ==None):
                continue

            animateEpisodePath = os.path.join(animatePath,str(episode)+".txt")   
            #logger.debug("animateEpisodePath={}".format(animateEpisodePath))  
 
            if not os.path.isfile(animateEpisodePath):
                listSaveOrRead(path = animateEpisodePath,mode="save",arg = [])

            record = listSaveOrRead(path = animateEpisodePath)
            record.append(sol)
            listSaveOrRead(path = animateEpisodePath,mode="save",arg = record)

        #对象下所有子内容
        files= os.listdir(animatePath)
        for file in files:
            n = os.path.splitext(file)[0]

            #生成html
            table = htmlTable(["名称",'磁力链接','大小','时间'])
            infos = listSaveOrRead(path = os.path.join(animatePath,file))
            for info in infos:
                table.addLineContent([info["title"],info["magent"],info["size"],info["time"]])
            
            
            table.save(os.path.join(animatePath,n+".html"))

            if(recordUpdate(name,int(n))):
                newMsgList.append(int(n))
                htmlStr = table.getHtmlStr()
                se = SendEmail()
                title = name + " 更新了[" + str(n) + "]"
                se.send(title,htmlStr)

        return newMsgList

    #此函数将所有爬取对象都进行发送
    def saveResult2(self,downInfo,name):
        if len(downInfo) == 0 or downInfo == None:
                return

        animatePath = os.path.join(self.resultPath,name)
        if not os.path.exists(animatePath):
            os.makedirs(animatePath)
        else:
            shutil.rmtree(animatePath)   
            os.makedirs(animatePath)

        table = htmlTable(["名称",'磁力链接','大小','时间'])
        updateList = []
        for sol in downInfo:
            table.addLineContent([sol["title"],sol["magent"],sol["size"],sol["time"]])
            
            title = sol['title']
            episode = getNumInAnimateName(title)
            if(episode == None):
                logger.warning("未找到集数：{}".format(title))
            else:
                if(recordUpdate(name,episode)):
                    updateList.append(episode)

        table.save(os.path.join(animatePath,name+".html"))
        updateList.sort()
        #判断是否有集数更新，但是不管是否都回发送邮件
        htmlStr = table.getHtmlStr()
        se = SendEmail()
        if(updateList !=[]):
            EmailTitle = name + " 有更新 " + str(updateList) + ""
            se.send(EmailTitle,htmlStr)
            return EmailTitle
        else:
            EmailTitle = name + " 无更新"
            se.send(EmailTitle,htmlStr)
            return ""
        
    def loop(self):
        #while(True):
            #if(time.strftime("%H:%M", time.localtime()) == "14:39"):
                #print("hello")
                vxContent = ""
                for sol in self.searchList:
                    msg = self.task(sol) 
                    if(msg !=""):
                        vxContent = vxContent + msg + "\t\r\n"
                if(vxContent != ""):
                    vxPost("有更新",vxContent)

                #time.sleep(60)
                #break
            

if __name__ == '__main__':
    app = spiderAnimate()
    app.loop()
