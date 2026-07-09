# Agent Instructions

This repository uses the SpecRepo workflow in `specrepo/`.

## Default Rule

For feature work, behavior changes, public API changes, CLI changes, config
changes, provider changes, Git behavior changes, or test strategy changes, do
not start implementation until there is an approved architecture record under
`specrepo/approved/`.

## Agent Handoffs

Use the specialized SpecRepo agents for workflow gates when they are available:

- Use `@request-author` to create or refine feature requests in
  `specrepo/requests/`. It automatically chains to `@spec-reviewer` then
  `@architecture-approver`.
- Use `@spec-coder` only after an approval record and matching implementation
  review exist. It automatically chains to `@implementation-reviewer` then
  `@test-reviewer`.
- Use `@specrepo-bootstrapper` to create the `specrepo/` structure if it does
  not exist.

You never need to call `@spec-reviewer`, `@architecture-approver`,
`@implementation-reviewer`, or `@test-reviewer` directly. Call only the primary
agents (`@request-author`, `@spec-coder`) and let the chain handle the rest.

If a required handoff agent is unavailable, follow the same gate manually and
record that the specialized agent was unavailable.

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
4. Update baseline specs only if the proposed architecture changes the approved
   understanding of the project.
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

When asked to implement an approved change:

1. Read the approval record under `specrepo/approved/`.
2. Read the approved proposal referenced by that approval record.
3. Read the current baseline specs in `specrepo/specs/`.
4. Use `@implementation-reviewer` to create or verify the implementation review
   under `specrepo/implementation-reviews/`.
5. Implement only within the approved scope.
6. Run the approved verification plan or record why it could not be run.
7. If all required verification commands pass, run
   `$HOME/.config/opencode/specrepo-autocommit` with a four-line summary as the
   final command. Do not run it when verification fails, is skipped, or cannot
   run. The hook blocks autocommit on `main`.
8. Use `@test-reviewer` to review coverage and verification evidence before
   closing the change.

If the approved architecture is incomplete, inconsistent, or requires material
changes during implementation, stop and return to the proposal workflow.

## Current Project Shape

- Package root: `<package-or-app-root>`
- Tests: `<test-root>`
- Runtime config source of truth: `<runtime-config-path-or-none>`
- Default verification: `<test-command-or-none>`
