# Ray

## 相关资料整理

* [官方doc](https://docs.ray.io/en/latest/index.html)
* [github](https://github.com/ray-project/ray)
* [ray paper](https://arxiv.org/abs/1712.05889)

## 主要组件

* Gcs: Global Control State, 存储了代码，输入参数，返回值
* Raylet:Local Scheduler, Worker通过Raylet和Gcs通信。
* Redis
