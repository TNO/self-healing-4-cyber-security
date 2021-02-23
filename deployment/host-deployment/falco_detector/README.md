### Falco 

Here lives the falco (sort-of) we actually pull the latest docker image then remount our config which is the `/falco` directory.

> kubectl apply -f falco-pod.yaml

There is two ways to launch but note that the docker run script does not support `kubectl logs containerid`

Falco uses eBPF and occasional syscall drops are "Normal"
 
`falco_etc_export.tar.gz' is a rules directory backup incase you break it
