import os
import MySQLdb
import sqlite3
from dotenv import find_dotenv, load_dotenv


#从云拉去数据
def connectServerDbReadTable(table):
    load_dotenv(find_dotenv('.env'))
    host = os.environ.get("HOST")
    dbname = os.environ.get("DBNAME")
    password = os.environ.get("PASSWORD")
    database = os.environ.get("DATABASE")
    port = int(os.environ.get("PORT"))
    try:
        serverdb = MySQLdb.connect(
            host=host,    
            user=dbname,        
            passwd=password,  
            db=database,
            port = port
            )     
    except:
        return None
    serverCur = serverdb.cursor()
    sql = """SELECT * from {}""".format(table)
    serverCur.execute(sql)
    res = serverCur.fetchall()
    serverdb.close()
    return res

#清空本地表
def clearOrCreatClientTable(table):
    clientdb = sqlite3.connect("./Animation.db")
    clientCur = clientdb.cursor()
    sql = """DELETE FROM {}""".format(table)
    try:
        clientCur.execute(sql)
        print("clear table {} success".format(table))
    except:
        print("clear table {} fail,create table".format(table))
        clientCur.execute("""CREATE TABLE IF NOT EXISTS {} (name TEXT,searchKey TEXT,week TEXT)""".format(table))
    clientdb.commit()
    clientdb.close()

#填充
def insertClientTable(table, data):
    clientdb = sqlite3.connect("./Animation.db")
    clientCur = clientdb.cursor()
    insert_sql = """insert into {} (name,searchKey,week) values(?,?,?);""".format(table)
    for row in data:
        para = (row[1],row[2],row[3])
        clientCur.execute(insert_sql, para)
    clientdb.commit()
    clientdb.close()

def getAnimationDb():
    tableList = connectServerDbReadTable("searchList")
    if(tableList == None):
        return False
    for table in tableList:
        # 从云端拉去此表数据
        print("table: {}".format(table[1]))
        data = connectServerDbReadTable(table[1])
        if(data == None):
            continue
        print(data)
        # 判断本地有无此表，没有就建立，有就清空
        clearOrCreatClientTable(table[1])
        # 填充数据
        insertClientTable(table[1],data)
