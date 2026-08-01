# k3d references

## check prerequisites

Before creating a cluster, run `scripts/check-prereqs` to confirm the required
CLI tools (`k3d`, `kubectl`, `helm`, `docker`, `python3`) are installed. It
reports each tool's version and exits non-zero listing any that are missing, so
a half-install fails fast.

```bash
scripts/check-prereqs
```

## cluster create command exposing ports 80 and 443 on the load balancer

Host `9080` → loadbalancer `80` (HTTP), host `9443` → loadbalancer `443`
(HTTPS), host `6550` → API `6443`. LoadBalancer Services (e.g. ArgoCD) are
reached through these host ports via klipper-lb; the `nodePort*` values a chart
may set are not on the traffic path.

```bash
k3d cluster create \
  --api-port 6550 \
  --port "9080:80@loadbalancer" \
  --port "9443:443@loadbalancer" \
  --servers 3 \
  --k3s-arg '--disable=traefik@server:*' \
  --wait \
  --timeout 360s

kubectl wait node \
  --selector kubernetes.io/os=linux \
  --for condition=Ready

kubectl wait deployment metrics-server \
  --namespace kube-system \
  --for condition=Available \
  --timeout=360s; sleep 2

kubectl wait pods \
  --namespace kube-system \
  --selector k8s-app=metrics-server \
  --for condition=Ready \
  --timeout=360s
```

## delete the cluster

Tear the environment down with `scripts/cluster-delete`. It deletes the k3d
cluster (default name `k3s-default`) and lists remaining clusters. Override the
name with an optional argument:

```bash
scripts/cluster-delete            # deletes k3s-default
scripts/cluster-delete my-cluster # deletes a named cluster
```
