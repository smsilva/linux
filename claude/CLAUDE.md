# Instructions

## General
- Concise responses, actionable
- No preamble ("Sure!", "Great question!")
- No narration before tool calls
- Don't restate the question
- Skip hedging phrases ("Note that...", "Keep in mind...")
- Explain only non-obvious logic

## Bash scripts
- No file extension on executables
- Long-form CLI options (`--yes`, not `-y`)
- 2-space indent; `do`/`then` on same line as `while`/`if`
- Lowercase locals; UPPERCASE env vars
- Always quote: `"${variable}"`
- stdin fallback: `input_file="${1:-/dev/stdin}"`
- Required args: `${var?}`
- Add script's own directory to `$PATH` to reference sibling scripts
- Show only a short prefix when printing secrets: `"${SECRET:0:3}"`
- Use `set -e` only for scripts with sequential steps that must all succeed
- When call a script, split each argument onto its own line for readability:
```bash
./command-or-script \
  --option1 value1 \
  --option2 value2 \
  --option3 value3
```
