# Spec-Driven Workflow

This workflow keeps requested behavior, approved architecture, and code changes
separate. Agents must follow the gates below.

## Directory Authority

This file is the repository-specific state machine for SpecRepo work in this
repository. Reusable opencode agents may execute the roles, but they must read
`specrepo/spec.yaml`, this workflow, the baseline specs, and the active
request/proposal/approval/review records before acting.

Reusable opencode mechanics belong in `$HOME/.config/opencode/agents/`. Repository-specific
project facts, gates, decisions, templates, and verification commands belong in
`specrepo/`.

## State Machine

Each state's transition is governed by deterministic gates defined in
`specrepo/spec.yaml` under `required_gates`. Entry gates must pass before the
state is reached; exit gates must pass before the state is left.

| State | Directory | Owner | Entry Gates | Exit Gates |
| --- | --- | --- | --- | --- |
| `requested` | `requests/` | Request author, normally `@request-author` | — | `request_file_exists` |
| `architecture_proposed` | `proposals/` | Spec reviewer | `request_file_exists`, `current_specs_read` | `approved_architecture_exists` |
| `approved` | `approved/` | Architecture-approver | `approved_architecture_exists` | `implementation_review_exists` |
| `implementation_reviewed` | `implementation-reviews/` | Implementation reviewer | `approved_architecture_exists`, `implementation_review_exists`, `test_plan_exists` | — |
| `implementing` | source tree | Coding agent | `approved_architecture_exists`, `implementation_review_exists`, `test_plan_exists` | — |
| `verified` | source tree | Coding agent | `tests_run_or_exception_recorded` | `specs_updated_if_behavior_changed` |
| `closed` | `approved/` | Human or coding agent | `specs_updated_if_behavior_changed` | — |

Gate definitions (check type, pattern, spec reference) are in
`specrepo/spec.yaml` under `required_gates`.

## Agent Handoffs

Use specialized SpecRepo agents for the workflow gates when they are available:

- `@request-author` owns creating or refining request files in
  `specrepo/requests/` before architecture work begins.
- `@spec-reviewer` owns the transition from `requested` to
  `architecture_proposed`.
- `@architecture-approver` reviews proposal readiness and creates the approval
  record automatically when the proposal meets the review criteria.
- `@implementation-reviewer` owns the transition from `approved` to
  `implementation_reviewed`.
- `@spec-coder` owns implementation after approval and implementation review
  gates are satisfied.
- `@test-reviewer` reviews coverage and verification evidence after
  implementation and before closeout when available.

Primary agents must not skip missing gate artifacts. If a required specialized
agent is unavailable, the primary agent must follow the same gate manually and
record that the specialized agent was unavailable.

## Request Intake

Feature requests belong in `specrepo/requests/` and should use
`specrepo/templates/feature-request.md`.

Use `@request-author` when a feature idea needs to be converted into a request
or when an existing request needs clearer behavior, acceptance criteria,
constraints, non-goals, or impacted-area notes. The request author may create or
switch to a git branch named `request/<request-name>` before editing files, then
create or edit request files only. It must not create proposals, approvals,
implementation reviews, baseline spec updates, or implementation changes.

The request must include:

- Problem or opportunity.
- Desired user-visible behavior.
- Acceptance criteria.
- Constraints or non-goals.
- Any known compatibility concerns.

**Gate:** The `request_file_exists` gate (defined in `specrepo/spec.yaml`) must
pass for the workflow to leave the `requested` state. It checks that at least
one file matching `specrepo/requests/*.md` exists.

## Architecture Proposal

The spec reviewer, normally `@spec-reviewer`, processes one request at a time.

Required actions:

1. Read `specrepo/spec.yaml` and the baseline specs listed there.
2. Read the relevant source files and tests.
3. Create `specrepo/proposals/YYYY-MM-DD-short-name/architecture.md` from
   `specrepo/templates/architecture-proposal.md`.
4. Identify which baseline specs will need updating when the proposal changes
   approved project architecture, product behavior, quality gates, or
   terminology. The actual spec edits happen during implementation.
5. Stop. The architecture proposal is complete. Do not implement code.

The proposal must state whether baseline specs were changed.

**Gate:** The `current_specs_read` gate (defined in `specrepo/spec.yaml`) must
pass for the workflow to enter the `architecture_proposed` state. It checks
that all four baseline spec files exist under `specrepo/specs/`.

## Automatic Approval

The architecture-approver (`@architecture-approver`) creates the approval record
automatically when a proposal meets the review criteria. No separate human
approval prompt is required.

The approval record is created at
`specrepo/approved/YYYY-MM-DD-short-name/approval.md` using
`specrepo/templates/approval-record.md`.

The approval record must include:

- Link to request.
- Link to approved proposal.
- Approval decision.
- Approved scope.
- Any conditions or required follow-up.

Humans stay in control by deciding whether to call `@spec-coder` for
implementation. If the architecture-approver returns `revise` or `reject`, or
if the human simply does not like the proposed approach, no implementation
should start.

Implementation may not begin without an approval record.

**Gate:** The `approved_architecture_exists` gate (defined in
`specrepo/spec.yaml`) must pass for the workflow to enter the `approved` state.
It checks that an approval record exists at
`specrepo/approved/*/approval.md`.

## Coding-Agent Architecture Review

Before editing code, use `@implementation-reviewer` to create an implementation
review from `specrepo/templates/implementation-review.md` under
`specrepo/implementation-reviews/YYYY-MM-DD-short-name.md`.

The review must confirm:

- Approved architecture is internally consistent.
- Approved scope maps to concrete files or modules.
- Public API, CLI, config, and tests impacted by the change are identified.
- Any unresolved issue is marked as a blocker.

If the implementation review finds that the approved architecture is incomplete
or unsafe, implementation stops and returns to the proposal workflow instead of
changing code.

**Gates:** The `implementation_review_exists` and `test_plan_exists` gates
(defined in `specrepo/spec.yaml`) must pass for the workflow to enter the
`implementation_reviewed` state. `implementation_review_exists` checks that an
implementation review file exists under `specrepo/implementation-reviews/*.md`.
`test_plan_exists` checks that the approved proposal or implementation review
contains a `## Test Plan` section.

## Implementation

Implementation agents may edit code only inside the approved scope.

If implementation reveals that architecture must change materially, stop and
return to the proposal step. Do not silently expand the design.

After implementing, update the affected baseline specs when the implementation
changes user-visible behavior. The approved proposal's Baseline Spec Updates
section identifies which specs are expected to change. The
`specs_updated_if_behavior_changed` gate enforces this before close.

## Verification

The default verification command is defined in `specrepo/spec.yaml` under
`commands.test`.

If tests cannot be run, record the reason in the implementation review or final
implementation notes.

After all required verification commands pass, implementation agents should run
`$HOME/.config/opencode/specrepo-autocommit` with a four-line summary as their
final command. Do not run the hook when verification fails, is skipped, or
cannot run. The hook blocks autocommit on `main`.

Use `@test-reviewer` to review the implemented diff, tests, and verification
evidence before closing the change when that agent is available.
