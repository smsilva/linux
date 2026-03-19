---
name: use-browser
description: Enable browser use with Playwright Python. Use this skill when the user asks to access or interact with a web page, scrape information from a website, automate web tasks, or perform any action that requires a real browser environment. This skill allows you to navigate websites, fill out forms, click buttons, and extract data as if you were using a browser yourself.
---

This skill enables browser use with Playwright, allowing you to access and interact with web pages, scrape information, automate tasks, and perform any action that requires a real browser environment. You can navigate websites, fill out forms, click buttons, and extract data as if you were using a browser yourself.

## Usage

When the user asks to perform a task that requires browser interaction, use this skill to execute the necessary Playwright commands. For example:

- To navigate to a website: `await page.goto('https://example.com');`
- To fill out a form: `await page.fill('#username', 'myUsername');`
- To click a button: `await page.click('#submit');`
- To extract data: `const text = await page.textContent('#result');`

## Playwright Installation

To use this skill, ensure that Playwright is installed in your Python environment. You can install it using pip:

```bash
pip install playwright --break-system-packages -q && playwright install chromium 2>&1 | tail -5
```

After installing Playwright, you may need to install the necessary browser binaries:

```bash
playwright install
```

## Capture Screenshots

You can also capture screenshots of web pages using Playwright:

```python
await page.screenshot(path='/tmp/web/<web-site-main-name>/screenshots/image-<timestamp>.png');
```
