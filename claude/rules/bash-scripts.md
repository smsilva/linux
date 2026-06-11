# Bash scripts

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
