# spider-animate


## 简述
为了便利舍弃通用性，毕竟这软件就是自用的

## 使用

## 操作
* 下载spider-animate.zip，解压后双击执行exe文件即可
* 界面中，通过年份季度筛选此季度的番剧，目前支持的数量被保存在animation.db中，sqlite会的自己加载去改。我会根据自己的需要更新云端数据库，本地的可以通过帮助中的按钮来拉更新。
![](./pic/p_1.png)

* 结果被保存在result文件夹中，可以直接通过按钮打开，有两种格式html和csv。
![](../../pic/p_2.png)

* 打开后能看到名称、大小、和磁力链接、种子链接

## 功能按钮

* 更新时间：打印番剧更新时间是星期几
* 爬今日：爬取今日更新的番剧
* 爬所有：爬取选择季度的番剧
* 打开结果文件夹：如其名


## 菜单栏


### 帮助

* 拉取番列表
通过云端数据库更新本地数据库的番剧列表。


* 使用说明
链接github项目主页


## 开发
### 环境
```
pip install -r requirements.txt
```
### 执行

```
python ./main.py
```

### 打包
```
pyinstaller -F ./main.py --noconsole -p C:\Users\dell\AppData\Local\Programs\Python\Python39\Lib;C:\Users\dell\AppData\Local\Programs\Python\Python39\Lib\site-packages; 
```