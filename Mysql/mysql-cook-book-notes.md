## Mysql CookBook 笔记

- [基本命令](#基本命令)
    - [登录mysql](#登录mysql)
    - [数据库相关命令](#数据库操作)
    - [表相关命令](#表相关命令)
    - [record相关命令](#record相关命令)
    - [授权认证相关命令](#授权认证相关命令)

- [sql查询](#sql查询)
    - [基本的select 语句](#基本的select语句)
    - [order by](#order-by)
    - [distinct](#distinct)
    - [Null](#Null)
    - [view](#view)
    - [join](#join)
    - [subquery](#subquery)
    - [join和subquery](#join和subquery)
        - [inner join](#inner-join)
        - [outer join](#outer-join)
        - [self join](#self-join)

    - [limit](#limit)

- [字符串](#字符串)
    - [字符串存储类型](#字符串存储类型)
    - [charset](#charset)
    - [字符串匹配](#字符串匹配)
    - [字符串变换函数](#字符串变换函数)

- [日期和时间](#日期和时间)


- [统计汇总](#统计汇总)
    - [group by]
    - [having]

### 摘要

本文主要包含了mysql cookbook这本书中介绍的mysql基本知识。msyql用户管理，table的create, update, insert, drop,
sql query select， group by聚合统计，以及inner join, inner join self, outer join(left join, right join)的基本用法。

### 基本命令

##### 登录mysql

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

数据库相关命令
-----
dump, import数据库

```bash
#dump cookbook整个数据库
$mysqldump cookbook > dump.sql

#dump cookbookd的limbs table
$mysqldump coookbook limbs >limbs.sql
$mysql -h other-host other_database <dump.sql

```

create, drop数据库

```bash
#创建数据库
mysql>create database cookbook;

#选用cookbook数据库;
mysql>use cookbook;

#删除数据库
mysql>drop database cookbook;

#显示所有数据库
mysql>show databases;
```

表相关命令
-----

```bash
#创建表limbs
mysql>create table limbs (thing varchar(20), legs int, arms int);

#添加两列name, age
mysql>alter table limbs add (name varchar(20), age int);

#重命名列arms -> newarms;
mysql>alter table limbs change arms newarms int;

#删除legs列
mysql>alter table limbs drop legs;

#删除表limbs
msyql>drop table limbs

#clone一个table
mysql> create table new_limbs like limbs;
mysql> insert into new_limbs select * from limbs;
mysql> insert into new_limbs select * from limbs where thing="human";

#template table, 由mysql负责删除它
mysql> create tamplate table  table_name select * form limbs where thing="human";

#查看table对应的engine
mysql> select engine from information_schema.tables
     > where table_name = "limbs";

mysql>show table status like "limb";

#查看表limbs的scheme
mysql>show create table limbs;

```

record相关命令
-----


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


授权认证相关命令
-----

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


sql查询语句
---

#### 基本的select 语句


```bash
mysql>select * from limbs;
mysql>select thing, legs from limbs;
#where
msyql>select thing, legs, arms from limbs where thing='fish';
msyql>select thing, legs, arms from limbs where thing like 'f%';
msyql>select thing, legs, arms from limbs where thing='fish' and legs=0;
```

给选中的列，用内置函数做变化，重命名。

```bash
mysql> select date_format(t "%M, %e, %Y") as date_sent,
     >        concat(srcuser, "@", srchost) as sender,
     >        size from mail;
```

#### order by

```bash
#默认是升序:ASC
mysql> select * from mail where destuser="tricia"
     > order by scchost, srcuser;

#降序: DESC
mysql> select * from mail where destuser="tricia"
     > order by size desc;

#多列排序
mysql> select * from mail where destuser="tricia"
     > order by size desc, srcuser;
```

#### distinct

```bash
#distinct多列
mysql> select distinct srcuser from mail;

#distinct 单列
mysql> select distinct year(t), month(t), dayofmonth(t) from mail;
```

#### NULL 

NULL, is null, is not null

```bash
mysql> select * from expt where score is null;
mysql> select * from expt where score is not null;
mysql> select subject, test, if(score is null, "unknow", "score") as "score" from expt;
```

#### view
view,一个虚拟的table, 然后可以像正常的table一样在上面select

```bash
mysql> create view mail_view as
     > select
     > date_format(t, "%M %e, %Y") as date_sent,
     > concat(srcuser, "@", srchost) as sender,
     > concat(dstuser, "@", dsthost) as recipient,
     > size from mail;
```

#### join

使用join或者子查询从多个表中select数据

```bash
mysql> select id, name, service, contact_name
     > from profile
     > inner join profile_concat on id = profile_id;
```

#### subquery
subquery（子查询）
```bash
mysql> select * from profile_concat
     > where profile_id = (select id from profile where nmae="Nancy");
```

#### limit
limit: 获取结果中某个range内的数据。

```bash
mysql> select * from profile limit @skip_count, @show_count;
```

字符串
-----

选择字符串存储类型
* char   最大长度255, mysql存储的时候，使用fixed width, 不足的用空格填充。
* varchar 最大长度65535
* tinytext 最大长度255
* text 最大长度65535
* mediumtext 最大长度16777215
* longtext 最大长度4294967295

#### charset

```bash
msyql> show character set;
mysql> set @s=convert("你好世界" using utf8);
mysql> select length(@s), char_length(@s);
mysql> create table mytbl
     > (
     >   utf8str varchar(100) character set utf8 collate utf8_danish_ci,
     >   sjsstr  varchar(100) character set sjis collate sjis_janpanse_ci
```

设置connect时候的charset

```ini
#直接在mysql的配置文件中设置
[mysql]
default-character-set=utf8
```

```bash
#jdbc的设置
jdbc:mysql://localhost/cookbook?characterEncoding=UTF-8

#python的设置
conn_params = {
    "database": "cookbook",
    "host": "localhost",
    "user": "user",
    "charset": "utf8"
}
```

检查当前连接的charset
```bash
mysql> select user(), charset(user()), collation(user());
```

#### 字符串变换函数

```bash
# upser lower
mysql>select thing, upper(thing), lower(thing) from limbs;

# change charset
mysql>select b
     >upper(convert(b using latin1)) as upper,
     >lower(convert(b using latin1)) as lowr,
     >from t;

#left, mid, right
mysql>set @date="2015-07-21";
     >select @date,
     >left(@date, 4) as year,
     >mid(@date, 6, 2) as month
     >right(@date, 2) as day;

#substring_index
mysql>set @email = "postmaster@example.com";
     >select @email,
     >substring_index(@email, '@', 1) as user,
     >substring_index(@email, '@', -1) as host

#concat
mysql>update metal set anme = contact(name, "idle");

#locate, 搜索子串
mysql>select name, locate("in", name), locate("in,  name, 3) from metal
```

#### 字符串匹配

```bash
# like
msyql> select name from metal where name like "%in%";
msyql> select name from metal where name like "__at%";
msyql> select name from metal where name not like "%i%";

#re
#[:alnum:], [:alpha:], [:blank:], [:digit:], [:lower:]
#[:print:], [:space:], [:upper:], [:xdigit:]

mysql> select name from metal where name REGEXP "^me";
mysql> select name from metal where name REGEXP "d$";
mysql> select name from metal where name REGEXP "^..at";
mysql> select name from metal where name REGEXP "^[aeiou]|d$";
mysql> select name from metal where name REGEXP "^[[:digit:]]+|[[:alpha:]]+$";
mysql> select name from metal where name REGEXP "^([[:digit:]]+|[[:alpha:]]+)$";
```

### 时间和日期

date, time, datetime, timestamp, timezone

### 统计汇总

关键词: min, max, count, avg, sum, groupy , having

```bash
mysql>select count(*) from mail;

#groupby
mysql>select srcuser, count(*) from mail group by srcuser;

#groupyby多列
mysql>select srcuser, srchost, count(srcuser)
     >from mail
     >group by srcuser, srchost;

#having: group by with condition.
mysql>select count(*), name from driver_log
     >group by name
     >having count(*) > 3;

#having 嵌套子查询
mysql>select name, avg(miles) as driver_avg from driver_log
     >group by name
     >having driver_avg < (select avg(miles) from driver_log)

#group by expression result
mysql>select monthname(statehood) as month
     >count(*) as count
     >from states group by month having count > 1

mysql>select floor(pop/500000) as `max pop(millions)`
     >count(*) as count
     >from states group by `max pop(millions)`

#get top rank
mysql>select name, sum(miles)
     >from driver_log
     >group by name
     >order by sum(miles) desc limit 1;
```

Join和子查询
----

关键词: inner join, left join, right join, on, using, where.

##### inner join

```bash
mysql> select * from artist
     >inner join painting
     >order by artistd.a_id;

#join with on
mysql>select * from artist
     >inner join painting
     >on artist.a_id = painting.a_id
     >order by artist.a_id;

#join with using
mysql>selet * from artist
     >inner join painting
     >using a_id
     >order by a_id;

#join with where
mysql>selet * from artist
     >inner join painting
     >using a_id
     >order where painting.state = "KY"

#三张表的inner join
mysql>select artist.name, painting.title, states.name
     >from artist inner join painting inner join states
     >on artist.a_id = painting.a_id and painting.state = states.abbrev
     >where painting.state = "KY";

#三张表的join: movie -> move_actor_link -> actor， 多对多的关系。
mysql>select a.actor
     >from movies as m
     >inner join movies_actors_link as l
     >inner join actors as a
     >on m.id = l.movie_id and a.id = l.actor_id
     >where m.move="the fellowship of the ring"
     >order by a.actor

#不同db之间的table的join
mysql>select db1.artist.name, db2.painting.title
     >from db1.artist inner join db2.painting
     >on db1.artist.a_id = db2.painting.a_id
```

##### outer join

使用outer join查找table之间mistach的数据行

查找在painting中没有数据行的artist.

```bash
#使用left join
mysql>select *
     >from artist left join painting
     >on artist.a_id = painting.a_id
     >where paiting.a_id is NULL;
     >order by artist.a_id;

#使用子查询
mysql>select *
     >from aritst
     >where a_id not in (select a_id from painting);
```

##### self join

```bash
#查找和某个title同一个画家的作品。
mysql>select p2.title
     >from painting as p1 inner join painting as p2
     >on p1.a_id = p2.a_id
     >where p1.title = "The potato Easters" and p2.title <> p1.title;

#join中的on可以使用表达式。
mysql> select s2.name, s2.statehood
     > from states as s1 inner join states as s2
     > on year(s1.statehood) = year(s2.statehood) and s1.name <> s2.name
     > where s1.name = "New work"
     > oreder by s2.name;
```

查找每组的极值（最大值或者最小值）

```bash
# 创建一个临时表
mysql> create table tmp
     > select a_id, max(price) as max_price from painting
     > group by a_id;

#然后和它join
mysql> select artist.name, painting.title, paiting.price
     > from  artist inner join painting inner join tmp
     > on painting.a_id = aritist.a_id
     > and painting.a_id = tmp.a_id
     > and painting.price = tmp.max_price;

mysql> select p1.a_id, p1.title, p1.price
     > from painting as p1
     > left join painting as p2
     > on p1.a_id = p2.a_id and p1.price < p2.price
     > where p2.a_id is NULL;
```
