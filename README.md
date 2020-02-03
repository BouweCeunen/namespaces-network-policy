# Namespaces Network Policy
Applies network policy which blocks incoming traffic from other namespaces when a namespace is created.

Feel free to read about this with some more details on [Medium](https://medium.com/axons/essential-kubernetes-tools-94503209d1cb).

[![DockerHub Badge](https://dockeri.co/image/bouwe/namespaces-network-policy)](https://hub.docker.com/r/bouwe/namespaces-network-policy)

## Installation
Set the excluded namespaces in the configmap. If a configmap is omitted, kube-system is automatically excluded.

```
kubectl apply -f kubernetes/
```

