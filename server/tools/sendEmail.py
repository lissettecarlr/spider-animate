import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from config.setting import readMyEmailInfo,readRcvEmail
except:
    def readMyEmailInfo():
        return "lissettecarlr1@163.com" , "XXX"
    def readRcvEmail():
        return ["mbdx98@163.com"]


class SendEmail():
    def __init__(self):
        self.name ,self.password = readMyEmailInfo()
        self.receivers = readRcvEmail()
        self.serverHost = 'smtp.163.com'
        self.serverPort = 465
        
    def send(self,title,content):
        if(self.name == None or self.password==None):
            return False
        #邮件内容设置
        msg = MIMEMultipart('related')
        #邮件主题       
        msg['Subject'] = title 
        #发送方信息
        msg['From'] = self.name 
        #接受方信息     
        msg['To'] = self.receivers[0]  

        msg.attach(MIMEText(content,'html','utf-8'))
        #登录并发送邮件
        try:
            # server = smtplib.SMTP() 
            # server.connect(self.serverHost,self.serverPort)
            server=smtplib.SMTP_SSL(self.serverHost, self.serverPort) 
            server.login(self.name, self.password) 
            #发送
            server.sendmail(self.name,self.receivers,msg.as_string()) 
            #退出
            server.quit() 
            print('success')
            return True
        except smtplib.SMTPException as e:
            print('error',e) #打印错误

#server.connect('smtp.163.com',465)

if __name__ == '__main__':
    test = SendEmail()
    test.send("测试","test")
