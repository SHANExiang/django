# -*- coding:utf-8 -*-
# 配置了服务器地址、端口、发送的url、请求的超时时间，以及日志文件路径


import os

# 远端接收数据的服务器
Params= {
    'server': '192.168.169.225',
    'port': 8080,
    'url': '/assets/report/',
    'request_timeout': 30,
}

# 日志文件配置
PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')
