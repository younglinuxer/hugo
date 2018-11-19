+++
date = "2018-08-04T23:14:05+08:00"
title = "Mysql(1)"
categories = ["db"]
tags = ["mysql"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

#### mysql 常用

##### 安装
```bash
#centos7 安装5.7
yum install https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm #5.7
yum install mysql-community-server #注意安装版本5.7
#centos7 安装5.6
yum install http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
yum install mysql-community-server #注意安装版本5.6
# 8.0 同理

#centos6 安装5.7
yum install http://dev.mysql.com/get/mysql57-community-release-el6-9.noarch.rpm
yum install mysql-community-server
#centos6 安装5.6
yum install http://repo.mysql.com/mysql-community-release-el6-5.noarch.rpm
yum install mysql-community-server
#或者
yum install http://dev.mysql.com/get/mysql57-community-release-el6-9.noarch.rpm
yum-config-manager --disable mysql57-community
yum-config-manager --enable mysql56-community
yum install mysql-community-server
```
###### 参数优化
```bash

详见 https://github.com/RodrigoViolante/my.cnf.git 根据自己的情况取舍
```
###### 数据目录设置
```bash
```
###### 磁盘选择+文件系统选择
###### 日志优化
###### 字符集设置
##### 备份与恢复
###### 逻辑备份
###### 物理备份
```bash
yum install percona-xtrabackup -y
#使用innobackupex 备份数据库
innobackupex  --password=$PASSWORD --user=$USER --host=$HOST --port=$PORT --stream=tar $TO/$HOSTNAME-db-$date | gzip > $TO/$HOSTNAME-db-$date.tgz
#会生成相关的binlog和position信息（重要）
#恢复数据库  下面2步是必须执行的 网上大多数教程都有点问题
innobackupex --apply-log /data/backup/xxxxxxx
innobackupex --move-back /data/backup/xxxxxxx/
```
###### 数据迁移验证



