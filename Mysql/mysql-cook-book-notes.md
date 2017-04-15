## Mysql CookBook 笔记

### 基本命令

登录mysql

```bash
$mysql -h localhost -u user -p
```

执行文件中的sql语句
```bash
# 使用数据库cookbook,执行limbs中的sql语句。
$mysql cookbook <limibs.sql

#登陆后，source limbs中的sql语句。
mysql>source limbs.sql
```

dump和导入数据库

```bash
$mysqldump cookbook > dump.sql
$mysql -h other-host cookbook<dump.sql
```

创建，删除database
```bash
mysql>create database cookbook; //创建数据库
mysql>use cookbook; //选用cookbook数据库;
mysql>drop database cookbook; //删除数据库
mysql>show databases;//显示所有数据库
```

创建，修改，删除table
```bash
#创建表limbs
mysql>create table limbs (thing varchar(20), legs int, arms int);

#查看表limbs的scheme
mysql>show create table limbs;

#添加两列name, age
mysql>alter table limbs add (name varchar(20), age int);

#重命名列arms -> newarms;
mysql>alter table limbs change arms newarms int;

#删除legs列
mysql>alter table limbs drop legs;

#删除表limbs
msyql>drop table limbs
```

在table中 insert, update, delete数据行

```bash
# 创建表
mysql>drop table if exists limbs;
mysql>create table limbs(thing varchar(20), legs  int, arms int);

# 插入数据
mysql>insert into limbs (thing, legs, arms) values("human", 2, 2);
mysql>insert into limbs (thing, legs, arms) values("fish", 0, 1);

#更新数据
mysql>update limbs set arms=0 legs=0 where thing='fish';

#从limbs表中删除一行
mysql>delete from limbs where thing='fish' limit 1;
```


创建，删除，授权，取消授权，查看所有创建的用户, 修改密码
```bash
#创建用户
mysql>create user 'cbuser'@'localhost' identified by 'cbpass';

#创建用户
mysql>insert into mysql.user(Host, User, Password) values("localhost", "cbuser", password("cbpass"));

#删除用户
mysql>delete from user where User="cbuser" and Host="localhost"

#修改用户密码k
mysql>update mysql.user set password=password("newpassword") where User="cbuser" and Host="localhost";

#授权, 将cookbook数据库所有表的所有权利grant给'cbuser'
mysql>grant all on cookbook.* to 'cbuser'@'localhost';

#授权，一部分权: select, update
mysql>grant select,update on cookbook.* to 'cbuser'@'localhost';

#取消授权
mysql>revoke udpate on cookbook.* from 'cbuser'@'localhost';

#查看所有的用户
mysql>select * from mysql.user;
```
