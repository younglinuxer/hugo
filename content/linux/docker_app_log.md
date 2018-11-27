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
1.根据
```
###### 日志处理脚本
```bash
#!/bin/bash
LOGS_OUT_DIR=/data/logs
BACKNUM=30
YETDAY=`date -d last-day +%F`
SERVICES_LIST="talust-common talust-email talust-evi talust-file talust-im talust-notify talust-sms talust-pay talust-item talust-order talust-approval talust-clockin talust-contract talust-enterprise talust-notice talust-recruit talust-reports talust-training talust-storage talust-assessment talust-config talust-gateway talust-register talust-management talust-message talust-job talust-txmanager talust-rabbitmq talust-user"
# docker ps |grep xxxxx|grep -v k8s_POD_|awk '{print $1}' 獲取容器ID
# docker logs -t `docker ps |grep talust-gateway|grep -v k8s_POD_|awk '{print $1}' `|grep `date -d last-day +%FF` 獲取容器日志 -t 按時間格式輸出后過濾時間 date -d last-day +%F獲取前一天的日期

SAVA_LOGS(){
        # 保存日志
        for app in $SERVICES_LIST; do
                # docker logs -t `docker ps |grep $app|grep -v k8s_POD_|awk '{print $1}' `|grep `date -d last-day +%F` > $LOGS_OUT_DIR/$app_`date -d last-day +%F`.log 2>&1  grep 查找时间会出现 部分报错日志无法保存
                docker logs --since="$YETDAY" `docker ps |grep $app|grep -v k8s_POD_|awk '{print $1}'` > $LOGS_OUT_DIR/$app-$YETDAY.log 2>&1
        done
}

SEND_ERR(){
        YET_LOG=`ls $LOGS_OUT_DIR/*$YETDAY.log`
        mv $LOGS_OUT_DIR/app_err.log $LOGS_OUT_DIR/app_err-`date +%F`.log
        for app_log in $YET_LOG; do
                echo "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx $app_log xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" >>$LOGS_OUT_DIR/app_err.log
                # 项目应用log4j 都配有日期 过滤掉日期后就只剩下报错的日志了  所有项目报错日志统一输出到app_err.log下面
                #grep -v $YETDAY $app_log >>$LOGS_OUT_DIR/app_err.log 
                grep -v -E "`date +%F`|2018-11-26" $app_log >>$LOGS_OUT_DIR/app_err.log
        done
        # 发送报错日志
        python sendmail_file.py younglinuxer@gmail.com $YETDAY-err  $LOGS_OUT_DIR/app_err.log
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

##### 部署方式(单台 多台)
