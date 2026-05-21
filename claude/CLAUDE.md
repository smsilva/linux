# Instructions

## General
- Always use English when creating Agent Skills
- Never translate technical terms (e.g., "API", "endpoint", "commit", "pull request")
- Concise actionable responses
- No preamble (e.g., "Sure!", "Great question!")
- No narration before tool calls
- Don't restate the question
- Skip hedging phrases ("Note that...", "Keep in mind...")
- Explain only non-obvious logic
- Offer to open artifacts like pdf files using `open <file>` or `xdg-open <file>` instead of just returning the path
- `~/.claude/` entries (skills/, CLAUDE.md, agents/) are symlinks into `~/git/linux/claude/` — paths like `${HOME}/.claude/skills/...` resolve to versioned locations automatically
- Folder structures should reflect the ideas they contain; files at deeper levels must not repeat parent folder names unless genuinely meaningful

## Bash scripts
- No file extension on executables
- Long-form CLI options (`--yes`, not `-y`)
- 2-space indent; `do`/`then` on same line as `while`/`if`
- Lowercase locals; UPPERCASE env vars
- Always quote: `"${variable}"`
- stdin fallback: `input_file="${1:-/dev/stdin}"`
- Required args: `${var?}`
- Add script's own directory to `${PATH}` to reference sibling scripts
- Show only a short prefix when printing secrets: `"${SECRET:0:3}"`
- Use `set -e` only for scripts with sequential steps that must all succeed
- Python scripts should use `argparse` for CLI parsing, not manual `$1`, `$2` handling
- When calling a script, split each argument onto its own line for readability:
```bash
command-or-script \
  --long-option-1 value1 \
  --long-option-2 value2
```
