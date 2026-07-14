---
name: specrepo-verification
description: Run or review SpecRepo verification evidence against approved scope and repository quality rules.
compatibility: opencode
metadata:
  owner-agent: spec-coder,test-reviewer
---

## Purpose

Use this skill after implementation to run or review verification for an
approved SpecRepo change.

## Required Inputs

- Repository-root `AGENTS.md`, especially the current project shape and default verification command.
- `specrepo/specs/quality.md`.
- Approval record.
- Approved proposal.
- Implementation review.
- Current git diff.
- Relevant tests or verification artifacts.

## Procedure For Implementation Agents

1. Run the approved verification plan from the proposal or implementation review.
2. If no narrower command is specified, run the default verification command recorded in `AGENTS.md` or `specrepo/specs/quality.md`.
3. If no default command is configured, record that explicitly.
4. If verification cannot run, record the exact reason in the implementation review or final implementation notes.
5. Do not proceed to autocommit unless required verification passed and test review returns `pass`.

## Procedure For Review Agents

1. Compare tests and verification evidence against the approved proposal and implementation review.
2. Check that public API, CLI, config, provider, prompt, Git behavior, docs, and user-visible changes have focused tests or explicit justification.
3. Confirm verification commands actually ran, or that a credible exception was recorded.
4. Return recommendation `pass`, `needs more tests`, or `blocked`.

## Output Boundary

Review agents are read-only. Implementation agents may update tests, docs, and baseline specs only within approved scope.
