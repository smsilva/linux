# Crossplane v2 examples

Minimal examples of *using* an installed provider. The skill installs providers
and functions but otherwise shows no consuming manifest — these fill that gap.

## `resourcegroup-namespaced.yaml`

A namespaced Azure `ResourceGroup` Managed Resource (MR). This is the payoff of
the Crossplane v2 model: Managed Resources can live inside a namespace instead
of being cluster-scoped.

### Cluster-scoped vs namespaced groups

The Upbound family v2 providers expose every Managed Resource in **two** API
groups:

| Group | Scope | apiVersion example |
|-------|-------|--------------------|
| `azure.upbound.io` | cluster-scoped (legacy v1 shape) | `azure.upbound.io/v1beta1` |
| `azure.m.upbound.io` | namespaced (v2 model) | `azure.m.upbound.io/v1beta1` |

The `.m.` infix marks the namespaced variant. Namespaced MRs set
`metadata.namespace`; cluster-scoped ones omit it. This example uses the
namespaced group, which is the value proposition of Crossplane v2.

The owning provider is `upbound-provider-azure-management`, installed by
`assets/crossplane/packages/values-azure.yaml`.

### Confirm the apiVersion

`azure.m.upbound.io/v1beta1` is verified against the installed CRD
(`resourcegroups.azure.m.upbound.io`, scope `Namespaced`, served+storage
`v1beta1`) and passes a server-side dry-run. Re-confirm on your own cluster:

```bash
kubectl get crds | grep resourcegroup
kubectl explain resourcegroup --api-version=azure.m.upbound.io/v1beta1
kubectl apply --dry-run=server -f references/crossplane/examples/resourcegroup-namespaced.yaml
```

### Apply

```bash
kubectl apply -f references/crossplane/examples/resourcegroup-namespaced.yaml
```

### Inspect

```bash
kubectl get resourcegroup -n default
kubectl describe resourcegroup example-rg -n default
```

### Scope / caveat

This demonstrates the namespaced **shape** only. Provisioning a real Azure
ResourceGroup additionally requires Azure credentials (a `Secret`) and a
ProviderConfig that the MR references via `spec.providerConfigRef`. That setup
is out of scope here — without it the MR stays unready, but the manifest is
still valid and shows the namespaced form.

`spec.providerConfigRef` requires **both** `kind` and `name` in v2. A namespaced
MR can point at a namespaced `ProviderConfig` (group `azure.m.upbound.io`, lives
in the same namespace) or a cluster-scoped `ClusterProviderConfig` (shared
across namespaces). The example uses `kind: ProviderConfig`.
