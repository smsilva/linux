# Apps

One folder per application or utility, grouping everything about it:

```
apps/<app>/
  config/     snapshot of the app's config directory (e.g. ~/.config/<app>)
  install     installer (to be migrated from scripts/utilities/<app>/)
  README.md   what is versioned, what is left out, how to restore and refresh
```

## Rules

- The repository is public: never version passwords, tokens, stream keys, API keys, or unique install/cookie IDs. List what was left out in the app's `README.md`.
- Version only what you would restore on a new machine; skip logs, caches and files the app regenerates.
- Use the app's own name for the folder (`obs-studio`, not `obs`).
