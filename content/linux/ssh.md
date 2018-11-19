+++
date = "2018-08-04T23:16:49+08:00"
title = "Ssh"
categories = ["linux"]
tags = ["linux"]
toc = true
author = "younglinuxer"
comments = true
author_homepage =  "https://younglinuxer.github.io/hugo/"

+++

#### ssh 配置
```bash

#监听选项
Port 65322 #监听端口
#ListenAddress 0.0.0.0 #绑定监听地址
#ListenAddress ::

#数字签名(私钥) 保存的位置 rsa dsa ecdsa 为签名的算法  默认为rsa
HostKey /etc/ssh/ssh_host_rsa_key 
#HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

#密码和key 选项
# Ciphers and keying
#RekeyLimit default none

#日志选项
# Logging
#LogLevel INFO #日志级别选项

#认证选项
# Authentication:
#LoginGraceTime 2m  #限定用户认证时间为2分钟 如果用户登录时间超过2M就不允许访问
#StrictModes yes  #设置ssh在接收登录请求之前是否检查用户根目录和rhosts文件的权限和所有权 
#MaxAuthTries 6  #登陆错误6次后 将拒绝登陆
#MaxSessions 10  #最大允许多少个连接 TTY
#PubkeyAuthentication yes  是否开启公钥认证


# The default is to check both .ssh/authorized_keys and .ssh/authorized_keys2
# but this is overridden so installations will only check .ssh/authorized_keys
#用户认证key 文件保存的位置
AuthorizedKeysFile	.ssh/authorized_keys

#AuthorizedPrincipalsFile none

#AuthorizedKeysCommand none
#AuthorizedKeysCommandUser nobody

# For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
#HostbasedAuthentication no
# Change to yes if you don't trust ~/.ssh/known_hosts for
# HostbasedAuthentication
#IgnoreUserKnownHosts no
# Don't read the user's ~/.rhosts and ~/.shosts files
#IgnoreRhosts yes

# To disable tunneled clear text passwords, change to no here!
#PermitEmptyPasswords no #允许空密码登录

# Change to no to disable s/key passwords
#ChallengeResponseAuthentication yes
ChallengeResponseAuthentication no #是否自动接收认证 ssh连接要输入 yes的那个东西

# Kerberos options
#KerberosAuthentication no
#KerberosOrLocalPasswd yes
#KerberosTicketCleanup yes
#KerberosGetAFSToken no
#KerberosUseKuserok yes

# GSSAPI options #应用程序接口选项
GSSAPIAuthentication yes
GSSAPICleanupCredentials no
#GSSAPIStrictAcceptorCheck yes
#GSSAPIKeyExchange no
#GSSAPIEnablek5users no

# Set this to 'yes' to enable PAM authentication, account processing,
# and session processing. If this is enabled, PAM authentication will
# be allowed through the ChallengeResponseAuthentication and
# PAM authentication via ChallengeResponseAuthentication may bypass
# If you just want the PAM account and session checks to run without
# and ChallengeResponseAuthentication to 'no'.
# WARNING: 'UsePAM no' is not supported in Red Hat Enterprise Linux and may cause several
# problems.
UsePAM yes #允许key登录

#AllowAgentForwarding yes
#AllowTcpForwarding yes
#GatewayPorts no
X11Forwarding yes #交互式处理 可以使用xshell 远程相关图形界面
#X11DisplayOffset 10
#X11UseLocalhost yes
#PermitTTY yes
#PrintMotd yes
#PrintLastLog yes
#TCPKeepAlive yes
#UseLogin no
#UsePrivilegeSeparation sandbox
#PermitUserEnvironment no
#Compression delayed
#ClientAliveInterval 0
#ClientAliveCountMax 3
#ShowPatchLevel no
#PidFile /var/run/sshd.pid
#MaxStartups 10:30:100
#PermitTunnel no
#ChrootDirectory none
#VersionAddendum none

# no default banner path
#Banner none

# Accept locale-related environment variables
AcceptEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES
AcceptEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
AcceptEnv LC_IDENTIFICATION LC_ALL LANGUAGE
AcceptEnv XMODIFIERS

# override default of no subsystems
Subsystem	sftp	/usr/libexec/openssh/sftp-server

# Example of overriding settings on a per-user basis
#Match User anoncvs
#	X11Forwarding no
#	AllowTcpForwarding no
#	PermitTTY no
#	ForceCommand cvs server
UseDNS no #是否反向验证dns 一般设为no  yes回去查找一遍 影响连接速度
AddressFamily inet #"any"(默认)、"inet"(仅IPv4)、"inet6"(仅IPv6)
PermitRootLogin yes #是否允许root登录
SyslogFacility AUTHPRIV #日志记录
PasswordAuthentication yes #是否允许密码认证 可以用key登录

```

##### 常用配置更改
```bash
Port 65322 #端口更改
UseDNS no #禁用dns反向验证
AddressFamily inet #只允许ipv4登录
PermitRootLogin no #不允许root登录
SyslogFacility AUTHPRIV
PasswordAuthentication no #不允许密码登录

```
##### 使用key登录
```bash
1.生成公钥(使用xshell工具生成  或者使用命令 ssh-keygen(  -t rsa -b 2048 参数自己选填))
2.新建用户
useradd -g wheel ops #指定用户组 wheel 该用户组有sudo 权限 (详见 /etc/sudoers)
3.配置用户的key
mkdir /home/ops/.ssh
vim  /home/ops/.ssh/authorized_keys #这里填写你自己的公钥内容
4.登录验证 
xshell 登录用户ops 公钥选择你生成的公钥
ssh   ssh -i younglinuxer -p65322 ops@{node_ip} #注意younglinuxer 为秘钥文件 权限为600 (chmod 600 younglinuxer)
```
##### 使用外部认证ldap
##### 免密登录
```bash
ssh-keygen -t rsa -b 2048 回车 回车 回车
ssh-copy-id $IP #$IP为你需要远程登录地址，按照提示输入yes 和root密码
```
##### ssh 升级
```bash
#centos6 默认ssh版本比较低 一般处于漏洞考虑会升级ssh
#自己编译会容易比较出错 记得先开启telnet 或者自己预留能连接上的工具  这里提供一个不错的git    https://gist.github.com/add912b9b4c3899ec26c488a91446a84.git
#代码如下：

#!/bin/bash
# Copyright © 2016 Faishal Saiyed
cd
timestamp=$(date +%s)
if [ ! -f openssh-7.3.zip ]; then wget https://github.com/faishal/openssh-portable/releases/download/cent.os.6.7.openssh.7.3p1/openssh-7.3.zip; fi;
unzip -o openssh-7.3.zip -d openssh-7.3p1
cd openssh-7.3p1/
cp /etc/pam.d/sshd pam-ssh-conf-$timestamp
rpm -U *.rpm
yes | cp pam-ssh-conf-$timestamp /etc/pam.d/sshd
/etc/init.d/sshd restart

```