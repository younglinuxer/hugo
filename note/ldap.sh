#!/bin/bash

#安装ldap 配置　ocserver　vpn　认证
#安装ldap 服务
yum install openldap*
#安装　ocserv vpn
yum install ocserv

#花生壳动态域名解析　vpn 穿透
openconnect  21b160b468.51mypc.cn:56988

