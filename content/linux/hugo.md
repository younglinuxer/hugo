---
title: "Hugo"
date: 2018-06-08T22:31:38+08:00
draft: true
categories: ["linux"]
tags: ["linux"]
toc: true
---

##### hugo 博客搭建说明

##### 准备工作
```
1.配置hugo 运行环境　
2.github 新建一个Repositories　配置github pages （提供一个域名　并托管blog代码）
3.注册 disqus （增加评论系统）　//需要翻墙
4.注册七牛云　　(免费云存储　cdn加速)
5.网易云音乐生成播放器外链　(增加一个音乐播放器)
6.选择一个自己觉得好看的皮肤
```
[hugo 下载地址](https://github.com/gohugoio/hugo/releases)
[disqus评论系统注册](https://disqus.com/profile/signup/)
[七牛云注册](https://www.qiniu.com/)
[hugo 模板](https://themes.gohugo.io/)
[网易云音乐生成外链教程](https://jingyan.baidu.com/article/d7130635dcdf6813fdf475c7.html)

[hugo安装官方文档](http://www.gohugo.org/)


##### 安装　hugo
```
1.点击上述链接下载最新版本的安装包
2.解压得到一个执行文件'hugo' 
3.将hugo移动到对应 path 路径下面　linux(/usr/local/sbin) win(c:/windows/system32)
```
//常用命令

***注意　hugo新建页面生成文件用md　编辑采用markdown语法　hugo会读取md文件生成对应的html文件 执行hugo命令时需要在生成站点的目录下执行***
```
# 生成站点
hugo new site /data/app/hugo
# 创建一个abut页面
hugo new about.md
# 创建一个目录和页面　
hugo new linux/linuxMint.md

#本地运行hugo 进行调试
hugo server --theme={yourtheme} --buildDrafts
// 简写　hugo server -t {younrteme} -D 
// 更多参数　参考　hugo --help



# 安装皮肤
# 创建　themes 目录
mkdir /data/app/hugo/themes
cd data/app/hugo/themes 
git clone https://github.com/coderzh/hugo-pacman-theme.git

# 替换配置文件　如果启动有问题　就执行下面命令
cp -r themes/｛youthemes｝/exampleSite/ 　．
#如果报错找不到对应皮肤　请检查themes下面对应的目录名字是否正确
```
//目录说明
![avatar](http://p9ym53fcj.sabkt.gdipper.com/hugo_tree)

##### 部署自己的blog 
[github pages 可以参考这篇文章](https://www.jianshu.com/p/e68fba58f75c)

```
#　生成public目录（blog的静态页面） 指定皮肤和url (默认localhost)
hugo --theme=hugo-pacman-theme --baseUrl="https://younglinuxer.github.io/hugo/" 
# 提交到　github
$ cd public
$ git init
$ git remote add origin https://github.com/｛your Repositories｝
$ git add -A
$ git commit -m "first commit"
$ git push -u origin master

访问你github pages 主页就可以得到你的blog 了 

```

##### 增加评论系统＆＆网易云音乐链接

/注册　disqus　成功后选择　i want to install disqus on my site 

按提示操作注册后会生成你注册帐号对应的代码块　

```html
<div id="disqus_thread"></div>
<script>

/**
*  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
*  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
/*
var disqus_config = function () {
this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
};
*/
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');
s.src = 'https://https-younglinuxer-github-io-hugo.disqus.com/embed.js'; //这里对应你帐号生成的js 
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
                            
```

找到安装皮肤中对应disqus 代码　
/layout/partials/comment.html

`这里使用模板映射配置文件到对应的代码　但是配置文件没有这个选项　添加尝试了一下仍然不行　这里直接把disqus给出来的代码替换掉就行了`

```html
{{ if .Site.Params.DisqusShortName }}
<section class="comment">
<div id="disqus_thread"></div>
</section>
<script>
/**
* RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
* LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables
*/
var disqus_config = function () {
this.page.url = {{ .Permalink }};
this.page.identifier = {{ .Permalink }};
};
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');

s.src = '//{{ .Site.Params.DisqusShortName }}.disqus.com/embed.js';

s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>
{{ end }}

```