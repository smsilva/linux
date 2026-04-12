---
name: bash-scripts
description: Create or update bash scripts following the conventions of the existing scripts in `~/git/linux/scripts/bin/`.
license: MIT
---

# bash-scripts skill

Create bash scripts following the conventions of the existing scripts in `~/git/linux/scripts/bin/`.

## Using an existing script as reference

When the user mentions a script by name as a reference (e.g. "based on my script foo", "following script bar", "like script baz"), **always locate and read that script first** before writing anything:

1. Run `which <script>` to locate it via `${PATH}` — this is the primary lookup since scripts are installed as executables in `${PATH}`
2. If not found via `which`, fall back to searching in `~/git/linux/scripts/bin/` (and subdirectories)
3. Read its full content
4. Follow its conventions, structure, and patterns — treating it as the authoritative template for that task

Only fall back to the generic template below if the script is not found by either method.

## Core principles

- **Unix philosophy**: each script does one thing and does it well
- **Composable**: scripts should work with pipes (`|`), stdin, and stdout
- **No extension**: scripts have no `.sh` extension (they are executables in `$PATH`)

## Variable naming

- **Local variables**: always lowercase with underscores (`input_file`, `dry_run`, `start_date`)
- **Environment variables**: always UPPERCASE (`ARM_SUBSCRIPTION_ID`, `KUBECONFIG`)
- Quote variables in expansions: `"${variable}"` — not `$variable`

## Script structure

### Minimal script (no options needed)

```bash
#!/bin/bash
arg1="${1}"
arg2="${2}"

# logic here
```

> **Shebang**: use `#!/bin/bash` for portability. `#!/usr/bin/env bash` is also acceptable when bash portability across non-standard PATH environments is needed (e.g. macOS, cross-platform scripts).

### Script with options (use `foo` as the canonical template)

```bash
#!/bin/bash
this_script_path="$(realpath ${0})"
this_script_name="${this_script_path##*/}"
this_script_directory="${this_script_path%/*}"

PATH="${this_script_directory}:${PATH}"

show_usage() {
  cat <<EOF

  <One-line description of what the script does>

    Options:

      -h,  --help     Show this help
      -n,  --name     <description> (default: <value>)
      -dr, --dry-run  Dry Run (default: false)

    Examples:

      ${this_script_name} --name bar file

      ${this_script_name} file

      ${this_script_name} < file

      sort file | ${this_script_name}
EOF
}

while [[ "${1}" =~ ^- && ! "${1}" == "--" ]]; do
  case $1 in
    -h | --help )
      show_usage
      exit 1
      ;;

    -n | --name )
      shift
      name="${1}"
      ;;

    -dr | --dry-run )
      if [[ -n "${2}" && "${2}" =~ ^(true|false)$ ]]; then
        dry_run="${2}"
        shift
      else
        dry_run=true
      fi
      ;;

    - )
      input_file="/dev/stdin"
      ;;

    * )
      echo "Invalid option: ${1}"
      show_usage
      exit 1
      ;;

  esac
  shift
done

if [[ "${1}" == '--' ]]; then shift; fi

# Positional args after options
if [[ -z "${input_file}" ]]; then
  input_file="${1:-/dev/stdin}"
fi

# Defaults for optional flags
dry_run="${dry_run:-false}"
name="${name:-bar}"

# Script logic here
```

## Key patterns

### Stdin / file fallback

Always support reading from a file argument OR stdin:

```bash
input_file="${1:-/dev/stdin}"
while read -r line; do
  echo "${line}"
done < "${input_file}"
```

### Required argument validation

Use `${var?}` to fail fast with a clear error when a required variable is unset:

```bash
url="${1}"
openssl s_client -connect ${url?}:443 ...
```

### Dry-run flag

Boolean flags, only in cases when the script will make changes, accept an optional `true`/`false` value, defaulting to `true` when the flag is present alone:

```bash
-dr | --dry-run )
  if [[ -n "${2}" && "${2}" =~ ^(true|false)$ ]]; then
    dry_run="${2}"
    shift
  else
    dry_run=true
  fi
  ;;
```

### Referencing sibling scripts

Add the script's own directory to `$PATH` so sibling scripts are callable by name:

```bash
this_script_directory="${this_script_path%/*}"
PATH="${this_script_directory}:${PATH}"
```

### `set -e`

Use `set -e` when the script has sequential steps that must all succeed:

```bash
#!/bin/bash
set -e
```

Skip it for scripts that handle errors explicitly or use pipelines.

### Secrets / sensitive values

Never print full secret values. Show only a prefix for confirmation:

```bash
echo "ARM_CLIENT_SECRET: ${ARM_CLIENT_SECRET:0:3}"
```

## CLI option names

Always use long-form option names when available — `--yes` instead of `-y`, `--verbose` instead of `-v`, `--output` instead of `-o`. This applies to both scripts written here and CLI commands used as examples or references. Short forms (`-y`, `-v`) are only acceptable inside `show_usage` to document the short alias.

## Style

- Indent with 2 spaces
- Opening `do`/`then` on the same line as `while`/`if`
- `case` closing `;;` aligned with the option pattern
- Long commands broken with `\` and 2-space indent per continuation
- heredoc delimiter: `EOF`
- No trailing semicolons inside `if`/`while` blocks
