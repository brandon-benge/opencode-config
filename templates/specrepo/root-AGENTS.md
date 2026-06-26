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
  `specrepo/requests/` before architecture work begins.
- Use `@spec-reviewer` to turn requests in `specrepo/requests/` into
  architecture proposals in `specrepo/proposals/`.
- Use `@architecture-approver` to review proposal readiness and, after an
  explicit human approval prompt, create the approval record.
- Use `@implementation-reviewer` to create the required implementation review
  under `specrepo/implementation-reviews/` before code is edited.
- Use `@spec-coder` only after an approval record and matching implementation
  review exist.
- Use `@test-reviewer` after implementation and verification evidence exist to
  check test coverage and residual risk.

Do not rely on a general-purpose coding agent to silently perform missing
workflow gates. If a required handoff agent is unavailable, follow the same
gate manually and record that the specialized agent was unavailable.

## Spec Review Path

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

When asked to review a feature request or update architecture:

1. Read `specrepo/spec.yaml`, `specrepo/workflow.md`, and the baseline specs in
   `specrepo/specs/`.
2. Read the request from `specrepo/requests/`.
3. Create or update an architecture proposal under `specrepo/proposals/`.
4. Update baseline specs only if the proposed architecture changes the approved
   understanding of the project.
5. Stop and ask for human approval. Do not implement code.

## Approval Path

When asked to approve architecture:

1. Use `@architecture-approver` to review the proposal for approval readiness.
2. If the recommendation is `approve`, read the proposal and review findings.
3. If the human approves, send an explicit prompt to `@architecture-approver`:

   ```text
   @architecture-approver I approve
   specrepo/proposals/YYYY-MM-DD-short-name/architecture.md.

   Create the approval record using the repository's approval-record template.
   Name me as the human approver for this opencode session.
   Conditions: <None, or the exact approval conditions to record>.
   ```

4. Do not treat an approval-readiness recommendation as approval. The approval
   record under `specrepo/approved/` is authoritative only after the human
   sends the explicit approval prompt.

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
