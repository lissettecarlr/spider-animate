
class htmlTable():
    # 初始化传入表头
    def __init__(self,head = ["aaa","bbb","ccc"]):
        if(head != None):
            self.tableHead = head
            # 构建表头
            self.partTableHead = ""
            self.headLen = len(self.tableHead)
            for i in range(0,self.headLen):
                tx = self.tableHead[i]
                data = str(tx)
                self.partTableHead = self.partTableHead + '<th>' + data + '</th>'
            #表尾
            self.partEnd = '''    
                    </thead> 
                    </table>
                    <p></p>
                </body>
                </html>
            '''
            #首部
            self.partTitle = """<!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width,initial-scale=1.0">
                <style>
                table {
                    width: 2000px;
                    opacity: 100;
                }
                th {
                    color: rgba(0, 0, 0, 0.85);
                    width: 200px;
                    font-weight: 500;
                    text-align: center;
                    background: lightsteelblue;
                    border-bottom: 2px solid #e8e8e8;
                }
                tr {
                    color: rgba(0, 0, 0, 0.85);
                    width: 200px;
                    font-weight: 500;
                    text-align: center;
                    background: lightsteelblue;
                    border-bottom: 2px solid #e8e8e8;

                }
                tr td {
                    padding: 16px 6px;
                    overflow-wrap: break-word;
                    text-align: center;
                }
                table:hover{
                    opacity: 1;
                }
                p {
                    width: 1600px;
                    border-style:solid;
                    border-width:0 0 0.2px 0;
                    border-color:rgba(79, 125, 224, 0.85);
                }
                </style>
                </head>
                <body>
                    <table>
                    <thead>
                    """
            #内容
            self.partTableContent = ""

    def addLineContent(self,info=[]):
        self.partTableContent= self.partTableContent + """ <tr style="border: 1px solid #1b1e24;"> """
        for i in range(0,self.headLen):
            tx = info[i]
            if(tx == None):
                data = ""
            else:
                data = str(tx)
            self.partTableContent = self.partTableContent + '<td>' + data + '</td>' 
        self.partTableContent = self.partTableContent +'</tr>'

   
    def clearContent(self):
        self.partTableContent = ""

    def getHtmlStr(self):
        return self.partTitle + self.partTableHead + self.partTableContent + self.partEnd

    def save(self,path):
        content = self.getHtmlStr()
        with open(path, "w") as code:
            code.write(content)


# test = htmlTable()
# test.addLineContent([1,2,3])
# test.addLineContent([3,4,5])
# test.save()