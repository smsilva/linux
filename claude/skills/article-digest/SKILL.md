---
name: article-digest
description: Use when the user shares a URL or article and asks to extract key learnings, summarize topics, or generate a digest formatted for Google Chat, Slack, or similar messaging tools.
---

# Article Digest

## Overview

Fetch an article, extract the main learnings as short bullet topics, and write a `.txt` file formatted for Google Chat (bold via `*text*`, no icons/emoji).

## Steps

1. Fetch the article URL with `WebFetch` — prompt: "Extract all main topics, key concepts, problems, solutions, and conclusions."
2. If the page returns only navigation (no body), requires auth (LinkedIn, Substack paywall, Google Docs), or redirects to a login wall — search via `WebSearch` for the article title + year to find an alternate source, then fetch that.
3. Extract 6–12 short topic groups. Each group: one bold header line + 1–3 plain lines of substance.
4. Write to `~/tmp/articles/<article-title-condensed>.txt` (e.g. `~/tmp/articles/context-lake-ai-agents.txt`). Create the directory if it doesn't exist.
5. Offer to open: `xdg-open <file>`.

## Output format (Google Chat)

```
*Title of the article*

*Topic header*
Short sentence or two. No bullet dashes, no emoji, no markdown except *bold*.

*Another topic header*
Content here.

<original URL, bare, on its own line>
```

Rules:
- Bold only with `*asterisks*` (Google Chat syntax)
- No `-` bullets, no `#` headers, no emoji
- Numbers allowed for ordered lists when order matters
- Portuguese unless user specifies otherwise
- Keep each topic group under 4 lines
- Bare URL on the last line of the file — no "Fonte:" label

## Google Chat: sharing with link

To share in Google Chat with a clickable title:
1. Paste the article title in the message field
2. Select the title text
3. In the dynamic menu that appears, click "Insert link"
4. Paste the article URL

Include this instruction as a tip at the end of the response to the user.
