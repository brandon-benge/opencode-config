# Spec-Driven Workflow

This workflow keeps requested behavior, approved architecture, and code changes
separate. Agents must follow the gates below.

## Directory Authority

This file is the repository-specific state machine for SpecRepo work in this
repository. Reusable opencode agents may execute the roles, but they must read
`specrepo/spec.yaml`, this workflow, the baseline specs, and the active
request/proposal/approval/review records before acting.

Reusable opencode mechanics belong in `opencode-config/`. Repository-specific
project facts, gates, decisions, templates, and verification commands belong in
`specrepo/`.

## State Machine

| State | Directory | Owner | Exit Criteria |
| --- | --- | --- | --- |
| `requested` | `requests/` | Request author, normally `@request-author` | Feature request is clear enough to review. |
| `architecture_proposed` | `proposals/` | Spec reviewer | Proposal explains product, architecture, tests, and risks. |
| `awaiting_approval` | `proposals/` | Human approver | Human accepts, rejects, or asks for revision. |
| `approved` | `approved/` | Human approver | Approval record points to the accepted proposal. |
| `implementation_reviewed` | `implementation-reviews/` | Implementation reviewer | Approved architecture is confirmed implementable. |
| `implementing` | source tree | Coding agent | Code and tests are updated within approved scope. |
| `verified` | source tree | Coding agent | Test results or verification exceptions are recorded. |
| `closed` | `approved/` | Human or coding agent | Final status and changed files are recorded. |

## Agent Handoffs

Use specialized SpecRepo agents for the workflow gates when they are available:

- `@request-author` owns creating or refining request files in
  `specrepo/requests/` before architecture work begins.
- `@spec-reviewer` owns the transition from `requested` to
  `architecture_proposed`.
- `@architecture-approver` reviews proposal readiness before the human approval
  decision, but does not replace human approval.
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
edit request files only; it must not create proposals, approvals,
implementation reviews, baseline spec updates, or implementation changes.

The request must include:

- Problem or opportunity.
- Desired user-visible behavior.
- Acceptance criteria.
- Constraints or non-goals.
- Any known compatibility concerns.

## Architecture Proposal

The spec reviewer, normally `@spec-reviewer`, processes one request at a time.

Required actions:

1. Read `specrepo/spec.yaml` and the baseline specs listed there.
2. Read the relevant source files and tests.
3. Create `specrepo/proposals/YYYY-MM-DD-short-name/architecture.md` from
   `specrepo/templates/architecture-proposal.md`.
4. Update baseline specs only when the proposal changes approved project
   architecture, product behavior, quality gates, or terminology.
5. Stop and ask for human approval. Do not implement code.

The proposal must state whether baseline specs were changed.

## Approval

Human approval is recorded by creating an approval file from
`specrepo/templates/approval-record.md` under
`specrepo/approved/YYYY-MM-DD-short-name/approval.md`.

Use `@architecture-approver` for the agent-first approval flow:

1. Ask `@architecture-approver` to review the proposal for approval readiness.
2. If the recommendation is `approve`, read the proposal and review findings
   yourself.
3. If you approve, send an explicit approval prompt back to
   `@architecture-approver`.
4. `@architecture-approver` creates the final approval record only after that
   explicit human approval prompt.

Approval prompt format:

```text
@architecture-approver I approve
specrepo/proposals/YYYY-MM-DD-short-name/architecture.md.

Create the approval record using the repository's approval-record template.
Name me as the human approver for this opencode session.
Conditions: <None, or the exact approval conditions to record>.
```

An approval-readiness recommendation is not approval. Do not create, move, or
treat any file as approved until the human sends an explicit approval prompt.

The approval record must include:

- Link to request.
- Link to approved proposal.
- Approval decision.
- Approved scope.
- Any conditions or required follow-up.

Implementation may not begin without this record.

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

## Implementation

Implementation agents may edit code only inside the approved scope.

If implementation reveals that architecture must change materially, stop and
return to the proposal step. Do not silently expand the design.

## Verification

The default verification command is defined in `specrepo/spec.yaml` under
`commands.test`.

If tests cannot be run, record the reason in the implementation review or final
implementation notes.

Use `@test-reviewer` to review the implemented diff, tests, and verification
evidence before closing the change when that agent is available.
