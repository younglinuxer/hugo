+++
date = "2018-08-04T23:19:23+08:00"
title = "Jenkins"
categories = ["linux"]
tags = ["jenkins"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

#### jenkins　小结
#### 安装　（jenkins node mvn）
```bash
mkdir /data/{app,bin,src,jenkins_home} -pv

wget http://mirrors.jenkins.io/war/latest/jenkins.war -P /data/src/
wget http://mirrors.hust.edu.cn/apache/maven/maven-3/3.5.4/binaries/apache-maven-3.5.4-bin.tar.gz -P /data/src/
wget https://nodejs.org/dist/v8.11.3/node-v8.11.3-linux-x64.tar.xz -P /data/src/

mkdir /data/app/jenkins
tar zxvf /data/src/apache-maven-3.5.4-bin.tar.gz  -C /data/app
tar xf /data/src/node-v8.11.3-linux-x64.tar.xz  -C /data/app

#创建npm 命令软链接
cd /data/app/node/bin
for i in `ls`;do ln -s /data/app/node/bin/$i /usr/local/sbin/$i ;done

#设置maven_home jenkins_home
cat /etc/profile.d/jenkins.sh 
    export JENKINS_HOME=/data/jenkins_home/
    export MAVEN_HOME=/data/app/maven-3.3.9
    export PATH=$PATH:$MAVEN_HOME/bin

#运行jenkins 指定端口为58080 

yum install java-1.8.0-openjdk java-1.8.0-openjdk-devel  #jenkins 最新版本最好使用openjdk
java -jar /data/app/jenkins/jenkins.war --httpPort=58080

#默认数据存放在JENKINS_HOME下　浏览器打开　＜ip＞：＜port＞ 按照提示安装 

```

#### 插件使用
安装时选择默认插件进行安装　如报错超时可以到官网下载对应插件进行上传　
<https://plugins.jenkins.io>

#####　推荐插件

```bash
1.Git+Parameter+Plugin #可以选择编译不同分支下的代码　https://blog.csdn.net/qq_20641565/article/details/79132797
2.gogs gogos #设置webhook根据提交触发jenkins执行项目构建　https://www.cnblogs.com/stulzq/p/8629720.html

```
　
##### 邮件配置

```bash
# 设置系统系统管理员邮箱后 邮件才会生效
系统管理　> 系统设置　> Jenkins Location > <your_email>

#设置邮件服务器
系统管理　> 系统设置　>　邮件通知　> 使用stmp认证　<根据自己实际情况进行填写>　完成后发送测试邮件

```

####  编译参数
##### 触发编译
```bash
#两种方式scm 定时检测代码仓库变动后进行编译　webhook＿gogs 根据请求进行编译　scm 在网络延迟比较的情况下不要使用
1.SCM 　任务　> 构建触发器 > 勾选轮询scm > H/5 * * * * # 每５分钟检测代码仓库是否有变动
2.webhook 安装gogos插件　> 任务　> 勾选　Use Gogs secret　> gogos 设置webhook 推送

```

##### java程序编译

```bash
#java 程序下载完成后　需要把整个项目编译一次　生成项目依赖　首次不要单独编译某个项目　会报错找不到相关依赖

######################## java 程序编译脚本　根据提交的update-service 文件对指定项目进行编译
#!/bin/bash
#程序构建 生成jar包在 /data/jenkins_home/workspace/spring-younglinuxer-auth/｛app｝/target 下面
export MAVEN_HOME=/data/app/maven-3.3.9
export PATH=$PATH:$MAVEN_HOME/bin
HOME=/data/jenkins_home/workspace/talent-chain-cloud-project
DEPLOY=`cat ${HOME}/update-service`
#循环需要更新的项目　并判断特定的项目进行编译
for i in ${DEPLOY}; do
	mvn clean -f $i
	mvn compile -DskipTests -f $HOME/$i
	mvn package -DskipTests -f $HOME/$i
	mvn install -DskipTests -f $HOME/$i
done
echo "编译完成　开始生成dockerfile"
sleep 5
rm -fr /data/jenkins_home/docker/*
#循环部署项目
for i in $DEPLOY; do
	if [[ $i == younglinuxer-enterprises ]]; then
		#statement
		for app in `ls -l $HOME/younglinuxer-enterprises|grep ^d|awk '{print $9}'`; do
			#statements
			mkdir /data/jenkins_home/docker/$app -pv
			cp $HOME/younglinuxer-enterprises/$app/target/*.jar /data/jenkins_home/docker/$app/
			cp /data/jenkins_home/dockerfile/* /data/jenkins_home/docker/$app/
			sed -i "s@APP_NAME@$app@g" /data/jenkins_home/docker/${app}/Dockerfile
		done
	elif [[ $i == younglinuxer-framework ]]; then
		#statements
		for app in `ls -l $HOME/younglinuxer-framework|grep ^d|awk '{print $9}'`; do
			#statements
			mkdir /data/jenkins_home/docker/$app -pv
			cp ${HOME}/younglinuxer-framework/$app/target/*.jar /data/jenkins_home/docker/$app/
			cp /data/jenkins_home/dockerfile/* /data/jenkins_home/docker/$app/
			sed -i "s@APP_NAME@$app@g" /data/jenkins_home/docker/$app/Dockerfile
		done
	elif [[ $i == younglinuxer-commons ]]; then
		#statements
		for app in `ls -l $HOME/younglinuxer-commons|grep ^d|awk '{print $9}'`; do
			#statements
			mkdir /data/jenkins_home/docker/$app -pv
			cp ${HOME}/younglinuxer-commons/$app/target/*.jar /data/jenkins_home/docker/$app/
			cp /data/jenkins_home/dockerfile/* /data/jenkins_home/docker/$app/
			sed -i "s@APP_NAME@$app@g" /data/jenkins_home/docker/$app/Dockerfile
		done
	else
		mkdir /data/jenkins_home/docker/$i -pv
		cp $HOME/$i/target/*.jar /data/jenkins_home/docker/$i/
		cp /data/jenkins_home/dockerfile/* /data/jenkins_home/docker/$i/
		sed -i "s@APP_NAME@$i@g" /data/jenkins_home/docker/$i/Dockerfile

	fi
done

```

##### node编译

```bash
# npm 编译指定标签　如果依赖下载过慢可以使用　cnpm(阿里单独出来的使用阿里的源仓库)
####### node 编译脚本

#!/bin/bash
npm config set unsafe-perm true
npm config set electron_mirror https://npm.taobao.org/mirrors/electron/
npm config set sass-binary-site https://npm.taobao.org/mirrors/node-sass/
npm config set registry http://dev.younglinuxer.com:18002/nexus/repository/npm
#npm install -d
npm install -g
npm update
npm config set unsafe-perm true
###放弃npm 编译 采用cnmp 进行编译
#HOME=/data/jenkins_home/workspace/ui-manager-project-test-enterprise
#cd $HOME
npm install 
npm run build:test
# 更新源码目录
rm -fr /data/jenkins_home/younglinuxer-ui/app/enterprise/
mv /data/jenkins_home/workspace/ui-manager-enterprise/dist /data/jenkins_home/younglinuxer-ui/app/enterprise

```

##### 程序编译说明
```bash
# java
mvn 编译生成jar包　> 根据编译的项目在/data/jenkins_home/docker生成对应的项目　> 移动对应项目的jar包和Dockerfile到/data/jenkins_home/docker/<project>  > 根据项目名替换Dockerfile
> 根据项目名编译docker 并推送到harbor仓库

#node 
npm编译程序 > 替换docker(/data/jenkins_home/younglinuxer-ui)对应的源码　> 编译docker并推送到harbor仓库

```

#### 打包镜像
```bash
#打包镜像并推送到docker 仓库
#!/bin/bash
# docker 编译并推送镜像
docker login -uyuan.yang -paA52419589 https://dev.younglinuxer.com:18443
for i in `ls /data/jenkins_home/docker`
do
	docker build -t dev.younglinuxer.com:18443/younglinuxer-v2/$i /data/jenkins_home/docker/$i/
    docker push dev.younglinuxer.com:18443/younglinuxer-v2/$i:latest
    docker tag dev.younglinuxer.com:18443/younglinuxer-v2/$i:latest  dev.younglinuxer.com:18443/younglinuxer-v2/$i:`date +%F`
    docker push dev.younglinuxer.com:18443/younglinuxer-v2/$i:`date +%F`
done 

```


#### 发布应用到测试环境
```python
# 编写python 脚本连接到远程服务器　jenkins 插件不支持目前服务器的ssh方式　
#!/usr/bin/env python
#-*- coding: utf-8 -*-
#ssh 远程执行操作
import paramiko

s = paramiko.SSHClient()

s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# s.connect(hostname='192.168.123.105',port=22,username='root',password='yuan')
s.connect(hostname='172.17.234.25',port=65322,username='root',password='younglinuxer.666test')
stdin, stdout, stderr = s.exec_command("sh /data/bin/update-gateway.sh")

print stdout.read()

print stderr.read()

s.close()

```

##### 根据不同项目判断更新服务
```bash
#!/bin/bash
#程序构建 生成jar包在 /data/jenkins_home/workspace/spring-younglinuxer-auth/｛app｝/target 下面
export MAVEN_HOME=/data/app/maven-3.3.9
export PATH=$PATH:$MAVEN_HOME/bin
HOME=/data/jenkins_home/workspace/talent-chain-cloud-project
DEPLOY=`cat ${HOME}/update-service`
##### 根据需要更新的服务远程执行更新操作 python脚本调用到测试服务器上执行更新脚本
for i in $DEPLOY; do
	if [[ $i == younglinuxer-enterprises ]]; then
		#statement
		python /data/bin/enterprise.py
	elif [[ $i == younglinuxer-framework ]]; then
		#st
        python /data/bin/gateway.py
	elif [[ $i == younglinuxer-commons ]]; then
		#statements
        python /data/bin/commons.py
	else
		python /data/bin/other.py

	fi
done
```
##### 服务器端执行
```bash
#单个项目更新
#!/bin/bash
#只重建一个服务 后台启动 强制重建 不重启相关容器 注意参数　--force-recreate --no-deps
docker-compose -f /data/app/younglinuxer-v2/docker-compose-framework.yml pull
docker-compose -f /data/app/younglinuxer-v2/docker-compose-framework.yml up -d --force-recreate --no-deps ui-manager
# 一组项目更新 全部重建
docker-compose -f /data/app/younglinuxer-v2/docker-compose-commons.yml pull
docker-compose -f /data/app/younglinuxer-v2/docker-compose-commons.yml down
docker-compose -f /data/app/younglinuxer-v2/docker-compose-commons.yml up -d

```
#### kubernetes 发布
`所有服务编写deployment文件 放在/data/app/kubernets 目录下面`

`docker版本号采用与Jenkins构建版本号一致 不采用时间作为版本号`

`应用暂时不适用滚动发布 直接delete后create  不要使用apply(可能会出现应用无法及时更新)` 

##### 服务端
```bash
#!/bin/bash
#更新 kubernets pod 
#获取网关的docker_id
GW_DOCKERID=`docker ps -a|grep dev.younglinuxer.com:18443/younglinuxer-v2/younglinuxer-gateway|awk '{print $1}'`

echo "更新服务　$1"
#$1 接受传入服务名 $2 接受传入docker_tag
sed -i "s#image:.*#image: dev.younglinuxer.com:18443/younglinuxer-v2/$1:$2#g" /data/app/kubernets/$1*.yaml
sleep 3
kubectl delete -f /data/app/kubernets/$1*.yaml
kubectl create -f /data/app/kubernets/$1*.yaml
sleep 5
#echo "重启网关 ing...."
#docker restart $GW_DOCKERID
```
##### JENKINS 服务器
`python远程执行命令 传入参数 服务名 docker_tag`
```bash
```

#### 失败邮件发送
```bash

项目> 构建后操作　> E-mail Notifcation > 填写邮件地址　多个使用　','分开
# 构建失败会发送邮件通知相关负责人

```