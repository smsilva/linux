# Archived skills

Skills out of use, kept so they can come back. Claude Code does not detect them here: it scans `~/.claude/skills/`, which is a symlink to `claude/skills/`, and this folder is outside it.

## Bring one back

```bash
git mv claude/archived/skills/<name> claude/skills/<name>
```

Then remove its `"<name>": "off"` line from `skillOverrides` in `claude/settings.json`, if it has one (`about-me`, `all-skills-review`, `daily`, `use-browser` and `video-captions` do today).

## Third-party skills

`diagnosing-bugs` and `grill-me` are symlinks into `~/.git/{owner}/{repo}/`. They left `claude/skills/third-party.md` because `/skill-from-github-repository-update bootstrap` reinstalls every row of it. To bring one back, also add its row again:

| skill | url |
|-------|-----|
| diagnosing-bugs | https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs |
| grill-me | https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me |
