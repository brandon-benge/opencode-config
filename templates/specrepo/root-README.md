# SpecRepo

This directory is the repository-specific source of truth for spec-driven
development in this repository. Feature work starts here, architecture changes
are approved here, and implementation agents use the approved records before
editing code.

Reusable opencode agent profiles, permissions, and general workflow guidance
live in `opencode-config/`. This `specrepo/` directory owns the local project
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
| `approved/` | Human-approved architecture records for implementation. |
| `implementation-reviews/` | Coding-agent reviews of approved architecture before code edits. |
| `templates/` | Copyable templates for each workflow artifact. |

## Quick Start For A Feature Request

1. Ask `@request-author` to create or refine
   `requests/YYYY-MM-DD-short-name.md` from `templates/feature-request.md`.
2. `@request-author` creates and switches to branch
   `request/YYYY-MM-DD-short-name` before editing the request file.
3. Confirm the request, constraints, acceptance criteria, and user impact.
4. Ask `@spec-reviewer` to process the request.
5. The spec reviewer updates `specs/` and creates a proposal in `proposals/`.
6. Ask `@architecture-approver` to review approval readiness.
7. If the human approves, send the approval prompt to `@architecture-approver`
   so it creates the approval record in `approved/`.
8. A coding agent reads the approved record, writes an implementation review in
   `implementation-reviews/`, then implements the change.

No implementation work should begin until the relevant approved architecture
record exists.
