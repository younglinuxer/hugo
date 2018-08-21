+++
date = "2018-07-30T16:26:13+08:00"
title = "Redis"
categories = ["db"]
tags = ["redis"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

### redis

#### 安装及配置

```bash
# centos 下安装　redis
yum install redis -y
#基础配置　
#允许后台启动
daemonize yes # 默认daemonize no
#配置监听
bind ｛ip,or 0.0.0.0｝ # 默认bind 127.0.0.1
#设置密码　
requirepass　｛password｝ #默认　requirepass　foobared　去掉注释　将foobared 　改为你的密码
#配置开启数据库的数量
databases ｛int｝　# databases 16 默认数据库数量16个
#主从模式配置（集群模式）
slaveof {master_ip} {master_port} #redis从服务器　配置文件增加如下行　
masterauth {master_passwd} #主redis 服务器的密码
# 持久化存储


```

#### 常用命令

```bash
- 命令是不区分大小写的，但是这里为了方便和后面的 key value 进行区分所以我全部写大写，你也可以用小写。
    - 但是需要注意的是：key 是完全区分大小写的，比如 key=codeBlog 和 key=codeblog 是两个键值
官网命令列表：<http://redis.io/commands>
SET key value` #设值。eg：`SET myblog blog.youngblog.cc`
GET key #取值
INCR key #递增数字
DECR key #递减数字
KEYS * #查看当前数据库下所有的 key
APPEND key value #给尾部追加内容，如果要追加的 key 不存在，则相当于 SET key value
STRLEN key #返回键值的长度，如果键不存在则返回 0
SELECT DATABASE #选择对应的数据库
MSET key1 value1 key2 value2 #同时设置多值
MGET key1 value1 key2 value2 #同时取多值
EXPIRE key 27 #设置指定键的生存时间，27 的单位是秒
TTL key #查看键的剩余生存时间
    - 返回 -2，表示不存在，过了生存时间后被删除
    - 返回 -1，表示没有生存时间，永久存储
    - 返回正整数，表示还剩下对应的生存时间
PERSIST key #清除生成时间，重新变成永久存储（重新设置 key 的值也可以起到清除生存时间的效果）
FLUSHDB #清空当前数据库所有键值
FLUSHALL #清空所有数据库的所有键值

INFO #查看当前redis 的状态　用于监控等

CONFIG GET * #查看所有配置
config set　# 临时设置
config rewrite　# 永久设置将目前服务器的参数配置写入redis conf

redis-cli -h 192.168.123.105 -p 6379 -a younglinuxer #指定host 指定port 指定　password

```
##### 监控
```bash
redis-cli -h 192.168.123.105 -a younglinuxer info | $1 #获取redis 当前状态 自己获取对应监控项进行监控（推荐ｚａｂｂｉｘ）
```
##### 配置文件更新
```bash
config set xxxx #临时设置
config rewrite . #将当前设置写入配置文件　永久生效

```
##### 

#### 持久化,备份与恢复　RDB AOF
redis 数据存储有２种方式　rdb aof 根据配置文件使用不同策略进行数据保存　（推荐使用　rdb 或者　rdb +aof ）
##### rdb
```bash
rdb 支持性能较好　导入导出数据会比较快　但发生故障可能会存在丢失数据的可能（根据触发策略刷新到磁盘　存在时间差比较长）
/etc/redis.conf rdb 策略配置
    save 900 1　# 服务器在900秒之内被修改了1次
    save 300 10　# 服务器在300秒之内被修改了10次
    save 60 10000　# 服务器在60秒之内被修改了10000次


# rdb 备份恢复
redis-cli -h 192.168.123.105 -a younglinuxer save #刷新数据到磁盘/备份 生成文件　默认　/var/lib/redis/dump.rdb
#恢复测试
cp dump.rdb dump.rdb`date +%F` #备份数据　
redis-cli -h 192.168.123.105 -a younglinuxer FLUSHALL　# 清空所有数据 
systemctl stop redis  #先停止redis
/bin/cp  dump.rdb`date +%F` dump.rdb -f #将rdb数据文件　覆盖
××××××注意：
    如果同时开启rdb aof 备份　恢复时需要先更改配置文件关闭aof备份 appendonly no 否则不会恢复rdb 
systemctl start redis  
KEYS * # 查看redis 数据是否导入

```
##### aof
```bash
aof 备份的安全性比较高　但是性能相对较弱

/etc/redis.conf 配置文件配置
    #AOF 和 RDB 持久化方式可以同时启动并且无冲突。  
    #如果AOF开启，启动redis时会加载aof文件，这些文件能够提供更好的保证。 
    appendonly yes
    # 只增文件的文件名称。（默认是appendonly.aof）  
    # appendfilename appendonly.aof 
    #redis支持三种不同的写入方式：  
    # no:不调用，之等待操作系统来清空缓冲区当操作系统要输出数据时。很快。  
    # always: 每次更新数据都写入仅增日志文件。慢，但是最安全。
    # everysec: 每秒调用一次。折中。
    appendfsync everysec  
    # 设置为yes表示rewrite期间对新写操作不fsync,暂时存在内存中,等rewrite完成后再写入.官方文档建议如果你有特殊的情况可以配置为'yes'。但是配置为'no'是最为安全的选择。
    no-appendfsync-on-rewrite no  
    # 自动重写只增文件。  
    # redis可以自动盲从的调用‘BGREWRITEAOF’来重写日志文件，如果日志文件增长了指定的百分比。  
    # 当前AOF文件大小是上次日志重写得到AOF文件大小的二倍时，自动启动新的日志重写过程。
    auto-aof-rewrite-percentage 100  
    # 当前AOF文件启动新的日志重写过程的最小值，避免刚刚启动Reids时由于文件尺寸较小导致频繁的重写。
    auto-aof-rewrite-min-size 64mb

#生成备份文件　
redis-cli -h 192.168.123.105 -a younglinuxer config set appendonly yes # 生成/var/lib/redis/appendonly.aof 记录redis 存储相关的数据
测试　set name younglinuxer  #设置一个值　然后`cat /var/lib/redis/appendonly.aof ` 会同步到/var/lib/redis/appendonly.aof 

#恢复测试　
FLUSHALL #清楚所有key
redis-cli -h 192.168.123.105 -a younglinuxer --pipe < /var/lib/redis/appendonly2018-08-01.aof #导入aof
#KEYS * #导入后查看是否存在数据


```

#### py_redis随机生成
```python
# -*- coding: utf-8 -*-
import random
import redis

r=redis.StrictRedis(host='192.168.123.105',port=6379, password='younglinuxer')
for i in range(100):
    r.set(i, random.randint(1,1000))
# a=[r.get(i) for i in range(100)]
# print a
```

#### 参考
http://wiki.jikexueyuan.com/project/all-about-redis/　
https://www.jianshu.com/p/bedec93e5a7b