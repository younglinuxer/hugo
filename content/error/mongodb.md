+++
date = "2018-11-09T14:26:32+08:00"
title = "Mongodb"
categories = ["故障"]
tags = ["故障"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://blog.youngblog.cc"

+++

### mongodb 报错SCRAM-SHA-1 authentication failed for ....

#### 故障现象
```bash
docker 运行mongodb:3.6 报错
[conn6] SCRAM-SHA-1 authentication failed for talust on xxxxx from client 172.20.0.3:33426 ; UserNotFound: Could not find user xxxxx
```
#### 故障分析
```bash
docker exec -it xxx bash #进入容器 连接mongodb 排查问题
```

#### 解决办法
```bash
docker exec -it {docker-id} bash 
连接到mongodb 
mongo -uadmin -p --authenticationDatabase admin 
show dbs 
use admin 
# 查看所有用户
db.system.users.find()  

#创建数据库 并分配权限
use talust_blockchain
switched to db talust_blockchain
> db.createUser({user: "user", pwd: "passwd", roles:["dbOwner"]})
Successfully added user: { "user" : "xxx", "roles" : [ "dbOwner" ] }

# 返回查看日志 已经能成功连接数据库 
xxxx-mongodb_1    | 2018-07-12T16:24:52.575+0000 I NETWORK  [listener] connection accepted from 172.20.0.3:33482 #34 (2 connections now open)
xxx-mongodb_1    | 2018-07-12T16:24:52.575+0000 I NETWORK  [conn34] received client metadata from 172.20.0.3:33482 conn34: { driver: { name: "mongo-java-driver", version: "unknown" }, os: { type: "Linux", name: "Linux", architecture: "amd64", version: "3.10.0-693.2.2.el7.x86_64" }, platform: "Java/Oracle Corporation/1.8.0_111-internal-alpine-r0-b14" }
xxx-mongodb_1    | 2018-07-12T16:24:52.733+0000 I ACCESS   [conn34] Successfully authenticated as principal talust on talust_blockchain


 ****************************************************************************************常用命令
#插入数据测试
db.talust_blockchain.insert({"name":"younglinuxer"})

#验证用户登录
db.auth("talust","dasf")
Error: Authentication failed.
0
> db.auth("user","password")
1

#查看数据库
show dbs 

# 查看用户
show users 
```