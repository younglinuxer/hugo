+++
date = "2018-08-04T23:15:40+08:00"
title = "Nginx"
categories = ["linux"]
tags = ["linux"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

### nginx 一些故障处理

#### vue项目404
```bash
#在server配置下添加 
try_files $uri $uri/ /index.html;
#官方说明
https://router.vuejs.org/guide/essentials/history-mode.html#example-server-configurations
```

#### 应用防火墙

#### Google代理模块

#### 4层转发 tcp udp
```bash
#设置stream 模块包含的配置文件 (注意stream 应该和http配置同层 stream属于4层)
#详见 https://docs.nginx.com/nginx/admin-guide/load-balancer/tcp-udp-load-balancer/
stream {
    include /etc/nginx/stream.d/*.conf;

    }

server {
        listen                65443;
        proxy_pass            172.17.234.25:6443;
       } 

#设置udp
server {
        listen                53 udp; 
        proxy_pass            xxxx udp;
       } 
```

#### 禁止未配置的域名访问+监控统计
```json
# cat /etc/nginx/conf.d/_default.conf
# 配置http的未配置域名处理 
server {
        listen       80 default_server;
        server_name  _;
        access_log      off;
        return 444;
    }

#配置https 未配置域名处理
server {
    listen 443 ssl default_server;
    server_name _;

    ssl_certificate /etc/nginx/certs/fullchain.pem;     
    ssl_certificate_key /etc/nginx/certs/privkey.pem;
    access_log      off;
    return 444;
    }

# nginx 监控配置
server {
       listen          localhost:18081;
       server_name     nginx_status.localhost;
       location /nginx_status {
               stub_status     on;
               access_log      off;
               allow           127.0.0.1;
               deny            all;
       }
}

```

#### 免费生产泛域名ssl证书
```bash
#免费生产ssl 泛域名解析网址 https://certbot.eff.org/  #安装按照网址提示操作

#如生产ssl报错 可尝试加入如下参数
certbot -d *.youngblog.cc --installer nginx --manual --preferred-challenges dns certonly

# 按照提示 添加dns解析 等待DNS 生效后 通过验证

nslookup -q=txt {your_domain} 查询txt 记录类型的值

```
