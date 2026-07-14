# SpecRepo

This directory is the repository-specific source of truth for spec-driven
development in this repository. Feature work starts here, architecture changes
are approved here, and implementation agents use the approved records before
editing code.

Reusable opencode agent profiles, permissions, prompts, and skills live in
`$HOME/.config/opencode/`. This `specrepo/` directory owns local decision
records and baseline specs those reusable agents must read before acting.

## Current Project

- Product: <Project Name>
- Primary package or app: `<package-or-app>`
- Primary runtime: <language/version>
- Test runner: `<test-command>`
- Current baseline architecture: `specrepo/specs/architecture.md`
- Workflow rules: root `AGENTS.md`, opencode skills, and agent prompts.

## Directory Map

| Path | Purpose |
| --- | --- |
| `specs/` | Approved baseline specs for the current project. |
| `requests/` | Incoming feature requests. Add one file per request. |
| `proposals/` | Draft architecture proposals created from requests. |
| `approved/` | Auto-approved architecture records (created by @architecture-approver). |
| `implementation-reviews/` | Coding-agent reviews of approved architecture before code edits. |
| `templates/` | Copyable templates for each workflow artifact. |

## Quick Start For A Feature Request

1. Ask `@request-author` to create or refine
   `requests/YYYY-MM-DD-short-name.md` from `templates/feature-request.md`.
2. `@request-author` loads the `specrepo-request` skill, then creates and
   switches to branch
   `request/YYYY-MM-DD-short-name` before editing the request file.
3. `@request-author` automatically chains to `@spec-reviewer` (architecture
   proposal) then `@architecture-approver` (automatic approval record if
   criteria are met).
4. Review the proposal and architecture-approver recommendation. If satisfied,
   ask `@spec-coder` to implement. If not, stop here.
5. `@spec-coder` reviews the approved architecture, implements within scope,
   runs verification, and chains to `@test-reviewer` for coverage review.
6. Review the implementation summary and git diff, then merge when ready.

No implementation work should begin until the relevant approved architecture
record exists.

## OpenCode Skills

SpecRepo procedures live in opencode skills and are granted per agent by
`opencode.jsonc`:

| Skill | Purpose |
| --- | --- |
| `specrepo-request` | Request intake and branch setup. |
| `specrepo-proposal` | Architecture proposal creation. |
| `specrepo-approval` | Proposal review and approval records. |
| `specrepo-implementation-review` | Pre-code implementation review. |
| `specrepo-verification` | Verification execution and evidence review. |
| `specrepo-autocommit` | Final autocommit hook after passing test review. |
