---
name: presentation-prep
description: Use when organizing raw content into slide-ready format, or when the user says "prepare slides", "structure this for a presentation", "brief for pptx".
---

# Presentation Prep

Transforms raw content into slide-ready structure using David Phillips' 5 cognitive principles ("How to Avoid Death by PowerPoint").

## The 5 Principles

### 1. One message per slide
Each slide = one idea. Two messages → two slides.
Human attention hijacks toward the familiar (a name, a number) and loses the rest.

### 2. No text-voice redundancy
- **Slide**: image + few keywords that *reinforce* the speech
- **Speaker notes**: the full text that would be spoken
- Rule: if it's written on the slide, don't say it — if you're going to say it, don't write it

### 3. Size = importance
The visually largest element captures eyes automatically.
Most templates make the title the largest element — **wrong**.
- Shrink the title
- Enlarge the most important element on the slide
- Only one element should stand out by size

### 4. Contrast guides attention
- **Dark background**: the presenter becomes the highest-contrast object in the room; the slide is visual support
- **White background**: the slide competes with the presenter
- **List build technique (progressive reveal)**: reveal bullet items one at a time using animation builds
  - Current item: full brightness (white on dark background)
  - Previous items: dimmed to ~40% opacity / gray — visible for context but no longer competing for attention
  - Never show the full list at once; each item gets its moment as the sole high-contrast element
  - David Phillips: *"I show the first topic, then I remove it with contrast"*

### 5. Maximum 6 objects per slide
Above 6 objects, the brain is forced to *count* instead of *see* — 500% more cognitive effort; audience disengages.
- Objects include: logos, icons, table rows, list items, text boxes, shapes, page numbers
- More slides with fewer objects > fewer crowded slides
- Remove page numbers, repeated corporate logos, footer text from every slide

## Workflow when receiving content for slides

1. **Identify key messages** — how many are there? Each becomes a slide
2. **Separate** what goes on the slide vs. in speaker notes
3. **Define visual hierarchy** — largest element = most important message (not the title)
4. **Count objects** per slide — ≤ 6; split if exceeded

## Default patterns

**Progressive reveal is the default.** Almost every content slide should split into multiple reveals — `animations: none` is the exception, reserved for opening/closing slides.

### Standard slide types

- **Opening**: title alone → title + subtitle
- **Topic with detail**: keyword bright → keyword dimmed + body content
- **Topic list (per-section)**: each topic as its own progressive item (no body — just one keyword per reveal)
- **Flow diagram**: keyword + nodes revealed one per reveal (each node becomes active; previous nodes dim; keyword bright on first reveal, dimmed on subsequent)
- **Numbered list of steps**: one item per reveal; previous items dimmed

### Topics, not sentences

The body of a content slide is a **keyword phrase** (2–4 words), not a complete sentence. Descriptive sentences belong in `notes`. If you find yourself writing "Well-defined issues take time…" on a slide, that's prose — extract the keyword ("Repetitive work") and move the sentence to notes.

### Icons: off by default

Do not add icons unless the user explicitly asks. When the user requests icons:
- **Monochromatic** (white on dark background)
- **Simple outline style** (e.g. Phosphor Icons Light, Heroicons outline)
- **Same family throughout the deck** — never mix Phosphor with Font Awesome

### Vertical spacing for progressive lists

Ensure footer clearance with an explicit calculation:

```
N items × (itemH + gap) ≤ (footerY - listTop)
```

Example: a 5-item list between y=1.1 and y=5.1 → `itemH + gap = 0.80` (e.g. `itemH=0.68, gap=0.12`).

## Reference assets

| File | Purpose |
|---|---|
| `assets/reference-presentation.odp` | 18-slide neutral reference (dark theme): opening/closing slides, pill labels, dominant keywords, progressive-build sequences, warning tables, flow diagrams. Use as visual spec when implementing from scratch. |
| `assets/animation-example.odp` | Minimal working example of progressive reveal animations in LibreOffice/Impress format. |

For ODP animation XML and implementation details, see [references/odp-animations.md](references/odp-animations.md).

## Expected output for pptx skill

Deliver as YAML:

**Field definitions:**

| Field | What goes here |
|---|---|
| `message` | The ONE idea this slide communicates — one sentence max |
| `visual` | The dominant visual element(s): image, icon, keyword, code snippet, table, or diagram. Describe **what** appears — not layout, not size, not position. Size follows Principle 3 automatically. **Forbidden:** size words (`large`, `small`), position words (`centered`, `left`, `right`, `horizontal`, `side by side`, `top`, `bottom`), the `"Small title: '...'"` pattern, and animation descriptions (those belong in `animations`). |
| `notes` | Everything the presenter would speak — text that must NOT appear on the slide (Principle 2) |
| `animations` | `progressive-build` (default) or `none` (opening/closing only). In pptxgenjs (no native animation support): implement as **duplicate slides** — one per reveal. Active: full brightness, bold. Previous: dimmed (`DIM` from validated palette). Future: hidden. Title and section labels persist on every duplicate. Arrows: full brightness toward active item; dimmed between already-shown items. For ODP native animations, see [references/odp-animations.md](references/odp-animations.md). |
| `objects` | Count every visible element: title, keywords, icons, list items, images, table rows |

```yaml
deck:
  title: "Presentation Title"
  filename: "presentation-title.pptx"
  background: dark  # dark recommended; light only if explicitly requested
  transition: fade  # uniform across all slides

slides:
  - id: 1
    type: opening  # title slide with presentation theme
    message: "..."
    visual: "Icon or thematic image + presentation name as dominant keyword"
    notes: "..."
    animations: none
    objects: 2

  - id: 2
    message: "..."
    visual: "Keyword or diagram that anchors the message — no layout instructions"
    notes: "Full spoken text — nothing from here should appear on the slide"
    animations: none  # or: progressive-build (dim previous items to ~40% opacity as each bullet is revealed)
    objects: 4

  - id: N
    type: closing  # thank-you + contact info; omit if context doesn't call for it
    message: "..."
    visual: "..."
    notes: "..."
    animations: none
    objects: 2
```

### Validated dark palette

| Token | Hex | Use |
|---|---|---|
| `BG` | `0A0E1A` | Slide background |
| `WHITE` | `FFFFFF` | Active keyword, label |
| `BODY` | `C0D2E4` | Body text (high contrast on BG) |
| `DIM` | `6B7A8D` | Previous-reveal items, dimmed keyword (validated for projector; avoid `565E6B` — too dark) |
| `ACCENT` | `4A9EF4` | Footer rule, flow-diagram borders |

Section label: 10pt, bold, white, `charSpacing: 3`, uppercase. Footer: thin horizontal line at y=5.2 in `ACCENT` with `transparency: 60` — anchors the bottom of every content slide.

## Visual QA (required before delivery)

After generating the `.pptx`, convert to images (`soffice --convert-to pdf` + `pdftoppm -jpeg -r 150`) and dispatch a **subagent** for visual inspection. The subagent catches problems the generator cannot see: overflow, dead space, invisible icons, last item clipping the footer, insufficient dimming for projector, vertical position inconsistencies across slides in the same section.

Iterate until zero critical issues remain.
