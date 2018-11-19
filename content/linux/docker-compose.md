+++
date = "2018-06-15T10:03:33+08:00"
title = "Docker Compose"
categories = ["linux"]
tags = ["linux"]
toc = true
author = "younglinuxer"
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

##### docker-compose 说明

#### 介绍　

python 编写的docker编排工具　相较于k8s　Swarm 等轻量的多　只需要按照自己的需求编写成对应的docker-compose 文件就行了　
一般按照yaml的语法编写成docker-compose.yaml(对应设置网络模式,端口映射,文件挂载等)就行了,docker-compose 命令行与docker 类似　比如　`docker-compose ps` = `docker ps` 

#### 安装
```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/sbin/docker-compose

chmod a+x /usr/local/sbin/docker-compose

```
#### 常用命令说明
```bash
Usage:
  docker-compose [-f <arg>...] [options] [COMMAND] [ARGS...]

Options:
  -f, --file FILE             Specify an alternate compose file (default: docker-compose.yml)　#指定配置文件　默认docker-compose.yml
  -p, --project-name NAME     Specify an alternate project name (default: directory name) #指定项目名　默认根据文件夹命名　


Commands:
  build              Build or rebuild services　#编译或者重新编译对应的服务　docker镜像是自己编写dockerfile 而不是从镜像仓库拉的时候需要添加这个选项　会根据dockerfile 编译成对应的镜像
  bundle             Generate a Docker bundle from the Compose file
  config             Validate and view the compose file
  create             Create services
  down               Stop and remove containers, networks, images, and volumes　#删除一组服务　并删除对应的网络　镜像　和相关文件服务 (如果需要重新编译相关镜像　则需要使用down 删除所有　不然会使用原有的组件
  events             Receive real time events from containers
  exec               Execute a command in a running container　#运行一条命令到对应容器　同　docker exec -it 'containername' bash
  help               Get help on a command
  kill               Kill containers 
  logs               View output from containers #查看日志　如docker-compose -f xx/docker-compose.yaml logs 
  pause              Pause services　#暂停
  port               Print the public port for a port binding #查看对应的绑定的公用端口　docker-compose -f docker-compose.yml port proxy  443　（proxy 为对应的服务名　docker-compose  ps --services　查看服务名　）
  ps                 List containers　#查看一组服务中所运行哦容器
  pull               Pulls service images
  push               Push service images
  restart            Restart services　#重启
  rm                 Remove stopped containrs　# 删除一组服务的容器　但不会移除相关的网络和文件
  run                Run a one-off command
  scale              Set number of containers for a service
  start              Start services　# 启动一组服务　后台运行
  stop               Stop services　#停止一组服务
  unpause            Unpause services　#恢复暂停
  up                 Create and start container　#创建一组服务并运行　前台
  version            Show the Docker-Compose version information　

```


docker-compose　编排文件示例

编排服务对应的

```yaml
version: "3" # 版本２　版本３　对应docker－compose的版本不一样需要注意 

services:＃对应编排的服务顶格写
  prometheus:
    build:
      context: ./prometheus
    links:
      - "alertmanager:alertmanager"
      - "blackbox_exporter:blackbox_exporter"
    ports:
      - "9090:9090"
    networks:
      - prometheus
      

  blackbox_exporter:
    build: ./blackbox_exporter
    image: blackbox_exporter
    networks:
      - prometheus
  alertmanager:
    build: ./alertmanager
    image: alertmanager
    depends_on:
      - sms_alert
    links:
      - "sms_alert:sms_alert"
    volumes:
      - ./data/alertmanager:/alertmanager
    ports:
      - "9093:9093"
    networks:
      - prometheus
      
  sms_alert:
    build: ./sms_alert/app
    image: sms_alert
    ports:
      - "9092:9092"
    networks:
      - prometheus

  mysqld_exporter_test:
    build: ./mysqld_exporter
    image: mysqld_exporter_test
    environment:
      - DATA_SOURCE_NAME=root:123456@(172.16.30.118:3306)/
    ports:
      - "9104:9104"
    networks:
      - prometheus

  mysqld_exporter_uat:
    build: ./mysqld_exporter
    image: mysqld_exporter_uat
    environment:
      - DATA_SOURCE_NAME=gateway:gatewaypre@(172.16.30.129:3306)/
    networks:
      - prometheus

  consul_exporter_uat:
    build: ./consul_exporter
    image: consul_exporter_uat
    command:
      - "-consul.server=http://172.16.30.129:8500"
    ports:
      - "9107:9107"
    networks:
      - prometheus
      
  consul_exporter_test:
    build: ./consul_exporter
    image: consul_exporter_test
    command:
      - "-consul.server=http://172.16.30.123:8500"
    networks:
      - prometheus
    



volumes:
  prometheus:

networks:
  prometheus:
```

##### 挂载nginx 目录

##### 网络模式

#####