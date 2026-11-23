# nereus-registry-cleanup

Runs Nereus's `scripts/registry/cleanup --apply` every day at 04:30 (getnereus/nereus#2151). It removes every tag of the local k3d registry (`localhost:5111`) and every local docker image of Nereus that is not the latest release, not in use (by a docker container or a Pod of any k3d cluster) and older than 24 hours, then runs the registry's garbage collection. The scenes' builds filled the registry with 12.6 GB in a few days; the first run left 4.0 GB.

The collection is skipped while a scene's cluster exists (a scene may be pushing); the tags are still removed, and the next day's run frees their blobs. Before the run, the service fetches the tags of Nereus's main clone, since the latest release is its highest tag `v*`.

## Commands

```bash
systemctl --user list-timers nereus-registry-cleanup.timer
systemctl --user start nereus-registry-cleanup.service    # run now
journalctl --user --unit nereus-registry-cleanup.service  # the last runs
~/git/getnereus/nereus/scripts/registry/cleanup           # the plan, without removing anything
```

## Install

```bash
. scripts/utilities/nereus-registry-cleanup/install.sh
```
