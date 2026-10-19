---
name: speak-words
description: Use when English words sound wrong in the `speak` voice (Piper, pt-BR), when the owner asks to tune, add or review the pronunciation vocabulary ("vocabulário do speak", "essa palavra soa estranha", "ajustar a pronúncia", "speak-words"), or to grow it from the words used in a repository's history.
---

# speak-words

`speak` (`~/git/linux/scripts/bin/speak`) reads pt-BR with a Portuguese Piper voice, so English terms sound odd. `~/.config/speak/words` holds one `word=respelling` per line; `speak` replaces each word (whole word, case-insensitive) before Piper reads the text. This skill finds the respelling the owner likes, by ear, and saves it.

## What works (learned with `merge` and `request`, 2026-10-18)

- **Respell in Portuguese letters, by syllables of names the owner already hears well:** `merge` = the MER of "Mércia" + "ji" → `mér-jí`; `request` → `ríkuéchte`. The owner is from Recife: an `s` before a consonant or at the end sounds better as a "ch" (`chiado`).
- **A hyphen splits syllables that blend** (`mér-jí`); `rr` before a consonant swallows it (`mérrjí` sounded like "mérrí").
- **Do not use IPA or audio splicing:** dictionary phonemes sent to the voice and syllables cut from real words were tried and dropped; the voice reshapes each sound by its neighbours, and cuts leave seams ("merziê").
- **Play only the word, never a sentence**, and one sample at a time when the owner asks; a clip under half a second gets swallowed by the sound card, so the page plays through `speak` itself.

## Steps

1. **Pick the words:** the ones the owner names, else the most frequent English terms of the repository's history (`git log --all --format='%s%n%b'`, counted, stop words and ids removed), skipping those already in `~/.config/speak/words`.
2. **Draft eight respellings per word** in a JSON file in the scratchpad: `{"<word>": ["...", ...]}`. Vary one thing at a time: the stressed vowel (é/ê/â), the `r`, the `s` (chiado or not), the final vowel (i, e, none).
3. **Open the page in the visual companion** (`superpowers:brainstorming`, `visual-companion.md`): render it with `render-page --data <json> --out <screen_dir>/speak-words.html` (this skill's directory; a new `--out` name on every render). The page: the word list on top, one word below; each spelling editable, ▶ plays it, ★ chooses, ≈ marks "right direction", ✕ discards as "far off", "nenhuma serve: +10" discards all and asks for ten more. Choices and discards survive reloads (localStorage); discarded spellings go into `_discarded` of the JSON, and `_reset: {"<word>": "<token>"}` starts a word over.
4. **Play on the computer, not in the browser:** a background watcher speaks each ▶ through `speak`:
   ```bash
   tail -n0 -F "<state_dir>/events" | while read -r line; do
     word="$(jq -r 'select(.choice == "say") | .word // empty' <<< "${line}")"
     [[ "${word}" =~ ^[[:alpha:]\ \'-]{1,40}$ ]] && { pkill -x pw-play; speak "${word}" & }
   done
   ```
   and a `Monitor` on the same file reports `more`, `like` and `unlike` (log every line to a file in the scratchpad: the server clears `events` on each new screen).
5. **On "+10":** read the word's ≈ (keep that direction) and ✕ (avoid that sound) from the log, write ten new spellings that repeat none of `_discarded`, render a new page.
6. **On ★:** add or replace `word=respelling` in `~/.config/speak/words`, then `speak` a short pt-BR sentence that uses the word, to hear it in context.

## Rules

- Only the main session calls `speak`; a subagent never does.
- Keep the owner's own respellings as typed, accents included.
