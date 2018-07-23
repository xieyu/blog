## 统计gpu,cpu利用率脚本


```bash
#!/bin/bash
start=$(date +%s)
while [ 1 ]
do
    cpu=$(awk -v a="$(awk '/cpu /{print $2+$4,$2+$4+$5}' /proc/stat; sleep 1)" '/cpu /{split(a,b," "); print 100*($2+$4-b[1])/($2+$4+$5-b[2])}'  /proc/stat)
    seconds=$(expr $(date +%s) - $start)
    gpu_util=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits)
    echo "$seconds, $cpu, $gpu_util"
    #sleep 1
done

```
