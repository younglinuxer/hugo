+++
date = "2018-07-29T11:18:25+08:00"
title = "Rabbitmq"
categories = ["db"]
tags = ["db"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++
### rabbitmq 

#### 单机安装
 有 EPEL 源的情况（需要安装的内容较多，宽带要能跟上）：
  ```bash
sudo yum install erlang
```
 RabbitMQ 官网提供 Erlang 安装包：
  下载地址：<http://www.rabbitmq.com/releases/erlang/>
  下载好之后，安装下面两个文件：
  ```bash
  sudo yum localinstall -y esl-erlang_18.1-1~centos~6_amd64.rpm
  sudo yum localinstall -y esl-erlang-compat-18.1-1.noarch.rpm
```
 安装 RabbitMQ

此时（2016-04），最新版：**3.6.1**
```bash
yum install rabbitmq-server 
sudo yum install -y rabbitmq-server-3.6.1-1.noarch.rpm #安装rpm　下载包
#启动服务：
    先看下自己的主机名：`hostname`，我的主机名是：**younglinux**
    先修改一下 host 文件：`vim /etc/hosts`，添加一行：`127.0.0.1 younglinux`（必须这样做）
    启动：service rabbitmq-server start  systemctl start rabbitmq-server ，启动一般都比较慢，所以别急
    停止：service rabbitmq-server stop
    重启：service rabbitmq-server restart
    设置开机启动：chkconfig rabbitmq-server on  systemctl enable rabbitmq-server
    查看日志　tailf /var/log/rabbitmq/rabbit@talust-k8s.log

```
#### 集群安装
```bash

1.安装rabbitmq-server (所有节点都需要安装) 
2.所有节点添加对应　/etc/hosts 添加所有节点的主机和ip
3.所有节点,设置一致的　/var/lib/rabbitmq/.erlang.cookie　#将一个节点的cookie复制到其他节点 并更改权限　chomd 400  /var/lib/rabbitmq/.erlang.cookie && chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie
4.节点加入集群　rabbitmqctl stop_app　＆＆　rabbitmqctl join_cluster rabbit@node1　＆＆　rabbitmqctl start_app
　　#使用内存节点则添加参数　rabbitmqctl join_cluster --ram rabbit@node1 　
5.查看集群状态 rabbitmqctl cluster_status
# 其他问题根据日志进行排除
```


#### 常用命令
```bash
#开启web　管理
rabbitmq-plugins enable rabbitmq_management  #centos6 不在默认环境变量下面　/usr/lib/rabbitmq/bin/　 执行rpm -ql rabbitmq-server 进行查找
systemctl restart rabbitmq-server #重启ｍｑ 生效

rabbitmqctl add_user young "password"  #新增用户young
rabbitmqctl set_user_tags young administrator  #设置用户tag administrator
 rabbitmqctl help  set_permissions 
rabbitmqctl set_permissions -p / young '.*' '.*' '.*'  #设置用户权限，这里设置/(根目录) 所有权限
rabbitmqctl list_queues #查看所有队列
rabbitmqctl status #查看运行状态

```
#### 用户管理命令
```bash
# 在rabbitmq的内部数据库添加用户；
add_user <username> <password>  
# 删除一个用户；
delete_user <username>  
# 改变用户密码（也是改变web管理登陆密码）；
change_password <username> <newpassword>  
# 清除用户的密码，该用户将不能使用密码登陆，但是可以通过SASL登陆如果配置了SASL认证；
clear_password <username> 
# 设置用户tags；
set_user_tags <username> <tag> ...
# 列出用户；
list_users  
# 创建一个vhosts；
add_vhost <vhostpath>  
# 删除一个vhosts；
delete_vhost <vhostpath>  
# 列出vhosts；
list_vhosts [<vhostinfoitem> ...]  
# 针对一个vhosts给用户赋予相关权限；
set_permissions [-p <vhostpath>] <user> <conf> <write> <read>  
# 清除一个用户对vhosts的权限；
clear_permissions [-p <vhostpath>] <username>  
# 列出哪些用户可以访问该vhosts；
list_permissions [-p <vhostpath>]   
# 列出该用户的访问权限；
list_user_permissions <username>  # 示例如上（常用命令）
set_parameter [-p <vhostpath>] <component_name> <name> <value>
clear_parameter [-p <vhostpath>] <component_name> <key>
list_parameters [-p <vhostpath>]
```

#### queues && exchange状态信息
```bash
# 返回queue的信息，如果省略了-p参数，则默认显示的是"/"vhosts的信息；
list_queues [-p <vhostpath>] [<queueinfoitem> ...]  
# 返回exchange的信息；
list_exchanges [-p <vhostpath>] [<exchangeinfoitem> ...]  
# 返回绑定信息；
list_bindings [-p <vhostpath>] [<bindinginfoitem> ...] 
# 返回链接信息；
list_connections [<connectioninfoitem> ...]  
# 返回目前所有的channels；
list_channels [<channelinfoitem> ...]  
# 返回consumers；
list_consumers [-p <vhostpath>]  
# 显示broker的状态；
status  
# 显示环境参数的信息；
environment  
# 返回一个服务状态report；
report
```
#### 集群管理　
```bash
# clusternode表示node名称，--ram表示node以ram node加入集群中。默认node以disc node加入集群，在一个node加入cluster之前，必须先停止该node的rabbitmq应用，即先执行stop_app；
join_cluster <clusternode> [--ram]  
# 显示cluster中的所有node；
cluster_status                      
# 改变一个cluster中节点的模式，该节点在转换前必须先停止，不能把一个集群中唯一的disk node转化为ram node；
stop_app
change_cluster_node_type disc | ram
start_app
# 远程移除cluster中的一个node，前提是该node必须处于offline状态，如果是online状态，则需要加--offline参数；
forget_cluster_node [--offline]     
# 更新集群节点；
update_cluster_nodes clusternode    
# 同步镜像队列；
sync_queue queue                    
# 取消同步镜像队列；
cancel_sync_queue queue
```