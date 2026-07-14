---
name: specrepo-approval
description: Review SpecRepo architecture proposals and create approval records when proposals are ready.
compatibility: opencode
metadata:
  owner-agent: architecture-approver
---

## Purpose

Use this skill when reviewing a proposal and, when appropriate, creating an
approval record under `specrepo/approved/`.

## Required Inputs

- Repository-root `AGENTS.md`, when present.
- Baseline specs under `specrepo/specs/`.
- The request referenced by the proposal.
- The proposal being reviewed.
- `specrepo/templates/approval-record.md`.

## Review Criteria

- The proposal solves the request.
- Scope and non-goals are explicit.
- Public API, CLI, config, prompt/provider, Git behavior, docs, and tests are addressed or marked not applicable.
- File-level implementation impact is plausible.
- Test plan covers risk and user-visible behavior.
- Risks and approval conditions are concrete.
- Baseline spec updates match the proposed architecture.

## Procedure

1. Return a recommendation: `approve`, `revise`, or `reject`.
2. If the recommendation is `approve`, create `specrepo/approved/YYYY-MM-DD-short-name/approval.md`.
3. Use the approval-record template and include request link, proposal link, decision, approved scope, and approval conditions.
4. If the recommendation is `revise` or `reject`, do not create an approval record.

## Output Boundary

Allowed:

- `specrepo/approved/*/approval.md`

Forbidden:

- Implementation reviews.
- Implementation source or test changes.
