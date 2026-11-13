# disk-watch

Keeps the root disk at a healthy level and says so before it fills. In November 2026 the disk reached 94%: k3s marked DiskPressure, evicted pods and failed the scenes. The causes were a GNOME tracker in an error loop that wrote 55 GB of `syslog` in a few days, Docker images and build cache left by the scene builds, and Terraform providers copied into twenty `.terraform` folders. Every cleanup was manual, and nothing capped the logs or warned before the disk was full.

## What it does

| Piece | When | What |
|---|---|---|
| `disk-watch check` | every 15 minutes (`disk-watch-check.timer`) | measures `/`; at 80% (warning) or 90% (critical) writes the alert file, sends a desktop notification and names the five directories that grew most since the previous snapshot; below 80% removes the alert |
| status line | every prompt | `claude-status-line` shows ` ⚠ disk 85% `, amber at warning, red at critical |
| `disk-watch hook` | `SessionStart` and `UserPromptSubmit` | the first session to see a new alert level gets the order to send one `PushNotification` to the owner's phone; the others stay quiet; a rise from warning to critical pushes again |
| `disk-watch gc` | daily at 04:00 (`disk-watch-gc.timer`) | `docker image prune --all --filter until=72h` (an image a running scene still uses is kept) and `docker builder prune --max-used-space 10GB` |
| journald cap | always | `SystemMaxUse=1G` in `/etc/systemd/journald.conf.d/size.conf` |
| syslog cap | every hour | `maxsize 500M` in `/etc/logrotate.d/rsyslog`, with `logrotate.timer` moved to hourly |

The snapshot is a `du --max-depth=3` of `/` (about a minute, at idle I/O priority), taken once a day and whenever an alert rises, kept in `~/.local/state/disk-watch/sizes.tsv` with the previous one next to it.

## Commands

```bash
disk-watch status          # the last measurement and the alert, if any (numbers only)
disk-watch status --paths  # also the directories that grew: names from du, so read them yourself, never hand them to a model
disk-watch check           # measure now
disk-watch gc --dry-run    # the Docker prune commands, without running them
systemctl --user list-timers 'disk-watch-*'
```

Thresholds and paths come from the environment: `DISK_WATCH_THRESHOLD_WARNING` (80), `DISK_WATCH_THRESHOLD_CRITICAL` (90), `DISK_WATCH_PATH` (`/`), `DISK_WATCH_SNAPSHOT_DEPTH` (3), `DISK_WATCH_SNAPSHOT_MAX_AGE_HOURS` (24).

## Install

`scripts/utilities/install.sh` sources `install.sh` here: it copies the user units, enables both timers and writes the two caps with `sudo`. The units run the script from the main clone, `~/git/linux`.

## The push

A script cannot reach the owner's phone by itself here: `PushNotification` is a Claude Code tool. So the alert waits for the next prompt or session start, and the hook hands the push to one session. A deterministic channel (a self-hosted ntfy, for example) can replace the hook later without changing the alert file.
