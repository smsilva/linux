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
ArgoCD server as a `LoadBalancer` on node ports `32080` (HTTP) and `32444`
(HTTPS):

```yaml
server:
  service:
    type: LoadBalancer
    nodePortHttp: 32080
    nodePortHttps: 32444
    servicePortHttp: 80
    servicePortHttps: 443
    servicePortHttpName: http
    servicePortHttpsName: https
    namedTargetPort: true
```

This pairs with the k3d cluster that maps `32080:80@loadbalancer` (see
`k3d.md`), so the CLI logs in at `localhost:32080`.

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
argocd login localhost:32080 \
  --username admin \
  --password "${argocd_password}" \
  --insecure
```
