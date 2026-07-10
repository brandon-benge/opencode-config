# Agent Instructions

This repository uses the SpecRepo workflow in `specrepo/`.

## Default Rule

For feature work, behavior changes, public API changes, CLI changes, config
changes, provider changes, Git behavior changes, or test strategy changes, do
not start implementation until there is an approved architecture record under
`specrepo/approved/`.

## Agent Handoffs

Use the specialized SpecRepo agents for workflow gates when they are available.
Agent chaining is defined in `specrepo/spec.yaml` under `agent_handoffs`:

- `auto` handoffs run automatically to the next agent.
- `human_decision` handoffs stop and tell the reviewer what action is required.

Primary agents (`@request-author`, `@spec-coder`) call the chain; you never
need to call `@spec-reviewer`, `@architecture-approver`,
`@implementation-reviewer`, or `@test-reviewer` directly unless a handoff
agent is unavailable. If unavailable, follow the same gate manually and record
that the specialized agent was unavailable.

## Request Path

When asked to create or refine a feature request:

1. Use `@request-author` when available.
2. Read `specrepo/spec.yaml`, `specrepo/workflow.md`,
   `specrepo/templates/feature-request.md`, and the baseline specs in
   `specrepo/specs/`.
3. Derive the request name from the target request filename or feature title.
4. Before editing files, create and switch to a git branch named
   `request/<request-name>`. If the branch already exists or the working tree
   has pre-existing changes, stop and ask how to proceed.
5. Create or update one request under `specrepo/requests/`.
6. Stop before architecture. Do not create proposals, approval records,
   implementation reviews, baseline spec updates, or implementation changes.

## Proposal Path

When asked to review a feature request or create architecture:

1. Read `specrepo/spec.yaml`, `specrepo/workflow.md`, and the baseline specs in
   `specrepo/specs/`.
2. Read the request from `specrepo/requests/`.
3. Create or update an architecture proposal under `specrepo/proposals/`.
4. Identify which baseline specs will need updating if the proposed architecture
   changes the approved understanding of the project. The actual spec edits
   happen during implementation.
5. Stop. The architecture proposal is complete. Do not implement code.

## Approval Path

The architecture-approver creates the approval record automatically when a
proposal meets the review criteria. No separate human approval prompt is
required.

1. Use `@architecture-approver` to review the proposal for approval readiness.
2. If the recommendation is `approve`, the approval record is created
   automatically under `specrepo/approved/`.
3. If the recommendation is `revise` or `reject`, no record is created. Refine
   the request and re-run the chain.
4. If the human simply does not like the proposed approach, do not call
   `@spec-coder`. No implementation should start without an approval record.

## Implementation Path

When asked to implement an approved change, follow the agent_handoffs in
`specrepo/spec.yaml`. In summary:

1. Read the approval record under `specrepo/approved/`.
2. Read the approved proposal referenced by that approval record.
3. Read the current baseline specs in `specrepo/specs/`.
4. Follow the coder_to_impl_reviewer handoff to create or verify the
   implementation review.
5. Implement only within the approved scope.
6. If implementation changed user-visible behavior, update the affected baseline
   specs. The approved proposal's Baseline Spec Updates section indicates which
   specs are expected to change.
7. Run the approved verification plan or record why it could not be run.
8. If all required verification commands pass, run
   `$HOME/.config/opencode/specrepo-autocommit` with a four-line summary as the
   final command. Do not run it when verification fails, is skipped, or cannot
   run. The hook blocks autocommit on `main`.
9. Follow the coder_to_test_reviewer handoff to review coverage and verification
   evidence before closing the change.

If the approved architecture is incomplete, inconsistent, or requires material
changes during implementation, stop and return to the proposal workflow.

## Current Project Shape

- Package root: `<package-or-app-root>`
- Tests: `<test-root>`
- Runtime config source of truth: `<runtime-config-path-or-none>`
- Default verification: `<test-command-or-none>`
