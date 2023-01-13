import requests
from loguru import logger
from config.setting import readVxKey


def vxPost(vxtitle,vxtext):
    serverKey = readVxKey()
    if(serverKey == ""):
        return False
    url = "https://sctapi.ftqq.com/" + serverKey+".send"
    print(url+"|"+vxtitle+"|"+vxtext)
    data = {
    "text":vxtitle,
    "desp":vxtext
    }
    try:
        r = requests.post(url, data)
        logger.info("微信推送成功")
        return True
    except:
        logger.error("微信推送失败")
        return False