# Crossplane references

## install Crossplane via Helm

Run the install script. It adds and updates the `crossplane-stable` Helm repo,
installs the `crossplane-stable/crossplane` chart into the `crossplane-system` namespace, waits for the deployment to become
`Available`, and lists the resulting pods.

```bash
scripts/crossplane-install
```

## verify the installation

```bash
kubectl get pods --namespace crossplane-system
```

## install packages

Crossplane providers and functions are packaged as a local Helm chart at
`assets/crossplane/packages`. Which items get installed and at which versions is
driven entirely by `values.yaml`.

Each entry under `items` renders one `Function` or `Provider`:

| Field | Meaning |
|-------|---------|
| `name` | `metadata.name` of the package resource |
| `kind` | `Function` or `Provider` (sets the correct `apiVersion`) |
| `package` | OCI image reference, without the tag |
| `version` | image tag; if empty, `latest` is used |
| `enabled` | set to `false` to skip the item (default `true`) |

Before installing, check for newer package versions and pin them — see
`updates.md`.

The default `values.yaml` installs nothing (`items: []`). Bundled subset files
pick a curated group:

| Values file | Installs |
|-------------|----------|
| `values-aws.yaml` | AWS family provider + service providers |
| `values-azure.yaml` | Azure family provider + service providers |
| `values-functions.yaml` | composition functions |
| `values-providers.yaml` | helm/kubernetes/terraform/keycloak providers |

Helm replaces (does not merge) list values across `--values` flags, so install
one subset per release. Preview the rendered manifests:

```bash
helm template crossplane-aws assets/crossplane/packages \
  --values assets/crossplane/packages/values-aws.yaml
```

Install (or upgrade) a subset into the cluster:

```bash
helm upgrade --install crossplane-aws assets/crossplane/packages \
  --namespace crossplane-system \
  --values assets/crossplane/packages/values-aws.yaml
```

For a custom selection, copy a subset file and toggle `enabled`, edit the
`items` list, or pin versions with the `version` field.

Check that the packages become healthy:

```bash
kubectl get providers,functions
```

## use an installed provider

For a minimal example of consuming a provider — a namespaced Azure
`ResourceGroup` Managed Resource — see `crossplane/examples/`.
