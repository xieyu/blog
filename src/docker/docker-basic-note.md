## Docker 学习笔记1: 基本使用方法

### 序

之前做python web开发，为了避免不同项目之间python package的冲突，一般都采用virutal env的方式来解决，虽然可以通过脚本方式来解决开发环境共享，部署之类的问题，但终究还是有些麻烦，最近服务端后台开发中用到了docker, 发现它真是神器。几个月使用下来，愈发觉得docker是个好工具，我觉得的docker有以下几个好处:

- 可以通过DockerFile build出容器运行环境镜像，而且DockerFile可以放到git repo中版本管理
- 开发，测试，生产环境的一致性，team内组员之间可以快速的搭建开发环境。
- 方便服务端的集成自动化测试。
- 不影响host, 彻底干净的环境, 想装啥装啥，跟glibc以及各种乱七八糟的包依赖冲突说拜拜。
- 一键运行，直接把容器启动起来服务就起来了。

这里先推荐两本看着不错的书《第一本docker书》这本书偏向于docker的基本使用，另外一本是《docker容器与容器云》这本偏向于docker背后的实现原理，讲述的范围比较广，是深入研究docker一本好书。


### 基本概念

刚接触docker的时候，很容易把docker的容器和虚拟机混淆起来。觉得docker中容器就是一个虚拟机，第一个想法是我该怎么ssh到这个虚拟机上去? (可以通过docker exec -it container_name /bin/bash 到container里面), 然而事实上docker中的容器(container)就是一组进程，它们运行在一个沙盒之中，docker基于linux的namespace和cgroup以及aufs搭建了这沙盒，因此就无所谓的ssh到某个docker容器内之说了。

docker中有三个基本的概念，image, container, repo。image是静态的一堆文件(包含/rootfs以及各种container相关的配置）之类的，container是跑起来的进程，repo是存放image的远程仓库, 他们之前的关系如下图：

<p align="center">
<img src="./images/docker-concept-relations.png" align="center" width="400px"/>
</p>

docker中基本的命令分类:

- 环境信息: docker info, docker version
- 镜像仓库命令：login, logout, pull, push, search
- 镜像管理：build, image, import, load, save, tag, commit
- 容器管理: attach, export, inspect, port, ps, stats, top, wait, cp, diff, update
- 容器生命周期管理：create, start, stop, restart, exec, kill
- 资源管理: volume, network
- 系统日志: events, history, logs

#### 常用命令例子和说明

##### image

* 以当前目录为context, 使用当前目录中的DockerFile文件，创建image 名为 "python-flask"的镜像

~~~~shell
docker build -t "python-fask" .
~~~~


* 以abc目录为context, 使用abc目录下的DockerFile文件，创建image 名为 "python-flask"的镜像

~~~~shell
docker build -t "python-fask" abc
~~~~

##### container

* 使用python-flask镜像，创建一个名为'my-web-app'的容器（容器的名字很重要，后面各种操作都会使用到容器名, 如果没有名字的话,docker会自动随机生成一个名字）

~~~~shell
docker run -it -d "my-web-app"  "python-flask" -v host-dir:container-dir -p host-port:container-port /bin/bash
~~~~

* 停止运行容器my-web-app

~~~~shell
docker stop my-web-app
~~~~

* 启动容器my-web-app

~~~~shell
docker start my-web-app
~~~~

* 重启容器my-web-app

~~~~shell
docker restart my-web-app
~~~~

* 删除容器my-web-app

~~~~shell
docker rm my-web-app
~~~~

* 强制删除容器my-web-app，即使容器在运行状态

~~~~shell
docker rm -f my-web-app
~~~~

* 查看容器my-web-app的输出

~~~~shell
docker logs my-web-app
~~~~

* 查看容器my-web-app中进程

~~~~shell
docker top my-web-app
~~~~

* 在容器my-web-app的环境中，执行/bin/bash命令

~~~shell
docker exec -it container-name /bin/bash
~~~

### Dockerfile

DockerFile相当于image的蓝图或者模板，docker会根据DockerFile中的指令去build出docker镜像, 最基本的指令有FROM, ADD, RUN, ENV, CMD, VOLUME, ENTRYPOINT

一个简单dockerfile例子

~~~shell
FROM centos:7
RUN yum update -y; yum clean all
VOLUME /web
CMD ["/start.sh"]
~~~



### compose


### network


### 常见问题以及解决方法

1. 时区问题
