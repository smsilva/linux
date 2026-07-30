# Updating provider versions

Upbound providers are published to the OCI registry `xpkg.upbound.io`, whose
`tags/list` endpoint returns the full tag set (unlike the Crossplane function
proxy). The discovery script filters to strict semver (`vX.Y.Z`) and returns the
highest.

## Discover the latest version

```bash
scripts/latest-provider-version upbound/provider-family-azure
# v2.6.2

scripts/latest-provider-version upbound/provider-family-aws
# v2.6.3
```

Pass a second arg to target a different registry (e.g. a `crossplane-contrib`
provider on `xpkg.upbound.io` is the default; only override when the package
lives elsewhere):

```bash
scripts/latest-provider-version crossplane-contrib/provider-keycloak
```

## Apply

Edit the matching `values-*.yaml` under `assets/crossplane/packages/`:

| Cloud / group   | values file            |
|-----------------|------------------------|
| AWS             | `values-aws.yaml`      |
| Azure           | `values-azure.yaml`    |
| Tooling (helm/k8s/terraform/keycloak) | `values-providers.yaml` |

Pin the **family** provider **and its service providers** to the same exact
tag. A major float (`version: v2`) on a service provider resolves to whatever
revision the registry last tagged `v2`, which is often older than the family
tag you pinned — the service then reports `Healthy=False` with `incompatible
dependencies: ... is incompatible with constraint vX.Y.Z`. Keep the whole
family in lockstep on one tag. Then reinstall one subset per release (Helm
replaces list values, it does not merge):

```bash
helm upgrade --install crossplane-azure assets/crossplane/packages \
  --namespace crossplane-system \
  --values assets/crossplane/packages/values-azure.yaml

kubectl get providers
```

Wait for health before using them:

```bash
kubectl wait providers.pkg.crossplane.io --all \
  --for condition=Healthy --timeout=360s
```
