+++
date = "2018-06-05T12:30:05+08:00"
title = "linux Mint "
categories = ["linux"]
tags = ["linux"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "http://blog.youngblog.cc"

+++
#### linux Mint 安装优化记录

#### 描述 
```
最近为了戒掉游戏 决定放弃windows的坑 入了linux的坑 对比了几个不同的发行版本 最后决定使用 linux Mint 
记录一下系统的安装和一部分软件优化的使用
```

#### 系统安装
```
1.官方下载最新版　https://www.linuxmint.com/download.php (cinnamon,MATE,xfce,KDE 分别对应不同的桌面　我们这里选择安装ｃinnamon)
2.下载　“软碟通”　并将镜像刻录到U盘　重启电脑并通过ｕ盘启动　就直接能进入系统安装界面按提示一步步安装就行了
3.关于笔记本硬盘分区　SSD硬盘安装系统文件系统默认 ext4 另外一块机械硬盘使用btrfs 
      找到自己需要挂载的硬盘　　fdisk -l  (找到自己对应的硬盘为　/dev/sda)
      格式化硬盘　mkfs.btrfs /dev/sda　-f (-f  force　)
      挂载硬盘　mount /dev/sda /younglinuxer/ 
      添加到fstab  
      ##### by young 2018-06-06
      /dev/sda /younglinxer               btrfs    defaults 0       0

```

#### 软件安装

```
1.音乐软件apt源带有　spotify的安装包,但是无奈vpn服务器的流量有限　果断猪厂的音乐软件　‘网易云音乐’　支持deepin和ubuntu 这里选择ubuntu　
    ****网易云音乐自带的启动链接有问题 这里给出一个解决方式　×××右键新建一个启动器　启动命令填写　‘sudo netease-cloud-music’
2.浏览器　默认有火狐浏览器　可以安装chromium（chrome）//自带的apt源就有
3.输入法　选择安装中文会自带的有fcitx的输入法　但有点小问题　这里选择单独选择安装搜狗输入法　
4.IDE工具　这里使用idea　官网下载最新版解压使用就行　下载商业版可以有更多的支持　下方提供 idea注册码
5.数据库连接工具　mysql-workbench　apt install 就行
6.服务器连接工具　目前有putty 但是个人习惯使用xhell 并不习惯　仍然在继续探索ing
7.微信安装　直接使用网页版　chrome 可以右键直接将网页保存到桌面　和正常使用一样
```
[猪厂音乐软件](https://music.163.com/#/download)
[搜狗输入法下载](https://pinyin.sogou.com/linux/?r=pinyin)
[idea 注册码](http://idea.lanyus.com/)

#### 翻墙＆问题处理
sublimt 中文无法输入问题

```
git clone https://github.com/lyfeyaj/sublime-text-imfix.git  /data/src
cd /data/src/sublime-text-imfix 
./sublime-imfix 
// 执行上面脚本后会在/opt/sublime_text/ 生成相关依赖　更改/usr/bin/subl 
// 如果还无法输入中文　请添加下面内容到　/etc/profile.d/sublime.sh
 export LD_PRELOAD=/opt/sublime_text/libsublime-imfix.so
```

翻墙采用shadowsocks + kcp 


```
shadowsocks kcp 安装教程具体请网上自行搜索
```
```
//kcp配置
wget https://github.com/xtaci/kcptun/releases/download/v20180316/kcptun-linux-amd64-20180316.tar.gz /data/src
cd /data/src && tar xf kcptun-linux-amd64-20180316.tar.gz 
mv kcp_client /usr/local/sbin 
//添加　开启启动程序　kcp_client -c /etc/shadowsocks/kcp.json　
```
```
//shadowsocks配置
wget https://github.com/shadowsocks/shadowsocks-go/releases/download/1.1.5/shadowsocks-local-linux64-1.1.5.gz /data/src
cd /data/src && gunzip shadowsocks-local-linux64-1.1.5.gz
mv ./shadowsocks-local-linux64-1.1.5 /usr/local/sbin/ss-client
//添加开启启动程序　
```

```
//pac 自动代理分流
// apt install python-pip gcc 
pip install genpac
cd /etc/shadowsocks 
genpac --proxy="SOCKS5 127.0.0.1:1080" --gfwlist-proxy="SOCKS5 127.0.0.1:1080" -o autoproxy.pac --gfwlist-url="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"

// 生成文件　/etc/shadowsocks/autoproxy.pac 

修改网络设置　设置网络自动代理　输入下面地址
file:///etc/shadowsocks/autoproxy.pac

```
