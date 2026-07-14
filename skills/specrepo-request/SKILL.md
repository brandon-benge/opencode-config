---
name: specrepo-request
description: Create and refine SpecRepo feature requests without proposing architecture or changing implementation files.
compatibility: opencode
metadata:
  owner-agent: request-author
---

## Purpose

Use this skill when creating or refining a request under `specrepo/requests/`.

## Required Inputs

- Repository-root `AGENTS.md`, when present.
- `specrepo/templates/feature-request.md`.
- Baseline specs under `specrepo/specs/`.
- Existing request file, when refining an existing request.

## Procedure

1. Identify whether the user is asking for a new request or refinement.
2. Derive a lowercase hyphenated request name from the feature title or target filename.
3. Before editing, inspect `git status` and create `request/<request-name>` with `git switch -c request/<request-name>`.
4. If the branch exists or the worktree has pre-existing changes, stop and ask how to proceed.
5. Create or update exactly one request under `specrepo/requests/` from the template.
6. Remove placeholder text and template guidance from the concrete request.
7. Mark unknown impacted areas as `unknown` instead of guessing.
8. Stop before architecture work.

## Output Boundary

Allowed:

- `specrepo/requests/*.md`

Forbidden:

- Architecture proposals.
- Approval records.
- Implementation reviews.
- Baseline spec updates.
- Implementation source or test changes.
