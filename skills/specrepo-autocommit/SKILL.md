---
name: specrepo-autocommit
description: Finalize an approved SpecRepo implementation by calling the Python-backed specrepo-autocommit custom tool after verification and a passing test review. Use only for the final commit step of an approved implementation.
metadata:
  owner-agent: spec-coder
---

## Purpose

Use this skill only as the final command after an approved implementation has
passed required verification and `@test-reviewer` returned `pass`.

## Preconditions

All preconditions must be true:

- An approval record exists under `specrepo/approved/`.
- The approved proposal referenced by that record was followed.
- A matching implementation review exists under `specrepo/implementation-reviews/`.
- Required verification commands passed.
- `@test-reviewer` returned recommendation `pass`.
- The working branch is not `main`.

## Tool call

Call the `specrepo-autocommit` custom tool with:

```json
{"summary":"<summary of what changed>"}
```

Before calling the tool, require `AUTOCOMMIT_PARAMS` to be set to the user's
YAML configuration file. The Python implementation announces the resolved file
path, passes it to `autocommit` with `--config-file`, and fails when the
variable or file is missing. It does not select behavior based on
`OPENCODE_API_KEY`.

If the tool fails after finding the configuration file, report the displayed
`AUTOCOMMIT_PARAMS` location so the user can update it. Refer the user to the
[config overrides guide](https://github.com/brandon-benge/langchain_autocommit/blob/main/README.md#config-overrides)
for configuration instructions.

## Prohibitions

Do not call the tool when:

- Verification failed, was skipped, or could not run.
- `@test-reviewer` returned `blocked` or `needs more tests`.
- The implementation exceeded approved scope.
- The current branch is `main`.
