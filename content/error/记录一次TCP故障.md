+++
date = "2018-11-08T16:07:01+08:00"
title = "记录一TCP故障处理"
categories = ["故障"]
tags = ["故障"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://blog.youngblog.cc"

+++

### 记录一TCP故障处理

#### 故障想象
```bash
1.办公室网络无法正常访问阿里云部分服务器(时好时坏 断断续续 ) (tcp 直接拒绝) 
2.除办公室网络,其他网络都能正常访问
3.mtr工具测试没有丢包情况
```

#### 故障排查
```bash
1.怀疑本地网络相关限制  检查本地网络是否有相关限制(本地没有限制 但是重启网络后会暂时好个几分钟 然后又开始抽风)
2.通过 tracetcp 进行链路跟踪 发现到阿里云机房后开始网络不通(不同于 tracert  tracetcp 可以跟踪端口 详情https://help.aliyun.com/knowledge_detail/40572.html)
3.怀疑 是阿里云相关服务给屏蔽办公室公网 (添加安盾服务白名单 无效果 提阿里云工单帮忙检查)
4.阿里云无相关限制 继续排查
5.本地访问相关服务抓包,服务器抓包 (对比两边的抓包数据 查看是否有正常建立连接 )
6.发现数据包有到达服务器 但是数据包无返回 (tcp retransmission )
7.如果问题出在服务器(为啥其他地方都能正常访问) 如果问题出在办公室(为啥只有公司的应用服务器无法连接 )
```

#### 结果处理
```bash
最后查出问题在内核参数设置上 服务器上配置了2条内核参数存在问题 (https://help.aliyun.com/knowledge_detail/41297.html?spm=a2c4g.11186631.2.4.47625807bDgZCz)
设置内核参数：
net.ipv4.tcp_tw_recycle=0
net.ipv4.tcp_timestamps=0

办公室出口路由器为 OPENWRT 用户上网用IPTABLES 转发到三层交换机上 (估计是OPENWRT的内核参数与服务器内核参数不一致)
(最后感谢阿里云的兄弟 帮忙处理)
```

##### 参考资料
```bash
https://yq.aliyun.com/articles/475509
https://blog.csdn.net/wireless_tech/article/details/6405755
https://blog.csdn.net/zhuyiquan/article/details/68925707
```