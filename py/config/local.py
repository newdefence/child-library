# coding=utf-8

import urllib

# 数据库连接地址
# mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
mongodb = "mongodb://%(username)s:%(password)s@%(hosts)s/%(database)s?%(options)s" % {
    "username": 'defencezhang',
    "password": 'qaz123',
    "hosts": 'cluster0-shard-00-00-oxtxc.azure.mongodb.net:27017',
    # ('cluster0-shard-00-00-oxtxc.azure.mongodb.net:27017', 'cluster0-shard-00-01-oxtxc.azure.mongodb.net:27017', 'cluster0-shard-00-02-oxtxc.azure.mongodb.net:27017',)
    'database': 'cj',
    'options': urllib.urlencode({
        'ssl': 'true', # lower(str(True)).
        'replicaSet': 'Cluster0-shard-0',
        'authSource': 'admin',
        'retryWrites': 'true',
    }),
}

# 二维码域名
QrCodeHost = '127.0.0.1:8999'

# string = 'mongodb://defencezhang:<PASSWORD>@cluster0-shard-00-00-oxtxc.azure.mongodb.net:27017,cluster0-shard-00-01-oxtxc.azure.mongodb.net:27017,cluster0-shard-00-02-oxtxc.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
# mongo "mongodb://cluster0-shard-00-00-oxtxc.azure.mongodb.net:27017,cluster0-shard-00-01-oxtxc.azure.mongodb.net:27017,cluster0-shard-00-02-oxtxc.azure.mongodb.net:27017/test?replicaSet=Cluster0-shard-0" --ssl --authenticationDatabase admin --username defencezhang --password <PASSWORD>

