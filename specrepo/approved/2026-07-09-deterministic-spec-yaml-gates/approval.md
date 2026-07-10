# Approval Record: Deterministic SpecRepo Gates With Verifiable Conditions

Status: approved
Date: 2026-07-09
Approver: architecture-approver (automatic)
Request: `specrepo/requests/deterministic-spec-yaml-gates.md`
Approved Proposal: `specrepo/proposals/2026-07-09-deterministic-spec-yaml-gates/architecture.md`

## Decision

Approved

## Approved Scope

- `templates/specrepo/spec.yaml` — replace `required_gates` and `states` with
  structured schema (gates with `check.type`, states with `entry_gates`/`exit_gates`)
- `templates/specrepo/workflow.md` — update State Machine table and section
  references to match structured gates
- `templates/specrepo/specs/quality.md` — add `{#documentation-rules}` anchor
- `templates/specrepo/specs/glossary.md` — add gate, entry_gate, exit_gate terms

## Conditions

1. **State consistency**: The `implementing` state's `entry_gates` should
   include `test_plan_exists` for full consistency with the original
   `before_implementation` gate list. This is a minor change — the transitive
   coverage via `implementation_reviewed` is sufficient, but adding it makes
   the state self-documenting.
2. **Agent prompts**: The existing agent prompts under `prompts/` may contain
   gate-evaluation logic that references the old flat structure. If so, they
   need a follow-up update. This is not a blocker for this approval but should
   be documented during implementation.
3. **Test the bootstrapper**: After the template changes, run
   `@specrepo-bootstrapper` against a temporary directory to confirm the
   generated `specrepo/spec.yaml` validates against the proposed schema.

## Notes

Implementation should create a new branch from `main` named
`impl/deterministic-spec-yaml-gates` and edit only the four files listed in
scope. No source code, runtime config, or agent prompts should be changed as
part of this work.
