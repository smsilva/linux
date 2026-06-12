---
name: article-digest
description: Use when the user shares a URL or article and asks to extract key learnings, summarize topics, or generate a digest formatted for Google Chat, Slack, Discord, Telegram, or similar messaging tools. Accepts an optional format parameter.
---

# Article Digest

## Overview

Fetch an article, extract the main learnings as short topic groups, and write a `.txt` file. Default format: Google Chat. Pass a second argument to target another platform.

## Format parameter

Syntax: `/article-digest <url> [format]`

| Format        | Bold         | Italic       | Notes                              |
|---------------|--------------|--------------|------------------------------------|
| `google-chat` | `*text*`     | `_text_`     | **default**                        |
| `slack`       | `*text*`     | `_text_`     | same syntax as Google Chat         |
| `telegram`    | `*text*`     | `_text_`     | same syntax (MarkdownV2)           |
| `whatsapp`    | `*text*`     | `_text_`     | same syntax                        |
| `discord`     | `**text**`   | `_text_`     | double asterisk                    |
| `markdown`    | `**text**`   | `_text_`     | generic MD; `##` headers allowed   |
| `plain`       | no markup    | no markup    | line breaks only; ideal for email  |

If the format argument is not recognized, fall back to `google-chat` and warn the user.

## Steps

1. Fetch the article URL with `WebFetch` — prompt: "Extract the author name, publication date, and all main topics, key concepts, problems, solutions, and conclusions."
2. If the page returns only navigation (no body), requires auth (LinkedIn, Substack paywall, Google Docs), or redirects to a login wall — search via `WebSearch` for the article title + year to find an alternate source, then fetch that.
3. Extract 6–12 short topic groups. Each group: one bold header line + 1–3 plain lines of substance. Keep each content line to a single concise sentence — break compound or multi-part content into separate short lines rather than long paragraphs.
4. Write to `~/tmp/articles/<article-title-condensed>.txt` for the default format, or `~/tmp/articles/<article-title-condensed>-<format>.txt` when a non-default format is specified (e.g. `context-lake-ai-agents-discord.txt`). Create the directory if it doesn't exist.
5. If the digest has more than 6 topic groups, deliver the full version first, then immediately present a reduction suggestion: which topics could be merged or removed to condense it as much as possible without losing the article's essence. Don't apply the reduction unless the user approves.
6. Offer to open: `xdg-open <file>`.

## Output format

Apply bold/italic markers from the format table above. The structure is always:

```
<bold>Title of the article</bold>

<bold>author name</bold>
<italic>publication date</italic>

<bold>Topic header</bold>
Short sentence. No bullet dashes, no emoji.

<bold>Another topic header</bold>
Content here.

<original URL, bare, on its own line>
```

Rules:
- No `-` bullets, no `#` headers (except `markdown` format), no emoji
- Numbers allowed for ordered lists when order matters
- Portuguese unless user specifies otherwise
- Keep each topic group under 4 lines
- Prefer short paragraphs: one sentence per line. Split long sentences into shorter lines instead of packing several ideas into one line
- Right after the title: author name on its own line in bold, then publication date on the next line in italic. If author or date can't be found, write what is known or skip the missing line.
- Bare URL on the last line of the file — no "Fonte:" label

## Sharing tips

**Google Chat:** to share with a clickable title:
1. Paste the article title in the message field
2. Select the title text
3. In the dynamic menu that appears, click "Insert link"
4. Paste the article URL

**Discord / Slack / Telegram / WhatsApp:** paste the content directly — formatting renders automatically.

Include the relevant tip at the end of the response to the user based on the format used.
