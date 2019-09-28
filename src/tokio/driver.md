# tokio driver

driver负责将底层的io事件传递给相应的等待任务，事件驱动主要依赖于``mio::poll``, driver另外一个作用
是建立task和事件之间的以来关系。

每个mio event都有个token, driver根据该token建立到SchduleIo的映射，然后在task.poll的时候，会使用schedulIo中预先定义好的wake方法。

## task <-> mio event

task和mio event通过token 建立关系，两者通过Context关联起来

![task-token-event](./task-token-event.svg)

![task-event-detail](./task-event-detail.svg)
