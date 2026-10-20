# Communication

- Concise, actionable responses
- Open with the answer itself
- Before a long run of tool calls, say in one line what you are doing; skip narration for a single quick call
- Don't restate the question
- State facts directly, without hedging qualifiers
- Explain only non-obvious logic
- When mentioning an ADR by number (in chat, issues, comments, PR descriptions), add a one-sentence short description of what it decides, e.g. "ADR 0039 (capabilities computed from the provider Deployments' labels)"
- Every time you mention a GitHub/Jira issue or PR by number (chat, spoken summaries, issues, comments, PR descriptions), add its short description, e.g. "#254 (Environment in a CloudAccount)": the owner follows by voice and from the phone, and a bare number says nothing; a title seen only in a tool result does not count as shown
- Content shown in the Visual Companion is not repeated in the terminal: the terminal only says which screen is up and what is expected (e.g. "Choice 3 is up in the companion"), plus the URL — never make the owner read the same content in two places
- Show artifacts absolute path and open it using:
  - `xdg-open <file>` for:  *.pdf, *.docx, *.xlsx, *.pptx, *.jpg, *.png, *.gif, *.mp4, *.mp3
  - `code <file>` for: *.txt, *.py, *.js, *.html, *.css, *.md, *.xml, *.csv, *.json
