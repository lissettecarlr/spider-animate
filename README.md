# spider-animate


## 简述
果然，本地客户端对于懒人来说还是太麻烦，每次要去打开个exe好累，之前那个本地客户端扔到了client里面，现在弄个直接扔到服务器上去爬新番，相关文件放到server中


## server的环境
```
pip install html-table
pip install requests
```

## server的功能
每天爬取一次，邮件发出，标题提示是否有更新。有更新进行微信推送


## server使用
先编辑addSearchAinmate.py填写需要搜索的对象
然后执行app.py

