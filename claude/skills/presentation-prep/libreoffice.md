# LibreOffice + PPTX

## Standard palette → hex mapping

When editing color via OOXML (`<a:srgbClr val="...">`), don't guess the hex from a swatch name. Empirical mapping confirmed via the LibreOffice Character → Font Effects dialog:

- **Dark Gray 1** = `#666666`
- `#1C1C1C` is a darker custom black-ish gray, NOT Dark Gray 1.

If a user says "I applied Dark Gray N", open the saved `.pptx` and read the actual `srgbClr` byte before assuming — don't trust palette-name memory.

## Auditing colors deterministically

Parse per `<a:r>...</a:r>` run boundary, NOT across the whole XML — greedy regex spanning multiple runs gives false positives all matching the same color.

```python
for m in re.finditer(r'<a:r>(.*?)</a:r>', content, re.DOTALL):
    run = m.group(1)
    text = re.search(r'<a:t>([^<]+)</a:t>', run)
    color = re.search(r'<a:srgbClr val="([0-9A-Fa-f]+)"/>', run)
```

Always re-extract from the saved `.pptx` on disk (not the `/tmp` working dir) to prove changes persisted.

## Edit-while-open trap

LibreOffice locks the file (`.~lock.<file>#`) and the `.pptx` mtime won't change until the user saves. If hex audit doesn't match what the user reports seeing, check the file timestamp before debugging the mapping.

## Packing without validation

`presentation.xml` may have `notesMasterIdLst` after `sldIdLst` violating OOXML schema strict mode. Pack with `--validate false` (office/pack.py) or use direct `zip -qr` if the official pack script rejects the layout.