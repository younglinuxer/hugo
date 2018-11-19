+++
date = "2018-07-16T22:22:25+08:00"
title = "Yum"
categories = ["linux"]
tags = ["linux"]
toc = true
comments = true
author = "younglinuxer"
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

## yum 安装软件的一些技巧

##### 添加源
```bash
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

##### 查询软件版本
```bash
yum list docker-ce --showduplicates | sort -r
yum install docker-ce-<VERSION STRING> #安装指定版本
```

##### 安装开发软件组
```bash
yum -y group install "Development Tools"
```


##### provides
```bash
#查找包含文件的软件包 如报错缺少文件　又不知道缺少啥软件的时候可以通过yum 搜索
yum provides libneon.so 

#查询命令属于哪个软件包 如查询nslookup 属于哪个软件包 
yum provides */nslookup
```

##### 显示软件包的依赖信息
```bash
yum deplist nginx  
```

##### yum search
```bash
yum search jdk
yum list *jdk* #yum list 支持正则
``` 

##### 更新软件包　
```bash
yum update -y #更新软件
yum makecache fast #更新索引加快搜索速度
yum clean all  #清理缓存　删除　/var/cache/yum/
```


##### 完全卸载yum包
rpm -qa|grep yum|xargs rpm -e--nodeps


# 其他插件

yum-plugin-downloadonly