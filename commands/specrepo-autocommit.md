---
description: Finalize verified SpecRepo changes with autocommit
agent: spec-coder
---

Load the `specrepo-autocommit` skill and enforce all of its preconditions.

Use `$ARGUMENTS` as the summary when it is non-empty. Otherwise, derive a
concise summary from the verified diff. Then call the native OpenCode tool
`specrepo-autocommit` exactly once with this argument shape:

```json
{"summary":"<summary of what changed>"}
```

This is a tool call, not a shell command. Do not invoke the Python file
directly and do not use `git commit` as a fallback. Report whether the tool
ran, was blocked, was rejected, or failed, following the loaded skill.
