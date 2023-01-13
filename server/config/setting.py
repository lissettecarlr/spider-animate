from json import load, dump


from defaultCfg import  projectPath


# 如果没有配置文件则新建一个
def settinInit():
    try:
        open(projectPath + '/config/animate.json',encoding= 'utf-8')
    except:
        data={"animate":[],"emailName":"","emailPassword":"","revEmailList":"","vxKey":""}
        with open(projectPath + '/config/animate.json', 'w',encoding='utf-8') as file:
            dump(data, file,ensure_ascii=False,indent = 4)


def settinRead():
    with open(projectPath + '/config/animate.json',encoding= 'utf-8') as file:
        data = load(file)
    return data


def settinSet(data):
    with open(projectPath + '/config/animate.json', 'w',encoding='utf-8') as file:
        dump(data, file,ensure_ascii=False,indent = 4)
 

# 新增一个搜索对象，包含名称与附加搜索关键词
def addNewAnimate(name,otherKey):
    data = settinRead()
    for sol in data["animate"]:
        if(sol["name"] == name):
            return False

    data["animate"].append({"name":name,"key":otherKey,"episode":[]})
    settinSet(data)
    return True


# 给一个对象增加已存在集数
def recordUpdate(name,number):
    data = settinRead()
    #print(data)
    for sol in data["animate"]:
        if(sol["name"] == name):
            for e in sol["episode"]:
                if(int(e) == int(number)): #如果已经存在这个集数
                    return False
            sol["episode"].append(int(number))
            sol["episode"].sort()
            settinSet(data)
            return True

def readMyEmailInfo():
    data = settinRead()
    # print(data)
    return data["emailName"],data["emailPassword"]

def readRcvEmail():
    data = settinRead()
    return data["revEmailList"]

def readVxKey():
    data = settinRead()
    return data["vxKey"]