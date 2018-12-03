+++
date = "2018-11-27T18:47:57+08:00"
title = "docker日志持久化及报警"
categories = ["linux"]
tags = ["docker"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://blog.youngblog.cc"

+++

### docker 日志持久化及应用日志报错巡检

##### docker & k8s 日志常用操作
```bash
docker logs 
    -f #跟踪日志输入
    -t #输出时间 如果日志默认没有时间 则会在日志输出时添加上时间
    --tail #和linux下的tail 命令类似
    --since #查找特定时间之后的日志 如  docker logs --since="2018-11-26" 查找26号之后的日志
    --until #查找特定时间之前的日志  

#/etc/docker/daemon.json 日志相关配置配置日志切割,level,大小,等 
#docker logs 能获取到切割后的日志 kubectl logs 则不能获取到所有日志
```

##### ELK or EFK 的弊端
```bash
1.占用服务器资源太高 
2.对于容器的日志处理并不友好 
3.能实现日志持久化 但是对于大日志查询过于繁琐(可能为个人习惯问题)
```

##### 实现脚本
###### 脚本思路
```bash
1.根据docker ps 匹配出业务应用的docker容器,过滤掉K8S的守护,用awk取出docker_id(K8S部署后pod的名字为pod_name+随机字符串)
2.使用docker logs 获取前一天的日志(docker 配有日志切割 当日志达到一定大小后自动切割,docker logs 能获取到切割后的日志,但是kubectl logs 只能获取到未切割的日志)
3.loop所有项目的日志并重定向到规划的日志目录
4.grep 取出异常的日志(本文是直接过滤掉正常的日志,所有项目logs均统一输出标准时间,如项目报错则不会输出时间,这里直接取无时间输出的日子,自己使用时根据自己的实际情况修改),并将异常日志输出到单独的文件
5.邮件发送错误日志
```
###### 日志处理脚本
```bash
#!/bin/bash
LOGS_OUT_DIR=/data/logs
BACKNUM=30
YETDAY=`date -d last-day +%F`
SERVICES_LIST="talust-common talust-email talust-evi talust-file talust-im talust-notify talust-sms talust-pay talust-item talust-order talust-approval talust-clockin talust-contract talust-enterprise talust-notice talust-recruit talust-reports talust-training talust-storage talust-assessment talust-config talust-gateway talust-register talust-management talust-message talust-job talust-txmanager talust-rabbitmq talust-user"

SAVA_LOGS(){
	# 保存日志
	for app in $SERVICES_LIST; do
		/opt/kube/bin/docker logs --since="$YETDAY" `/opt/kube/bin/docker ps |grep $app|grep -v k8s_POD_|awk '{print $1}'` > $LOGS_OUT_DIR/$app-$YETDAY.log 2>&1
	done
}

SEND_ERR(){
	YET_LOG=`ls $LOGS_OUT_DIR/*$YETDAY.log`
	mv $LOGS_OUT_DIR/app_err.log $LOGS_OUT_DIR/app_err-`date +%F`.log
	for app_log in $YET_LOG; do
		echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx $app_log xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" >>$LOGS_OUT_DIR/app_err.log 
		grep -v -E "`date +%F`|$YETDAY" $app_log >>$LOGS_OUT_DIR/app_err.log 
	done
	# 发送报错日志
	python /data/bin/sendmail_file.py younglinuxer@gmail.com $YETDAY-err  $LOGS_OUT_DIR/app_err.log
}

DEL_EXPIRE(){
	# 删除指定过期时间的日志
	find $LOGS_OUT_DIR -mtime +$BACKNUM | xargs rm -rf {};
}

SAVA_LOGS
SEND_ERR
DEL_EXPIRE
```
###### 邮件发送脚本
```python
#!/usr/bin/python
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from  email.mime.multipart import  MIMEMultipart
from  email.mime.text import MIMEText
from  email.mime.application import MIMEApplication
from email.header import Header
import sys

#邮箱服务器地址
mail_host = 'smtp.mxhichina.com'
#邮箱用户名
mail_user = 'dev@talust.org'
#邮箱密码
mail_pass = 'xxxxxx'
to_list=["yuanby@talust.org","1352794122@qq.com"]

#传入content 为日志文件  读取后通过邮件发送
#邮件发送
def send_mail(to_list,sub,content):
    # me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    me=mail_user
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = me
    # msg['To'] = ";".join(to_list)
    msg['To'] = to_list
    part = MIMEText(open(content,'r').read(),_charset='utf-8')
    msg.attach(part)
    part =MIMEApplication(open(content,'rb').read())
    msg.attach(part)
    # msg["Accept-Language"]="zh-CN"
    # msg["Accept-Charset"]="ISO-8859-1,utf-8"
    try:
        s = smtplib.SMTP_SSL(mail_host,465)
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == "__main__":
    print sys.argv[1]
    print sys.argv[2]
    print sys.argv[3]
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3])

```

##### 部署方式(单台 多台)
```bash
#生产多台节点解决方案
1.日志保存到公用存储下(如nfs 上边脚本只运行第一个函数收集日志,不对日志进行处理)
2.所有节点部署定时任务定期刷新日志到存储 (如节点比较多可以写到 saltstack 或者ansible 里面)
3.选取其中一个节点 执行日志过滤并发送邮件
```
