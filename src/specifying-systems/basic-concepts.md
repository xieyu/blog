## 基本概念整理

英文部分为《Specifying Systems》这本书的摘抄，中文部分为个人理解。

## Chapter1: Get Started

感觉是高中的数学知识, 数理逻辑和集合论

#### Specification

A Specification is a written description of what a system is supposed to do.

使用数学语言（集合论，数理逻辑，时序逻辑）来精确的描述系统。

#### properties

properties: true for every possible execution
* safety: a safety property asserts that nothing bad happens
* livenes: a livenes property asserts something good eventually happens[1]
* real-time properties:  ??

livenes property 可以用Temporal logic来描述

TODO: 添加一些例子
properties说明的是系统的本身属性？

#### Propositional Logic (命题逻辑)

* `/\`: and, F `/\` G equals TRUE iff both F and G equal TRUE
* `\/`:  or,  F `\/` G equals TRUE iff F or G equal TRUE
* `\not`: not, `\not` F equals TRUE iff F equals FALSE
* `=>`: F `=>` G, F的条件比Ｇ更强
* `<->`: 等价？

#### Sets

* 交，并，子集，差集

#### Predict Logic (谓词逻辑)

* 任意量词 universal quantification (for all) 
* 存在量词 existenial quantification(there exist)


## Chapter 2: Specifying a Simple Clock

#### Behaviors

* Behavior: A Sequence of states, 一个状态序列
* State: an assignment of values to variables
* variables: 这个表示什么？对系统某个特征的抽象?
* Temporal formula: assertion about behavior
* Theorem: 满足所有behavior的Temporla formula, 反应着系统中不变的特征？表示系统的本质特征？
* `hr'`: the next state of hr, the ' in hr' is red prime
* `[]`, temporal logic operator, []F asserts that formual F is always true.
* sutering steps: hr' = hr 停留的状态


#### Hour Spec in TLA+

Hour Clock定义如下
MODULE有点类似于变成语言中package模块的概念.

```
---------------------- MODULE HourClock ------------
EXTENDS Naturals
VARIABLE hr

HCini == hr \in (1 .. 12)

HCnext == hr' = IF hr # 12 THEN hr + 1 ELSE 1

HC == HCini /\ [][HCnext]_hr
----------------------------------------------------
THEOREM HC => []HCini
====================================================
```

1. Spec开头声明Module, MODULE 名HourClock要和文件名HourClocl.tla一致
2. Spec结尾以一行===结束
3. EXTENDS　Naturals 表示引用Naturals中的defenitions和operator.(和普通语言的import包类似)
4. == 表示定义
5. hr'表示hr的下一个状态

