---
name: specrepo-implementation-review
description: Create the pre-code SpecRepo implementation review for an approved architecture.
compatibility: opencode
metadata:
  owner-agent: implementation-reviewer
---

## Purpose

Use this skill before implementation when an approved change has no matching
implementation review under `specrepo/implementation-reviews/`.

## Required Inputs

- Repository-root `AGENTS.md`, when present.
- Baseline specs under `specrepo/specs/`.
- Approval record under `specrepo/approved/`.
- Approved proposal referenced by the approval record.
- `specrepo/templates/implementation-review.md`.
- Relevant source, test, and documentation files needed to validate the implementation map.

## Review Criteria

- Approved architecture is internally consistent.
- Approved scope maps to concrete source, test, and documentation files.
- Public API, CLI, config, provider, prompt, and Git behavior impacts are clear.
- The test plan is executable.
- No implementation blocker remains.

## Procedure

1. Create `specrepo/implementation-reviews/YYYY-MM-DD-short-name.md`.
2. Use review decision `Proceed` when the architecture is implementable.
3. Use review decision `Stop for revised architecture` when the approved design is incomplete, inconsistent, unsafe, or requires material changes.
4. Do not implement code after writing the review.

## Output Boundary

Allowed:

- `specrepo/implementation-reviews/*.md`

Forbidden:

- Implementation source or test changes.
