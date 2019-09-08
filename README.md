# namespaces-network-policy
Applies network policy which blocks incoming traffic from other namespaces when a namespace is created.

[![DockerHub Badge](https://dockeri.co/image/bouwe/namespaces-network-policy)](https://hub.docker.com/r/bouwe/namespaces-network-policy)

## Installation
Set the excluded namespaces in the configmap. If a configmap is omitted, kube-system is automatically excluded.

```
kubectl apply -f kubernetes/
```

