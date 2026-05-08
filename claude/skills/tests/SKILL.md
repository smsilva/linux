---
name: tests
description: Run all tests in the current repository
disable-model-invocation: true
---

- Detect the test framework(s) in use (pytest, jest, go test, bats, etc.) and run all tests
- Report: total, passed, failed, skipped
- On failure, show only failing test names and their errors
