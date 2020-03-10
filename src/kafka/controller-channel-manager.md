# Kafka Controller: channelManager


Controller和Broker之间采用队列来做异步通信,有专门的线程负责网络数据收发。

每次broker上线，Conntroller会新建一个RequestSendThread线程，当broker下线时候，会销毁该线程。

Controller和每个broker之间都有个RequestSendThread, Controller 将请求放到broker对应的请求队列中。
在RequestSendThread发送完请求，收到broker的响应之后，通过预先设置好的`sendEvent`回调，通过eventManager 采用异步的方式通知controller。



![channel-manager](./channel-manager.svg)

