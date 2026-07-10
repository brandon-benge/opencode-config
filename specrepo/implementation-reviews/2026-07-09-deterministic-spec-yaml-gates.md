# Implementation Review: Deterministic SpecRepo Gates With Verifiable Conditions

Status: implementation_reviewed
Date: 2026-07-09
Reviewer: spec-coder
Approval Record: `specrepo/approved/2026-07-09-deterministic-spec-yaml-gates/approval.md`

## Approved Architecture Readback

The `templates/specrepo/spec.yaml` template currently defines `required_gates`
as flat lists of strings and `states` as a flat list of names. The approved
architecture replaces both with a structured schema:

- **required_gates** becomes a map keyed by gate name, where each value has a
  `description`, `check` block (with `type` + `pattern` and optional extras
  like `section_heading`, `command_ref`), and optional `spec_ref`.
- **states** becomes a list of maps, each with `name`, `entry_gates`,
  `exit_gates`, and optional `artifacts_required`.

The workflow template, quality spec, and glossary are updated to reference the
new structured gates.

## Consistency Check

- Product behavior is clear: yes
- Architecture boundaries are clear: yes
- Public API impact is clear: not applicable
- CLI impact is clear: not applicable
- Config impact is clear: yes — `templates/specrepo/spec.yaml` field structure
- Test plan is clear: yes — 4 verification steps in the proposal

## Implementation Map

| Path | Planned Change |
|---|---|
| `templates/specrepo/spec.yaml` | Replace flat `required_gates` and `states` with structured schema |
| `templates/specrepo/workflow.md` | Update State Machine table with Entry Gates/Exit Gates columns; link section references to gate spec_ref targets |
| `templates/specrepo/specs/quality.md` | Add `{#documentation-rules}` heading anchor |
| `templates/specrepo/specs/glossary.md` | Add gate, entry_gate, exit_gate terms |

## Questions Or Blockers

- None. The approved architecture is consistent and maps to concrete template
  files.

## Verification Plan

1. `grep -c 'check:' templates/specrepo/spec.yaml` — confirms the new
   structured gates exist (expected: 7 gates × at least 1 `check:` each)
2. `python3 -c "import yaml; spec=yaml.safe_load(open('templates/specrepo/spec.yaml')); gates=spec.get('required_gates',{}); states=spec.get('states',[]); [print(f'OK: state {s[\"name\"]} gates resolve') for s in states for g in s.get('entry_gates',[])+s.get('exit_gates',[]) if g in gates]"` — confirm all state gate references resolve
3. Confirm the 4 planned files have been edited and no other files have changed

## Review Decision

Proceed
