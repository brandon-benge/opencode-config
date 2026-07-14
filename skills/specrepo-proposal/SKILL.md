---
name: specrepo-proposal
description: Turn a SpecRepo request into an architecture proposal while keeping implementation changes out of scope.
compatibility: opencode
metadata:
  owner-agent: spec-reviewer
---

## Purpose

Use this skill when creating or updating an architecture proposal under
`specrepo/proposals/`.

## Required Inputs

- Repository-root `AGENTS.md`, when present.
- Baseline specs under `specrepo/specs/`.
- The relevant request under `specrepo/requests/`.
- `specrepo/templates/architecture-proposal.md`.
- Source and test files needed to ground the design.

## Procedure

1. Read the request and summarize the requested behavior.
2. Compare the request against product, architecture, quality, and glossary specs.
3. Inspect source and tests only as needed to avoid speculative architecture.
4. Create `specrepo/proposals/YYYY-MM-DD-short-name/architecture.md` from the proposal template.
5. Cover current architecture, proposed boundaries, data flow, public API, CLI, config, prompt/provider, Git behavior, expected file impact, test plan, risks, and non-goals.
6. State which baseline specs need updates during implementation.
7. Stop before approval and implementation.

## Output Boundary

Allowed:

- `specrepo/proposals/*/architecture.md`

Forbidden:

- Approval records.
- Implementation reviews.
- Implementation source or test changes.
