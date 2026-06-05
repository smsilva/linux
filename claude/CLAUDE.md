# Instructions

## Communication
- Concise, actionable responses
- No preamble ("Sure!", "Great question!")
- No narration before tool calls
- Don't restate the question
- Skip hedging ("Note that...", "Keep in mind...")
- Explain only non-obvious logic
- Offer to open artifacts with `xdg-open <file>` instead of returning bare paths

## Workflow
- Walk Skeleton: ship a thin end-to-end slice early for feedback
- Bitbucket PRs: 
  - Generate a description
  - Save it as `/tmp/<branch>-pr.txt` but using markdown
  - Open with `xdg-open`
  - Display the Bitbucket URL for creation (`https://bitbucket.org/.../pull-requests/new?source=<branch>&t=1`)

## Language
- Write Agent Skills in English
- Never translate technical terms (API, endpoint, commit, push, pull request, cache, parse)

## Architecture
- `~/.claude/` entries (skills/, CLAUDE.md, agents/) are symlinks into `~/git/linux/claude/`
- Don't repeat parent folder names in nested file names

## Bash scripts
- No file extension on executables
- Long-form CLI options (`--yes`, not `-y`)
- 2-space indent
- `do`/`then` on same line as `while`/`if`
- Lowercase locals; UPPERCASE env vars
- Always quote: `"${variable}"`
- stdin fallback: `input_file="${1:-/dev/stdin}"`
- Required args: `${var?}`
- Add script's own directory to `${PATH}` to reference sibling scripts
- Print secrets with short prefix only: `"${SECRET:0:3}"`
- Use `set -e` only for scripts with sequential steps that must all succeed
- Python scripts: use `argparse`, not manual `$1`, `$2` handling
- Split long CLI calls one argument per line:
```bash
command-or-script \
  --long-option-1 value1 \
  --long-option-2 value2
```
