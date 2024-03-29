
import requests
from bs4 import BeautifulSoup
import random
import os
import sys

# userAgent
userAgent = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36"
    ]
# 请求头
headers = {"User-Agent": random.choice(userAgent),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'reffer':'https://www.36dm.club/' 
          }


seedFilePath = os.path.dirname(os.path.realpath(sys.argv[0]))

htmlParser = "html.parser"

def requestsGet(url):
    if(url.find('http',0) == -1):
        return None
    try:
        return requests.get(url, headers = headers , timeout=10)
    except:
        return None

def requestsPost(url):
    try:
        return requests.post(url, headers = headers , timeout=10)
    except:
        return None

def soupGet(text):
    return BeautifulSoup(text,htmlParser)


#############################################################################################

from HTMLTable import HTMLTable

def createHtmlTable(name):
    table = HTMLTable(caption=name)
    table.append_header_rows((
        ('名称',  '链接',  '大小'),
    ))  

    table.set_style({
    'border-collapse': 'collapse',
    'word-break': 'keep-all',
    'white-space': 'nowrap',
    'font-size': '14px',
    })

    table.set_cell_style({
        'border-color': '#000',
        'border-width': '1px',
        'border-style': 'solid',
        'padding': '5px',
    })

    # 表头样式
    table.set_header_row_style({
        'color': '#fff',
        'background-color': '#48a6fb',
        'font-size': '18px',
    })

    # 覆盖表头单元格字体样式
    table.set_header_cell_style({
        'padding': '15px',
    })

    return table

def appendHtmlTable(table,name,url,size):
    table.append_data_rows((    
        (name, url, size),
    ))

def saveHtmlTable(table,path):
    html =  table.to_html()
    with open(path,"a") as code:
        code.write(html)


###############################################################

import sqlite3


path = os.path.dirname(os.path.realpath(sys.argv[0]))
dbName = path + "\\"+'Animation.db'
# 插入数据
def insertAnimationInfo(title,url1,url2,size,time):
    # 存入数据库
    conn = sqlite3.connect(dbName)
    cur = conn.cursor()
    insert_sql = """insert into animationInfo (title,url1,url2,size,time) values(?,?,?,?,?);"""
    para = (title,url1,url2,size,time)
    cur.execute(insert_sql, para)
    conn.commit()
    conn.close()

#查询搜索目标是否存在
def selectAnimationInfo(title):
    conn = sqlite3.connect(dbName)
    cur = conn.cursor()
    sql = """SELECT title from animationInfo WHERE title='{}' """.format(title)
    cur.execute(sql)
    res = cur.fetchall()
    conn.close()
    if(res == []):
        return False
    else:
        return True

def selectTable(tableName):
    conn=sqlite3.connect(dbName)
    cursor = conn.execute("SELECT * from " + tableName)
    res = []
    for row in cursor:
        res.append({"name":row[0],"key":row[1],"week":row[2]})
    conn.close()
    return res

def selectTablebyTodayWeek(tableName):
    from datetime import datetime
    week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    dayOfWeek = datetime.now().weekday()
    #print(week_list[dayOfWeek])

    conn=sqlite3.connect(dbName)
    sql = """SELECT * from {} WHERE week='{}' """.format(tableName,week_list[dayOfWeek])
    #sql = """SELECT * from {} WHERE week='{}' """.format(tableName,"星期三")
    #print(sql)
    cursor = conn.execute(sql)
    res = []
    for row in cursor:
        res.append({"name":row[0],"key":row[1]})
    conn.close()
    return res

#print(selectTablebyTodayWeek("search202207"))

# re = selectAnimationInfo("[Nekomoe kissaten][Isekai Ojisan][04][1080p][JPSC].mp4")
#re = selectAnimationInfo("123")
# print(re)