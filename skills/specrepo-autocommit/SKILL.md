---
name: specrepo-autocommit
description: Finalize an approved SpecRepo implementation by running the local autocommit hook after verification and test review pass.
compatibility: opencode
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

## Command

Run:

```bash
$HOME/.config/opencode/specrepo-autocommit "<four-line summary>"
```

The summary must contain exactly four non-empty lines.

Set `AUTOCOMMIT_PARAMS` only when the user or environment provides a config
file path for the autocommit CLI.

## Prohibitions

Do not run the hook when:

- Verification failed, was skipped, or could not run.
- `@test-reviewer` returned `blocked` or `needs more tests`.
- The implementation exceeded approved scope.
- The current branch is `main`.
