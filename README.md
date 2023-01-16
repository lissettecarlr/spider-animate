# spider-animate


## 简述
果然，本地客户端对于懒人来说还是太麻烦，每次要去打开个exe好累，之前客户端代码扔到了client文件夹里面了，现在弄个直接扔到服务器上去爬新番，相关文件放到server中。目前肯定用后者，所有此文档只说server端


## server的环境
```
pip install requests
pip install loguru
pip install beautifulsoup4
```

## server的功能
每天爬取一次，邮件发出，标题提示是否有更新。有更新进行微信推送


## server使用
* 进入目录
```
cd server
```
* 编辑和加入爬取动画
```
vim addSearchAinmate.py
python addSearchAinmate.py
```
* 邮箱相关配置和执行时间
```
vim config
vim config/animate.json

"emailName": "lissettecarlr1@163.com",
"emailPassword": "",
"revEmailList": [
    "mbdx98@163.com"
],
"vxKey": ""

vim defaultCfg.py

alarmClock = "23:00"
```
后台运行
```
nohup python app.py>run.log &
```


