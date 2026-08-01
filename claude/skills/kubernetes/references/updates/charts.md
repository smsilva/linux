# Updating Helm chart versions

The cluster components themselves — Crossplane core and ArgoCD — are Helm
charts, not Crossplane packages. Their versions live in the install scripts, not
in a `values-*.yaml`. Pin them the same way: discover, then edit the script.

## Discover the latest version

```bash
scripts/latest-chart-version crossplane-stable/crossplane
# 2.3.4

scripts/latest-chart-version argo/argo-cd
# 10.2.1
```

The script runs `helm repo update` then `helm search repo <chart> --versions`.
helm excludes pre-releases by default, so the first result is the latest stable
chart version. Pass the repo URL as a second arg to add it first if it is not
registered yet:

```bash
scripts/latest-chart-version argo/argo-cd https://argoproj.github.io/argo-helm
```

## Apply

| Chart              | Pinned in                | How                                   |
|--------------------|--------------------------|---------------------------------------|
| Crossplane core    | `scripts/crossplane-install` | edit the `--version` flag on `helm install` |
| ArgoCD             | `scripts/argocd-install` | edit the `--version` flag on `helm upgrade --install` |

After editing, rerun the matching install script to upgrade in place.

Note: the chart version and the app version can differ (e.g. argo-cd chart
`10.2.1` ships ArgoCD app `v3.4.5`). `latest-chart-version` prints the **chart**
version, which is what the `--version` flag expects.
