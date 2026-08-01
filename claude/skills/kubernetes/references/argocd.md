# ArgoCD references

## install the ArgoCD CLI

Run the CLI install script. It fetches the latest release tag from GitHub and
installs the `argocd` binary to `/usr/local/bin`:

```bash
scripts/argocd-cli-install
```

The Helm install script (`scripts/argocd-install`) also runs this automatically
if the CLI is missing.

## install ArgoCD via Helm and login with the CLI

Run the install script. It installs the `argo/argo-cd` Helm chart into the
`argocd` namespace using the values in `assets/argocd/service.yaml`, waits for
the deployments, installs the ArgoCD CLI if missing, and logs in.

```bash
scripts/argocd-install
```

## values applied to the Helm chart

The chart is installed with `assets/argocd/service.yaml`, which exposes the
ArgoCD server as a `LoadBalancer` on ports 80 and 443:

```yaml
server:
  service:
    type: LoadBalancer
    servicePortHttp: 80
    servicePortHttps: 443
    servicePortHttpName: http
    servicePortHttpsName: https
    namedTargetPort: true
```

This pairs with the k3d cluster that maps `9443:443@loadbalancer` (see
`k3d.md`), so the CLI logs in at `localhost:9443` over HTTPS. k3d routes the
LoadBalancer Service through that host port via klipper-lb, so the randomly
assigned NodePorts are irrelevant.

## retrieve the initial admin password

```bash
kubectl \
  --namespace argocd \
  get secret argocd-initial-admin-secret \
  --output jsonpath="{.data.password}" \
| base64 --decode
```

## login with the ArgoCD CLI

```bash
argocd login localhost:9443 \
  --username admin \
  --password "${argocd_password}" \
  --insecure
```
