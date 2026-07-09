# SpecRepo

This directory is the repository-specific source of truth for spec-driven
development in this repository. Feature work starts here, architecture changes
are approved here, and implementation agents use the approved records before
editing code.

Reusable opencode agent profiles, permissions, and general workflow guidance
live in `$HOME/.config/opencode/agents/`. This `specrepo/` directory owns the local project
facts and decision records those reusable agents must read before acting.

## Current Project

- Product: <Project Name>
- Primary package or app: `<package-or-app>`
- Primary runtime: <language/version>
- Test runner: `<test-command>`
- Current baseline architecture: `specrepo/specs/architecture.md`
- Workflow rules: `specrepo/workflow.md`

## Directory Map

| Path | Purpose |
| --- | --- |
| `spec.yaml` | Machine-readable project and workflow manifest. |
| `workflow.md` | Required state machine and agent handoff rules. |
| `specs/` | Approved baseline specs for the current project. |
| `requests/` | Incoming feature requests. Add one file per request. |
| `proposals/` | Draft architecture proposals created from requests. |
| `approved/` | Auto-approved architecture records (created by @architecture-approver). |
| `implementation-reviews/` | Coding-agent reviews of approved architecture before code edits. |
| `templates/` | Copyable templates for each workflow artifact. |

## Quick Start For A Feature Request

1. Ask `@request-author` to create or refine
   `requests/YYYY-MM-DD-short-name.md` from `templates/feature-request.md`.
2. `@request-author` creates and switches to branch
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
