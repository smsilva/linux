# Communication

- Concise, actionable responses; open with the answer itself
- Before a long run of tool calls, say in one line what you are doing; skip it for a single quick call
- Don't restate the question
- State facts directly, without hedging
- Explain only non-obvious logic
- ADR by number (chat, issues, comments, PR descriptions): add one sentence on what it decides, e.g. "ADR 0039 (capabilities computed from the provider Deployments' labels)"
- GitHub/Jira issue or PR by number, on every mention (chat, spoken summaries, issues, comments, PR descriptions): add its short description, e.g. "#254 (Environment in a CloudAccount)": the owner follows by voice and from the phone, and a bare number says nothing; a title seen only in a tool result does not count as shown
- Show an artifact's absolute path and open it:
  - `xdg-open <file>`: pdf, docx, xlsx, pptx, jpg, png, gif, mp4, mp3
  - `code <file>`: txt, py, js, html, css, md, xml, csv, json
- A summary that asks for the owner's decisions uses colors (owner, 2026-11-03), so it can be read first and decided at the end:
  - 🟢 only information, one line, no number; 🟠 to review, with a suggestion of high confidence; 🔴 depends on the owner's answer.
  - The order on screen is 🟢, 🟠, 🔴. Numbers start at 1 on the first item that asks for action and follow the screen across the colors.
  - 🔴 always waits for the owner's answer. A 🟠 the owner does not mention counts as accepted, only after every 🔴 is answered; never act on one before that.
  - The summary ends with the agent's weighing, not a sample reply: one line per 🔴, with the recommendation and its reason in as few words as possible.
- Anchored sessions (running on the owner's machine in tmux, driven through Remote Control from the phone or claude.ai/code, as opposed to cloud sessions): whenever a task ends with something that needs the owner's answer (a decision, an approval, a `/ship`), send a `PushNotification`, one line under 200 characters that leads with what the owner must answer (owner, 2026-11-08).
