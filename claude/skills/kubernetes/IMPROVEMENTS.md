# Skill improvement backlog

Proposals gathered 2026-07-30. Not yet implemented unless marked done.

## 1. Align k3d / ArgoCD ports  — DONE (2026-07-30)

Implemented and validated end-to-end: recreated the k3d cluster with the clean
scheme (dropped redundant `32080:80`), removed cosmetic `nodePort*` from
`service.yaml`, updated `argocd-install` + `k3d.md` + `argocd.md` to log in at
`localhost:9443`. `scripts/argocd-install` now auto-logs-in successfully.


**Problem.** The current port scheme is redundant and has a gap:

- `k3d.md` maps both `9080:80@loadbalancer` and `32080:80@loadbalancer` — two
  host ports pointing at the same loadbalancer port 80.
- `9443:443@loadbalancer` exists, but `assets/argocd/service.yaml` advertises
  HTTPS on `nodePortHttps: 32444`, which k3d never maps.
- `argocd.md` logs in at `localhost:32080`. That reaches serverlb:80 and works
  by coincidence; the `nodePortHttp/Https` fields in `service.yaml` are
  cosmetic — k3d exposes LoadBalancer Services via klipper-lb hostPorts, not via
  those NodePorts.

**Proposed scheme (clean, no redundancy):**

| Host port | Loadbalancer | Purpose        |
|-----------|--------------|----------------|
| 6550      | 6443         | Kubernetes API |
| 9080      | 80           | HTTP ingress / ArgoCD HTTP  |
| 9443      | 443          | HTTPS ingress / ArgoCD HTTPS |

- Drop the redundant `32080:80` mapping.
- ArgoCD CLI logs in at `localhost:9443` (HTTPS, `--insecure`) or
  `localhost:9080` (HTTP).
- `service.yaml` keeps `type: LoadBalancer` on ports 80/443; the explicit
  `nodePort*` values can stay or be dropped (they are not on the traffic path).

**Test plan:** delete the current k3d cluster, recreate with the proposed
scheme, reinstall Crossplane + ArgoCD, confirm ArgoCD CLI login succeeds.

## 2 + 3. Helm chart version-update coverage  — DONE (2026-07-30)

Added `scripts/latest-chart-version <repo/chart> [repo-url]` (via
`helm search repo --versions -o json`), `references/updates/charts.md`, and a
row in the `updates.md` table. Pinned ArgoCD to chart `10.2.1` in
`argocd-install` (was unpinned); Crossplane core stays at `2.3.4`. Reinstall
validated end-to-end (argo-cd-10.2.1 / app v3.4.5, auto-login OK).

## 4. Teardown script  — DONE (2026-07-30)

Added `scripts/cluster-delete` running `k3d cluster delete` (default cluster
`k3s-default`, overridable via `$1`), documented in `references/k3d.md`.

No way to tear the environment down. Add `scripts/cluster-delete`
(`k3d cluster delete`) to close the create→use→destroy loop.

## 5. Prerequisite check  — DONE (2026-07-30)

Added `scripts/check-prereqs`: checks `k3d`/`kubectl`/`helm`/`docker`/`python3`,
prints a ✓/✗ checklist with versions, exits non-zero listing any missing tools.
Referenced from a "check prerequisites" section near the top of `k3d.md`.

`scripts/check-prereqs` (or a note in `k3d.md`) validating `k3d`/`kubectl`/
`helm` are present with minimum versions, to fail fast before a half-install.

## 6 + 7. Install-script robustness  — DONE (2026-07-30)

`crossplane-install` and `argocd-install` gained `set -e` and switched critical
commands from `&> /dev/null` to `> /dev/null` (stderr now surfaces, non-zero
exits abort). `argocd-install` now prepends its own dir to `PATH` and invokes
`argocd-cli-install` directly (was `sh argocd-cli-install`, which ignored the
shebang and cwd). crossplane-install validated live (reinstalled clean).

## 8. Namespaced Managed Resource example  — DONE (2026-07-30)

Added `references/crossplane/examples/resourcegroup-namespaced.yaml` + README.
apiVersion `azure.m.upbound.io/v1beta1` verified against the live CRD (scope
Namespaced) and passes `kubectl apply --dry-run=server`. Fixed during
validation: v2 `providerConfigRef` requires `kind` (added `kind: ProviderConfig`);
documented namespaced ProviderConfig vs cluster-scoped ClusterProviderConfig.

## 9. Route teardown + prereqs in SKILL.md  — DONE (2026-07-30)

Added two rows to the SKILL.md routing table (teardown → k3d.md, prereqs →
k3d.md). updates.md row already present.
