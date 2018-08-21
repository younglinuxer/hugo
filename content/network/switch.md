+++
date = "2018-08-05T10:10:01+08:00"
title = "Switch"
categories = ["linux"]
tags = ["linux"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

#### 华为交换机配置

##### 基础配置
```bash
#ssh 配置
# 配置vty用户界面
system-view 
user-interface vty 0 4 
authentication-mode aaa 
quit 
# 创建ssh用户并配置其认证方式为password
aaa
local-user <user> password cipher <password>
local-user <user> level 15
local-user <user> service-type telnet terminal ssh web   
```
　
###### vty配置（用户权限）　
###### vlan划分　
```bash

```

###### 地址池划分　
###### dhcp
###### acl

##### 常用配置
###### 链路聚合
###### 路由配置
###### nat上网

