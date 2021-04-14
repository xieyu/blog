# Conf Change

## PD 触发conf change

![](./dot/tikv_conf_change.svg)

### PeerFsmDelegate::propose_conf_change

向raft propose conf change

![](./dot/tikv_propose_conf_change.svg)

### ApplyDelegate::exec_change_peer

![](./dot/exec_change_peer.svg)

### PeerFsmDelegate::on_ready_change_peer

添加节点

![](./dot/on_ready_change_peer.svg)
