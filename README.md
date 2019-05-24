AIKnoSearch个性化学习平台网站
========================
    1.基于Python3 + Django + elasticsearch + redis +MySQL 技术架构开发的搜索引擎网站，
    实现了实时搜索，基于用户关键词的推荐功能。
    2.网站域名www.aiknosearch.com

Versions
--------
1.0.0

Install
-------
####本地测试
* 下载

    git clone myaddress
    
* 搭建虚拟环境(windows) 
    ```
    pip install - i https://pypi.douban.com -r aikno_req.txt
    ```
    若出现mysqlclient安装异常，打开文件夹req_local安装本地whl包
    ```
    pip install mysqlclient-1.4.2-cp37-cp37m-win_amd64.whl
    ```
    若出现 No module named 'win32api'
    ```
    pip install -i https://pypi.douban.com/simple pypiwin32    
    ```
    
        
* Run(本地运行)

    安装redis 
        
    安装mysql      
        
    若安装Pycharm

        打开Pycharm 指定虚拟环境
        终端中输入 manage.py makemigrate
        终端中输入 manage.py migrate 
        配置Django 并运行
        浏览器输入127.0.0.1:8000
        
    若未安装Pycharm
    
        进入项目目录下
        终端中输入 manage.py makemigrate
        终端中输入 manage.py migrate
        manage.py runserver 127.0.0.1:8000
        浏览器输入127.0.0.1:8000
    

 

    


Deploy
-----
    基于Nginx + Uwsgi + Docker(服务环境)部署，稳定运行。
    网站域名 www.aiknosearch.com
    
     

