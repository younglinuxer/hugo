+++
date = "2018-08-04T23:16:26+08:00"
title = "Tomcat"
categories = ["linux"]
tags = ["linux"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

#### tomcat配置

##### 配置规范
```bash
#使用项目名命名为user 项目使用{user}用户运行
useradd -d /data/app/{user} -s /sbin/nologin {user}
#保证{user}的home 目录下属主始终为{user}
cp -r tomcat/* /data/app/{user} && chown -r {user}:{user} /data/app/{user}
CATALINA_OPTS 根据服务器配置和服务器运行项目数量更改 具体方法见下文
tomcat shutdown_port(8005) web_port(8080) 根据项目规范并统一端口
最大并发数限制 超时限制(注意不要与上层的超时限制冲突[如负载均衡器等])
禁用manager功能等
```
##### catalina.sh 配置
```bash
#catalina.sh 为tomcat核心脚本
1.JAVA_HOME(默认使用系统的jdk 也可以指定jdk位置[比如一台服务器运行几个不同版本的jdk这种奇葩需求])
2.CATALINA_HOME CATALINA_BASE (默认取值为当前catalina所在的应用目录 tomcat多实例的核心配置就是传入不同的CATALINA_BASE)
3.CATALINA_OUT 定义日志输出文件,如没有特殊配置所有日志输出到$CATALINA_BASE/logs/catalina.out (可以根据自己需求自己定义日志的输出位置,或者在启动脚本中定义日志输出)
4.JAVA_OPTS  JVM相关策略设置等 详见下文
```
###### CENTOS6启动脚本
```bash
#centos6 启动脚本
#!/bin/bash
# chkconfig: 2345  80 50
. /etc/rc.d/init.d/functions

ret=0

app_name={{app_name}}

start() {
                echo -n "start $app_name"
                daemon daemonize -a -c /data/app/$app_name/ \
                        -p /var/run/$app_name.pid \
                        -u $app_name \
                        -o /data/logs/app/$app_name.log \
                        -e /data/logs/app/$app_name.log \
                         /data/app/$app_name/bin/catalina.sh run

}

stop() {
                echo -n  "stop $app_name"
                killproc -p /var/run/$app_name.pid
                if [ $? -eq 0 ];then
                   rm -rf /var/run/$app_name.pid
                fi
                echo
               
}


# See how we were called.
case "$1" in
  start)
        status -p /var/run/$app_name.pid > /dev/null 2>&1 && exit 0
        start
        ;;
  stop)
        stop
        ;;
  restart)
        stop
        start
        ;;
  status)
        status -p /var/run/$app_name.pid
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 1
esac

exit $ret

```
###### CENTOS7 SYSTEM SCRIPT
```bash
# Systemd unit file for tomcat
[Unit]
Description=Apache Tomcat Web Application Container
After=syslog.target network.target

[Service]
Type=forking

Environment=CATALINA_PID=/data/app/{user}/temp/tomcat.pid
Environment=CATALINA_HOME=/data/app/{user}
Environment=CATALINE_BASE=/data/app/{user}
Environment=CATALINA_OUT=/data/logs/{user}.log
Environment='CATALINE_OPTS=-Xms128M -Xmx765M -server -XX:+UseParallelGC'
Environment='JAVA_OPTS=-Djava.awt.haedless=true -Djava.security.egd=file:/dev/./urandom'

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/bin/kill -15 $MAINPID

User={user}
Group={user}

[Install]
WantedBy=multi-user.target
```
###### JAVA_OPTS 设置
```bash 
注:部分参数未能理解   
 JAVA_OPTS: "-server -Xms2048m -Xmx2048m -Xmn512m -XX:PermSize=256M -XX:MaxPermSize=256m -Xss256k"
 JAVA_OPTS="-Dfile.encoding=UTF-8 -server -Xms6144m -Xmx6144m -XX:NewSize=1024m -XX:MaxNewSize=2048m -XX:PermSize=512m -XX:MaxPermSize=512m -XX:MaxTenuringThreshold=10 -XX:NewRatio=2 -XX:+DisableExplicitGC"   
 -Dfile.encoding：默认文件编码
 -server：表示这是应用于服务器的配置，JVM 内部会有特殊处理的
 -Xmx1024m：设置JVM最大可用内存为1024MB
 -Xms1024m：设置JVM最小内存为1024m。此值可以设置与-Xmx相同，以避免每次垃圾回收完成后JVM重新分配内存。
 -XX:NewSize：设置年轻代大小
 -XX:MaxNewSize：设置最大的年轻代大小
 -XX:PermSize：设置永久代大小
 -XX:MaxPermSize：设置最大永久代大小
 -XX:NewRatio=4：设置年轻代（包括 Eden 和两个 Survivor 区）与终身代的比值（除去永久代）。设置为 4，则年轻代与终身代所占比值为 1：4，年轻代占整个堆栈的 1/5
 -XX:MaxTenuringThreshold=10：设置垃圾最大年龄，默认为：15。如果设置为 0 的话，则年轻代对象不经过 Survivor 区，直接进入年老代。对于年老代比较多的应用，可以提高效率。如果将此值设置为一个较大值，则年轻代对象会在 Survivor 区进行多次复制，这样可以增加对象再年轻代的存活时间，增加在年轻代即被回收的概论。
 -XX:+DisableExplicitGC：这个将会忽略手动调用 GC 的代码使得 System.gc() 的调用就会变成一个空调用，完全不会触发任何 GC
```
###### 无法停止tomcat
```bash
如果使用 shutdown.sh 还无法停止 tomcat，可以修改其配置：vim shutdown.sh
把最尾巴这一行：exec "$PRGDIR"/"$EXECUTABLE" stop "$@"
改为：exec "$PRGDIR"/"$EXECUTABLE" stop 10 -force
```

##### conf 配置
###### 链接池配置
```xml
<!--server.xml-->
<!--默认配置未打开 -->
<Executor name="tomcatThreadPool" namePrefix="catalina-exec-"
                maxThreads="150" minSpareThreads="4"/>
<!--修改配置为-->
<Executor
        name="tomcatThreadPool"
        namePrefix="catalina-exec-"
        maxThreads="500"
        minSpareThreads="30"
        maxIdleTime="60000"
        prestartminSpareThreads = "true"
        maxQueueSize = "100"
/>
<!--重点参数解释：-->
<!--maxThreads，最大并发数，默认设置 200，一般建议在 500 ~ 800，根据硬件设施和业务来判断-->
<!--minSpareThreads，Tomcat 初始化时创建的线程数，默认设置 25-->
<!--prestartminSpareThreads，在 Tomcat 初始化的时候就初始化 minSpareThreads 的参数值，如果不等于 true，minSpareThreads 的值就没啥效果了-->
<!--maxQueueSize，最大的等待队列数，超过则拒绝请求-->
<!--maxIdleTime，如果当前线程大于初始化线程，那空闲线程存活的时间，单位毫秒，默认60000=60秒=1分钟。-->
```
###### 端口更改
```xml
<!--修改如下端口shutdown端口-->
<Server port="{{shutdown_prot}}" shutdown="SHUTDOWN">
<!--修改如下端口http端口-->
<Connector port="{{http_prot}}" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443"/>
<!--注释掉下面这行-->
<Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />

```
###### 日志配置
```bash
1.catalina 中指定 CATALINA_OUT的输出文件
2.配置logging.properties 
```

##### tomcat + redis + seesion
```bash
多台tomcat实现seesion的共享(如原项目没有考虑到集群模式等情况) 
详见：
https://github.com/jcoleman/tomcat-redis-session-manager.git
```