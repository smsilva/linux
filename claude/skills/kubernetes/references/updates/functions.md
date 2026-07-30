# Updating composition function versions

Functions are published by the `crossplane-contrib` org. The **GitHub releases
API** is the authoritative source for their latest version.

## Discover the latest version

```bash
scripts/latest-function-version function-kcl
# v0.12.2
```

The script queries `https://api.github.com/repos/crossplane-contrib/<name>/releases/latest`
and prints its `tag_name`.

## Apply

Edit the matching entry in `assets/crossplane/packages/values-functions.yaml`,
setting `version` to the discovered tag, then reinstall:

```bash
helm upgrade --install crossplane-functions assets/crossplane/packages \
  --namespace crossplane-system \
  --values assets/crossplane/packages/values-functions.yaml

kubectl get functions
```

## Why not the OCI registry

`xpkg.crossplane.io` is a proxy in front of `ghcr.io`. Its `/v2/.../tags/list`
endpoint is paginated at 100 tags and ordered by **push time**, not semver, and
the pages are dominated by `v0.0.0-<timestamp>` pseudo-versions — so the newest
release routinely falls off the first page. Listing tags there reports a stale
version. Use the GitHub releases API instead.
