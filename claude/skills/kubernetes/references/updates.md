# Updating package versions

Always check the latest version **before** installing or upgrading a Crossplane
package, then pin it in the matching `values-*.yaml` under
`assets/crossplane/packages/`.

| Resource type            | Guide            | values file(s) to edit                          |
|--------------------------|------------------|-------------------------------------------------|
| Composition functions    | `updates/functions.md` | `values-functions.yaml`                   |
| Providers (AWS/Azure/…)  | `updates/providers.md` | `values-aws.yaml`, `values-azure.yaml`, `values-providers.yaml` |

## General rules

- Each `items[]` entry has a `version` field; set it to the discovered tag.
- An empty `version: ""` resolves to `latest` at install time — avoid it; pin
  an explicit tag so installs are reproducible.
- Discovery scripts live in `scripts/` and print a single tag to stdout, so you
  can splice them straight into an edit (e.g. `scripts/latest-function-version
  function-kcl`).
