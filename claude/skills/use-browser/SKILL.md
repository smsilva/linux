---
name: use-browser
description: Enable browser use with Playwright Python. Use this skill when the user asks to access or interact with a web page, scrape information from a website, automate web tasks, or perform any action that requires a real browser environment. This skill allows you to navigate websites, fill out forms, click buttons, and extract data as if you were using a browser yourself.
---

This skill enables browser use with Playwright, allowing you to access and interact with web pages, scrape information, automate tasks, and perform any action that requires a real browser environment.

## Installation

```bash
pip install playwright --break-system-packages -q && playwright install chromium 2>&1 | tail -5
```

## Scripts

Ready-to-use scripts live in `claude/skills/use-browser/scripts/`. Run them directly with `python3 scripts/<name>` or copy/adapt as needed.

All scripts save output under `/tmp/web/<site-name>/`.

| Script | Purpose | Usage |
|---|---|---|
| `screenshot` | Full-page screenshot | `screenshot <url> [output_path]` |
| `scrape-text` | Extract visible text | `scrape-text <url>` |
| `scrape-html` | Extract full HTML | `scrape-html <url>` |
| `scrape-links` | List all links (href + text) | `scrape-links <url>` |
| `wait-and-scrape` | Wait for selector, extract text | `wait-and-scrape <url> <selector>` |
| `multi-page` | Paginate and collect items | `multi-page <url> <item_sel> <next_sel> [max_pages]` |
| `auth-session` | Login and reuse saved session | `auth-session login <url> <user> <pass>` / `auth-session use <url>` |

## Patterns

### Headless vs headed

```python
browser = await p.chromium.launch(headless=True)   # default, no window
browser = await p.chromium.launch(headless=False)  # visible window for debugging
```

### Intercept network requests

```python
await page.route("**/*.{png,jpg,gif}", lambda r: r.abort())  # block images
await page.route("**/api/**", lambda r: print(r.url) or r.continue_())
```

### Execute JavaScript

```python
result = await page.evaluate("() => window.__SOME_GLOBAL__")
await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
```

### Handle dialogs

```python
page.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
```

### Set viewport and user agent

```python
ctx = await browser.new_context(
    viewport={"width": 1280, "height": 720},
    user_agent="Mozilla/5.0 ..."
)
```
